"""File Watcher Service implementation."""

import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class FileChangeEvent:
    """Represents a file change event."""

    path: Path
    event_type: str  # created, modified, deleted
    timestamp: datetime = field(default_factory=datetime.now)


class Debouncer:
    """Debounces rapid file changes to prevent UI flickering."""

    def __init__(self, delay_ms: int = 500):
        """Initialize debouncer.

        Args:
            delay_ms: Delay in milliseconds before triggering callback
        """
        self.delay_ms = delay_ms
        self._pending: dict[str, FileChangeEvent] = {}
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self._callback: Callable[[list[FileChangeEvent]], None] | None = None

    def set_callback(self, callback: Callable[[list[FileChangeEvent]], None]) -> None:
        """Set the callback to invoke after debounce period."""
        self._callback = callback

    def add_event(self, event: FileChangeEvent) -> None:
        """Add an event to the debounce queue."""
        with self._lock:
            # Use path as key to deduplicate rapid changes to same file
            self._pending[str(event.path)] = event

            # Cancel existing timer
            if self._timer:
                self._timer.cancel()

            # Start new timer
            self._timer = threading.Timer(self.delay_ms / 1000.0, self._flush)
            self._timer.start()

    def _flush(self) -> None:
        """Flush pending events to callback."""
        with self._lock:
            if self._pending and self._callback:
                events = list(self._pending.values())
                self._pending.clear()
                self._callback(events)

    def cancel(self) -> None:
        """Cancel any pending debounce."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._pending.clear()


class SpecFileWatcher:
    """Watches spec files for changes and triggers callbacks.

    Uses watchdog for file system monitoring with debouncing
    to prevent rapid-fire updates.
    """

    def __init__(
        self,
        workspace_path: Path,
        callback: Callable[[list[FileChangeEvent]], None],
        debounce_ms: int = 500,
    ):
        """Initialize the file watcher.

        Args:
            workspace_path: Path to the workspace root
            callback: Function to call when files change
            debounce_ms: Debounce delay in milliseconds
        """
        self.workspace_path = workspace_path
        self.specs_path = workspace_path / ".kiro" / "specs"
        self._callback = callback
        self._debouncer = Debouncer(debounce_ms)
        self._debouncer.set_callback(callback)
        self._observer = None
        self._running = False

    def start(self) -> None:
        """Start watching for file changes."""
        if self._running:
            return

        if not self.specs_path.exists():
            logger.warning(f"Specs directory not found: {self.specs_path}")
            return

        try:
            from watchdog.events import FileSystemEventHandler
            from watchdog.observers import Observer

            class SpecEventHandler(FileSystemEventHandler):
                def __init__(handler_self, watcher: "SpecFileWatcher"):
                    handler_self.watcher = watcher

                def on_modified(handler_self, event):
                    if not event.is_directory and event.src_path.endswith(".md"):
                        handler_self.watcher._on_change(Path(event.src_path), "modified")

                def on_created(handler_self, event):
                    if not event.is_directory and event.src_path.endswith(".md"):
                        handler_self.watcher._on_change(Path(event.src_path), "created")

                def on_deleted(handler_self, event):
                    if not event.is_directory and event.src_path.endswith(".md"):
                        handler_self.watcher._on_change(Path(event.src_path), "deleted")

            self._observer = Observer()
            handler = SpecEventHandler(self)
            self._observer.schedule(handler, str(self.specs_path), recursive=True)
            self._observer.start()
            self._running = True
            logger.info(f"Started watching: {self.specs_path}")

        except ImportError:
            logger.warning("watchdog not installed, file watching disabled")
        except Exception as e:
            logger.error(f"Failed to start file watcher: {e}")

    def stop(self) -> None:
        """Stop watching for file changes."""
        if not self._running:
            return

        self._debouncer.cancel()

        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=2.0)
            self._observer = None

        self._running = False
        logger.info("Stopped file watcher")

    def _on_change(self, path: Path, event_type: str) -> None:
        """Handle a file change event."""
        event = FileChangeEvent(path=path, event_type=event_type)
        self._debouncer.add_event(event)
        logger.debug(f"File {event_type}: {path}")

    @property
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self._running


def get_debounce_count(debouncer: Debouncer) -> int:
    """Get the number of pending events in debouncer (for testing)."""
    with debouncer._lock:
        return len(debouncer._pending)
