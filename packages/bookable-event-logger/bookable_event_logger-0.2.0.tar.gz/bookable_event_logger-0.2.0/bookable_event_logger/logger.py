import os
import json
import uuid
import logging
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple, Union, List

from google.cloud import pubsub_v1
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class EventLogger:
    """
    EventLogger publishes structured JSON events to a Pub/Sub topic.
    Pub/Sub → BigQuery subscription inserts the event into BigQuery
    using the table schema.
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        topic_name: Optional[str] = None,
        environment: Optional[str] = None,
        service_name: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id or os.getenv("LOG_GCP_PROJECT")
        self.topic_name = topic_name or os.getenv("LOG_TOPIC", "events")
        self.environment = environment or os.getenv("LOG_ENVIRONMENT")
        self.service_name = service_name or os.getenv("LOG_SERVICE_NAME")
        self.credentials_path = credentials_path or os.getenv("LOG_GCP_CREDENTIALS")

        # LOG_GCP_CREDENTIALS is now OPTIONAL
        required = {
            "LOG_GCP_PROJECT / project_id": self.project_id,
            "LOG_TOPIC / topic_name": self.topic_name,
            "LOG_ENVIRONMENT / environment": self.environment,
            "LOG_SERVICE_NAME / service_name": self.service_name,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(
                "Missing required config for EventLogger: " + ", ".join(missing)
            )

        # Local dev: use key file if provided
        if self.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        else:
            # GCP: rely on attached service account / ADC
            self.publisher = pubsub_v1.PublisherClient()

        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name)

        # Store pending futures for proper flushing
        self._pending_futures: List[pubsub_v1.publisher.futures.Future] = []

        logger.debug(
            "EventLogger initialized for service=%s, environment=%s, topic=%s",
            self.service_name,
            self.environment,
            self.topic_path,
        )

    def _build_event(
        self,
        *,
        service: Optional[str],
        level: str,
        event_type: str,
        correlation_id: Optional[str],
        data: Dict[str, Any],
        actor: Optional[Dict[str, Any]],
        error: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        service_name = self.service_name
        actor_obj = actor or {}
        data_obj = data or {}
        error_obj = error or {}

        event = {
            "event_id": str(uuid.uuid4()),
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "service": service_name,
            "event_type": event_type,
            "level": level,
            "environment": self.environment,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            # `actor`, `data`, and `error` are JSON-encoded strings
            "actor": json.dumps(actor_obj),
            "data": json.dumps(data_obj),
            "error": json.dumps(error_obj)
        }
        return event

    def log_event(
        self,
        *,
        event_type: str,
        level: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Dict[str, Any],
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None
    ) -> Tuple[Dict[str, Any], Optional[pubsub_v1.publisher.futures.Future]]:
        """Publish an event to Pub/Sub in the agreed schema."""
        event = self._build_event(
            service=service,
            level=level,
            event_type=event_type,
            correlation_id=correlation_id,
            data=data,
            actor=actor,
            error=error,
        )

        payload = json.dumps(event).encode("utf-8")
        logger.info("[EventLogger] %s %s - %s", event_type, level, event["event_id"])

        try:
            future = self.publisher.publish(self.topic_path, payload)
            # Store future for later flushing
            self._pending_futures.append(future)
            logger.debug("Published event %s to %s", event["event_id"], self.topic_path)
            return event, future
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to publish event to Pub/Sub: %s", e)
            return event, None

    async def flush_async(self, timeout: float = 5.0):
        """
        Async method to wait for all pending publish futures to complete.
        This ensures all messages are sent before the application exits.

        Args:
            timeout: Maximum time to wait for futures to complete (seconds)
        """
        if not self._pending_futures:
            logger.debug("No pending futures to flush")
            return

        logger.debug(f"Flushing {len(self._pending_futures)} pending event(s)")

        async def wait_for_future(future):
            """Wait for a single future to complete in an executor"""
            loop = asyncio.get_event_loop()
            try:
                await asyncio.wait_for(
                    loop.run_in_executor(None, future.result),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.warning(f"Future timed out after {timeout}s")
            except Exception as e:
                logger.error(f"Error waiting for future: {e}")

        # Wait for all futures concurrently
        await asyncio.gather(*[wait_for_future(f) for f in self._pending_futures], return_exceptions=True)

        # Clear the list after flushing
        flushed_count = len(self._pending_futures)
        self._pending_futures.clear()
        logger.debug(f"Flushed {flushed_count} event(s)")

    def flush(self, timeout: float = 5.0):
        """
        Synchronous method to wait for all pending publish futures to complete.
        Blocks until all messages are sent or timeout is reached.

        Args:
            timeout: Maximum time to wait for futures to complete (seconds)
        """
        if not self._pending_futures:
            logger.debug("No pending futures to flush")
            return

        logger.debug(f"Flushing {len(self._pending_futures)} pending event(s)")

        for future in self._pending_futures:
            try:
                future.result(timeout=timeout)
            except Exception as e:
                logger.error(f"Error flushing future: {e}")

        flushed_count = len(self._pending_futures)
        self._pending_futures.clear()
        logger.debug(f"Flushed {flushed_count} event(s)")

    def log(
        self,
        level: str,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        """Generic dynamic-level log method."""
        return self.log_event(
            level=level,
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def debug(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,


    ):
        return self.log_event(
            level="debug",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def success(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        return self.log_event(
            level="success",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def failed(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        return self.log_event(
            level="failed",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def info(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        return self.log_event(
            level="info",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def warning(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        return self.log_event(
            level="warning",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )

    def error(
        self,
        event_type: str,
        correlation_id: Optional[str] = None,
        actor: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ):
        return self.log_event(
            level="error",
            event_type=event_type,
            correlation_id=correlation_id,
            actor=actor or {},
            data=data or {},
            error=error or {},
            service=service
        )


class NoOpEventLogger:
    """No-op event logger that silently ignores all logging calls."""

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return {}, None
        return _noop

    async def flush_async(self, timeout: float = 5.0):
        """No-op flush for compatibility"""
        pass

    def flush(self, timeout: float = 5.0):
        """No-op flush for compatibility"""
        pass


_event_logger: Union[EventLogger, NoOpEventLogger, None] = None


def init_event_logger(
    project_id: Optional[str] = None,
    topic_name: Optional[str] = None,
    environment: Optional[str] = None,
    service_name: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> EventLogger:
    """Initialize the global event logger instance."""
    global _event_logger
    _event_logger = EventLogger(
        project_id=project_id,
        topic_name=topic_name,
        environment=environment,
        service_name=service_name,
        credentials_path=credentials_path,
    )
    logger.info(
        "EventLogger initialized for service=%s, environment=%s",
        _event_logger.service_name,
        _event_logger.environment,
    )
    return _event_logger


def get_event_logger() -> Union[EventLogger, NoOpEventLogger]:
    """Get the global event logger instance, or a NoOp logger if not initialized."""
    global _event_logger
    if _event_logger is None:
        logger.debug("EventLogger not initialized, using NoOpEventLogger")
        return NoOpEventLogger()
    return _event_logger
