"""Tests for templatetags"""

# pylint: disable=missing-docstring

from unittest import TestCase

from unittest_fixtures import Fixtures, given

from gbp_feeds.django.gbp_feeds.templatetags import url_tags

from . import lib


@given(lib.context)
class FullURLTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        url = url_tags.full_url(fixtures.context, "dashboard")

        self.assertEqual("http://testserver/", url)

    def test_with_kwargs(self, fixtures: Fixtures) -> None:
        url = url_tags.full_url(fixtures.context, "gbp-machines", machine="babette")

        self.assertEqual("http://testserver/machines/babette/", url)
