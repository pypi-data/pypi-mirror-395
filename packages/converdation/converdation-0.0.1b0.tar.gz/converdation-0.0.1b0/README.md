# Converdation

## Install
```
pip install converdation
```

## Quick start
```python
from converdation import convert, generate, format_value

xml_text = convert({"hello": "world"}, "json", "xml")
json_text = convert(xml_text, "xml", "json")
iso_text = convert(1700000000, "unix_timestamp", "datetime_iso")
timestamp = convert(iso_text, "datetime_iso", "unix_timestamp")

lorem_words = generate("lorem_ipsum", words=5)
pretty = format_value("json", {"b": 2, "a": 1}, indent=4, sort_keys=True)
```

## API
- `convert(value, source, target) -> Any`
  - Built-ins: `json->xml`, `xml->json`, `unix_timestamp->datetime_iso`, `datetime_iso->unix_timestamp`.
  - Inputs: `json->xml`: `Mapping | list | tuple`; `xml->json`: `str`; `unix_timestamp->datetime_iso`: `int | float`; `datetime_iso->unix_timestamp`: `str`.
  - Raises `ConversionError` on wrong type/format/missing converter.

- `generate(name, **kwargs) -> Any`
  - Built-ins: `lorem_ipsum`.
  - Params (`lorem_ipsum`): only one of `words: int` | `sentences: int` | `paragraphs: int`. Optional: `words_per_sentence=12`, `sentences_per_paragraph=4`.
  - Raises `ConversionError` on wrong type or mixed modes.

- `format_value(name, value, **kwargs) -> Any`
  - Built-ins: `json`.
  - Input: JSON-compatible value or JSON string. Options: `indent=2`, `sort_keys=False`, `ensure_ascii=False`.
  - Raises `ConversionError` on bad JSON or unsupported type.

- Registration
  - `register_converter(obj)`: fields `source`, `target`, method `convert(value)`.
  - `register_generator(obj)`: field `name`, method `generate(**kwargs)`.
  - `register_formatter(obj)`: field `name`, method `format(value, **kwargs)`.