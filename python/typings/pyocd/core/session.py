from types import TracebackType
from typing import Any, Optional

from pyocd.core.soc_target import SoCTarget

class Session():
    def __enter__(self) -> 'Session': ...
    def __exit__(self, exc_type: Optional[type], value: Any, traceback: Optional[TracebackType]) -> bool: ...

    @property
    def target(self) -> Optional[SoCTarget]: ...
