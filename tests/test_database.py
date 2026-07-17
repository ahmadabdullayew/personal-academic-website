from __future__ import annotations

import pytest

from paw.database import database_configuration
from paw.environment import EnvironmentConfigurationError


def test_database_configuration_accepts_in_memory_test_sqlite() -> None:
    assert database_configuration("sqlite:///:memory:") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


def test_database_configuration_decodes_a_postgresql_url_and_configures_its_pool() -> None:
    assert database_configuration(
        "postgresql://user%40name:p%40ss@db.internal:5433/website",
        pool_max=17,
    ) == {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "website",
        "USER": "user@name",
        "PASSWORD": "p@ss",
        "HOST": "db.internal",
        "PORT": "5433",
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"pool": {"min_size": 1, "max_size": 17}},
    }


def test_database_configuration_uses_the_default_postgresql_port() -> None:
    configuration = database_configuration("postgres://user:password@localhost/website")

    assert configuration["PORT"] == "5432"


def test_database_configuration_preserves_a_supported_tls_mode() -> None:
    configuration = database_configuration(
        "postgresql://user:password@localhost/website?sslmode=verify-full"
    )

    assert configuration["OPTIONS"]["sslmode"] == "verify-full"


def test_database_configuration_rejects_an_unsupported_engine() -> None:
    with pytest.raises(EnvironmentConfigurationError, match="must use PostgreSQL"):
        database_configuration("mysql://localhost/website")


@pytest.mark.parametrize(
    "url",
    [
        "postgresql:///website",
        "postgresql://localhost",
    ],
)
def test_database_configuration_requires_a_host_and_database_name(url: str) -> None:
    with pytest.raises(EnvironmentConfigurationError, match="lacks a host or database name"):
        database_configuration(url)


def test_database_configuration_rejects_a_malformed_port() -> None:
    with pytest.raises(EnvironmentConfigurationError, match="is malformed"):
        database_configuration("postgresql://localhost:not-a-port/website")


@pytest.mark.parametrize(
    "url",
    [
        "postgresql://localhost/website?connect_timeout=5",
        "postgresql://localhost/website?sslmode=disable",
        "postgresql://localhost/website?sslmode=require&sslmode=verify-full",
    ],
)
def test_database_configuration_rejects_unsupported_query_options(url: str) -> None:
    with pytest.raises(EnvironmentConfigurationError, match="query options|invalid sslmode"):
        database_configuration(url)
