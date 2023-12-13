from typing import Any, Mapping, Optional

from .session import Session

class ConnectHelper:
    @staticmethod
    def session_with_chosen_probe(
            blocking: bool = True,
            return_first: bool = False,
            unique_id: Optional[str] = None,
            auto_open: bool = True,
            options: Optional[Mapping[str, Any]] = None,
            **kwargs: dict[Any, Any]
            ) -> Optional[Session]: ...
