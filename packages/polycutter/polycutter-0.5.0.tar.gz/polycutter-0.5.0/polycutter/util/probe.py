import json
import subprocess
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProbeCommandError(Exception):
    """Raised when ffprobe returns a non-zero exit code."""

    def __init__(self, returncode: int, stderr: str):
        super().__init__(f"ffprobe failed with exit code {returncode}")
        self.returncode = returncode
        self.stderr = stderr


class ProbeParseError(Exception):
    """Raised when ffprobe output cannot be parsed."""

    def __init__(self, message: str, stdout: str = ""):
        super().__init__(message)
        self.stdout = stdout


def run_ffprobe_json(cmd: List[str], *, logger=None) -> Dict[str, Any]:
    """Run ffprobe and parse JSON output."""
    if logger:
        logger.debug(f"running ffprobe: {' '.join(cmd)}")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise ProbeCommandError(-1, str(exc)) from exc

    if proc.returncode != 0:
        raise ProbeCommandError(proc.returncode, proc.stderr.strip())

    stdout = proc.stdout.strip()
    if not stdout:
        raise ProbeParseError("ffprobe produced no output", stdout=proc.stdout)

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ProbeParseError(
            f"failed to parse ffprobe output: {exc}", stdout=proc.stdout
        ) from exc


def probe_duration(
    input_path: Path, ffprobe_path: str, *, logger=None
) -> Optional[Fraction]:
    """
    Probe video duration for segment parsing.
    Returns None on error and logs warnings if a logger is provided.
    """
    cmd = [
        ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(input_path),
    ]

    try:
        data = run_ffprobe_json(cmd, logger=logger)
        duration_str = data.get("format", {}).get("duration")
        if duration_str:
            return Fraction(Decimal(duration_str))
        if logger:
            logger.warn("duration not found in ffprobe output")
    except FileNotFoundError:
        if logger:
            logger.warn(f"ffprobe executable not found at '{ffprobe_path}'")
    except ProbeCommandError as exc:
        if logger:
            logger.warn(f"ffprobe failed: {exc.stderr or exc}")
    except ProbeParseError as exc:
        if logger:
            logger.warn(f"could not parse ffprobe output: {exc}")
    except Exception as exc:
        if logger:
            logger.warn(f"unexpected error probing duration: {exc}")

    return None
