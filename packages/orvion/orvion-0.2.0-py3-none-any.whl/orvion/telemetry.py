"""Telemetry module for Orvion SDK.

Opt-in telemetry that helps improve SDK reliability.
No PII is collected. Can be disabled with enabled=False.

Telemetry is sent to Orvion's backend, which forwards it to Datadog.
This keeps the Datadog API key secure on Orvion's servers.
"""

import asyncio
import platform
import sys
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx

SDK_NAME = "orvion-python"
SDK_VERSION = "0.2.0"


class TelemetryEventType(str, Enum):
    """Types of telemetry events."""

    SDK_INIT = "sdk.init"
    SDK_SHUTDOWN = "sdk.shutdown"
    CREATE_CHARGE = "sdk.create_charge"
    VERIFY_CHARGE = "sdk.verify_charge"
    CONFIRM_PAYMENT = "sdk.confirm_payment"
    GET_ROUTES = "sdk.get_routes"
    HEALTH_CHECK = "sdk.health_check"
    CACHE_HIT = "sdk.cache_hit"
    CACHE_MISS = "sdk.cache_miss"
    CACHE_REFRESH = "sdk.cache_refresh"
    ERROR = "sdk.error"
    API_ERROR = "sdk.api_error"
    TIMEOUT = "sdk.timeout"
    AUTH_ERROR = "sdk.auth_error"
    LATENCY = "sdk.latency"


@dataclass
class TelemetryConfig:
    """Configuration for SDK telemetry."""

    enabled: bool = False
    service_name: str = "orvion-sdk"
    service_version: str = SDK_VERSION
    # Backend URL for telemetry endpoint (defaults to main Orvion API)
    endpoint: Optional[str] = None


@dataclass
class TelemetryEvent:
    """A telemetry event matching backend schema."""

    event_type: str
    timestamp: Optional[str] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TelemetryBatch:
    """Batch of telemetry events to send to backend."""

    sdk_name: str
    sdk_version: str
    events: List[Dict[str, Any]]
    service_name: Optional[str] = None
    service_version: Optional[str] = None
    environment: Optional[str] = None
    runtime: Optional[str] = None
    platform: Optional[str] = None


