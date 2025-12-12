"""Tests for .views.utils"""

# pylint: disable=missing-docstring,unused-argument

from unittest import TestCase

import feedgenerator as fg
from unittest_fixtures import Fixtures, given, params, where

from gbp_feeds.django.gbp_feeds.views import utils

from . import lib


@params(feed_type=[utils.FeedType.ATOM, utils.FeedType.RSS])
@params(feed_cls=[fg.Atom1Feed, fg.Rss201rev2Feed])
class CreateFeedTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        feed = utils.create_feed(fixtures.feed_type, "http://gbp.invalid/")

        self.assertIsInstance(feed, fixtures.feed_cls)
        self.assertEqual(feed.feed["title"], "Gentoo Build Publisher")
        self.assertEqual(feed.feed["link"], "http://gbp.invalid/")
        self.assertEqual(
            feed.feed["description"], "Latest Gentoo Build Publisher builds"
        )
        self.assertEqual(feed.feed["language"], "en")

    def test_stylesheets(self, fixtures: Fixtures) -> None:
        stylesheets = ["http://test.invalid/foo.css", "http://test.invalid/bar.css"]

        feed = utils.create_feed(
            fixtures.feed_type, "http://gbp.invalid/", stylesheets=stylesheets
        )

        self.assertEqual([i.url for i in feed.feed["stylesheets"]], stylesheets)


@given(lib.pulled_builds)
@params(feed_type=[utils.FeedType.ATOM, utils.FeedType.RSS])
class BuildFeedTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        builds = fixtures.publisher.repo.build_records.for_machine("babette")

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)

        self.assertEqual(3, feed.num_items())
        self.assertEqual("Gentoo Build Publisher", feed.feed["title"])
        self.assertEqual("http://gbp.invalid/", feed.feed["link"])
        self.assertEqual(
            "Latest Gentoo Build Publisher builds", feed.feed["description"]
        )

    def test_item(self, fixtures: Fixtures) -> None:
        builds = fixtures.publisher.repo.build_records.for_machine("babette")

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)
        item = feed.items[0]

        self.assertEqual(item["title"], "GBP build: babette 2")
        self.assertEqual(item["link"], "http://gbp.invalid/machines/babette/builds/2/")
        self.assertEqual(item["description"], "Build babette.2 has been pulled")
        self.assertEqual(item["unique_id"], "babette.2")
        self.assertEqual(item["author_name"], "Gentoo Build Publisher")
        self.assertEqual(item["pubdate"], builds[0].completed)

    def test_item_note(self, fixtures: Fixtures) -> None:
        publisher = fixtures.publisher
        builds = publisher.repo.build_records.for_machine("babette")

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)
        build = builds[0]
        build = builds[0] = publisher.repo.build_records.save(
            build, note="This is a note."
        )

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)
        item = feed.items[0]

        self.assertTrue(
            "This is a note." in item["content"], "Build note not found in feed content"
        )

    def test_item_published(self, fixtures: Fixtures) -> None:
        publisher = fixtures.publisher
        builds = publisher.repo.build_records.for_machine("babette")

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)
        build = builds[0]
        publisher.publish(build)
        build = builds[0] = publisher.repo.build_records.get(build)

        feed = utils.build_feed(utils.FeedType.RSS, "http://gbp.invalid/", [], builds)
        item = feed.items[0]

        self.assertRegex(
            item["content"],
            r">Published</th>\W*<td>yes</td>",
            "Build not shown as published",
        )


@given(lib.pulled_builds)
@where(pulled_builds__machines=["babette"], pulled_builds__num_builds=1)
class GetItemContentTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        build = fixtures.publisher.repo.build_records.for_machine("babette")[0]

        content = utils.get_item_content(build)

        self.assertTrue(content.startswith("<h3>babette 0</h3>"))


@given(lib.pulled_builds)
class GetCompletedBuilds(TestCase):
    def test_without_machine(self, fixtures: Fixtures) -> None:
        builds = utils.get_completed_builds(None)

        self.assertEqual(6, len(builds))

        prev = builds[0]
        assert prev.completed
        for build in builds[1:]:
            assert build.completed
            self.assertGreater(prev.completed, build.completed)
            prev = build

    def test_with_machine(self, fixtures: Fixtures) -> None:
        machine = "babette"

        builds = utils.get_completed_builds(machine)

        self.assertEqual(3, len(builds))

        for build in builds:
            self.assertEqual(machine, build.machine)

    def test_with_noncomplete_build(self, fixtures: Fixtures) -> None:
        machine = "babette"
        publisher = fixtures.publisher
        repo = publisher.repo
        records = repo.build_records
        build = records.for_machine(machine)[0]

        # When the first (babette) build is not completed
        records.save(build, completed=None)

        builds = utils.get_completed_builds(machine)

        self.assertEqual(2, len(builds))
        self.assertNotIn(build, builds)


@params(feed_type=[utils.FeedType.ATOM, utils.FeedType.RSS])
@params(ext=["atom", "rss"])
class GetFeedTypeTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        path = f"/feed.{fixtures.ext}"

        feed_type = utils.get_feed_type(path)

        self.assertEqual(fixtures.feed_type, feed_type)

    def test_other(self, fixtures: Fixtures) -> None:
        path = "/index.html"

        with self.assertRaises(ValueError):
            utils.get_feed_type(path)


@given(lib.pulled_builds)
@where(pulled_builds__machines=["babette"], pulled_builds__num_builds=1)
@params(feed_type=[utils.FeedType.ATOM, utils.FeedType.RSS])
class BuildLinkTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        build = fixtures.publisher.repo.build_records.for_machine("babette")[0]
        feed = utils.create_feed(fixtures.feed_type, "http://testserver/")

        url = utils.build_link(build, feed)

        self.assertEqual("http://testserver/machines/babette/builds/0/", url)
