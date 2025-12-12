from __future__ import annotations

import time
from typing import Dict, Iterable, Sequence


class PgvectorProbeError(RuntimeError):
    """Raised when pgvector verification fails."""


def wait_for_vectors(
    document_ids: Sequence[str],
    dsn: str,
    *,
    min_rows: int = 1,
    timeout: float = 30.0,
    poll_interval: float = 2.0,
) -> Dict[str, int]:
    """
    Poll the `chunk_vectors` table until every document ID has at least `min_rows`.

    Parameters
    ----------
    document_ids:
        Iterable of document UUID strings to verify.
    dsn:
        psycopg-compatible connection string.
    min_rows:
        Minimum number of rows that must exist in `chunk_vectors` for each document.
    timeout:
        Maximum number of seconds to wait before giving up.
    poll_interval:
        Delay between polls in seconds.
    """

    doc_set = {str(doc_id) for doc_id in document_ids if doc_id}
    if not doc_set:
        return {}

    try:
        import psycopg  # type: ignore[import]
    except ImportError as exc:  # pragma: no cover - handled by CLI command
        raise PgvectorProbeError(
            "psycopg is not installed. Install `psycopg[binary]` to enable pgvector verification."
        ) from exc

    deadline = time.time() + max(timeout, 0.0)
    counts: Dict[str, int] = {doc_id: 0 for doc_id in doc_set}
    pending: set[str] = set(doc_set)

    while pending and time.time() <= deadline:
        try:
            with psycopg.connect(
                dsn
            ) as conn:  # pragma: no cover - exercised in smoke test via monkeypatch
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT doc_id::text, COUNT(*) AS count
                        FROM chunk_vectors
                        WHERE doc_id = ANY(%s)
                        GROUP BY doc_id
                        """,
                        (list(pending),),
                    )
                    rows: Iterable[tuple[str, int]] = cur.fetchall()
        except Exception as exc:  # pragma: no cover - depends on runtime DB state
            raise PgvectorProbeError(str(exc)) from exc

        for doc_id, seen in rows:
            doc_id_str = str(doc_id)
            counts[doc_id_str] = int(seen)
            if seen >= min_rows and doc_id_str in pending:
                pending.remove(doc_id_str)

        if pending:
            time.sleep(max(poll_interval, 0.1))

    return counts
