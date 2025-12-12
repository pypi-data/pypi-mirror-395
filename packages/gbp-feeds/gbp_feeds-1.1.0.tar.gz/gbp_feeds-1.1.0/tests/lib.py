"""tests library"""

# pylint: disable=missing-docstring,redefined-outer-name

import random
from typing import Any, Iterable, Mapping
from unittest import mock

from django.http import HttpRequest
from django.template.context import Context
from faker import Faker
from faker.providers import BaseProvider
from gbp_testkit import fixtures as testkit
from gbp_testkit.factories import ArtifactFactory
from gentoo_build_publisher.build_publisher import BuildPublisher
from gentoo_build_publisher.types import Build
from unittest_fixtures import FixtureContext, Fixtures, fixture

fake = Faker()


class Provider(BaseProvider):
    def version(self) -> str:
        return f"{random.randint(0,9)}.{random.randint(0,9)}.{random.randint(0,9)}"

    def cpv(self) -> str:
        return f"{fake.word()}-{fake.word()}/{fake.word()}-{self.version()}"


fake.add_provider(Provider)


@fixture()
def mute_signals(_: Fixtures) -> FixtureContext[mock.Mock]:
    with mock.patch("gentoo_build_publisher.signals.PyDispatcherAdapter.emit") as m:
        yield m


@fixture(mute_signals, testkit.environ, testkit.publisher)
def pulled_builds(
    fixtures: Fixtures,
    machines: Iterable[str] = ("babette", "polaris"),
    num_builds: int = 3,
    packages_per_build: int = 3,
) -> list[str]:
    publisher: BuildPublisher = fixtures.publisher
    jenkins = publisher.jenkins
    builder: ArtifactFactory = jenkins.artifact_builder  # type: ignore[attr-defined]

    for i, machine in enumerate(machines):
        for j in range(num_builds):
            build = Build(machine, str(i + j))
            for _ in range(packages_per_build):
                builder.build(build, fake.cpv())
            publisher.pull(build)

    return publisher.repo.build_records.list_machines()


@fixture()
def request(
    _: Fixtures,
    path: str = "/feed.atom",
    server_name: str = "testserver",
    server_port: int = 80,
) -> HttpRequest:
    request = HttpRequest()
    request.path = path
    request.META["SERVER_NAME"] = server_name
    request.META["SERVER_PORT"] = server_port

    return request


@fixture(request)
def context(fixtures: Fixtures, context: Mapping[str, Any] | None = None) -> Context:
    context = context or {}

    return Context({"request": fixtures.request, **context})
