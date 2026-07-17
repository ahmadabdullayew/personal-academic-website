from __future__ import annotations

from paw.environment import load_environment


def main() -> None:
    environment = load_environment()
    print(
        "environment valid:",
        f"app_env={environment.app_env}",
        f"languages={','.join(environment.supported_languages)}",
    )


if __name__ == "__main__":
    main()
