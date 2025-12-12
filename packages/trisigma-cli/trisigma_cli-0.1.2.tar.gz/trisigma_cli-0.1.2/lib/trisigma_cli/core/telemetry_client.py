import asyncio
import atexit
import hashlib
import json
import logging
import platform
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from uuid import uuid4

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import VERIFY_SSL
from .telemetry_models import TelemetryEvent, TelemetryEventBatch
from .version import __version__

logger = logging.getLogger(__name__)

BATCH_SIZE = 50
FLUSH_INTERVAL_SEC = 10


class TelemetryClient:
    def __init__(
        self,
        api_url: str,
        access_token: str,
        installation_method: str = "unknown",
    ):
        self.api_url = api_url.rstrip("/")
        self.access_token = access_token
        self.installation_method = installation_method

        self.session_id = uuid4()
        self.cli_version = __version__
        self.python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        )
        self.os_platform = platform.system()

        self._buffer: List[TelemetryEvent] = []
        self._flush_task: Optional[asyncio.Task] = None
        self._active_flush_tasks: Set[asyncio.Task] = set()
        self._shutdown = False

        atexit.register(self._shutdown_sync)

    def _hash_repository_path(self, repository_path: Union[str, Path]) -> str:
        path_str = str(repository_path)
        return hashlib.sha256(path_str.encode()).hexdigest()

    def track_event(
        self,
        event_type: str,
        action: str,
        result: str,
        duration_ms: Optional[int] = None,
        parameters: Optional[Dict] = None,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
        repository_path: Optional[Union[str, Path]] = None,
    ):
        if self._shutdown:
            return

        repo_hash = None
        if repository_path:
            repo_hash = self._hash_repository_path(repository_path)

        event = TelemetryEvent(
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            session_id=self.session_id,
            cli_version=self.cli_version,
            installation_method=self.installation_method,
            python_version=self.python_version,
            os_platform=self.os_platform,
            repository_hash=repo_hash,
            action=action,
            result=result,
            duration_ms=duration_ms,
            parameters=parameters,
            error_type=error_type,
            error_message=error_message,
        )

        self._buffer.append(event)

        if len(self._buffer) >= BATCH_SIZE:
            try:
                _loop = asyncio.get_running_loop()
                task = asyncio.create_task(self._flush())
                self._active_flush_tasks.add(task)
                task.add_done_callback(self._active_flush_tasks.discard)
                logger.debug(
                    f"Created flush task (buffer={len(self._buffer)}, "
                    f"active_tasks={len(self._active_flush_tasks)})"
                )
            except RuntimeError:
                logger.debug(
                    f"No running event loop, buffer will be flushed on shutdown "
                    f"(buffer_size={len(self._buffer)})"
                )

    async def start(self):
        # Если task уже существует но завершился/отменился, пересоздаем
        if self._flush_task and (self._flush_task.done() or self._flush_task.cancelled()):
            self._flush_task = None
            
        if not self._flush_task:
            self._flush_task = asyncio.create_task(self._periodic_flush())
            logger.debug("Periodic flush task created")

    async def shutdown(self):
        self._shutdown = True
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
        await self._wait_active_tasks()
        await self._flush()

    async def _wait_active_tasks(self):
        if self._active_flush_tasks:
            active_count = len(self._active_flush_tasks)
            logger.debug(f"Waiting for {active_count} active flush tasks to complete")
            await asyncio.gather(*self._active_flush_tasks, return_exceptions=True)
            logger.debug(f"All {active_count} flush tasks completed")

    def _shutdown_sync(self):
        """
        Синхронный shutdown для atexit handler.

        Использует синхронный HTTP клиент (urllib) вместо asyncio,
        так как при вызове atexit интерпретатор уже завершается
        и asyncio не может создавать новые задачи.
        """
        if self._shutdown:
            return

        buffer_size = len(self._buffer)

        logger.debug(f"Telemetry shutdown: buffer={buffer_size} events")

        self._shutdown = True

        if not self._buffer:
            return

        events_to_send = self._buffer[:]
        self._buffer.clear()

        try:
            self._send_events_sync(events_to_send)
            logger.debug(f"Successfully sent {len(events_to_send)} telemetry events")
        except Exception as e:
            logger.debug(
                f"Failed to send {len(events_to_send)} telemetry events: "
                f"{type(e).__name__}: {e}"
            )

    async def _periodic_flush(self):
        logger.debug("Periodic flush task started")
        while not self._shutdown:
            try:
                logger.debug(f"Sleeping for {FLUSH_INTERVAL_SEC} seconds...")
                await asyncio.sleep(FLUSH_INTERVAL_SEC)
                logger.debug(f"Woke up, flushing {len(self._buffer)} events...")
                await self._flush()
                logger.debug("Flush completed")
            except asyncio.CancelledError:
                logger.debug("Periodic flush cancelled")
                break
            except Exception as e:
                logger.debug(f"Periodic flush error: {e}")

    async def _flush(self):
        if not self._buffer:
            return

        events_to_send = self._buffer[:]
        self._buffer.clear()

        try:
            await self._send_events(events_to_send)
            logger.debug(f"Successfully sent {len(events_to_send)} telemetry events")
        except Exception as e:
            logger.warning(
                f"Failed to send {len(events_to_send)} telemetry events "
                f"after retries: {type(e).__name__}: {e}"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((
            aiohttp.ClientError,
            aiohttp.ServerConnectionError,
            aiohttp.ServerDisconnectedError,
            aiohttp.ServerTimeoutError,
            asyncio.TimeoutError,
            ConnectionError,
            OSError,
        )),
        reraise=False,
    )
    async def _send_events(self, events: List[TelemetryEvent]):
        batch = TelemetryEventBatch(events=events)
        url = f"{self.api_url}/api/createTelemetryEvents"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        timeout = aiohttp.ClientTimeout(total=10)
        connector = aiohttp.TCPConnector(ssl=VERIFY_SSL)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                url,
                json={"events": [e.model_dump(mode='json') for e in batch.events]},
                headers=headers,
                timeout=timeout,
            ) as response:
                response.raise_for_status()

    def _send_events_sync(self, events: List[TelemetryEvent]):
        """
        Синхронная отправка событий через urllib.

        Используется в atexit handler, где asyncio может не работать.
        Включает retry логику с 3 попытками.
        """
        batch = TelemetryEventBatch(events=events)
        url = f"{self.api_url}/api/createTelemetryEvents"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = json.dumps(
            {"events": [e.model_dump(mode='json') for e in batch.events]}
        ).encode('utf-8')

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                context = ssl.create_default_context()
                if not VERIFY_SSL:
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE

                request = urllib.request.Request(
                    url,
                    data=payload,
                    headers=headers,
                    method='POST'
                )

                with urllib.request.urlopen(request, timeout=10, context=context) as response:
                    if response.status == 200:
                        return
                    else:
                        raise urllib.error.HTTPError(
                            url, response.status, f"HTTP {response.status}",
                            headers, None
                        )
            except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
                if attempt == max_attempts - 1:
                    raise
                logger.debug(
                    f"Telemetry send attempt {attempt + 1}/{max_attempts} failed: {e}"
                )
