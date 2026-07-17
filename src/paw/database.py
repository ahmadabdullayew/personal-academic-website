from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from paw.environment import EnvironmentConfigurationError


def database_configuration(url: str, pool_max: int = 10) -> dict[str, Any]:
    if url == "sqlite:///:memory:":
        return {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

    try:
        parsed = urlparse(url)
        port = parsed.port
    except ValueError as error:
        raise EnvironmentConfigurationError("DATABASE_URL is malformed") from error
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise EnvironmentConfigurationError("DATABASE_URL must use PostgreSQL or test SQLite")
    if not parsed.hostname or not parsed.path.strip("/"):
        raise EnvironmentConfigurationError("DATABASE_URL lacks a host or database name")

    query = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=True)
    unknown_options = set(query) - {"sslmode"}
    if unknown_options:
        raise EnvironmentConfigurationError("DATABASE_URL contains unsupported query options")
    ssl_modes = query.get("sslmode", [])
    if len(ssl_modes) > 1 or (
        ssl_modes and ssl_modes[0] not in {"require", "verify-ca", "verify-full"}
    ):
        raise EnvironmentConfigurationError("DATABASE_URL contains an invalid sslmode")

    options: dict[str, Any] = {"pool": {"min_size": 1, "max_size": pool_max}}
    if ssl_modes:
        options["sslmode"] = ssl_modes[0]

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname,
        "PORT": str(port or 5432),
        "CONN_MAX_AGE": 0,
        "OPTIONS": options,
    }
