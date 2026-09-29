"""Encounter-touch and result-window selection."""
from __future__ import annotations

import pandas as pd

from .config import ExtractWindow


def encounters_in_window(pat_enc: pd.DataFrame, window: ExtractWindow) -> pd.DataFrame:
    """Open at end of window OR admitted during window."""
    adm = pat_enc["HOSP_ADMSN_TIME"]
    dis = pat_enc["HOSP_DISCH_TIME"]
    admitted = (adm >= window.start) & (adm < window.end)
    still_open = adm < window.end
    still_open = still_open & (dis.isna() | (dis >= window.start))
    return pat_enc.loc[admitted | still_open].copy()


def results_in_window(order_results: pd.DataFrame, window: ExtractWindow) -> pd.DataFrame:
    t = order_results["RESULT_TIME"]
    return order_results.loc[(t >= window.start) & (t < window.end)].copy()


def adt_in_window(adt: pd.DataFrame, window: ExtractWindow) -> pd.DataFrame:
    t = adt["EFFECTIVE_TIME"]
    return adt.loc[(t >= window.start) & (t < window.end)].copy()
