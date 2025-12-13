import re
from veox.event_processor import EvolutionEventProcessor


def test_verbose_format_worker_line_and_pipeline():
    ep = EvolutionEventProcessor(verbose=True, progress_enabled=False)
    event = {
        "type": "result_received",
        "worker_id": "w1",
        "worker_name": "doug-cpu-worker-1",
        "candidate_id": "G0_BASELINE_RF",
        "fitness": 0.856421,
        "has_aggregated_metrics": True,
        "metrics": {"holdout_auc": 0.87, "holdout_accuracy": 0.83},
        "pipeline_stages": [
            "imputers:StandardScaler",
            "models:RandomForestBinaryClassifier",
        ],
    }
    out = ep.process_event(event)
    assert out is not None
    # Main worker line
    assert "doug-cpu-worker-1" in out
    assert "fitness=0.856421" in out
    assert "agg=✓" in out
    # Pipeline line
    assert "Pipeline:" in out
    assert "StandardScaler" in out
    # Holdout metrics line
    assert "holdout" in out.lower()
    # Progress summary should not appear for first event
    assert "Progress:" not in out


def test_progress_summary_after_multiple_events():
    ep = EvolutionEventProcessor(verbose=True, progress_enabled=False)
    base_event = {
        "type": "result_received",
        "worker_id": "w1",
        "worker_name": "doug-cpu-worker-1",
        "candidate_id": "G0_BASELINE_RF",
        "fitness": 0.9,
        "has_aggregated_metrics": True,
        "metrics": {"holdout_auc": 0.9},
    }
    # Trigger multiple events to hit periodic progress reporting (every 10 results)
    last_out = None
    for i in range(10):
        ev = dict(base_event)
        ev["candidate_id"] = f"G{i}_CAND"
        ev["fitness"] = 0.8 + i * 0.001
        last_out = ep.process_event(ev)
    assert last_out is not None
    # Should contain a progress summary block
    assert "Progress:" in last_out
    assert "Worker Activity" in last_out
