from collections.abc import Mapping
from typing import Any, Protocol


class Loader(Protocol):
    def load(self) -> Mapping[str, Any]: ...
