from __future__ import annotations
import logging
from typing import Any

log = logging.getLogger(__name__)
class MessageLogSession:
    """Context manager around BeginMessageLogging / EndMessageLogging & retrieval."""
    def __init__(self, app: Any) -> None:
        self._app = app

    def __enter__(self) -> MessageLogSession:
        if not bool(self._app.BeginMessageLogging()):
            log.warning("BeginMessageLogging() returned False")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._app.EndMessageLogging()

    def retrieve(self) -> str:
        """Retrieve buffered log messages."""
        return self._app.RetrieveLogMessages()
