from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Literal, Mapping, Protocol, TypeVar, runtime_checkable

from brikk.config._types import Loader

try:
    from ruamel.yaml import YAML
except ImportError:
    YAML = None


T = TypeVar("T", covariant=True)


@runtime_checkable
class _PydanticValidator(Protocol[T]):
    def model_validate(self, obj: Any, *, from_attributes: bool) -> T: ...


def load(
    validator: _PydanticValidator[T] | Callable[[Mapping[str, Any]], T],
    loaders: list[Loader],
) -> T:
    _ret = {key: val for loader in loaders for key, val in loader.load().items()}
    if isinstance(validator, _PydanticValidator):
        return validator.model_validate(_ret, from_attributes=False)
    return validator(_ret)


class EnvLoader:
    def __init__(
        self,
        environ: Mapping[str, str] | None = None,
        env_prefix: str = "BRIKK_",
        env_nested_delimiter: str = "__",
    ) -> None:
        self.__environ = environ
        self.__env_prefix = env_prefix
        self.__env_nested_delimiter = env_nested_delimiter

    def load(self) -> Mapping[str, Any]:
        _environ = self.__environ or os.environ

        _ret = {}
        for key, value in (
            (key.upper().strip(self.__env_prefix + "_").lower(), value)
            for key, value in _environ.items()
            if key.upper().startswith(self.__env_prefix)
        ):
            if self.__env_nested_delimiter not in key:
                _ret[key] = value
            else:
                keys = key.split(self.__env_nested_delimiter)

                _value = _ret
                for _key in keys[:-1]:
                    if _key not in _value:
                        _value[_key] = {}
                    _value = _value[_key]
                _value[keys[-1]] = value

        return _ret


class _SupportsRead(Protocol[T]):
    def read(self, length: int = ..., /) -> T: ...


class FileLoader:
    def __init__(
        self,
        path: str | os.PathLike[str],
        parser: Callable[[_SupportsRead[bytes]], Mapping[str, Any]],
        *,
        missing_ok: bool = False,
    ) -> None:
        self.__path = Path(path)
        self.__missing_ok = missing_ok
        self.__parser = parser

    def load(self) -> Mapping[str, Any]:
        if self.__missing_ok is True and self.__path.exists() is False:
            return {}

        with open(self.__path, "rb") as fp:
            return self.__parser(fp)


class JsonLoader(FileLoader):
    def __init__(
        self, path: str | os.PathLike[str], *, missing_ok: bool = False
    ) -> None:
        super().__init__(path, json.load, missing_ok=missing_ok)


if YAML is not None:

    class YamlLoader(FileLoader):
        _yaml = YAML

        def __init__(
            self,
            path: str | os.PathLike[str],
            *,
            missing_ok: bool = False,
            yaml_typ: Literal["rt", "safe", "unsafe", "full", "base"] | None = None,
            yaml_pure: bool = False,
        ) -> None:
            super().__init__(
                path,
                self._yaml(typ=yaml_typ, pure=yaml_pure).load,
                missing_ok=missing_ok,
            )
