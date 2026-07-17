from __future__ import annotations

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import ParseResult, parse_qs, urlparse

APP_ENVIRONMENTS = frozenset({"development", "preview", "production", "staging", "test"})
DEPLOYED_ENVIRONMENTS = frozenset({"preview", "production", "staging"})
CONTACT_DELIVERY_MODES = frozenset({"console", "disabled", "ses"})
LOG_LEVELS = frozenset({"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"})
LANGUAGE_TAG_PATTERN = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
BUCKET_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$")
PREVIEW_HOST_PATTERN = re.compile(
    r"^pr-[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.preview\.ahmadabdullayev\.com$"
)
SELECTED_AWS_REGION = "eu-central-1"
SELECTED_LANGUAGE = "en"
DEPLOYED_CONTACT_MODES = {
    "preview": "disabled",
    "staging": "disabled",
    "production": "ses",
}


class EnvironmentConfigurationError(ValueError):
    """Raised when the runtime environment contract is invalid."""


def _required(values: Mapping[str, str], name: str) -> str:
    value = values.get(name, "").strip()
    if not value:
        raise EnvironmentConfigurationError(f"{name} is required")
    return value


def _boolean(values: Mapping[str, str], name: str) -> bool:
    raw = _required(values, name).lower()
    if raw not in {"true", "false"}:
        raise EnvironmentConfigurationError(f"{name} must be exactly true or false")
    return raw == "true"


def _choice(values: Mapping[str, str], name: str, choices: frozenset[str]) -> str:
    value = _required(values, name)
    if value not in choices:
        expected = ", ".join(sorted(choices))
        raise EnvironmentConfigurationError(f"{name} must be one of: {expected}")
    return value


def _positive_integer(values: Mapping[str, str], name: str) -> int:
    raw = _required(values, name)
    try:
        value = int(raw)
    except ValueError as error:
        raise EnvironmentConfigurationError(f"{name} must be an integer") from error
    if value < 1:
        raise EnvironmentConfigurationError(f"{name} must be positive")
    return value


def _csv(values: Mapping[str, str], name: str) -> tuple[str, ...]:
    items = tuple(item.strip() for item in _required(values, name).split(",") if item.strip())
    if not items:
        raise EnvironmentConfigurationError(f"{name} must contain at least one value")
    if len(items) != len(set(items)):
        raise EnvironmentConfigurationError(f"{name} contains duplicates")
    return items


