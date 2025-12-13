from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `sink.api.sdk.resources` module.

    This is used so that we can lazily import `sink.api.sdk.resources` only when
    needed *and* so that users can just import `sink.api.sdk` and reference `sink.api.sdk.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("sink.api.sdk.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
