"""view utils for gbp-feeds"""

import datetime as dt
import enum
from typing import Any, Iterable, cast

import feedgenerator as fg
from django.template.loader import render_to_string
from django.urls import reverse
from gentoo_build_publisher import publisher
from gentoo_build_publisher.records import BuildRecord
from yarl import URL

from gbp_feeds.settings import Settings


class FeedType(enum.StrEnum):
    """Feed types (with MIME types)"""

    ATOM = "application/atom+xml"
    RSS = "application/rss+xml"


def build_feed(
    feed_type: FeedType, url: str, stylesheets: list[str], builds: Iterable[BuildRecord]
) -> fg.SyndicationFeed:
    """Return a populated Feed given the builds and feed_type"""
    feed = create_feed(feed_type, url, stylesheets=stylesheets)

    for build in builds:
        feed.add_item(
            title=f"GBP build: {build.machine} {build.build_id}",
            link=build_link(build, feed),
            description=f"Build {build} has been pulled",
            unique_id=str(build),
            content=get_item_content(build),
            author_name="Gentoo Build Publisher",
            pubdate=build.completed,
        )
    return feed


def create_feed(feed_type: FeedType, url: str, **extra: Any) -> fg.SyndicationFeed:
    """Create and return an (empty) SyndicationFeed

    The type of feed depends on feed_type.
    """
    settings = Settings.from_environ()

    return (fg.Rss201rev2Feed if feed_type == FeedType.RSS else fg.Atom1Feed)(
        title=settings.TITLE,
        link=url,
        description=settings.DESCRIPTION,
        language="en",
        **extra,
    )


def get_item_content(build: BuildRecord) -> str:
    """Return the feed item content for the given build"""
    packages_built = publisher.storage.get_metadata(build).packages.built
    context = {
        "build": build,
        "packages_built": packages_built,
        "published": publisher.published(build),
    }
    rendered = render_to_string("gbp_feeds/build.html", context)

    return rendered


def get_completed_builds(machine: str | None) -> list[BuildRecord]:
    """Return the completed builds for the given machine

    If machine is None, return the completed builds for all machines.

    The returned list is sorted by completed date (descending).
    """
    builds: list[BuildRecord] = []
    repo = publisher.repo
    machines = [machine] if machine else repo.build_records.list_machines()
    settings = Settings.from_environ()

    for m in machines:
        builds.extend(repo.build_records.for_machine(m))

    builds = [build for build in builds if build.completed is not None]
    builds.sort(key=lambda b: cast(dt.datetime, b.completed), reverse=True)

    return builds[: settings.ENTRIES_PER_FEED]


def get_feed_type(url_path: str) -> FeedType:
    """Return the FeedType given the request"""
    if url_path.endswith(".rss"):
        return FeedType.RSS
    if url_path.endswith(".atom"):
        return FeedType.ATOM

    raise ValueError(url_path)


def build_link(build: BuildRecord, feed: fg.SyndicationFeed) -> str:
    """Given the BuildRecord and request, return the url of the build

    For now this is the machine page of the build's machine.
    """
    location = reverse(
        "gbp-builds", kwargs={"machine": build.machine, "build_id": build.build_id}
    )
    return str(URL(feed.feed["link"]) / location.removeprefix("/"))
