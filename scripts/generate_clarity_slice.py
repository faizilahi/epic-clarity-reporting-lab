#!/usr/bin/env python3
"""Synthetic Clarity slice around the 2024-11-12 night window."""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
RNG = random.Random(1112)

N_PAT = 400
WINDOW_START = datetime(2024, 11, 12, 1, 0, 0)


def main() -> None:
    patients, encs, procs, results, adts = [], [], [], [], []
    proc_id = 0
    result_id = 0
    adt_id = 0
    csn = 100000

    for i in range(1, N_PAT + 1):
        pid = f"Z{i:06d}"
        patients.append(
            {
                "PAT_ID": pid,
                "PAT_MRN_ID": f"MRN{i:06d}",
                "BIRTH_DATE": f"{RNG.randint(1940,2005)}-{RNG.randint(1,12):02d}-{RNG.randint(1,28):02d}",
                "SEX": RNG.choice(["F", "M"]),
            }
        )
        # Most have a stay overlapping the night
        if RNG.random() < 0.7:
            csn += 1
            admit = WINDOW_START - timedelta(hours=RNG.randint(2, 72))
            if RNG.random() < 0.15:
                # Admit during window
                admit = WINDOW_START + timedelta(minutes=RNG.randint(10, 180))
            discharge = None
            if RNG.random() < 0.25:
                discharge = WINDOW_START + timedelta(minutes=RNG.randint(30, 200))
            encs.append(
                {
                    "PAT_ENC_CSN_ID": csn,
                    "PAT_ID": pid,
                    "HOSP_ADMSN_TIME": admit.isoformat(sep=" "),
                    "HOSP_DISCH_TIME": discharge.isoformat(sep=" ") if discharge else "",
                    "DEPARTMENT_ID": RNG.choice(["ED", "ICU", "MED", "SURG"]),
                }
            )
            # ADT events
            adt_id += 1
            adts.append(
                {
                    "ADT_ID": adt_id,
                    "PAT_ENC_CSN_ID": csn,
                    "EVENT_TYPE": "A01",
                    "EFFECTIVE_TIME": admit.isoformat(sep=" "),
                    "POINT_OF_CARE": "ED",
                }
            )
            if RNG.random() < 0.4:
                adt_id += 1
                xfer = max(admit, WINDOW_START) + timedelta(minutes=RNG.randint(5, 90))
                adts.append(
                    {
                        "ADT_ID": adt_id,
                        "PAT_ENC_CSN_ID": csn,
                        "EVENT_TYPE": "A02",
                        "EFFECTIVE_TIME": xfer.isoformat(sep=" "),
                        "POINT_OF_CARE": RNG.choice(["ICU", "MED", "SURG"]),
                    }
                )
            # Orders / results in window for ~half
            if RNG.random() < 0.5:
                proc_id += 1
                procs.append(
                    {
                        "ORDER_PROC_ID": proc_id,
                        "PAT_ENC_CSN_ID": csn,
                        "PROC_CODE": "LABBP",
                        "ORDER_TIME": (WINDOW_START + timedelta(minutes=RNG.randint(0, 200))).isoformat(sep=" "),
                    }
                )
                for loinc, val in (("8480-6", RNG.randint(110, 160)), ("8462-4", RNG.randint(60, 100))):
                    result_id += 1
                    results.append(
                        {
                            "RESULT_ID": result_id,
                            "ORDER_PROC_ID": proc_id,
                            "LOINC": loinc,
                            "ORD_VALUE": val,
                            "RESULT_TIME": (
                                WINDOW_START + timedelta(minutes=RNG.randint(5, 230))
                            ).isoformat(sep=" "),
                        }
                    )

    # Plant one orphan result (missing patient) for reject path
    proc_id += 1
    procs.append(
        {
            "ORDER_PROC_ID": proc_id,
            "PAT_ENC_CSN_ID": 999999,
            "PROC_CODE": "ORPHAN",
            "ORDER_TIME": WINDOW_START.isoformat(sep=" "),
        }
    )
    result_id += 1
    results.append(
        {
            "RESULT_ID": result_id,
            "ORDER_PROC_ID": proc_id,
            "LOINC": "2345-7",
            "ORD_VALUE": 1,
            "RESULT_TIME": (WINDOW_START + timedelta(minutes=40)).isoformat(sep=" "),
        }
    )
    encs.append(
        {
            "PAT_ENC_CSN_ID": 999999,
            "PAT_ID": "MISSING_PAT",
            "HOSP_ADMSN_TIME": WINDOW_START.isoformat(sep=" "),
            "HOSP_DISCH_TIME": "",
            "DEPARTMENT_ID": "ED",
        }
    )

    pd.DataFrame(patients).to_csv(DATA / "PATIENT.csv", index=False)
    pd.DataFrame(encs).to_csv(DATA / "PAT_ENC.csv", index=False)
    pd.DataFrame(procs).to_csv(DATA / "ORDER_PROC.csv", index=False)
    pd.DataFrame(results).to_csv(DATA / "ORDER_RESULTS.csv", index=False)
    pd.DataFrame(adts).to_csv(DATA / "CLARITY_ADT.csv", index=False)
    print(f"Clarity slice: {len(patients)} PATIENT, {len(encs)} PAT_ENC, {len(results)} ORDER_RESULTS")


if __name__ == "__main__":
    main()
