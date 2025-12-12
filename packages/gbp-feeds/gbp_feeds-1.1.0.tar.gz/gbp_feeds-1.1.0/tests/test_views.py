# pylint: disable=missing-docstring
from unittest import TestCase

import feedparser
import gbp_testkit.fixtures as testkit
from django.template.loader import render_to_string
from django.urls import reverse
from gentoo_build_publisher.build_publisher import BuildPublisher
from gentoo_build_publisher.records import BuildRecord
from gentoo_build_publisher.types import Build
from unittest_fixtures import Fixtures, given, params

from . import lib


@given(testkit.client, lib.pulled_builds)
@params(feed_type=["rss", "atom"])
class FeedTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        feed_type = fixtures.feed_type
        url = f"/feed.{feed_type}?foo=bar"
        client = fixtures.client

        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(f"application/{feed_type}+xml", response["Content-Type"])

    def test_machine_feed(self, fixtures: Fixtures) -> None:
        feed_type = fixtures.feed_type
        url = f"/machines/babette/feed.{feed_type}"
        client = fixtures.client

        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(f"application/{feed_type}+xml", response["Content-Type"])

    def test_feed_content(self, fixtures: Fixtures) -> None:
        url = "/machines/babette/feed.atom"
        client = fixtures.client
        publisher = fixtures.publisher
        response = client.get(url)

        d = feedparser.parse(response.text)

        self.assertEqual("Gentoo Build Publisher", d.feed.title)
        self.assertEqual("http://testserver/", d.feed.link)
        self.assertEqual(3, len(d.entries))

        entry = d.entries[0]
        self.assertEqual("GBP build: babette 2", entry.title)
        self.assertEqual("Build babette.2 has been pulled", entry.description)
        self.assertEqual("http://testserver/machines/babette/builds/2/", entry.link)

        content = entry.content[0]
        self.assertEqual("text/html", content.type)
        self.assertEqual("en", content.language)
        build = get_build(fixtures.publisher, "babette.2")
        packages_built = publisher.storage.get_metadata(build).packages.built
        expected = render_to_string(
            "gbp_feeds/build.html", {"build": build, "packages_built": packages_built}
        )
        self.assertEqual(expected.strip(), content.value.strip())

    def test_feed_content_machine(self, fixtures: Fixtures) -> None:
        url = "/feed.atom"
        client = fixtures.client
        publisher = fixtures.publisher
        response = client.get(url)

        d = feedparser.parse(response.text)

        self.assertEqual("Gentoo Build Publisher", d.feed.title)
        self.assertEqual("http://testserver/", d.feed.link)
        self.assertEqual(6, len(d.entries))

        entry = d.entries[0]
        self.assertEqual("GBP build: polaris 3", entry.title)
        self.assertEqual("Build polaris.3 has been pulled", entry.description)
        self.assertEqual("http://testserver/machines/polaris/builds/3/", entry.link)

        content = entry.content[0]
        self.assertEqual("text/html", content.type)
        self.assertEqual("en", content.language)
        build = get_build(fixtures.publisher, "polaris.3")
        packages_built = publisher.storage.get_metadata(build).packages.built
        expected = render_to_string(
            "gbp_feeds/build.html", {"build": build, "packages_built": packages_built}
        )
        self.assertEqual(expected.strip(), content.value.strip())


@given(testkit.client)
class FeedLinkTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        client = fixtures.client

        response = client.get("/")

        expected = """\
<div class="col text-center">
  <a href="/feed.rss">Feed <i class="bi bi-rss-fill"></i></a>
</div>
"""
        self.assertIn(expected, response.text)


@given(testkit.client, lib.pulled_builds)
class MachineDetailsFeedLinkTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        pulled_builds = fixtures.pulled_builds
        machine = pulled_builds[0]
        client = fixtures.client
        machine_page = client.get(f"/machines/{machine}/").text
        machine_feed = reverse("gbp-feeds-rss-machine", kwargs={"machine": machine})

        expected = f"""\
<li class="list-group-item d-flex justify-content-between align-items-center">
  Feed <span><a href="{machine_feed}"><span><i class="bi bi-rss"></i></span></a></span>
</li>
"""
        self.assertIn(expected, machine_page)


def get_build(publisher: BuildPublisher, build_id: str) -> BuildRecord:
    records = publisher.repo.build_records
    build = Build.from_id(build_id)

    return records.get(build)
