from .caveat import Caveat
from .macaroon import MACAROON_V1, MACAROON_V2, Macaroon
from .verifier import Verifier

__all__ = ["Macaroon", "Caveat", "Verifier", "MACAROON_V1", "MACAROON_V2"]


__author__ = "Tazkia Nizami, Evan Cordell"

__version__ = "2.0.0"
__version_info__ = tuple(__version__.split("."))
__short_version__ = __version__
