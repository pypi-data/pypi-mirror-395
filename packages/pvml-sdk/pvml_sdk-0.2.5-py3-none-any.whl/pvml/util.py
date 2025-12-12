from datetime import datetime, timedelta
from typing import Optional, Protocol


class Identifiable(Protocol):
    id: str


def get_id(obj_id: str | None = None, obj: Identifiable | None = None) -> str:
    if (obj_id is not None) and (obj is not None):
        raise ValueError(f"Both obj_id and obj cannot full")

    if obj_id is not None:
        return obj_id
    elif obj is not None:
        return obj.id
    else:
        raise ValueError(f"Both obj_id and obj cannot be None")


def get_epoch(days: int) -> int:
    """Convert number of days to Epoch

    :param int days: Number of days
    :return: int Epoch integer

    :example:

    >>> result = get_epoch(7)
    >>> print(result)
     1715792941000
    """
    current_date = datetime.now()
    target_date = current_date + timedelta(days=days)
    epoch_time = int(target_date.timestamp()) * 1000
    return epoch_time

def sniff_png_jpeg(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data[0:3] == b"\xFF\xD8\xFF":
        return "jpeg"
    return None
def convert_timestamp_to_datetime(timestamp: Optional[int]) -> Optional[datetime]:
    """Convert a timestamp to a datetime object, handling None values."""
    return datetime.fromtimestamp(timestamp / 1000) if timestamp is not None else None


def convert_string_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    """Convert a datetime string to a datetime object, handling None values."""
    return datetime.fromisoformat(datetime_str.replace("Z", "+00:00")) if datetime_str is not None else None
