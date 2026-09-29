"""Production-shaped night extract orchestration."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .clarity_tables import (
    load_clarity_adt,
    load_order_proc,
    load_order_results,
    load_pat_enc,
    load_patient,
)
from .config import DEFAULT_WINDOW, ExtractWindow
from .extract_window import adt_in_window, encounters_in_window, results_in_window


@dataclass
class NightExtractResult:
    window: ExtractWindow
    patients: int
    encounters: int
    results: int
    adt_events: int
    orphan_results: int
    census_open_start: int
    census_open_end: int
    fact_result: pd.DataFrame = field(repr=False)
    fact_adt: pd.DataFrame = field(repr=False)
    rejected: pd.DataFrame = field(repr=False)

    @property
    def census_delta(self) -> int:
        return self.census_open_end - self.census_open_start


def _census_open(pat_enc: pd.DataFrame, as_of) -> int:
    adm = pat_enc["HOSP_ADMSN_TIME"]
    dis = pat_enc["HOSP_DISCH_TIME"]
    return int(((adm <= as_of) & (dis.isna() | (dis > as_of))).sum())


def run_night_extract(window: ExtractWindow = DEFAULT_WINDOW) -> NightExtractResult:
    patient = load_patient()
    pat_enc = load_pat_enc()
    order_proc = load_order_proc()
    order_results = load_order_results()
    adt = load_clarity_adt()

    enc = encounters_in_window(pat_enc, window)
    res = results_in_window(order_results, window)
    adt_w = adt_in_window(adt, window)

    # Join results through ORDER_PROC to encounter and patient
    merged = res.merge(order_proc, on="ORDER_PROC_ID", how="left", suffixes=("", "_op"))
    merged = merged.merge(
        pat_enc[["PAT_ENC_CSN_ID", "PAT_ID"]],
        on="PAT_ENC_CSN_ID",
        how="left",
        suffixes=("", "_enc"),
    )
    known_pats = set(patient["PAT_ID"])
    orphan_mask = ~merged["PAT_ID"].isin(known_pats) | merged["PAT_ID"].isna()
    rejected = merged.loc[orphan_mask].copy()
    good = merged.loc[~orphan_mask].copy()

    fact_result = good[
        ["ORDER_PROC_ID", "PAT_ENC_CSN_ID", "PAT_ID", "LOINC", "ORD_VALUE", "RESULT_TIME"]
    ].copy()
    fact_result["EXTRACT_WINDOW_END"] = window.end.isoformat()

    fact_adt = adt_w.merge(
        pat_enc[["PAT_ENC_CSN_ID", "PAT_ID"]], on="PAT_ENC_CSN_ID", how="left"
    )

    return NightExtractResult(
        window=window,
        patients=int(patient["PAT_ID"].nunique()),
        encounters=len(enc),
        results=len(fact_result),
        adt_events=len(fact_adt),
        orphan_results=len(rejected),
        census_open_start=_census_open(pat_enc, window.start),
        census_open_end=_census_open(pat_enc, window.end),
        fact_result=fact_result,
        fact_adt=fact_adt,
        rejected=rejected,
    )
