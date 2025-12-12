"""SPSE data client package."""

from .cookie_manager import SPSECookieManager
from .json_getter import SPSEJsonGetter
from .detail_getter import SPSEDetailGetter
from .summary_getter import SPSESummaryGetter

__all__ = [
    "SPSECookieManager",
    "SPSEJsonGetter",
    "SPSEDetailGetter",
    "SPSESummaryGetter",
]

__version__ = "0.1.0"
