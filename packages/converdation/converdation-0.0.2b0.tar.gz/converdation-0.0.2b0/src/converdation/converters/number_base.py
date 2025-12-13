from typing import Any

from ..exceptions import ConversionError


_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _convert_from_decimal(value: int, base: int) -> str:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConversionError("Value must be int")
    if base < 2 or base > 36:
        raise ConversionError("Base must be between 2 and 36")
    if value == 0:
        return "0"
    negative = value < 0
    n = -value if negative else value
    parts: list[str] = []
    while n:
        n, rem = divmod(n, base)
        parts.append(_DIGITS[rem])
    text = "".join(reversed(parts))
    return "-" + text if negative else text


def _convert_to_decimal(text: str, base: int) -> int:
    if not isinstance(text, str):
        raise ConversionError("Value must be string")
    if base < 2 or base > 36:
        raise ConversionError("Base must be between 2 and 36")
    s = text.strip().lower()
    if s.startswith(("0b", "0o", "0x")):
        raise ConversionError("Prefixes 0b/0o/0x are not allowed")
    if "_" in s:
        raise ConversionError("Underscores are not allowed")
    if not s:
        raise ConversionError("Value must not be empty")
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    if not s:
        raise ConversionError("Value must not be empty")
    for ch in s:
        if ch not in _DIGITS[:base]:
            raise ConversionError("Invalid digit for base")
    value = int(s, base)
    return -value if negative else value


class DecimalToBinaryConverter:
    source = "decimal"
    target = "binary"

    def convert(self, value: Any) -> str:
        return _convert_from_decimal(value, 2)


class DecimalToOctalConverter:
    source = "decimal"
    target = "octal"

    def convert(self, value: Any) -> str:
        return _convert_from_decimal(value, 8)


class DecimalToHexConverter:
    source = "decimal"
    target = "hex"

    def convert(self, value: Any) -> str:
        return _convert_from_decimal(value, 16)


class BinaryToDecimalConverter:
    source = "binary"
    target = "decimal"

    def convert(self, value: Any) -> int:
        return _convert_to_decimal(value, 2)


class BinaryToOctalConverter:
    source = "binary"
    target = "octal"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 2)
        return _convert_from_decimal(decimal_value, 8)


class BinaryToHexConverter:
    source = "binary"
    target = "hex"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 2)
        return _convert_from_decimal(decimal_value, 16)


class OctalToDecimalConverter:
    source = "octal"
    target = "decimal"

    def convert(self, value: Any) -> int:
        return _convert_to_decimal(value, 8)


class OctalToBinaryConverter:
    source = "octal"
    target = "binary"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 8)
        return _convert_from_decimal(decimal_value, 2)


class OctalToHexConverter:
    source = "octal"
    target = "hex"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 8)
        return _convert_from_decimal(decimal_value, 16)


class HexToDecimalConverter:
    source = "hex"
    target = "decimal"

    def convert(self, value: Any) -> int:
        return _convert_to_decimal(value, 16)


class HexToBinaryConverter:
    source = "hex"
    target = "binary"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 16)
        return _convert_from_decimal(decimal_value, 2)


class HexToOctalConverter:
    source = "hex"
    target = "octal"

    def convert(self, value: Any) -> str:
        decimal_value = _convert_to_decimal(value, 16)
        return _convert_from_decimal(decimal_value, 8)

