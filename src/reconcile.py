"""Control totals a night-shift analyst would check before publishing."""
from __future__ import annotations

from .night_service import NightExtractResult


def control_totals(result: NightExtractResult) -> dict:
    return {
        "window": result.window.label,
        "clarity_patient_rows": result.patients,
        "pat_enc_in_window": result.encounters,
        "fact_result_rows": result.results,
        "clarity_adt_events": result.adt_events,
        "orphan_results_rejected": result.orphan_results,
        "census_open_at_watermark_start": result.census_open_start,
        "census_open_at_watermark_end": result.census_open_end,
        "census_delta": result.census_delta,
    }
