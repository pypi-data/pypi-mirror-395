from re import match
from typing import Any

from sisyphus_mirror.regexp import RSYNC_RATE_LIMIT_RE


def is_rsync_rate_limit(value: Any) -> bool:
    return (
        (isinstance(value, int) and value >= 0)
        or
        (isinstance(value, str) and bool(match(RSYNC_RATE_LIMIT_RE, value)))
    )
