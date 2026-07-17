from __future__ import annotations

import os
import secrets
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_HOSTS = {
    "preview": "pr-1.preview.ahmadabdullayev.com",
    "staging": "staging.ahmadabdullayev.com",
    "production": "ahmadabdullayev.com",
}


def main() -> None:
    for app_env, host in DEPLOYMENT_HOSTS.items():
        environment = os.environ.copy()
        environment.update(
            {
                "APP_ENV": app_env,
                "DJANGO_SETTINGS_MODULE": f"paw.settings.{app_env}",
                "DJANGO_DEBUG": "false",
                "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
                "DJANGO_ALLOWED_HOSTS": host,
                "DJANGO_CSRF_TRUSTED_ORIGINS": f"https://{host}",
                "SITE_BASE_URL": f"https://{host}",
                "DATABASE_URL": (
                    "postgresql://validation:validation@db.internal/website?sslmode=require"
                ),
                "DATABASE_POOL_MAX": "10",
                "AWS_REGION": "eu-central-1",
                "S3_ENDPOINT_URL": "https://s3.eu-central-1.amazonaws.com",
                "S3_BUCKET_QUARANTINE": "paw-validation-quarantine",
                "S3_BUCKET_PRIVATE": "paw-validation-private",
                "S3_BUCKET_PUBLIC": "paw-validation-public",
                "SQS_ENDPOINT_URL": "https://sqs.eu-central-1.amazonaws.com",
                "SQS_QUEUE_URL": (
                    "https://sqs.eu-central-1.amazonaws.com/000000000000/paw-validation-jobs"
                ),
                "DEFAULT_LANGUAGE": "en",
                "SUPPORTED_LANGUAGES": "en",
                "CONTACT_DELIVERY_MODE": "ses" if app_env == "production" else "disabled",
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
                f"--settings=paw.settings.{app_env}",
            ],
            cwd=ROOT,
            env=environment,
            check=False,
        )
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
