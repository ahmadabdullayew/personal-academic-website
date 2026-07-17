from __future__ import annotations

from collections.abc import MutableMapping
from unittest.mock import patch

import pytest

from paw.environment import (
    EnvironmentConfigurationError,
    RuntimeEnvironment,
    load_environment,
)


def valid_environment() -> MutableMapping[str, str]:
    return {
        "APP_ENV": "test",
        "DJANGO_SETTINGS_MODULE": "paw.settings.test",
        "DJANGO_DEBUG": "false",
        "DJANGO_SECRET_KEY": "test-only-secret-not-for-any-deployment",
        "DJANGO_ALLOWED_HOSTS": "testserver,localhost",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "http://testserver",
        "SITE_BASE_URL": "http://testserver",
        "DATABASE_URL": "sqlite:///:memory:",
        "DATABASE_POOL_MAX": "1",
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test",
        "S3_ENDPOINT_URL": "http://127.0.0.1:4566",
        "S3_BUCKET_QUARANTINE": "quarantine",
        "S3_BUCKET_PRIVATE": "private",
        "S3_BUCKET_PUBLIC": "public",
        "SQS_ENDPOINT_URL": "http://127.0.0.1:4566",
        "SQS_QUEUE_URL": "http://127.0.0.1:4566/queue",
        "DEFAULT_LANGUAGE": "en",
        "SUPPORTED_LANGUAGES": "en",
        "CONTACT_DELIVERY_MODE": "disabled",
        "ORCID_ENABLED": "false",
        "CROSSREF_ENABLED": "false",
        "LOG_LEVEL": "WARNING",
    }


def valid_production_environment() -> MutableMapping[str, str]:
    values = valid_environment()
    values.update(
        {
            "APP_ENV": "production",
            "DJANGO_SETTINGS_MODULE": "paw.settings.production",
            "DJANGO_SECRET_KEY": "s" * 64,
            "DJANGO_ALLOWED_HOSTS": "example.invalid",
            "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.invalid",
            "SITE_BASE_URL": "https://example.invalid",
            "DATABASE_URL": (
                "postgresql://user:password@db.example.invalid/website?sslmode=require"
            ),
            "AWS_ACCESS_KEY_ID": "",
            "AWS_SECRET_ACCESS_KEY": "",
            "S3_ENDPOINT_URL": "https://s3.example.invalid",
            "SQS_ENDPOINT_URL": "https://sqs.example.invalid",
            "SQS_QUEUE_URL": "https://sqs.example.invalid/000000000000/jobs",
        }
    )
    return values


def test_environment_accepts_the_test_contract() -> None:
    environment = RuntimeEnvironment.from_mapping(valid_environment())

    assert environment.app_env == "test"
    assert environment.supported_languages == ("en",)
    assert not environment.debug


def test_environment_loads_the_operating_system_contract() -> None:
    with patch.dict("os.environ", valid_environment(), clear=True):
        environment = load_environment()

    assert environment.app_env == "test"


def test_environment_rejects_a_missing_required_value() -> None:
    values = valid_environment()
    del values["AWS_REGION"]

    with pytest.raises(EnvironmentConfigurationError, match="AWS_REGION is required"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_requires_emulator_credentials_as_a_pair() -> None:
    values = valid_environment()
    values["AWS_SECRET_ACCESS_KEY"] = ""

    with pytest.raises(EnvironmentConfigurationError, match="supplied together"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_a_non_boolean_value() -> None:
    values = valid_environment()
    values["ORCID_ENABLED"] = "yes"

    with pytest.raises(EnvironmentConfigurationError, match="exactly true or false"):
        RuntimeEnvironment.from_mapping(values)


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("APP_ENV", "staging", "must be one of"),
        ("DJANGO_SETTINGS_MODULE", "paw.settings.production", "must be paw.settings.test"),
        ("CONTACT_DELIVERY_MODE", "smtp", "must be one of"),
        ("LOG_LEVEL", "TRACE", "must be one of"),
        ("SUPPORTED_LANGUAGES", "english", "valid BCP 47"),
        ("S3_BUCKET_PUBLIC", "Invalid_Bucket", "valid S3 bucket"),
        ("SITE_BASE_URL", "localhost:8000", "absolute HTTP"),
        ("S3_ENDPOINT_URL", "http://user:pass@localhost:4566", "must not contain credentials"),
        ("SQS_QUEUE_URL", "http://localhost:99999/queue", "valid HTTP"),
        ("DJANGO_ALLOWED_HOSTS", "http://testserver", "without schemes"),
        ("DJANGO_CSRF_TRUSTED_ORIGINS", "http://testserver/path", "without paths"),
    ],
)
def test_environment_rejects_documented_contract_violations(
    key: str,
    value: str,
    message: str,
) -> None:
    values = valid_environment()
    values[key] = value

    with pytest.raises(EnvironmentConfigurationError, match=message):
        RuntimeEnvironment.from_mapping(values)


