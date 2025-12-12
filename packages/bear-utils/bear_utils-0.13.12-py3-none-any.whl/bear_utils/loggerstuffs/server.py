"""A local logging server that writes logs to a file via HTTP requests."""

from collections import deque
from typing import TYPE_CHECKING, Literal, Self, TextIO

from funcy_bear.constants import ExitCode, HTTPStatusCode
from lazy_bear import LazyLoader

from bear_dereth.logger import LogLevel
from bear_dereth.logger.protocols.handler import Handler
from bear_dereth.logger.protocols.handler_manager import BaseHandlerManager
from bear_dereth.logger.records.record import LoggerRecord
from bear_utils.fastapi_server import FastAPIServer

if TYPE_CHECKING:
    from fastapi.responses import JSONResponse
else:
    JSONResponse = LazyLoader("fastapi.responses").to("JSONResponse")


class LoggingServer[T: TextIO](BaseHandlerManager):
    """A local server that writes logs to a file."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        level: LogLevel | int | str = LogLevel.DEBUG,
        handlers: list[Handler] | None = None,
        maxlen: int = 100,
    ) -> None:
        """Initialize the logging server."""
        self.host: str = host
        self.port: int = port
        self.handlers = handlers or []
        self.level: LogLevel = LogLevel.get(level, default=LogLevel.DEBUG)
        self.server = FastAPIServer(host=self.host, port=self.port)
        self.logs: deque[LoggerRecord] = deque(maxlen=maxlen)
        self._setup_routes()

    def response(
        self,
        status: str,
        message: str = "",
        status_code: HTTPStatusCode = HTTPStatusCode.SERVER_OK,
    ) -> JSONResponse:
        """Create a JSON response with the given content and status code."""
        return JSONResponse(content={"status": status, "message": message}, status_code=status_code.value)

    def _setup_routes(self) -> None:
        """Set up the FastAPI routes for logging and health check."""

        @self.server.app.post("/log", response_class=JSONResponse)
        async def log_message(request: LoggerRecord) -> JSONResponse:
            """Endpoint to log a message."""
            if request.level.value < self.level.value:
                return self.response(status="ignored", message="Log level is lower than server's minimum level")
            success: ExitCode = await self._emit_to_handlers(request)
            self.logs.append(request)
            if success != ExitCode.SUCCESS:
                return self.response(
                    status="error", message="Failed to write log", status_code=HTTPStatusCode.SERVER_ERROR
                )
            return self.response(status="success", status_code=HTTPStatusCode.SERVER_OK)

        @self.server.app.get("/health")
        async def health_check() -> JSONResponse:
            status: Literal["running", "stopped"] = "running" if self.server.running else "stopped"
            return JSONResponse(
                content={
                    "status": status,
                    "number_of_logs": len(self),
                    "handlers": len(self.handlers),
                },
                status_code=HTTPStatusCode.SERVER_OK,
            )

    async def _emit_to_handlers(self, record: LoggerRecord) -> ExitCode:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Emit a log message to all handlers."""
        try:
            for handler in self.handlers:
                if handler.should_emit(record.level):
                    handler.emit(record)
            return ExitCode.SUCCESS
        except Exception:
            return ExitCode.FAILURE

    def __len__(self) -> int:
        """Get the number of logged messages."""
        return len(self.logs)

    def get_logs(self) -> list[LoggerRecord]:
        """Get the list of logged messages."""
        return list(self.logs)

    async def __aenter__(self) -> Self:
        """Start the logging server."""
        if not self.server.running:
            await self.server.start()
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Stop the logging server."""
        await self.server.stop()
