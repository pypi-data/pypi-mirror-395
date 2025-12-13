"""FastAPI server for MarkDeck presentation viewer."""

from pathlib import Path
from typing import Any

import click
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from markdeck.parser import SlideParser

app = FastAPI(title="MarkDeck", description="Markdown presentation tool")

# Global variable to store the current presentation file
_current_file: Path | None = None
_watch_enabled: bool = False
_websocket_clients: list[WebSocket] = []


def set_presentation_file(file_path: str | Path | None) -> None:
    """
    Set the current presentation file.

    Args:
        file_path: Path to the markdown file or None to clear
    """
    global _current_file
    _current_file = Path(file_path) if file_path is not None else None


def enable_watch_mode(enabled: bool = True) -> None:
    """
    Enable or disable watch mode for hot reloading.

    Args:
        enabled: Whether to enable watch mode
    """
    global _watch_enabled
    _watch_enabled = enabled


async def notify_clients_reload() -> None:
    """Notify all connected WebSocket clients to reload."""
    disconnected = []
    for client in _websocket_clients:
        try:
            await client.send_json({"type": "reload"})
        except Exception:
            disconnected.append(client)

    # Remove disconnected clients
    for client in disconnected:
        if client in _websocket_clients:
            _websocket_clients.remove(client)


def get_static_dir() -> Path:
    """Get the path to the static directory."""
    return Path(__file__).parent / "static"


# Mount static files
app.mount("/static", StaticFiles(directory=get_static_dir()), name="static")


@app.get("/assets/{file_path:path}")
async def serve_asset(file_path: str) -> FileResponse:
    """
    Serve assets (images, etc.) from the presentation's directory.

    Args:
        file_path: Relative path to the asset file

    Returns:
        The requested file
    """
    if not _current_file:
        raise HTTPException(status_code=400, detail="No presentation file loaded")

    # Get the directory containing the presentation file
    presentation_dir = _current_file.parent

    # Resolve the asset path relative to the presentation directory
    asset_path = (presentation_dir / file_path).resolve()

    # Security check: ensure the resolved path is within the presentation directory
    try:
        asset_path.relative_to(presentation_dir.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    if not asset_path.exists():
        raise HTTPException(status_code=404, detail=f"Asset not found: {file_path}")

    return FileResponse(asset_path)


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """
    Serve the main presentation viewer HTML.

    Returns:
        HTML response with the viewer page
    """
    html_file = get_static_dir() / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=500, detail="Viewer HTML not found")

    content = html_file.read_text(encoding="utf-8")
    return HTMLResponse(content=content)


@app.get("/api/slides")
async def get_slides(file: str | None = None) -> dict[str, Any]:
    """
    Get parsed slides from the markdown file.

    Args:
        file: Optional file path (uses current file if not provided)

    Returns:
        JSON with slides and metadata
    """
    target_file = Path(file) if file else _current_file

    if not target_file:
        raise HTTPException(status_code=400, detail="No presentation file specified")

    if not target_file.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {target_file}")

    try:
        parser = SlideParser(target_file)
        return parser.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status message
    """
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for hot reloading.

    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    _websocket_clients.append(websocket)

    try:
        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in _websocket_clients:
            _websocket_clients.remove(websocket)


@app.get("/api/watch-enabled")
async def watch_enabled() -> dict[str, bool]:
    """
    Check if watch mode is enabled.

    Returns:
        Dictionary with watch_enabled status
    """
    return {"watch_enabled": _watch_enabled}


class SlideNotification(BaseModel):
    """Request model for slide navigation notification."""

    slide_index: int


@app.post("/api/log-notes")
async def log_speaker_notes(notification: SlideNotification) -> dict[str, str]:
    """
    Log speaker notes for the current slide to the server terminal.

    Args:
        notification: Slide index notification

    Returns:
        Success message
    """
    if not _current_file:
        raise HTTPException(status_code=400, detail="No presentation file loaded")

    try:
        parser = SlideParser(_current_file)
        slides = parser.parse()

        if notification.slide_index < 0 or notification.slide_index >= len(slides):
            raise HTTPException(status_code=400, detail="Invalid slide index")

        slide = slides[notification.slide_index]

        # Log to terminal with formatting
        click.echo(click.style("━" * 60, fg="blue"))
        click.echo(
            click.style(
                f"Slide {notification.slide_index + 1} / {len(slides)}", fg="blue", bold=True
            )
        )
        click.echo(click.style("━" * 60, fg="blue"))

        if slide.notes:
            click.echo(click.style("SPEAKER NOTES:", fg="cyan", bold=True))
            click.echo(slide.notes)
        else:
            click.echo(click.style("(No speaker notes for this slide)", fg="bright_black", italic=True))

        click.echo(click.style("━" * 60, fg="blue"))

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging notes: {str(e)}")
