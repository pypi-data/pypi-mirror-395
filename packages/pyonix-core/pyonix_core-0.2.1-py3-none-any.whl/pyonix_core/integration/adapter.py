from typing import Any, Callable, Iterable, Optional
import logging

from pyonix_core.integration.stream_wrapper import OnyxStreamWrapper
from pyonix_core.integration.resilience import with_onyx_retries

logger = logging.getLogger(__name__)


class OnyxSourceAdapter:
    """
    Adapter that wraps a paginated client method into the pipeline's Source interface.

    Minimal API:
      - configure(**cfg)
      - extract() -> iterator of items
      - cleanup()

    This is a thin adapter; real pipelines should subclass or implement additional
    lifecycle hooks as needed.
    """

    def __init__(self, client: Any, list_method: Callable[..., Any], *, page_param: str = "page", items_attr: str = "items"):
        self.client = client
        self.list_method = list_method
        self.page_param = page_param
        self.items_attr = items_attr
        self._configured = False

    def configure(self, **cfg) -> None:
        """Apply configuration to the underlying client if it supports a `configure` method.
        Otherwise store config for later use by the list method.
        """
        if hasattr(self.client, "configure"):
            self.client.configure(**cfg)
        self._cfg = cfg
        self._configured = True
        logger.debug("OnyxSourceAdapter.configure called with cfg=%s", cfg)

    def extract(self, **kwargs) -> Iterable[Any]:
        """Return a generator that yields items across pages.

        The underlying `list_method` is wrapped with resilience retries when called.
        """
        if not self._configured:
            # allow extraction without explicit configure but warn in logs (not using logging to keep dependency-free)
            logger.debug("OnyxSourceAdapter.extract called without explicit configure")

        # Build a resilient wrapper around the client's list method
        # Default: retry on generic Exception, but callers can pass specific exception tuples
        resilient = with_onyx_retries()(self.list_method)
        logger.debug("Wrapped list_method %s with resilience", getattr(self.list_method, '__name__', repr(self.list_method)))

        wrapper = OnyxStreamWrapper(resilient, items_attr=self.items_attr, page_param=self.page_param, **kwargs)
        logger.debug("OnyxStreamWrapper created with page_param=%s items_attr=%s", self.page_param, self.items_attr)
        return wrapper

    def cleanup(self) -> None:
        if hasattr(self.client, "close"):
            try:
                self.client.close()
            except Exception:
                pass


__all__ = ["OnyxSourceAdapter"]
