"""
File Watcher for Markdown Knowledge Base

This module provides automatic file watching and re-indexing capabilities
for the markdown knowledge base. It detects when files are created, modified,
or deleted and updates the knowledge base accordingly.
"""

import time
import threading
from pathlib import Path
from typing import Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from markdown_kb_manager import MarkdownKnowledgeBase


class MarkdownFileWatcher(FileSystemEventHandler):
    """
    File system event handler for markdown files.
    Monitors .md files and triggers re-indexing on changes.
    """

    def __init__(
        self,
        knowledge_base: MarkdownKnowledgeBase,
        debounce_seconds: float = 2.0,
        on_update_callback: Optional[Callable] = None
    ):
        """
        Initialize the file watcher.

        Args:
            knowledge_base: MarkdownKnowledgeBase instance to update
            debounce_seconds: Time to wait before processing changes (avoids rapid re-indexing)
            on_update_callback: Optional callback function called after updates
        """
        super().__init__()
        self.kb = knowledge_base
        self.debounce_seconds = debounce_seconds
        self.on_update_callback = on_update_callback

        # Track pending updates with debouncing
        self._pending_updates = set()
        self._update_timer = None
        self._lock = threading.Lock()

    def on_created(self, event: FileSystemEvent):
        """Handle file creation events."""
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"📝 Detected new file: {Path(event.src_path).name}")
            self._schedule_update(event.src_path, 'created')

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"✏️  Detected modification: {Path(event.src_path).name}")
            self._schedule_update(event.src_path, 'modified')

    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion events."""
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"🗑️  Detected deletion: {Path(event.src_path).name}")
            self._schedule_update(event.src_path, 'deleted')

    def on_moved(self, event: FileSystemEvent):
        """Handle file move/rename events."""
        if not event.is_directory:
            if hasattr(event, 'dest_path'):
                if event.src_path.endswith('.md') or event.dest_path.endswith('.md'):
                    print(f"📦 Detected move: {Path(event.src_path).name} -> {Path(event.dest_path).name}")
                    # Treat as delete old + create new
                    if event.src_path.endswith('.md'):
                        self._schedule_update(event.src_path, 'deleted')
                    if event.dest_path.endswith('.md'):
                        self._schedule_update(event.dest_path, 'created')

    def _schedule_update(self, file_path: str, event_type: str):
        """
        Schedule a knowledge base update with debouncing.

        Args:
            file_path: Path to the file that changed
            event_type: Type of event (created, modified, deleted)
        """
        with self._lock:
            self._pending_updates.add((file_path, event_type))

            # Cancel existing timer
            if self._update_timer is not None:
                self._update_timer.cancel()

            # Schedule new update
            self._update_timer = threading.Timer(
                self.debounce_seconds,
                self._process_pending_updates
            )
            self._update_timer.start()

    def _process_pending_updates(self):
        """Process all pending updates to the knowledge base."""
        with self._lock:
            if not self._pending_updates:
                return

            updates = list(self._pending_updates)
            self._pending_updates.clear()
            self._update_timer = None

        print(f"\n{'='*60}")
        print(f"Processing {len(updates)} file changes...")
        print(f"{'='*60}\n")

        # Group updates by type
        created_or_modified = []
        deleted = []

        for file_path, event_type in updates:
            if event_type == 'deleted':
                deleted.append(file_path)
            else:
                created_or_modified.append(file_path)

        # Process deletions
        for file_path in deleted:
            try:
                removed = self.kb.vector_kb.remove_file_chunks(file_path)
                if removed > 0:
                    print(f"  🗑️  Removed {Path(file_path).name} ({removed} chunks)")
            except Exception as e:
                print(f"  ✗ Error removing {file_path}: {e}")

        # Process creations/modifications
        for file_path in created_or_modified:
            try:
                if Path(file_path).exists():
                    self.kb.index_file(file_path)
            except Exception as e:
                print(f"  ✗ Error indexing {file_path}: {e}")

        # Print updated stats
        stats = self.kb.get_stats()
        print(f"\n{'='*60}")
        print("Knowledge base updated!")
        print(f"  Total files: {stats['total_files']}")
        print(f"  Total chunks: {stats['total_chunks']}")
        print(f"{'='*60}\n")

        # Call update callback if provided
        if self.on_update_callback:
            try:
                self.on_update_callback(stats)
            except Exception as e:
                print(f"  ⚠ Error in update callback: {e}")


class KnowledgeBaseWatcher:
    """
    High-level wrapper for watching and auto-updating knowledge base.
    """

    def __init__(
        self,
        knowledge_base: MarkdownKnowledgeBase,
        debounce_seconds: float = 2.0,
        on_update_callback: Optional[Callable] = None
    ):
        """
        Initialize the knowledge base watcher.

        Args:
            knowledge_base: MarkdownKnowledgeBase instance
            debounce_seconds: Time to wait before processing changes
            on_update_callback: Optional callback after updates
        """
        self.kb = knowledge_base
        self.event_handler = MarkdownFileWatcher(
            knowledge_base=knowledge_base,
            debounce_seconds=debounce_seconds,
            on_update_callback=on_update_callback
        )
        self.observer = Observer()
        self._is_watching = False

    def start(self, recursive: bool = True):
        """
        Start watching the knowledge base directory.

        Args:
            recursive: Whether to watch subdirectories recursively
        """
        if self._is_watching:
            print("⚠ Watcher is already running")
            return

        watch_path = str(self.kb.kb_dir)
        self.observer.schedule(
            self.event_handler,
            watch_path,
            recursive=recursive
        )
        self.observer.start()
        self._is_watching = True

        print(f"👁️  Watching knowledge base directory: {watch_path}")
        print(f"   (Recursive: {recursive}, Debounce: {self.event_handler.debounce_seconds}s)")
        print("   Press Ctrl+C to stop watching\n")

    def stop(self):
        """Stop watching the knowledge base directory."""
        if not self._is_watching:
            return

        self.observer.stop()
        self.observer.join()
        self._is_watching = False

        print("\n👋 Stopped watching knowledge base directory")

    def watch_forever(self, recursive: bool = True):
        """
        Start watching and block until interrupted.

        Args:
            recursive: Whether to watch subdirectories recursively
        """
        self.start(recursive=recursive)

        try:
            while self._is_watching:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⚠ Received interrupt signal...")
            self.stop()

    def is_watching(self) -> bool:
        """Check if the watcher is currently running."""
        return self._is_watching


def watch_knowledge_base(
    kb_dir: str,
    model_name: str = 'all-MiniLM-L6-v2',
    debounce_seconds: float = 2.0,
    recursive: bool = True,
    on_update_callback: Optional[Callable] = None
):
    """
    Convenience function to create and start a knowledge base watcher.

    Args:
        kb_dir: Directory containing markdown files
        model_name: Sentence transformer model name
        debounce_seconds: Time to wait before processing changes
        recursive: Whether to watch subdirectories recursively
        on_update_callback: Optional callback after updates

    Example:
        >>> def on_update(stats):
        ...     print(f"Updated! Files: {stats['total_files']}, Chunks: {stats['total_chunks']}")
        ...
        >>> watch_knowledge_base(
        ...     kb_dir="./my_knowledge_base",
        ...     on_update_callback=on_update
        ... )
    """
    # Initialize knowledge base
    print("Initializing knowledge base...")
    kb = MarkdownKnowledgeBase(kb_dir, model_name=model_name)

    # Index existing files
    kb.index_all_files()

    # Create and start watcher
    watcher = KnowledgeBaseWatcher(
        knowledge_base=kb,
        debounce_seconds=debounce_seconds,
        on_update_callback=on_update_callback
    )

    watcher.watch_forever(recursive=recursive)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python kb_file_watcher.py <knowledge_base_dir>")
        sys.exit(1)

    kb_dir = sys.argv[1]

    def update_callback(stats):
        """Callback to print stats after each update."""
        print(f"✨ Knowledge base stats: {stats['total_files']} files, {stats['total_chunks']} chunks")

    # Watch the knowledge base
    watch_knowledge_base(
        kb_dir=kb_dir,
        debounce_seconds=2.0,
        on_update_callback=update_callback
    )
