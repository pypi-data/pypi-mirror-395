"""gbp-feeds

Atom/RSS feeds for Gentoo Build Publisher
"""

import importlib.metadata

__version__ = importlib.metadata.version("gbp-feeds")

# Plugin definition
plugin = {
    "name": "gbp-feeds",
    "version": __version__,
    "description": "Atom/RSS feeds for Gentoo Build Publisher",
    "app": "gbp_feeds.django.gbp_feeds",
    "graphql": None,
    "urls": "gbp_feeds.django.gbp_feeds.views",
    "priority": -12,
}
