import json
from typing import Any, Mapping

from ..exceptions import ConversionError


class JsonFormatter:
    name = "json"

    def format(self, value: Any, **kwargs: Any) -> str:
        indent = kwargs.get("indent", 2)
        sort_keys = kwargs.get("sort_keys", False)
        ensure_ascii = kwargs.get("ensure_ascii", False)

        payload = value
        if isinstance(value, str):
            try:
                payload = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ConversionError("Invalid JSON string input") from exc
        elif not isinstance(value, (Mapping, list, tuple, int, float, bool)) and value is not None:
            raise ConversionError("JSON formatter accepts JSON-compatible python values only")

        try:
            return json.dumps(payload, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
        except Exception as exc:
            raise ConversionError("Failed to format JSON") from exc

