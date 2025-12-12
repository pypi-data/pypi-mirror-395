"""
Configuration for SPSE Client
Contains base settings, headers, and cookies configuration
"""

# Base URL
SPSE_BASE_URL = "https://spse.inaproc.id"

# Default category segment
DEFAULT_CATEGORY = "nasional"

# Detail and summary page suffix
SPSE_DETAIL_SUFFIX = "/pengumumanlelang"


def build_paths(category=None):
    """Return path and API segments for given category slug."""
    segment = (category or DEFAULT_CATEGORY).strip("/")
    return {
        "tender_path": f"/{segment}/lelang",
        "nontender_path": f"/{segment}/nontender",
        "tender_api": f"/{segment}/dt/lelang",
        "nontender_api": f"/{segment}/dt/pl",
    }

# HTTP Headers to mimic browser behavior
SPSE_HEADERS = {
    # Default user agent; can be overridden via SPSE_USER_AGENT env var in cookie_manager
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Headers for JSON API requests
SPSE_JSON_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://spse.inaproc.id',
    'Priority': 'u=1, i',
    'Sec-CH-UA': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# Default cookies (non-auth cookies)
# Intentionally left empty to avoid shipping tracking cookies; the server will set what it needs.
SPSE_DEFAULT_COOKIES = {}

# Retry configuration
RETRY_CONFIG = {
    'total': 3,
    'backoff_factor': 1,
    'status_forcelist': [500, 502, 503, 504]
}

# Request timeout (seconds)
REQUEST_TIMEOUT = 30
