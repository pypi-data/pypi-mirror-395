import re

RSYNC_RATE_LIMIT_RE = re.compile(r"^\d+(?:(?:\.\d+)?m)?$")
