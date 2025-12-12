"""Type stub for query_builder to help IDEs with autocomplete"""

from typing import TYPE_CHECKING, Any

from shadowlib._internal.api import RuneLiteAPI

if TYPE_CHECKING:
    from shadowlib.generated.query_proxies import ClientProxy

class Query:
    """Query builder for batch execution"""

    client: ClientProxy  # Generated proxy with all Client methods
    plugin: Any
    api: RuneLiteAPI

    def __init__(self, api: RuneLiteAPI, optimize: bool = True) -> None: ...
    def execute(self, selections: dict[str, Any] | None = None) -> dict[str, Any]: ...
    def select(self, **kwargs: Any) -> Query: ...

    # Add other commonly used methods here
    def callStatic(self, class_name: str, method_name: str, *args: Any) -> Any: ...
