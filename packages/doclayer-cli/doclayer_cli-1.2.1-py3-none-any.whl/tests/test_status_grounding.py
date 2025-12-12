from __future__ import annotations

from doclayer_cli.status import _compute_grounding_metrics


def test_compute_grounding_metrics_flags_missing_fields():
    trace = {
        "job_id": "job-1",
        "status": "complete",
        "result_payload": {
            "extracted_data": {
                "total": 100,
                "currency": "USD",
            }
        },
        "groundings": [
            {
                "field_name": "total",
                "span_start": None,
                "span_end": None,
            }
        ],
    }

    metrics = _compute_grounding_metrics(trace)

    assert metrics["coverage"] == 0.0
    assert len(metrics["missing"]) == 2
    assert {row["field"] for row in metrics["missing"]} == {"total", "currency"}


def test_compute_grounding_metrics_full_coverage():
    trace = {
        "job_id": "job-2",
        "status": "complete",
        "result_payload": {
            "extracted_data": {
                "total": 100,
            }
        },
        "groundings": [
            {
                "field_name": "total",
                "span_start": 10,
                "span_end": 20,
                "page": 1,
            }
        ],
    }

    metrics = _compute_grounding_metrics(trace)

    assert metrics["coverage"] == 1.0
    assert metrics["missing"] == []
