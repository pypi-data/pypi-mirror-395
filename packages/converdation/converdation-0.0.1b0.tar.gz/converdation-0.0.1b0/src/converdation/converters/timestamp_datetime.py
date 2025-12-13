from datetime import datetime, timezone
from typing import Any

from ..exceptions import ConversionError


class UnixToIsoConverter:
    source = "unix_timestamp"
    target = "datetime_iso"

    def convert(self, value: Any) -> str:
        if not isinstance(value, (int, float)):
            raise ConversionError("Unix timestamp must be numeric")
        timestamp_value = float(value)
        try:
            dt = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
            return dt.isoformat()
        except Exception as exc:
            raise ConversionError("Failed to convert Unix timestamp to ISO datetime") from exc


class IsoToUnixConverter:
    source = "datetime_iso"
    target = "unix_timestamp"

    def convert(self, value: Any) -> float:
        if not isinstance(value, str):
            raise ConversionError("Datetime value must be text")
        try:
            dt = datetime.fromisoformat(value)
        except Exception as exc:
            raise ConversionError("Invalid ISO datetime input") from exc
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        try:
            return dt.timestamp()
        except Exception as exc:
            raise ConversionError("Failed to convert ISO datetime to Unix timestamp") from exc

