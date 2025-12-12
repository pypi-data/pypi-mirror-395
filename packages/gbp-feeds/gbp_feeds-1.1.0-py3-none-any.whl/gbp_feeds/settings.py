"""Settings for gbp-feeds"""

from dataclasses import dataclass

from gbpcli.settings import BaseSettings


@dataclass(frozen=True)
class Settings(BaseSettings):
    """gbp-feeds settings"""

    env_prefix = "GBP_FEEDS_"

    # pylint: disable=invalid-name

    TITLE: str = "Gentoo Build Publisher"
    """Title for the Feed"""

    DESCRIPTION: str = "Latest Gentoo Build Publisher builds" ""
    """Description for the Feed"""

    ENTRIES_PER_FEED: int = 20
    """Entries per feed"""

    EXT_CSS: str = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
    )