@pytest.mark.parametrize("pool_size", ["many", "0", "-1"])
def test_environment_rejects_an_invalid_pool_size(pool_size: str) -> None:
    values = valid_environment()
    values["DATABASE_POOL_MAX"] = pool_size

    with pytest.raises(EnvironmentConfigurationError, match="must be (an integer|positive)"):
        RuntimeEnvironment.from_mapping(values)


@pytest.mark.parametrize("languages", [",,", "en,en"])
def test_environment_rejects_an_invalid_language_list(languages: str) -> None:
    values = valid_environment()
    values["SUPPORTED_LANGUAGES"] = languages

    with pytest.raises(
        EnvironmentConfigurationError,
        match="must contain at least one value|contains duplicates",
    ):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_reused_storage_boundaries() -> None:
    values = valid_environment()
    values["S3_BUCKET_PRIVATE"] = values["S3_BUCKET_PUBLIC"]

    with pytest.raises(EnvironmentConfigurationError, match="must be distinct"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_production_placeholders() -> None:
    values = valid_production_environment()
    values["DJANGO_SECRET_KEY"] = "test-only-secret-not-for-any-deployment"

    with pytest.raises(EnvironmentConfigurationError, match="at least 50 characters"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_production_debug_mode() -> None:
    values = valid_production_environment()
    values["DJANGO_DEBUG"] = "true"

    with pytest.raises(EnvironmentConfigurationError, match="must be false"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_a_non_https_production_origin() -> None:
    values = valid_production_environment()
    values["SITE_BASE_URL"] = "http://example.invalid"

    with pytest.raises(EnvironmentConfigurationError, match="must use HTTPS"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_sqlite_outside_tests() -> None:
    values = valid_environment()
    values.update(
        {
            "APP_ENV": "development",
            "DJANGO_SETTINGS_MODULE": "paw.settings.development",
        }
    )

    with pytest.raises(EnvironmentConfigurationError, match="permitted only"):
        RuntimeEnvironment.from_mapping(values)


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("DJANGO_ALLOWED_HOSTS", "other.invalid", "must include"),
        ("DJANGO_ALLOWED_HOSTS", "example.invalid,*", "must not contain"),
        ("DJANGO_CSRF_TRUSTED_ORIGINS", "https://other.invalid", "must include"),
        ("DATABASE_URL", "mysql://db.example.invalid/website", "must use PostgreSQL"),
        ("S3_ENDPOINT_URL", "http://s3.example.invalid", "must use HTTPS"),
    ],
)
def test_environment_rejects_unsafe_production_boundaries(
    key: str,
    value: str,
    message: str,
) -> None:
    values = valid_production_environment()
    values[key] = value

    with pytest.raises(EnvironmentConfigurationError, match=message):
        RuntimeEnvironment.from_mapping(values)


def test_environment_accepts_a_strict_production_contract() -> None:
    values = valid_production_environment()

    environment = RuntimeEnvironment.from_mapping(values)

    assert environment.app_env == "production"


def test_environment_rejects_static_aws_credentials_in_production() -> None:
    values = valid_production_environment()
    values["AWS_ACCESS_KEY_ID"] = "static-key"
    values["AWS_SECRET_ACCESS_KEY"] = "static-secret"

    with pytest.raises(EnvironmentConfigurationError, match="must use an IAM role"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_requires_database_tls_in_production() -> None:
    values = valid_production_environment()
    values["DATABASE_URL"] = "postgresql://user:password@db.example.invalid/website"

    with pytest.raises(EnvironmentConfigurationError, match="must require PostgreSQL TLS"):
        RuntimeEnvironment.from_mapping(values)


def test_environment_rejects_default_language_outside_supported_set() -> None:
    values = valid_environment()
    values["DEFAULT_LANGUAGE"] = "az"

    with pytest.raises(EnvironmentConfigurationError, match="must be included"):
        RuntimeEnvironment.from_mapping(values)
