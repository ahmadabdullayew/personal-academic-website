from __future__ import annotations

import shutil
import subprocess
import sys

import pytest
from scripts import build_requirements_matrix as builder


def _resolved_pdftotext(_command: str) -> str:
    return "/opt/poppler/bin/pdftotext"


def _missing_pdftotext(_command: str) -> None:
    return None


def test_pdftotext_preflight_rejects_a_missing_executable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(shutil, "which", _missing_pdftotext)

    with pytest.raises(
        RuntimeError,
        match=r"requires Poppler pdftotext >= 24\.02\.0.*not found on PATH",
    ) as error:
        builder._preflight_pdftotext()

    assert "sudo apt install poppler-utils" in str(error.value)
    assert "brew install poppler" in str(error.value)
    assert "pdftotext -v" in str(error.value)


def test_matrix_builder_surfaces_the_preflight_as_a_clean_cli_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(shutil, "which", _missing_pdftotext)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_requirements_matrix.py",
            "--srs-pdf",
            "/tmp/srs.pdf",
            "--backend-pdf",
            "/tmp/backend.pdf",
        ],
    )

    with pytest.raises(SystemExit, match=r"^error: Matrix regeneration requires") as error:
        builder.main()

    assert "not found on PATH" in str(error.value)


def test_pdftotext_preflight_accepts_the_tested_minimum_from_stderr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def supported_version(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert command == ["/opt/poppler/bin/pdftotext", "-v"]
        assert check is False
        assert capture_output is True
        assert text is True
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="",
            stderr="pdftotext version 24.02.0\nCopyright The Poppler Developers\n",
        )

    monkeypatch.setattr(shutil, "which", _resolved_pdftotext)
    monkeypatch.setattr(subprocess, "run", supported_version)

    assert builder._preflight_pdftotext() == "/opt/poppler/bin/pdftotext"


def test_pdftotext_preflight_rejects_an_outdated_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def outdated_version(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="pdftotext version 23.11.0\n",
            stderr="",
        )

    monkeypatch.setattr(shutil, "which", _resolved_pdftotext)
    monkeypatch.setattr(subprocess, "run", outdated_version)

    with pytest.raises(
        RuntimeError,
        match=r"found Poppler pdftotext 23\.11\.0.*requires >= 24\.02\.0",
    ):
        builder._preflight_pdftotext()


def test_pdftotext_preflight_rejects_unparseable_version_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unparseable_version(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="unknown PDF converter\n",
            stderr="",
        )

    monkeypatch.setattr(shutil, "which", _resolved_pdftotext)
    monkeypatch.setattr(subprocess, "run", unparseable_version)

    with pytest.raises(RuntimeError, match=r"could not parse the Poppler version") as error:
        builder._preflight_pdftotext()

    assert "unknown PDF converter" in str(error.value)
    assert ">= 24.02.0" in str(error.value)
