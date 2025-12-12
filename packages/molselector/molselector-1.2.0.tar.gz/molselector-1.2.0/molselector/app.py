"""Main FastAPI application for molecule selection."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

SUPPORTED_EXTENSIONS = {".xyz", ".mol", ".mol2"}
RESULTS_FILENAME = "selection_results.csv"
DEFAULT_FOLDER_ENV_VAR = "MOLSELECTOR_DEFAULT_FOLDER"


class AppState:
    """Container for mutable application state."""

    def __init__(self) -> None:
        self.folder: Optional[Path] = None
        self.files: List[Path] = []
        self.decisions: Dict[str, Dict[str, str]] = {}


state = AppState()

app = FastAPI()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class FolderRequest(BaseModel):
    folder: str


class DecisionRequest(BaseModel):
    path: str
    decision: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main web application."""
    picker_available, picker_reason = _folder_picker_available()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "supported_extensions": ", ".join(sorted(SUPPORTED_EXTENSIONS)),
            "default_folder": _get_default_folder(),
            "folder_picker": {"available": picker_available, "reason": picker_reason},
        },
    )


@app.post("/api/folder")
async def set_folder(payload: FolderRequest) -> Dict[str, object]:
    """Set the active folder and return the list of molecule files."""
    folder_path = Path(payload.folder).expanduser().resolve()
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="Folder not found or not a directory")

    files = _collect_molecule_files(folder_path)
    if not files:
        raise HTTPException(status_code=404, detail="No molecular files found in folder")

    decisions, results_file_present = _load_decisions(folder_path)

    state.folder = folder_path
    state.files = files
    state.decisions = decisions

    declined_count = sum(1 for entry in decisions.values() if entry.get("decision") == "decline")

    response_files = [
        {
            "path": str(path.relative_to(folder_path)),
            "name": path.name,
            "decision": decisions.get(str(path.relative_to(folder_path)), {}).get("decision"),
        }
        for path in files
    ]

    return {
        "folder": str(folder_path),
        "results_csv": str(folder_path / RESULTS_FILENAME),
        "files": response_files,
        "has_results": results_file_present,
        "declined_count": declined_count,
    }


@app.get("/api/folder/picker")
async def pick_folder() -> Dict[str, str]:
    """Open a native folder picker dialog and return the selected folder."""

    available, reason = _folder_picker_available()
    if not available:
        raise HTTPException(status_code=503, detail=reason or "Folder picker is not available on this system")

    try:
        folder = await run_in_threadpool(_open_folder_dialog)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    if not folder:
        raise HTTPException(status_code=400, detail="No folder selected")

    return {"folder": folder}


@app.get("/api/folder/picker/availability")
async def folder_picker_availability() -> Dict[str, object]:
    """Report whether the native folder picker can be used."""

    available, reason = _folder_picker_available()
    return {"available": available, "reason": reason}


@app.get("/api/molecule")
async def get_molecule(path: str = Query(..., description="Relative path to molecule")) -> Dict[str, str]:
    """Return the raw contents of a molecule file along with its format."""
    if state.folder is None:
        raise HTTPException(status_code=400, detail="Folder not set")

    file_path = _resolve_in_folder(path)

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file extension")

    try:
        content = file_path.read_text()
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail=f"Failed to read file: {exc}") from exc

    return {
        "filename": file_path.name,
        "format": file_path.suffix.lower().lstrip("."),
        "content": content,
    }


@app.post("/api/decision")
async def record_decision(payload: DecisionRequest) -> Dict[str, object]:
    """Record an accept/decline decision for a molecule."""
    if state.folder is None:
        raise HTTPException(status_code=400, detail="Folder not set")

    decision = payload.decision.strip().lower()
    if decision not in {"accept", "decline"}:
        raise HTTPException(status_code=400, detail="Decision must be 'accept' or 'decline'")

    file_path = _resolve_in_folder(payload.path)
    relative_key = str(file_path.relative_to(state.folder))

    entry = {
        "decision": decision,
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    state.decisions[relative_key] = entry
    _persist_decisions(state.folder, state.decisions)

    return {
        "file": relative_key,
        "decision": decision,
    }


def _collect_molecule_files(folder: Path) -> List[Path]:
    """Return a sorted list of supported molecule files within folder."""
    files = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files, key=lambda p: p.name.lower())


