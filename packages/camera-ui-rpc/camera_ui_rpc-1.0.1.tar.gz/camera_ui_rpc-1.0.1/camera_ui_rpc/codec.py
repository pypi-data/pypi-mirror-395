"""MessagePack encoding/decoding using ormsgpack for better performance."""

from datetime import date, datetime, time
from enum import Enum
from typing import Any

import ormsgpack


def _default_handler(obj: Any) -> Any:
    """Default handler for custom types."""
    if isinstance(obj, Enum):
        return obj.value
    # date and time objects need special handling
    if isinstance(obj, date) and not isinstance(obj, datetime):
        # Convert date to datetime at midnight for timestamp encoding
        return datetime.combine(obj, time.min)
    if isinstance(obj, time):
        # For time objects, return as string
        return obj.isoformat()
    # Let ormsgpack handle other types
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def encode(data: Any) -> bytes:
    """
    Encode data to MessagePack binary format using ormsgpack.

    Args:
        data: Any serializable data

    Returns:
        MessagePack encoded binary data
    """
    # Use ormsgpack with proper options for cross-language compatibility
    # OPT_DATETIME_AS_TIMESTAMP_EXT: Encode datetime as MessagePack timestamp extension
    # OPT_NON_STR_KEYS: Allow non-string dict keys
    # OPT_PASSTHROUGH_ENUM: Pass enums to default handler
    return ormsgpack.packb(
        data,
        default=_default_handler,
        option=ormsgpack.OPT_NON_STR_KEYS
        | ormsgpack.OPT_DATETIME_AS_TIMESTAMP_EXT
        | ormsgpack.OPT_PASSTHROUGH_ENUM,
    )


def decode(data: bytes) -> Any:
    """
    Decode MessagePack binary data using ormsgpack.

    Args:
        data: MessagePack binary data

    Returns:
        Decoded data
    """
    # Use ormsgpack with proper options
    # OPT_DATETIME_AS_TIMESTAMP_EXT: Deserialize timestamp extension objects to datetime
    # OPT_NON_STR_KEYS: Allow non-string dict keys
    return ormsgpack.unpackb(
        data, option=ormsgpack.OPT_DATETIME_AS_TIMESTAMP_EXT | ormsgpack.OPT_NON_STR_KEYS
    )
