from __future__ import annotations

import os
import secrets
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "APP_ENV": "production",
            "DJANGO_SETTINGS_MODULE": "paw.settings.production",
            "DJANGO_DEBUG": "false",
            "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
            "DJANGO_ALLOWED_HOSTS": "example.invalid",
            "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.invalid",
            "SITE_BASE_URL": "https://example.invalid",
            "DATABASE_URL": (
                "postgresql://validation:validation@db.example.invalid/website?sslmode=require"
            ),
            "DATABASE_POOL_MAX": "10",
            "AWS_REGION": "us-east-1",
            "S3_ENDPOINT_URL": "https://s3.us-east-1.amazonaws.com",
            "S3_BUCKET_QUARANTINE": "paw-validation-quarantine",
            "S3_BUCKET_PRIVATE": "paw-validation-private",
            "S3_BUCKET_PUBLIC": "paw-validation-public",
            "SQS_ENDPOINT_URL": "https://sqs.us-east-1.amazonaws.com",
            "SQS_QUEUE_URL": (
                "https://sqs.us-east-1.amazonaws.com/000000000000/paw-validation-jobs"
            ),
            "DEFAULT_LANGUAGE": "en",
            "SUPPORTED_LANGUAGES": "en",
            "CONTACT_DELIVERY_MODE": "disabled",
            "ORCID_ENABLED": "false",
            "CROSSREF_ENABLED": "false",
            "LOG_LEVEL": "WARNING",
        }
    )
    environment.pop("AWS_ACCESS_KEY_ID", None)
    environment.pop("AWS_SECRET_ACCESS_KEY", None)

    result = subprocess.run(
        [
            sys.executable,
            "manage.py",
            "check",
            "--deploy",
            "--settings=paw.settings.production",
        ],
        cwd=ROOT,
        env=environment,
        check=False,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
