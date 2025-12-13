from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def humanize_bytes(n_bytes: int) -> str:
    """Convert byte count into a human-readable string using binary prefixes."""
    if n_bytes <= 0:
        return "0 B"

    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]
    size = float(n_bytes)
    unit_index = 0

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def parse_timestamp(ts_str: str) -> float:
    """
    Parse timestamp strings (SS, MM:SS, HH:MM:SS) into seconds.
    Raises ValueError for malformed input.
    """
    parts = ts_str.strip().split(":")
    seconds = 0.0
    for i, part in enumerate(reversed(parts)):
        try:
            seconds += float(part) * (60**i)
        except ValueError:
            raise ValueError(f"invalid timestamp component '{part}' in '{ts_str}'")
    return seconds


def format_time(seconds: float) -> str:
    """Format seconds into hh:mm:ss.mmm or mm:ss.mmm strings."""
    if seconds < 0:
        seconds = 0

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    decimal_secs = Decimal(str(secs)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{decimal_secs:06.3f}"
    return f"{minutes}:{decimal_secs:06.3f}"
