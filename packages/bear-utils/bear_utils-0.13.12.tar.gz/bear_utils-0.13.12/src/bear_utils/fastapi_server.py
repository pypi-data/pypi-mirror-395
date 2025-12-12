"""A generic FastAPI server implementation."""

from typing import TYPE_CHECKING

from lazy_bear import LazyLoader
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    import threading

    from fastapi import FastAPI
    import uvicorn
else:
    FastAPI = LazyLoader("fastapi").to("FastAPI")
    uvicorn = LazyLoader("uvicorn")
    threading = LazyLoader("threading")


class UvicornConfig(BaseModel):
    """Configuration for Uvicorn server."""

    model_config = ConfigDict(serialize_by_alias=True)

    app: FastAPI = Field(...)

    host: str = ""
    port: int = 8000
    log_level: str = "error"
    workers: int = 1
    reload_: bool = Field(default=False, alias="reload")
    access_log: bool = False
    use_colors: bool = False
    debug: bool = False


def run_server(config: UvicornConfig) -> None:
    """Run the FastAPI server in a new event loop.

    Args:
        config: The Uvicorn configuration.
    """
    uvicorn.run(**config.model_dump(exclude_none=True))


class FastAPIServer:
    """A generic FastAPI server implementation."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        log_level: str = "error",
        workers: int = 1,
        reload_: bool = False,
        access_log: bool = False,
        use_colors: bool = False,
        debug: bool = False,
        fastapi: FastAPI | None = None,
        uvicorn_config: UvicornConfig | None = None,
    ) -> None:
        """Initialize the FastAPI generic server.

        Args:
            host: The host address to bind the server to.
            port: The port number to bind the server to.
            fastapi: An optional FastAPI application instance. If not provided, a new instance will be created.
        """
        self.app: FastAPI = fastapi or FastAPI()
        self.config: UvicornConfig = uvicorn_config or UvicornConfig(
            app=self.app,
            host=host,
            port=port,
            log_level=log_level,
            workers=workers,
            reload=reload_,
            access_log=access_log,
            use_colors=use_colors,
            debug=debug,
        )
        self._server_thread: threading.Thread | None = None
        self._running: bool = False

    async def start(self) -> None:
        """Start the server in a separate thread."""
        if self.running:
            return

        self.server_thread = threading.Thread(target=run_server, kwargs={"config": self.config})
        self.server_thread.daemon = True
        self.server_thread.start()
        self.running = True

    async def stop(self, timeout: int = 1) -> None:
        """Stop the server."""
        if not self.running:
            return
        self.running = False
        if self.server_thread is not None:
            self.server_thread.join(timeout=timeout)
            self.server_thread = None

    @property
    def running(self) -> bool:
        """Check if the server is running."""
        return self._running and self._server_thread is not None and self._server_thread.is_alive()

    @running.setter
    def running(self, value: bool) -> None:
        """Set the running state of the server."""
        self._running = value

    @property
    def server_thread(self) -> threading.Thread | None:
        """Get the server thread."""
        return self._server_thread

    @server_thread.setter
    def server_thread(self, thread: threading.Thread | None) -> None:
        """Set the server thread."""
        self._server_thread = thread


__all__ = ["FastAPIServer"]