class TelemetryManager:
    """
    Telemetry manager for Orvion SDK.

    Opt-in telemetry that helps improve SDK reliability.
    No PII is collected. Can be disabled with enabled=False.

    Telemetry is sent to Orvion's backend, which forwards it to Datadog.
    """

    MAX_BUFFER_SIZE = 50
    FLUSH_INTERVAL_SECONDS = 30.0

    def __init__(
        self,
        config: Optional[TelemetryConfig] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.config = config or TelemetryConfig()
        self._api_key = api_key
        self._base_url = (
            self.config.endpoint or base_url or "https://api.orvion.sh"
        ).rstrip("/")
        self._events: List[TelemetryEvent] = []
        self._flush_task: Optional[asyncio.Task] = None
        self._is_flushing = False
        self._http_client: Optional[httpx.AsyncClient] = None

        if self.config.enabled:
            self._start_periodic_flush()

    def _start_periodic_flush(self) -> None:
        """Start periodic flush task."""
        try:
            loop = asyncio.get_running_loop()
            self._flush_task = loop.create_task(self._periodic_flush())
        except RuntimeError:
            # No running loop, will flush on explicit calls
            pass

    async def _periodic_flush(self) -> None:
        """Periodically flush buffered events."""
        while self.config.enabled:
            try:
                await asyncio.sleep(self.FLUSH_INTERVAL_SECONDS)
                await self.flush()
            except asyncio.CancelledError:
                break
            except Exception:
                # Ignore errors in background flush
                pass

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=10.0)
        return self._http_client

    def _event_to_dict(self, event: TelemetryEvent) -> Dict[str, Any]:
        """Convert event to dictionary for JSON serialization."""
        result: Dict[str, Any] = {
            "event_type": event.event_type,
            "timestamp": event.timestamp or datetime.now(timezone.utc).isoformat(),
        }
        if event.duration_ms is not None:
            result["duration_ms"] = event.duration_ms
        if event.success is not None:
            result["success"] = event.success
        if event.error_message:
            result["error_message"] = event.error_message
        if event.error_code:
            result["error_code"] = event.error_code
        if event.metadata:
            result["metadata"] = event.metadata
        return result

    def add_event(self, event: TelemetryEvent) -> None:
        """Add a telemetry event to the buffer."""
        if not self.config.enabled:
            return

        if event.timestamp is None:
            event.timestamp = datetime.now(timezone.utc).isoformat()

        self._events.append(event)

        # Flush if buffer is full
        if len(self._events) >= self.MAX_BUFFER_SIZE:
            asyncio.create_task(self.flush())

    @asynccontextmanager
    async def record_operation(
        self,
        operation_name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        """Context manager for recording operation metrics."""
        if not self.config.enabled:
            yield
            return

        start_time = time.time()
        success = True
        error_message: Optional[str] = None
        error_code: Optional[str] = None

        try:
            yield
        except Exception as e:
            success = False
            error_message = str(e)
            error_code = type(e).__name__
            raise
        finally:
            event_type = f"sdk.{operation_name}"
            self.add_event(
                TelemetryEvent(
                    event_type=event_type,
                    duration_ms=(time.time() - start_time) * 1000,
                    success=success,
                    error_message=error_message,
                    error_code=error_code,
                    metadata=attributes,
                )
            )

    def emit(self, event: "LegacyTelemetryEvent") -> None:
        """Emit a telemetry event (legacy format, for backwards compatibility)."""
        if not self.config.enabled:
            return

        # Convert old format to new format
        event_type = event.name.replace("orvion.", "")
        success = event.attributes.get("success") if event.attributes else None
        duration_ms = event.attributes.get("duration_ms") if event.attributes else None

        # Remove known fields from metadata
        metadata = dict(event.attributes) if event.attributes else {}
        metadata.pop("success", None)
        metadata.pop("duration_ms", None)
        metadata.pop("error_type", None)

        self.add_event(
            TelemetryEvent(
                event_type=event_type,
                timestamp=(
                    datetime.fromtimestamp(event.timestamp, timezone.utc).isoformat()
                    if event.timestamp
                    else None
                ),
                duration_ms=duration_ms,
                success=success,
                error_code=event.attributes.get("error_type") if event.attributes else None,
                metadata=metadata if metadata else None,
            )
        )

    def record_init(
        self,
        base_url: str,
        cache_ttl: float,
    ) -> None:
        """Record SDK initialization."""
        self.add_event(
            TelemetryEvent(
                event_type=TelemetryEventType.SDK_INIT.value,
                success=True,
                metadata={
                    "base_url": base_url,
                    "cache_ttl_seconds": cache_ttl,
                    "sdk_version": self.config.service_version,
                },
            )
        )

    async def flush(self) -> None:
        """Flush buffered events to the backend."""
        if not self.config.enabled or not self._events or self._is_flushing:
            return

        self._is_flushing = True
        events_to_send = self._events.copy()
        self._events = []

        try:
            client = await self._get_client()

            batch = TelemetryBatch(
                sdk_name=SDK_NAME,
                sdk_version=SDK_VERSION,
                service_name=self.config.service_name,
                service_version=self.config.service_version,
                runtime=f"python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                platform=f"{platform.system().lower()} {platform.machine()}",
                environment=None,  # Could be set from env var
                events=[self._event_to_dict(e) for e in events_to_send],
            )

            headers = {"Content-Type": "application/json"}

            # Include API key if available for better attribution
            if self._api_key:
                headers["X-API-Key"] = self._api_key

            response = await client.post(
                f"{self._base_url}/v1/telemetry",
                json={
                    "sdk_name": batch.sdk_name,
                    "sdk_version": batch.sdk_version,
                    "service_name": batch.service_name,
                    "service_version": batch.service_version,
                    "runtime": batch.runtime,
                    "platform": batch.platform,
                    "environment": batch.environment,
                    "events": batch.events,
                },
                headers=headers,
            )

            if response.status_code != 200:
                # Re-add events to buffer on failure (up to max size)
                remaining = self.MAX_BUFFER_SIZE - len(self._events)
                if remaining > 0:
                    self._events = events_to_send[:remaining] + self._events

        except Exception:
            # Re-add events to buffer on network error
            remaining = self.MAX_BUFFER_SIZE - len(self._events)
            if remaining > 0:
                self._events = events_to_send[:remaining] + self._events
        finally:
            self._is_flushing = False

    async def shutdown(self) -> None:
        """Shutdown telemetry manager."""
        # Cancel periodic flush
        if self._flush_task and not self._flush_task.done():
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass

        # Add shutdown event and final flush
        if self._events or self.config.enabled:
            self.add_event(
                TelemetryEvent(
                    event_type=TelemetryEventType.SDK_SHUTDOWN.value,
                    success=True,
                )
            )
            await self.flush()

        # Close HTTP client
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()

        self.config.enabled = False

    def get_events(self) -> List[TelemetryEvent]:
        """Get collected events (for testing/debugging)."""
        return list(self._events)

    def clear_events(self) -> None:
        """Clear collected events."""
        self._events = []

    def is_enabled(self) -> bool:
        """Check if telemetry is enabled."""
        return self.config.enabled


# Legacy event format for backwards compatibility
@dataclass
class LegacyTelemetryEvent:
    """A telemetry event (legacy format)."""

    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


# Module-level singleton
_telemetry: Optional[TelemetryManager] = None


def init_telemetry(
    config: TelemetryConfig,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> TelemetryManager:
    """Initialize global telemetry instance."""
    global _telemetry
    _telemetry = TelemetryManager(config, api_key=api_key, base_url=base_url)
    return _telemetry


def get_telemetry() -> Optional[TelemetryManager]:
    """Get global telemetry instance."""
    return _telemetry
