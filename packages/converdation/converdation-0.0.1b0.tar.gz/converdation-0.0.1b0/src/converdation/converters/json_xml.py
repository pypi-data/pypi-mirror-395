import json
from typing import Any, Mapping
from xml.etree import ElementTree as ET

from ..exceptions import ConversionError


def _to_element(tag: str, value: Any) -> ET.Element:
    elem = ET.Element(tag)
    if value is None:
        elem.set("type", "null")
        return elem
    if isinstance(value, bool):
        elem.set("type", "bool")
        elem.text = "true" if value else "false"
        return elem
    if isinstance(value, int):
        elem.set("type", "int")
        elem.text = str(value)
        return elem
    if isinstance(value, float):
        elem.set("type", "float")
        elem.text = repr(value)
        return elem
    if isinstance(value, str):
        elem.set("type", "string")
        elem.text = value
        return elem
    if isinstance(value, Mapping):
        elem.set("type", "object")
        for key, val in value.items():
            child = _to_element("field", val)
            child.set("name", str(key))
            elem.append(child)
        return elem
    if isinstance(value, (list, tuple)):
        elem.set("type", "array")
        for item in value:
            child = _to_element("item", item)
            elem.append(child)
        return elem
    raise ConversionError("Unsupported JSON type for XML conversion")


def _from_element(elem: ET.Element) -> Any:
    type_attr = elem.attrib.get("type")
    if not type_attr:
        raise ConversionError("Missing type attribute in XML")

    if type_attr == "null":
        return None
    if type_attr == "bool":
        text = (elem.text or "").strip().lower()
        return text == "true"
    if type_attr == "int":
        try:
            return int(elem.text or "")
        except ValueError as exc:
            raise ConversionError("Invalid int value") from exc
    if type_attr == "float":
        try:
            return float(elem.text or "")
        except ValueError as exc:
            raise ConversionError("Invalid float value") from exc
    if type_attr == "string":
        return elem.text or ""
    if type_attr == "object":
        result = {}
        for child in elem:
            name = child.attrib.get("name")
            if name is None:
                raise ConversionError("Object field without name")
            result[name] = _from_element(child)
        return result
    if type_attr == "array":
        return [_from_element(child) for child in elem]

    raise ConversionError(f"Unknown type attribute: {type_attr}")


class JsonToXmlConverter:
    source = "json"
    target = "xml"

    def convert(self, value: Any) -> str:
        if not isinstance(value, (Mapping, list, tuple)):
            raise ConversionError("JSON input must be mapping or sequence")
        root = _to_element("root", value)
        try:
            return ET.tostring(root, encoding="unicode")
        except Exception as exc:
            raise ConversionError("Failed to convert JSON to XML") from exc


class XmlToJsonConverter:
    source = "xml"
    target = "json"

    def convert(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ConversionError("XML input must be text")
        try:
            root = ET.fromstring(value)
        except Exception as exc:
            raise ConversionError("Invalid XML input") from exc
        content = _from_element(root)
        try:
            return json.dumps(content)
        except Exception as exc:
            raise ConversionError("Failed to convert XML to JSON") from exc

