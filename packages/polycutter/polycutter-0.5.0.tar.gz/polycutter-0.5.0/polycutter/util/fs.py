import os
import shutil
from pathlib import Path
from typing import List


def ensure_writable_dir(path: Path) -> None:
    """Create a directory (if needed) and verify it is writable."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / f".polycut_write_test_{os.getpid()}"
        test_file.touch()
        test_file.unlink()
    except Exception as exc:
        raise OSError(f"directory '{path}' is not writable or cannot be created: {exc}") from exc


def remove_path(path: Path) -> None:
    """Remove a file or directory."""
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    except Exception as exc:
        raise OSError(f"failed to remove '{path}': {exc}") from exc


def format_output_pattern(pattern: str, index: int) -> Path:
    """Format an output pattern containing '{}' with a 1-based index."""
    try:
        return Path(pattern.format(index))
    except Exception as exc:
        raise ValueError(f"invalid output pattern '{pattern}': {exc}") from exc


def collect_existing_outputs(pattern: str, num_segments: int) -> List[Path]:
    """Return existing paths for a numbered output pattern."""
    existing: List[Path] = []
    for i in range(1, num_segments + 1):
        candidate = format_output_pattern(pattern, i).resolve()
        if candidate.exists():
            existing.append(candidate)
    return existing
