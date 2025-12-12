"""
Networking utilities for connecting the FlowHive agent to the control server.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, List

import websockets
from websockets.client import WebSocketClientProtocol

from .gpu_monitor import GPUStats
from .gpu_service import GPUService
from .manager import TaskManager
from .models import CommandGroup, GPUSnapshotMessage, Task, TaskStatus


LOG = logging.getLogger("core.control_plane")


class ControlPlaneEventPublisher:
    """Thread-safe helper that puts events onto the outbound queue."""

    def __init__(self, loop: asyncio.AbstractEventLoop, queue: "asyncio.Queue[Dict[str, Any]]") -> None:
        self._loop = loop
        self._queue = queue

    async def publish(self, event: Dict[str, Any]) -> None:
        fut = asyncio.run_coroutine_threadsafe(self._queue.put(event), self._loop)
        await asyncio.wrap_future(fut)


class TaskLogStreamer:
    """Forwards stdout/stderr chunks to the control plane."""

    def __init__(self, publisher: ControlPlaneEventPublisher) -> None:
        self._publisher = publisher

    async def emit(self, task_id: str, stream: str, data: str) -> None:
        line = data.rstrip("\r\n")
        if not line:
            return
        await self._publisher.publish(
            {
                "type": "task.log",
                "task_id": task_id,
                "stream": stream,
                "line": line,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )


class TaskStatusReporter:
    """Callback injected into TaskManager for status updates."""

    def __init__(self, publisher: ControlPlaneEventPublisher) -> None:
        self._publisher = publisher

    async def __call__(self, task: Task) -> None:
        await self._publisher.publish(
            {
                "type": "task.status",
                "task_id": task.id,
                "status": task.status.value,
                "return_code": task.return_code,
                "error": task.error,
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "finished_at": task.finished_at.isoformat() if task.finished_at else None,
            }
        )


@dataclass
class ControlPlaneConfig:
    ws_url: str
    agent_id: str
    account_username: Optional[str] = None
    account_password: Optional[str] = None
    api_key: Optional[str] = None
    label: Optional[str] = None
    reconnect_interval: float = 3.0


class ControlPlaneClient:
    """Maintains the WebSocket session to the control server."""

    def __init__(
        self,
        config: ControlPlaneConfig,
        task_manager: TaskManager,
        outbound_queue: "asyncio.Queue[Dict[str, Any]]",
    ) -> None:
        self._config = config
        self._manager = task_manager
        self._outbound = outbound_queue
        self._stop = asyncio.Event()
        self._connected = asyncio.Event()
        self._current_websocket: Optional[WebSocketClientProtocol] = None
        self._gpu_callback: Optional[callable] = None

    async def run_forever(self) -> None:
        backoff = self._config.reconnect_interval
        while not self._stop.is_set():
            try:
                headers = self._build_headers()
                LOG.debug(
                    "Connecting to control server",
                    extra={
                        "ws_url": self._config.ws_url,
                        "agent_id": self._config.agent_id,
                        "has_api_key": bool(self._config.api_key),
                        "has_username": bool(self._config.account_username),
                    },
                )
                async with websockets.connect(
                    self._config.ws_url,
                    additional_headers=headers,
                ) as websocket:
                    LOG.info("Connected to control server", extra={"ws_url": self._config.ws_url})
                    self._connected.set()
                    await self._session_loop(websocket)
            except asyncio.CancelledError:
                break
            except Exception as exc:  # pragma: no cover - network errors
                error_msg = str(exc)
                if "403" in error_msg or "rejected" in error_msg.lower() or "1008" in error_msg:
                    if self._config.api_key:
                        LOG.error(
                            "Authentication failed (policy violation). Check your API key. ws_url=%s",
                            self._config.ws_url,
                        )
                    else:
                        LOG.error(
                            "Authentication failed (policy violation). Check your credentials: account_username=%s, ws_url=%s",
                            self._config.account_username,
                            self._config.ws_url,
                        )
                elif "getaddrinfo failed" in error_msg or "11001" in error_msg:
                    LOG.error(
                        "DNS resolution failed. Cannot resolve hostname in URL: %s",
                        self._config.ws_url,
                        exc_info=False,
                    )
                    LOG.error(
                        "Please check:\n"
                        "  1. Is the control server running?\n"
                        "  2. Is the 'control_base_url' in your config correct?\n"
                        "  3. Can you reach the server from this machine? (try: ping <hostname>)\n"
                        "  4. For localhost, try: http://127.0.0.1:8000 or http://localhost:8000"
                    )
                else:
                    LOG.error("Control connection failed: %s", exc)
                self._connected.clear()
                await asyncio.sleep(backoff)

    async def close(self) -> None:
        self._stop.set()

    def _get_platform_release(self) -> str:
        """
        Get detailed platform release information.
        
        Returns:
            Detailed platform version string based on the operating system.
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows: Get version and edition info
            # platform.platform() returns something like 'Windows-10-10.0.19045-SP0'
            try:
                import sys
                if sys.platform == "win32":
                    # Try to get Windows version
                    version = platform.version()  # e.g., '10.0.19045'
                    release = platform.release()  # e.g., '10' or '11'
                    
                    # Try to get edition (Home, Pro, Enterprise, etc.)
                    try:
                        import winreg
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                        edition, _ = winreg.QueryValueEx(key, "EditionID")
                        display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
                        winreg.CloseKey(key)
                        return f"Windows {release} {edition} ({display_version})"
                    except:
                        return f"Windows {release} ({version})"
            except:
                pass
            return platform.platform()
        
        elif system == "Linux":
            # Linux: Try to get distribution info
            try:
                # Try using distro package (more reliable)
                import distro
                name = distro.name(pretty=True)  # e.g., "Ubuntu 20.04.6 LTS"
                if name:
                    return name
            except ImportError:
                pass
            
            # Fallback: try reading /etc/os-release
            try:
                with open("/etc/os-release", "r") as f:
                    lines = f.readlines()
                    info = {}
                    for line in lines:
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            info[key] = value.strip('"')
                    
                    # Try PRETTY_NAME first, then fallback to NAME + VERSION
                    if "PRETTY_NAME" in info:
                        return info["PRETTY_NAME"]
                    elif "NAME" in info and "VERSION" in info:
                        return f"{info['NAME']} {info['VERSION']}"
                    elif "NAME" in info:
                        return info["NAME"]
            except:
                pass
            
            # Last resort: return kernel version
            return f"Linux {platform.release()}"
        
        elif system == "Darwin":
            # macOS: Get version
            try:
                mac_ver = platform.mac_ver()[0]
                if mac_ver:
                    # Convert version to macOS name if possible
                    major_version = int(mac_ver.split('.')[0])
                    if major_version >= 13:
                        return f"macOS {mac_ver} (Ventura or later)"
                    elif major_version == 12:
                        return f"macOS {mac_ver} (Monterey)"
                    elif major_version == 11:
                        return f"macOS {mac_ver} (Big Sur)"
                    elif major_version == 10:
                        minor = int(mac_ver.split('.')[1])
                        if minor == 15:
                            return f"macOS {mac_ver} (Catalina)"
                        elif minor == 14:
                            return f"macOS {mac_ver} (Mojave)"
                    return f"macOS {mac_ver}"
            except:
                pass
            return f"macOS {platform.release()}"
        
        else:
            # Other systems: use platform.platform()
            return platform.platform()

    def _build_headers(self) -> Dict[str, str]:
        """
        Build WebSocket authentication headers.
        
        Supports both API key and username/password authentication.
        """
        headers = {
            "x-flowhive-agent": self._config.agent_id,
        }
        
        # Use API key if provided, otherwise use username/password
        if self._config.api_key:
            headers["x-flowhive-api-key"] = self._config.api_key
            LOG.debug("Using API key authentication")
        else:
            if self._config.account_username:
                headers["x-flowhive-account"] = self._config.account_username
            if self._config.account_password:
                headers["x-flowhive-password"] = self._config.account_password
            LOG.debug("Using username/password authentication", account=self._config.account_username)
        
        if self._config.label:
            headers["x-flowhive-label"] = self._config.label
            LOG.debug("Including label in WebSocket headers", label=self._config.label)
        else:
            LOG.debug("No label configured, not including x-flowhive-label header")
        
        # Add platform information with detailed release info
        system = platform.system()
        release = self._get_platform_release()
        headers["x-flowhive-platform"] = system  # Windows, Linux, Darwin, etc.
        headers["x-flowhive-platform-release"] = release
        LOG.debug("Including platform info", platform=system, release=release)
        
        return headers

    async def _session_loop(self, websocket: WebSocketClientProtocol) -> None:
        self._current_websocket = websocket
        
        # 注册 GPU 更新回调
        gpu_service = GPUService.instance()
        if gpu_service.monitor.available:
            self._register_gpu_callback(websocket, gpu_service)
            # 立即发送一次初始快照
            await self._send_gpu_snapshot(websocket, gpu_service)
        
        try:
            receiver = asyncio.create_task(self._consume_socket(websocket))
            sender = asyncio.create_task(self._flush_events(websocket))
            done, pending = await asyncio.wait(
                {receiver, sender},
                return_when=asyncio.FIRST_EXCEPTION,
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
            for task in done:
                if task.exception():
                    raise task.exception()
        finally:
            # 取消注册回调
            if self._gpu_callback:
                gpu_service = GPUService.instance()
                if gpu_service.monitor.available:
                    self._unregister_gpu_callback(gpu_service)
            self._current_websocket = None

    def _register_gpu_callback(self, websocket: WebSocketClientProtocol, gpu_service: GPUService) -> None:
        """Register callback for GPU updates."""
        loop = asyncio.get_event_loop()
        
        def on_gpu_update(stats: List[GPUStats]) -> None:
            """Callback called from monitor thread when GPU stats update."""
            if not self._current_websocket or self._stop.is_set():
                return
            
            # 使用 Pydantic 模型创建消息
            message = GPUSnapshotMessage.create(
                agent_id=self._config.agent_id,
                gpu_stats=stats,
            )
            
            # 从线程安全地调度到事件循环
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_gpu_message_safe(websocket, message),
                    loop
                )
            except Exception as e:
                LOG.debug("Failed to schedule GPU message: %s", e)
        
        gpu_service.monitor.register_callback(on_gpu_update)
        self._gpu_callback = on_gpu_update

    def _unregister_gpu_callback(self, gpu_service: GPUService) -> None:
        """Unregister GPU update callback."""
        if self._gpu_callback:
            gpu_service.monitor.unregister_callback(self._gpu_callback)
            self._gpu_callback = None

    async def _send_gpu_message_safe(
        self, websocket: WebSocketClientProtocol, message: GPUSnapshotMessage
    ) -> None:
        """Safely send GPU message, handling connection errors."""
        try:
            await websocket.send(json.dumps(message.to_dict()))
        except Exception as exc:
            LOG.debug("Failed to send GPU snapshot: %s", exc)

    async def _consume_socket(self, websocket: WebSocketClientProtocol) -> None:
        async for raw in websocket:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                LOG.warning("Dropped malformed control-plane message: %s", raw)
                continue
            await self._handle_message(message)

    async def _flush_events(self, websocket: WebSocketClientProtocol) -> None:
        retry_buffer: Optional[Dict[str, Any]] = None
        while True:
            event = retry_buffer or await self._outbound.get()
            try:
                await websocket.send(json.dumps(event))
                retry_buffer = None
            except Exception:
                retry_buffer = event
                raise

    async def _handle_message(self, message: Dict[str, Any]) -> None:
        msg_type = message.get("type")
        if msg_type == "task.dispatch":
            await self._handle_task_dispatch(message.get("task") or {})
        elif msg_type == "task.cancel":
            task_id = message.get("task_id")
            if task_id:
                cancelled = self._manager.cancel(task_id)
                await self._outbound.put(
                    {
                        "type": "task.status",
                        "task_id": task_id,
                        "status": TaskStatus.CANCELLED.value if cancelled else TaskStatus.PENDING.value,
                    }
                )
        elif msg_type == "gpu.request":
            LOG.debug("Received GPU request from control server")
            await self._handle_gpu_request()
        else:
            LOG.warning("Unknown control-plane message: %s", message)

    async def _handle_task_dispatch(self, payload: Dict[str, Any]) -> None:
        commands = payload.get("commands") or []
        if not commands:
            LOG.warning("Ignoring dispatch without commands: %s", payload)
            return
        workdir = payload.get("workdir")
        command_group = CommandGroup(
            commands=commands,
            env=payload.get("env") or {},
            workdir=Path(workdir) if workdir else None,
        )
        metadata = payload.get("metadata") or {}
        task_id = payload.get("id")
        task = self._manager.submit(
            command_group,
            metadata=metadata,
            task_id=task_id,
        )
        LOG.info(
            "Accepted task from control plane",
            extra={"task_id": task.id, "commands": len(command_group.commands)},
        )

    async def _handle_gpu_request(self) -> None:
        """Handle GPU request from control server - immediately send GPU snapshot."""
        if not self._current_websocket:
            LOG.warning("Received GPU request but no active websocket connection")
            return
        gpu_service = GPUService.instance()
        # Always send a response, even if GPU monitor is unavailable
        await self._send_gpu_snapshot(self._current_websocket, gpu_service, force=True)

    async def _send_gpu_snapshot(self, websocket: WebSocketClientProtocol, gpu_service: GPUService, force: bool = False) -> None:
        """Send GPU snapshot to control server.
        
        Args:
            websocket: The WebSocket connection to send the message on
            gpu_service: The GPU service instance
            force: If True, send an empty snapshot even if GPU monitor is unavailable
        """
        if not gpu_service.monitor.available:
            if not force:
                return
            # Send empty snapshot when forced and monitor unavailable
            LOG.warning(
                "GPU monitor unavailable. Possible reasons: "
                "pynvml not installed, no NVIDIA GPU, or NVML initialization failed. "
                "Sending empty GPU snapshot."
            )
            message = GPUSnapshotMessage.create(
                agent_id=self._config.agent_id,
                gpu_stats=[],
            )
            try:
                await websocket.send(json.dumps(message.to_dict()))
            except Exception as exc:
                LOG.debug("Failed to send GPU snapshot: %s", exc)
            return
        
        try:
            stats = gpu_service.snapshot()
            
            # 使用 Pydantic 模型创建消息
            message = GPUSnapshotMessage.create(
                agent_id=self._config.agent_id,
                gpu_stats=stats,
            )
            await websocket.send(json.dumps(message.to_dict()))
        except Exception as exc:
            LOG.debug("Failed to send GPU snapshot: %s", exc)

