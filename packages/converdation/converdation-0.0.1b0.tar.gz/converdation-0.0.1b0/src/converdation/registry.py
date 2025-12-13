from typing import Any, Dict, Generic, Tuple, TypeVar

from .converter import Converter, DataGenerator, Formatter
from .exceptions import ConversionError

T = TypeVar("T")


class _BaseRegistry(Generic[T]):
    def __init__(self) -> None:
        self._items: Dict[str | Tuple[str, str], T] = {}

    def register(self, key: str | Tuple[str, str], item: T, replace: bool) -> None:
        if key in self._items and not replace:
            raise ValueError("Item already registered")
        self._items[key] = item

    def get(self, key: str | Tuple[str, str]) -> T:
        if key not in self._items:
            raise ConversionError("Requested item not found")
        return self._items[key]

    def keys(self) -> list[str | Tuple[str, str]]:
        return sorted(self._items.keys(), key=lambda x: (str(x)))


class ConverterRegistry(_BaseRegistry[Converter]):
    def register(self, converter: Converter, replace: bool = False) -> None:  # type: ignore[override]
        source = getattr(converter, "source", None)
        target = getattr(converter, "target", None)
        if not source or not target:
            raise ConversionError("Converter must define source and target")
        key = (source.strip().lower(), target.strip().lower())
        super().register(key, converter, replace)

    def get(self, source: str, target: str) -> Converter:  # type: ignore[override]
        if not source or not target:
            raise ConversionError("Source and target must be provided")
        key = (source.strip().lower(), target.strip().lower())
        return super().get(key)

    def convert(self, value: Any, source: str, target: str) -> Any:
        converter = self.get(source, target)
        try:
            return converter.convert(value)
        except ConversionError:
            raise
        except Exception as exc:
            raise ConversionError("Conversion failed") from exc

    def available_pairs(self) -> list[tuple[str, str]]:
        return [(k[0], k[1]) for k in self.keys() if isinstance(k, tuple)]


class GeneratorRegistry(_BaseRegistry[DataGenerator]):
    def register(self, generator: DataGenerator, replace: bool = False) -> None:  # type: ignore[override]
        name = getattr(generator, "name", None)
        if not name:
            raise ConversionError("Generator must define name")
        key = name.strip().lower()
        super().register(key, generator, replace)

    def get(self, name: str) -> DataGenerator:  # type: ignore[override]
        if not name:
            raise ConversionError("Name must be provided")
        key = name.strip().lower()
        return super().get(key)

    def generate(self, name: str, **kwargs: Any) -> Any:
        generator = self.get(name)
        try:
            return generator.generate(**kwargs)
        except ConversionError:
            raise
        except Exception as exc:
            raise ConversionError("Generation failed") from exc

    def available(self) -> list[str]:
        return [k for k in self.keys() if isinstance(k, str)]


class FormatterRegistry(_BaseRegistry[Formatter]):
    def register(self, formatter: Formatter, replace: bool = False) -> None:  # type: ignore[override]
        name = getattr(formatter, "name", None)
        if not name:
            raise ConversionError("Formatter must define name")
        key = name.strip().lower()
        super().register(key, formatter, replace)

    def get(self, name: str) -> Formatter:  # type: ignore[override]
        if not name:
            raise ConversionError("Name must be provided")
        key = name.strip().lower()
        return super().get(key)

    def format(self, name: str, value: Any, **kwargs: Any) -> Any:
        formatter = self.get(name)
        try:
            return formatter.format(value, **kwargs)
        except ConversionError:
            raise
        except Exception as exc:
            raise ConversionError("Formatting failed") from exc

    def available(self) -> list[str]:
        return [k for k in self.keys() if isinstance(k, str)]


default_converter_registry = ConverterRegistry()
default_generator_registry = GeneratorRegistry()
default_formatter_registry = FormatterRegistry()


def register_converter(converter: Converter, *, replace: bool = False, registry: ConverterRegistry | None = None) -> None:
    target_registry = registry or default_converter_registry
    target_registry.register(converter, replace=replace)


def register_generator(generator: DataGenerator, *, replace: bool = False, registry: GeneratorRegistry | None = None) -> None:
    target_registry = registry or default_generator_registry
    target_registry.register(generator, replace=replace)


def register_formatter(formatter: Formatter, *, replace: bool = False, registry: FormatterRegistry | None = None) -> None:
    target_registry = registry or default_formatter_registry
    target_registry.register(formatter, replace=replace)


def convert(value: Any, source: str, target: str, registry: ConverterRegistry | None = None) -> Any:
    target_registry = registry or default_converter_registry
    return target_registry.convert(value, source, target)


def generate(name: str, registry: GeneratorRegistry | None = None, **kwargs: Any) -> Any:
    target_registry = registry or default_generator_registry
    return target_registry.generate(name, **kwargs)


def format_value(name: str, value: Any, registry: FormatterRegistry | None = None, **kwargs: Any) -> Any:
    target_registry = registry or default_formatter_registry
    return target_registry.format(name, value, **kwargs)


def get_converter_registry() -> ConverterRegistry:
    return default_converter_registry


def get_generator_registry() -> GeneratorRegistry:
    return default_generator_registry


def get_formatter_registry() -> FormatterRegistry:
    return default_formatter_registry


def _load_defaults() -> None:
    from .converters import builtin_converters
    from .generators import builtin_generators
    from .formatters import builtin_formatters

    for converter in builtin_converters:
        default_converter_registry.register(converter, replace=True)
    for generator in builtin_generators:
        default_generator_registry.register(generator, replace=True)
    for formatter in builtin_formatters:
        default_formatter_registry.register(formatter, replace=True)


_load_defaults()

