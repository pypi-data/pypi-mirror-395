"""File watcher for hot reloading presentations."""

import asyncio
from pathlib import Path

from watchfiles import awatch

from markdeck.server import notify_clients_reload


async def watch_file(file_path: Path) -> None:
    """
    Watch a file for changes and notify clients to reload.

    Args:
        file_path: Path to the file to watch
    """
    print(f"Watching {file_path.name} for changes...")

    async for changes in awatch(file_path):
        # Filter out non-modify events and only trigger on actual file changes
        for change_type, changed_path in changes:
            if Path(changed_path) == file_path:
                print(f"File changed: {file_path.name}, reloading...")
                await notify_clients_reload()
                break


def start_file_watcher(file_path: Path) -> None:
    """
    Start watching a file in the background.

    Args:
        file_path: Path to the file to watch
    """
    loop = asyncio.get_event_loop()
    loop.create_task(watch_file(file_path))
