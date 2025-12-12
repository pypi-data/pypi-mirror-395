from pathlib import Path

from doclayer_cli.ingest import UploadResult
from doclayer_cli.state import UploadStateStore


def test_state_store_records_and_skips(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    store = UploadStateStore(state_path, resume=True)

    path_ok = tmp_path / "ok.pdf"
    path_ok.write_bytes(b"data")
    success = UploadResult(
        path=path_ok,
        job_id="job-1",
        document_id="doc-1",
        status="success",
        size_bytes=4,
    )
    store.record(success)

    assert state_path.exists()
    assert store.should_skip(path_ok) is True

    # Reload from disk to ensure persistence works
    store_reloaded = UploadStateStore(state_path, resume=True)
    assert store_reloaded.should_skip(path_ok) is True


def test_state_store_does_not_skip_failures(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    store = UploadStateStore(state_path, resume=True)

    path_fail = tmp_path / "fail.pdf"
    path_fail.write_bytes(b"broken")
    failure = UploadResult(path=path_fail, error="boom", status="error")
    store.record(failure)

    assert store.should_skip(path_fail) is False
