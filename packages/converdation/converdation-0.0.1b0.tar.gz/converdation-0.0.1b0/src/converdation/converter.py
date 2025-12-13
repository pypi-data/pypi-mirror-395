from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Converter(Protocol):
    source: str
    target: str

    def convert(self, value: Any) -> Any:
        ...


@runtime_checkable
class DataGenerator(Protocol):
    name: str

    def generate(self, **kwargs: Any) -> Any:
        ...


@runtime_checkable
class Formatter(Protocol):
    name: str

    def format(self, value: Any, **kwargs: Any) -> Any:
        ...

