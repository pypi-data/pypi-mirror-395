# pylint: disable=missing-docstring
from unittest import TestCase

import gbp_testkit.fixtures as testkit
from unittest_fixtures import Fixtures, given

from . import lib


@given(testkit.client, lib.pulled_builds)
class ExtraHeaderTests(TestCase):
    def test_dashboard(self, fixtures: Fixtures) -> None:
        client = fixtures.client

        response = client.get("/")

        self.assertIn('href="http://testserver/feed.atom"', response.text)
        self.assertIn('href="http://testserver/feed.rss"', response.text)

    def test_machine_page(self, fixtures: Fixtures) -> None:
        client = fixtures.client

        response = client.get("/machines/babette/")

        self.assertIn(
            'href="http://testserver/machines/babette/feed.atom', response.text
        )
        self.assertIn(
            'href="http://testserver/machines/babette/feed.rss', response.text
        )

    def test_about_page(self, fixtures: Fixtures) -> None:
        client = fixtures.client

        response = client.get("/about/")

        self.assertIn('href="http://testserver/feed.atom"', response.text)
        self.assertIn('href="http://testserver/feed.rss"', response.text)