def _resolve_in_folder(relative_path: str) -> Path:
    """Resolve relative path safely inside the active folder."""
    assert state.folder is not None

    candidate = (state.folder / relative_path).resolve()
    try:
        candidate.relative_to(state.folder)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="File outside the selected folder") from exc

    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return candidate


def _load_decisions(folder: Path) -> tuple[Dict[str, Dict[str, str]], bool]:
    """Load existing decisions from CSV if present."""
    csv_path = folder / RESULTS_FILENAME
    csv_exists = csv_path.exists()
    if not csv_exists:
        return {}, False

    decisions: Dict[str, Dict[str, str]] = {}
    try:
        with csv_path.open("r", newline="") as handle:
            rows = list(_read_csv(handle))
    except Exception:
        return {}, csv_exists

    for row in rows:
        file_key = row.get("file")
        decision = row.get("decision")
        if file_key and decision in {"accept", "decline"}:
            decisions[file_key] = {"decision": decision, "timestamp": row.get("timestamp", "")}
    return decisions, csv_exists


def _persist_decisions(folder: Path, decisions: Dict[str, Dict[str, str]]) -> None:
    """Persist decisions dictionary to CSV."""
    csv_path = folder / RESULTS_FILENAME
    fieldnames = ["file", "decision", "timestamp"]

    with csv_path.open("w", newline="") as handle:
        writer = _csv_writer(handle, fieldnames)
        writer.writeheader()
        for file_key in sorted(decisions):
            data = {"file": file_key, **decisions[file_key]}
            writer.writerow(data)


def _read_csv(handle):
    import csv

    return csv.DictReader(handle)


def _csv_writer(handle, fieldnames):
    import csv

    return csv.DictWriter(handle, fieldnames=fieldnames)


def _folder_picker_available() -> tuple[bool, Optional[str]]:
    """Return whether a GUI folder picker can be shown on this system."""

    if sys.platform == "darwin":
        if shutil.which("osascript") is None:
            return False, "Folder picker requires AppleScript (osascript) support on macOS"
        return True, None

    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    if os.name != "nt" and not display:
        return False, "Folder picker is unavailable because no graphical display is configured"

    try:
        import tkinter as tk
    except Exception as exc:
        return False, f"Native folder picker is not available: {exc}"

    try:
        root = tk.Tk()
        root.withdraw()
        root.destroy()
    except Exception as exc:  # pragma: no cover - depends on system GUI availability
        return False, f"Native folder picker is not available: {exc}"

    return True, None


def _open_folder_dialog() -> str:
    """Show a native folder picker dialog and return the chosen path."""

    available, reason = _folder_picker_available()
    if not available:
        raise RuntimeError(reason or "Native folder picker is not available on this system")

    if sys.platform == "darwin":
        result = _macos_folder_dialog()
        if result is None:
            raise RuntimeError("macOS folder picker requires AppleScript support")
        return result

    return _tkinter_folder_dialog()


def _macos_folder_dialog() -> Optional[str]:
    """Use AppleScript to show a folder picker on macOS."""  # pragma: no cover - platform specific

    sentinel = "__USER_CANCELLED__"
    script = (
        "try\n"
        "    set chosenFolder to POSIX path of (choose folder with prompt \"Select the folder containing molecules\")\n"
        "    return chosenFolder\n"
        "on error number -128\n"
        f"    return \"{sentinel}\"\n"
        "end try"
    )

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None

    if result.returncode != 0:
        message = result.stderr.strip() or "Failed to open folder picker"
        raise RuntimeError(message)

    output = result.stdout.strip()
    if output == sentinel:
        return ""
    return output


def _tkinter_folder_dialog() -> str:
    """Fallback to Tkinter folder picker on non-macOS platforms."""  # pragma: no cover - UI side effect

    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as exc:  # pragma: no cover - depends on system GUI availability
        raise RuntimeError("Native folder picker is not available on this system") from exc

    root = tk.Tk()
    root.withdraw()

    try:
        root.attributes("-topmost", True)
    except Exception:  # pragma: no cover - attribute not supported on all platforms
        pass

    try:
        selected = filedialog.askdirectory()
    finally:
        root.destroy()

    return selected


__all__ = ["app"]


def _get_default_folder() -> Optional[str]:
    """Return the default folder from the environment if it is a directory."""

    raw_value = os.environ.get(DEFAULT_FOLDER_ENV_VAR)
    if not raw_value:
        return None

    try:
        path = Path(raw_value).expanduser().resolve()
    except Exception:
        return None

    if not path.exists() or not path.is_dir():
        return None

    return str(path)
