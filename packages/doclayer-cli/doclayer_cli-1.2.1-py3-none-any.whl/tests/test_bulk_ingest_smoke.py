from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from doclayer_cli.cli import app


def _create_runner() -> CliRunner:
    try:
        return CliRunner(mix_stderr=False)
    except TypeError:
        return CliRunner()


class _FakeCursor:
    def __init__(self):
        self._rows = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        requested = (params or [[]])[0]
        self._rows = [(requested[0], 2)]

    def fetchall(self):
        return self._rows


class _FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return _FakeCursor()


def _write_config(path: Path, base_url: str, tenant_id: str, project_id: str) -> Path:
    payload = {
        "default_profile": "default",
        "profiles": {
            "default": {
                "base_url": base_url,
                "tenant_id": tenant_id,
                "default_project": project_id,
                "output_format": "table",
            }
        },
    }
    path.write_text(json.dumps(payload, indent=2))
    return path


def test_bulk_ingest_smoke(tmp_path, monkeypatch):
    runner = _create_runner()

    config_path = _write_config(
        tmp_path / "config.json", "https://cli.test", "tenant-1", "project-1"
    )
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    sample_file = docs_dir / "invoice.txt"
    sample_file.write_text("invoice data")

    monkeypatch.setenv("DOCLAYER_API_KEY", "dly_testkey")
    monkeypatch.setenv("DOCLAYER_PG_DSN", "postgresql://local-test")

    psycopg_mod = pytest.importorskip("psycopg")
    monkeypatch.setattr(psycopg_mod, "connect", lambda dsn: _FakeConnection())

    respx_mod = pytest.importorskip("respx")

    with respx_mod.mock(assert_all_called=True) as mock:
        mock.post("https://cli.test/api/v4/ingest").mock(
            return_value=httpx.Response(
                200,
                json={
                    "job_id": "job-batch-1",
                    "document_id": "doc-batch-1",
                    "status": "pending",
                },
            )
        )

        result = runner.invoke(
            app,
            [
                "--config",
                str(config_path),
                "ingest",
                "batch",
                str(docs_dir),
                "--workers",
                "1",
                "--verify-vectors",
                "--pg-timeout",
                "0.1",
                "--pg-poll-interval",
                "0.05",
            ],
        )

    assert result.exit_code == 0, result.stdout
    assert "job-batc" in result.stdout  # table truncates long IDs
    assert "doc-batc" in result.stdout


def test_ingest_batch_policy_violation(tmp_path, monkeypatch):
    runner = _create_runner()

    config_path = _write_config(
        tmp_path / "config.json", "https://cli.test", "tenant-1", "project-1"
    )
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    sample_file = docs_dir / "invoice.txt"
    sample_file.write_text("invoice data")

    monkeypatch.setenv("DOCLAYER_API_KEY", "dly_testkey")

    respx_mod = pytest.importorskip("respx")

    with respx_mod.mock(assert_all_called=True) as mock:
        mock.post("https://cli.test/api/v4/ingest").mock(
            return_value=httpx.Response(
                403,
                json={
                    "message": "Policy violation: manifest blocked",
                    "code": "POLICY_DENIED",
                },
            )
        )

        result = runner.invoke(
            app,
            [
                "--config",
                str(config_path),
                "ingest",
                "batch",
                str(docs_dir),
                "--workers",
                "1",
            ],
        )

    assert result.exit_code != 0
    assert "Policy violation" in result.stdout
