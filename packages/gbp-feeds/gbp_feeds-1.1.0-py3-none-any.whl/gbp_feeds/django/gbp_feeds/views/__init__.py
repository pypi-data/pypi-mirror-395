"""Django views for gbp-feeds"""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from gentoo_build_publisher.django.gentoo_build_publisher.views.utils import view

from gbp_feeds.settings import Settings

from . import utils


@view("feed.rss", name="gbp-feeds-rss-main")
@view("feed.atom", name="gbp-feeds-atom-main")
@view("machines/<str:machine>/feed.rss", name="gbp-feeds-rss-machine")
@view("machines/<str:machine>/feed.atom", name="gbp-feeds-atom-machine")
def _(request: HttpRequest, *, machine: str | None = None) -> HttpResponse:
    """View to return the feed for the given machine, if applicable"""
    settings = Settings.from_environ()
    feed_type = utils.get_feed_type(request.path)
    feed_url = request.build_absolute_uri(reverse("dashboard"))
    stylesheets = [
        settings.EXT_CSS,
        request.build_absolute_uri(staticfiles_storage.url("gbp/gbp.css")),
    ]
    builds = utils.get_completed_builds(machine)
    feed = utils.build_feed(feed_type, feed_url, stylesheets, builds)

    response = HttpResponse(feed.writeString("utf-8"), content_type=str(feed_type))

    return response
