from datetime import datetime

import pandas as pd

from src.config import ExtractWindow
from src.extract_window import encounters_in_window, results_in_window


def test_open_encounter_included():
    window = ExtractWindow(datetime(2024, 11, 12, 1), datetime(2024, 11, 12, 5))
    enc = pd.DataFrame(
        [
            {
                "PAT_ENC_CSN_ID": 1,
                "PAT_ID": "Z1",
                "HOSP_ADMSN_TIME": datetime(2024, 11, 11, 20),
                "HOSP_DISCH_TIME": pd.NaT,
            }
        ]
    )
    out = encounters_in_window(enc, window)
    assert len(out) == 1


def test_result_outside_window_excluded():
    window = ExtractWindow(datetime(2024, 11, 12, 1), datetime(2024, 11, 12, 5))
    res = pd.DataFrame(
        [{"ORDER_PROC_ID": 1, "RESULT_TIME": datetime(2024, 11, 12, 6), "LOINC": "x", "ORD_VALUE": 1}]
    )
    assert results_in_window(res, window).empty
