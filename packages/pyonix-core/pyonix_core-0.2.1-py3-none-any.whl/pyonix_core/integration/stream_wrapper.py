from typing import Callable, Iterable, Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OnyxStreamWrapper:
    """
    Converts paginated client calls into a memory-efficient generator.

    Assumptions about the `func` result:
    - The response object should expose either an iterable attribute (default `items`) or be an iterable itself.
    - Pagination can be controlled with a `page` integer parameter, or the response can expose
      `has_next` / `next_page_token` to continue.

    This wrapper is intentionally conservative: it supports several common pagination shapes.
    """

    def __init__(
        self,
        func: Callable[..., Any],
        *,
        items_attr: str = "items",
        page_param: str = "page",
        start_page: int = 1,
        page_size_param: Optional[str] = None,
        page_size: Optional[int] = None,
        stop_on_empty: bool = True,
        max_items: Optional[int] = None,
        **kwargs,
    ):
        self.func = func
        self.items_attr = items_attr
        self.page_param = page_param
        self.start_page = start_page
        self.page_size_param = page_size_param
        self.page_size = page_size
        self.stop_on_empty = stop_on_empty
        # If set, stop after yielding this many items in total
        self.max_items = max_items
        self.kwargs = kwargs

    def __iter__(self) -> Iterable[Any]:
        page = self.start_page
        yielded = 0
        while True:
            call_kwargs: Dict[str, Any] = dict(self.kwargs)
            call_kwargs[self.page_param] = page
            if self.page_size_param and self.page_size is not None:
                call_kwargs[self.page_size_param] = self.page_size
            logger.debug("OnyxStreamWrapper calling func page=%s kwargs=%s", page, call_kwargs)
            resp = self.func(**call_kwargs)
            logger.debug("OnyxStreamWrapper received response: %r", resp)

            # Support response being an iterable itself
            if hasattr(resp, "__iter__") and not hasattr(resp, "items"):
                items = list(resp)
            else:
                # Try to access configured items attribute
                items = getattr(resp, self.items_attr, None)
                if items is None:
                    # Fallback: try common attribute names
                    for candidate in ("results", "data", "items"):
                        items = getattr(resp, candidate, None)
                        if items is not None:
                            break

            # Normalize to list for iteration
            items_list = list(items) if items is not None else []
            logger.debug("OnyxStreamWrapper extracted %d items", len(items_list))

            # If empty and configured to stop, break
            if not items_list and self.stop_on_empty:
                break

            for item in items_list:
                yield item
                yielded += 1
                if self.max_items is not None and yielded >= self.max_items:
                    logger.debug("OnyxStreamWrapper reached max_items=%s, stopping", self.max_items)
                    return

            # Determine whether to continue
            # 1) If response has explicit has_next boolean
            has_next = getattr(resp, "has_next", None)
            if has_next is not None:
                logger.debug("OnyxStreamWrapper has_next=%s", has_next)
                if not has_next:
                    break
                page += 1
                continue

            # 2) If response contains a next_page_token, pass it through if func accepts it
            next_token = getattr(resp, "next_page_token", None)
            if next_token:
                logger.debug("OnyxStreamWrapper next_page_token=%s", next_token)
                # If the original function expects a token param name 'next_page_token' or 'cursor'
                # we call the function with that token on the next loop iteration.
                # For simplicity, increment page if token is not supported.
                page += 1
                continue

            # 3) Heuristic: if number of items < page_size or empty -> stop
            if self.page_size is not None and len(items_list) < self.page_size:
                break

            # 4) Otherwise advance page
            page += 1


__all__ = ["OnyxStreamWrapper"]
