"""Logging client that sends log messages to a server via HTTP."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Self

from codec_cub.general.base_file_handler import BaseFileHandler
from lazy_bear import LazyLoader

from bear_dereth.di import Provide, inject
from bear_dereth.logger import LogLevel
from bear_dereth.logger.config.di import Container
from bear_dereth.logger.formatters.template_formatter import TemplateFormatter
from bear_dereth.logger.protocols import Handler

if TYPE_CHECKING:
    from collections.abc import Callable

    from httpx import Client, Response

    from bear_dereth.logger.records.record import LoggerRecord
else:
    Client, Response = LazyLoader("httpx").to_many("Client", "Response")


class APICaller(BaseFileHandler[dict[str, Any]]):
    """A HTTP client attempted to mimic a file-like object for logging."""

    def __init__(self, url: str, timeout: float = 5.0) -> None:
        self.url: str = url
        self.client: Client = Client(timeout=timeout)

    def write(self, data: dict[str, Any], **kwargs) -> Response:  # noqa: ARG002 # type: ignore[override]
        """Send a POST request to the server."""
        return self.client.post(url=self.url, json=data)

    @property
    def closed(self) -> bool:
        """Check if the HTTP client is closed."""
        return self.client.is_closed

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()


class LoggingClient(Handler[APICaller]):
    """Logger that calls HTTP endpoints but behaves like SimpleLogger."""

    default_caller: ClassVar[type] = APICaller
    caller_attr: ClassVar[str] = "write"
    caller: APICaller

    @inject
    def __init__(
        self,
        server_url: str | None = None,
        host: str = "http://localhost",
        port: int = 8080,
        level: LogLevel | int | str = LogLevel.DEBUG,
        error_callback: Callable[..., Any] = Provide[Container.error_callback],
        formatter: TemplateFormatter | None = None,
    ) -> None:
        """Initialize the logging client."""
        self.host: str = host
        self.port: int = port
        self.server_url: str = server_url or f"{self.host}:{self.port}"
        self.error_callback = error_callback
        self.level: LogLevel = LogLevel.get(level, default=LogLevel.DEBUG)
        self.formatter: TemplateFormatter = formatter or TemplateFormatter()
        self.kwargs = {"url": self.server_url, "timeout": 5.0}
        self.file = self.caller = self.factory()

    def emit(self, record: LoggerRecord, **kwargs) -> None:
        """Emit a log record by sending it to the server."""
        if self.caller and not self.disabled and self.should_emit(record.level):
            try:
                formatted_message: dict[str, Any] = self.formatter.format(record, as_dict=True, **kwargs)
                self.output_func(formatted_message)
            except Exception as e:
                self.error_callback(e)

    def __enter__(self) -> Self:
        """Enter the asynchronous context manager."""
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Exit the asynchronous context manager."""
        self.close()


__all__ = ["LoggingClient"]