def _parse_http_url(value: str, name: str, *, origin_only: bool = False) -> ParseResult:
    try:
        parsed = urlparse(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as error:
        raise EnvironmentConfigurationError(f"{name} must be a valid HTTP(S) URL") from error
    if parsed.scheme not in {"http", "https"} or not hostname:
        raise EnvironmentConfigurationError(f"{name} must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise EnvironmentConfigurationError(f"{name} must not contain credentials")
    if port is not None and not 1 <= port <= 65_535:
        raise EnvironmentConfigurationError(f"{name} contains an invalid port")
    if origin_only and (
        parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment
    ):
        raise EnvironmentConfigurationError(f"{name} must contain origins without paths or queries")
    return parsed


def _http_url(values: Mapping[str, str], name: str, *, origin_only: bool = False) -> str:
    value = _required(values, name)
    _parse_http_url(value, name, origin_only=origin_only)
    return value


def _database_url(values: Mapping[str, str]) -> str:
    value = _required(values, "DATABASE_URL")
    if value == "sqlite:///:memory:":
        return value
    try:
        parsed = urlparse(value)
        hostname = parsed.hostname
        _port = parsed.port
    except ValueError as error:
        raise EnvironmentConfigurationError("DATABASE_URL must be a valid URL") from error
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise EnvironmentConfigurationError("DATABASE_URL must use PostgreSQL or test SQLite")
    if not hostname or not parsed.path.strip("/"):
        raise EnvironmentConfigurationError("DATABASE_URL lacks a host or database name")
    try:
        query = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=True)
    except ValueError as error:
        raise EnvironmentConfigurationError("DATABASE_URL contains an invalid query") from error
    if set(query) - {"sslmode"}:
        raise EnvironmentConfigurationError("DATABASE_URL contains unsupported query options")
    ssl_modes = query.get("sslmode", [])
    if len(ssl_modes) > 1 or (
        ssl_modes and ssl_modes[0] not in {"require", "verify-ca", "verify-full"}
    ):
        raise EnvironmentConfigurationError("DATABASE_URL contains an invalid sslmode")
    return value


def _origins(values: Mapping[str, str], name: str) -> tuple[str, ...]:
    origins = _csv(values, name)
    for origin in origins:
        _parse_http_url(origin, name, origin_only=True)
    return origins


def _hosts(values: Mapping[str, str], name: str) -> tuple[str, ...]:
    hosts = _csv(values, name)
    for host in hosts:
        if (
            "://" in host
            or "/" in host
            or "@" in host
            or any(character.isspace() for character in host)
        ):
            raise EnvironmentConfigurationError(
                f"{name} must contain host names without schemes or paths"
            )
    return hosts


def _languages(values: Mapping[str, str], name: str) -> tuple[str, ...]:
    languages = _csv(values, name)
    if any(not LANGUAGE_TAG_PATTERN.fullmatch(language) for language in languages):
        raise EnvironmentConfigurationError(f"{name} must contain valid BCP 47 language tags")
    return languages


def _bucket_name(values: Mapping[str, str], name: str) -> str:
    value = _required(values, name)
    if not BUCKET_NAME_PATTERN.fullmatch(value) or ".." in value:
        raise EnvironmentConfigurationError(f"{name} must be a valid S3 bucket name")
    return value


@dataclass(frozen=True, slots=True)
class RuntimeEnvironment:
    app_env: str
    django_settings_module: str
    debug: bool
    secret_key: str
    allowed_hosts: tuple[str, ...]
    csrf_trusted_origins: tuple[str, ...]
    site_base_url: str
    database_url: str
    database_pool_max: int
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_endpoint_url: str
    s3_bucket_quarantine: str
    s3_bucket_private: str
    s3_bucket_public: str
    sqs_endpoint_url: str
    sqs_queue_url: str
    default_language: str
    supported_languages: tuple[str, ...]
    contact_delivery_mode: str
    orcid_enabled: bool
    crossref_enabled: bool
    log_level: str

    @classmethod
    def from_mapping(cls, values: Mapping[str, str]) -> RuntimeEnvironment:
        environment = cls(
            app_env=_choice(values, "APP_ENV", APP_ENVIRONMENTS),
            django_settings_module=_required(values, "DJANGO_SETTINGS_MODULE"),
            debug=_boolean(values, "DJANGO_DEBUG"),
            secret_key=_required(values, "DJANGO_SECRET_KEY"),
            allowed_hosts=_hosts(values, "DJANGO_ALLOWED_HOSTS"),
            csrf_trusted_origins=_origins(values, "DJANGO_CSRF_TRUSTED_ORIGINS"),
            site_base_url=_http_url(values, "SITE_BASE_URL", origin_only=True),
            database_url=_database_url(values),
            database_pool_max=_positive_integer(values, "DATABASE_POOL_MAX"),
            aws_region=_required(values, "AWS_REGION"),
            aws_access_key_id=values.get("AWS_ACCESS_KEY_ID", "").strip(),
            aws_secret_access_key=values.get("AWS_SECRET_ACCESS_KEY", "").strip(),
            s3_endpoint_url=_http_url(values, "S3_ENDPOINT_URL", origin_only=True),
            s3_bucket_quarantine=_bucket_name(values, "S3_BUCKET_QUARANTINE"),
            s3_bucket_private=_bucket_name(values, "S3_BUCKET_PRIVATE"),
            s3_bucket_public=_bucket_name(values, "S3_BUCKET_PUBLIC"),
            sqs_endpoint_url=_http_url(values, "SQS_ENDPOINT_URL", origin_only=True),
            sqs_queue_url=_http_url(values, "SQS_QUEUE_URL"),
            default_language=_required(values, "DEFAULT_LANGUAGE"),
            supported_languages=_languages(values, "SUPPORTED_LANGUAGES"),
            contact_delivery_mode=_choice(
                values,
                "CONTACT_DELIVERY_MODE",
                CONTACT_DELIVERY_MODES,
            ),
            orcid_enabled=_boolean(values, "ORCID_ENABLED"),
            crossref_enabled=_boolean(values, "CROSSREF_ENABLED"),
            log_level=_choice(
                {"LOG_LEVEL": _required(values, "LOG_LEVEL").upper()},
                "LOG_LEVEL",
                LOG_LEVELS,
            ),
        )
        environment.validate()
        return environment

    @classmethod
    def from_os(cls) -> RuntimeEnvironment:
        return cls.from_mapping(os.environ)

    def validate(self) -> None:
        expected_settings_module = f"paw.settings.{self.app_env}"
        if self.django_settings_module != expected_settings_module:
            raise EnvironmentConfigurationError(
                "DJANGO_SETTINGS_MODULE must be "
                f"{expected_settings_module} when APP_ENV is {self.app_env}"
            )
        if self.default_language not in self.supported_languages:
            raise EnvironmentConfigurationError(
                "DEFAULT_LANGUAGE must be included in SUPPORTED_LANGUAGES"
            )
        if len({self.s3_bucket_quarantine, self.s3_bucket_private, self.s3_bucket_public}) != 3:
            raise EnvironmentConfigurationError("S3 buckets must be distinct")
        if not urlparse(self.sqs_queue_url).path.strip("/"):
            raise EnvironmentConfigurationError("SQS_QUEUE_URL must include a queue path")
        if bool(self.aws_access_key_id) != bool(self.aws_secret_access_key):
            raise EnvironmentConfigurationError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be supplied together"
            )
        if self.app_env not in DEPLOYED_ENVIRONMENTS and not self.aws_access_key_id:
            raise EnvironmentConfigurationError(
                "local and test environments require explicit emulator AWS credentials"
            )
        database_scheme = urlparse(self.database_url).scheme
        if database_scheme == "sqlite" and self.app_env != "test":
            raise EnvironmentConfigurationError("SQLite is permitted only when APP_ENV is test")
        if self.app_env in DEPLOYED_ENVIRONMENTS:
            if self.aws_access_key_id or self.aws_secret_access_key:
                raise EnvironmentConfigurationError(
                    "deployed environments must use an IAM role instead of static AWS credentials"
                )
            if self.debug:
                raise EnvironmentConfigurationError(
                    "DJANGO_DEBUG must be false in deployed environments"
                )
            if len(self.secret_key) < 50 or any(
                marker in self.secret_key.lower()
                for marker in ("change-me", "development-only", "placeholder", "test-only")
            ):
                raise EnvironmentConfigurationError(
                    "DJANGO_SECRET_KEY must be at least 50 characters and not use a placeholder"
                )
            production_urls = {
                "SITE_BASE_URL": self.site_base_url,
                "S3_ENDPOINT_URL": self.s3_endpoint_url,
                "SQS_ENDPOINT_URL": self.sqs_endpoint_url,
                "SQS_QUEUE_URL": self.sqs_queue_url,
            }
            for name, value in production_urls.items():
                if urlparse(value).scheme != "https":
                    raise EnvironmentConfigurationError(
                        f"{name} must use HTTPS in deployed environments"
                    )
            site = urlparse(self.site_base_url)
            site_origin = f"{site.scheme}://{site.netloc}"
            if site.hostname not in self.allowed_hosts:
                raise EnvironmentConfigurationError(
                    "DJANGO_ALLOWED_HOSTS must include the SITE_BASE_URL host"
                )
            if "*" in self.allowed_hosts:
                raise EnvironmentConfigurationError("DJANGO_ALLOWED_HOSTS must not contain *")
            if site_origin not in {origin.rstrip("/") for origin in self.csrf_trusted_origins}:
                raise EnvironmentConfigurationError(
                    "DJANGO_CSRF_TRUSTED_ORIGINS must include the SITE_BASE_URL origin"
                )
            if database_scheme not in {"postgres", "postgresql"}:
                raise EnvironmentConfigurationError("deployed DATABASE_URL must use PostgreSQL")
            database_query = parse_qs(urlparse(self.database_url).query)
            if database_query.get("sslmode", [""])[0] not in {
                "require",
                "verify-ca",
                "verify-full",
            }:
                raise EnvironmentConfigurationError(
                    "deployed DATABASE_URL must require PostgreSQL TLS"
                )
            self._validate_selected_deployment_scope()

    def _validate_selected_deployment_scope(self) -> None:
        if self.aws_region != SELECTED_AWS_REGION:
            raise EnvironmentConfigurationError(
                f"deployed AWS_REGION must be {SELECTED_AWS_REGION}"
            )
        if self.default_language != SELECTED_LANGUAGE or self.supported_languages != (
            SELECTED_LANGUAGE,
        ):
            raise EnvironmentConfigurationError(
                "deployed language scope must contain only the selected en locale"
            )
        if self.orcid_enabled or self.crossref_enabled:
            raise EnvironmentConfigurationError(
                "ORCID_ENABLED and CROSSREF_ENABLED must remain false in deployed scope"
            )

        expected_contact_mode = DEPLOYED_CONTACT_MODES[self.app_env]
        if self.contact_delivery_mode != expected_contact_mode:
            raise EnvironmentConfigurationError(
                f"CONTACT_DELIVERY_MODE must be {expected_contact_mode} in {self.app_env}"
            )

        host = urlparse(self.site_base_url).hostname
        if not host:
            raise EnvironmentConfigurationError("SITE_BASE_URL must contain a host")
        if self.app_env == "preview":
            host_is_approved = PREVIEW_HOST_PATTERN.fullmatch(host) is not None
        else:
            expected_host = {
                "staging": "staging.ahmadabdullayev.com",
                "production": "ahmadabdullayev.com",
            }[self.app_env]
            host_is_approved = host == expected_host
        if not host_is_approved:
            raise EnvironmentConfigurationError(
                f"SITE_BASE_URL host is outside the selected {self.app_env} origin"
            )

        selected_origin = f"https://{host}"
        if self.site_base_url.rstrip("/") != selected_origin:
            raise EnvironmentConfigurationError(
                "SITE_BASE_URL must equal the selected origin without a path"
            )
        if self.allowed_hosts != (host,):
            raise EnvironmentConfigurationError(
                "DJANGO_ALLOWED_HOSTS must contain only the selected deployment host"
            )
        if tuple(origin.rstrip("/") for origin in self.csrf_trusted_origins) != (selected_origin,):
            raise EnvironmentConfigurationError(
                "DJANGO_CSRF_TRUSTED_ORIGINS must contain only the selected origin"
            )

        expected_service_hosts = {
            "S3_ENDPOINT_URL": "s3.eu-central-1.amazonaws.com",
            "SQS_ENDPOINT_URL": "sqs.eu-central-1.amazonaws.com",
            "SQS_QUEUE_URL": "sqs.eu-central-1.amazonaws.com",
        }
        service_urls = {
            "S3_ENDPOINT_URL": self.s3_endpoint_url,
            "SQS_ENDPOINT_URL": self.sqs_endpoint_url,
            "SQS_QUEUE_URL": self.sqs_queue_url,
        }
        for name, value in service_urls.items():
            if urlparse(value).hostname != expected_service_hosts[name]:
                raise EnvironmentConfigurationError(
                    f"{name} must use the selected eu-central-1 AWS endpoint"
                )


def load_environment() -> RuntimeEnvironment:
    return RuntimeEnvironment.from_os()
