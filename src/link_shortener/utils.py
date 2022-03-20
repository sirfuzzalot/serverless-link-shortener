"""
Utilities for URL Shortner
"""
import logging
import time
from typing import Dict, Any, Sequence, Callable, Optional

from pydantic import HttpUrl
from starlette.datastructures import URL

from .models import ShortId


log = logging.getLogger("url_shortener")


def build_url(url_id: ShortId, base_url: URL) -> HttpUrl:
    """Builds a short url"""
    base = base_url if str(base_url).endswith("/") else str(base_url) + "/"
    return HttpUrl(f"{base}{url_id}", scheme=base_url.scheme)


def call_with_backoff(
    callable: Callable[[Optional[Any]], Any],
    callable_args: Sequence[Any] = [],
    callable_kwargs: Dict[str, Any] = {},
    retries: int = 3,
) -> Any:
    """Calls the callable with the arguments provided.

    Retries with exponential backoff for x number of times.

    Raises:
        RuntimeError: If callable fails all attempts

    Returns:
        Any: the output of the callable
    """
    _try = 0
    for _ in range(retries):
        try:
            return callable(*callable_args, **callable_kwargs)
        except Exception as e:
            log.warning(e)

        time.sleep(_try**2)
        _try += 1
    else:
        raise RuntimeError(f"Callable Failed after {retries} attempts")
