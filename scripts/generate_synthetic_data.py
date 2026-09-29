"""Synthetic Clarity-style relational tables (teaching approximations, not Epic copy)."""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
random.seed(7)

DEPARTMENTS = [
    (101, "Med-Surg North", "Inpatient"),
    (102, "ICU", "Inpatient"),
    (103, "Emergency", "Emergency"),
    (104, "Outpatient Clinic A", "Ambulatory"),
    (105, "Outpatient Clinic B", "Ambulatory"),
]

N_PATIENTS = 800
N_ENCOUNTERS = 3200


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dep_df = pd.DataFrame(
        [
            {
                "DEPARTMENT_ID": d[0],
                "DEPARTMENT_NAME": d[1],
                "SERVICE_AREA": d[2],
            }
            for d in DEPARTMENTS
        ]
    )

    patients = []
    for i in range(1, N_PATIENTS + 1):
        patients.append(
            {
                "PAT_ID": i,
                "PAT_NAME": f"Synthetic Patient {i}",
                "SEX": random.choice(["F", "M"]),
                "BIRTH_DATE": (date(1945, 1, 1) + timedelta(days=random.randint(0, 25000))).isoformat(),
            }
        )
    pat_df = pd.DataFrame(patients)

    enc_types = ["Inpatient", "Emergency", "Ambulatory"]
    enc_rows = []
    for enc_id in range(1, N_ENCOUNTERS + 1):
        enc_type = random.choices(enc_types, weights=[0.25, 0.35, 0.40])[0]
        contact = date(2024, 1, 1) + timedelta(days=random.randint(0, 364))
        los = None
        if enc_type == "Inpatient":
            los = round(random.uniform(1.0, 8.5), 1)
        dep = random.choice([101, 102] if enc_type == "Inpatient" else [103, 104, 105])
        enc_rows.append(
            {
                "PAT_ENC_CSN_ID": enc_id,
                "PAT_ID": random.randint(1, N_PATIENTS),
                "DEPARTMENT_ID": dep,
                "CONTACT_DATE": contact.isoformat(),
                "ENC_TYPE": enc_type,
                "LENGTH_OF_STAY_DAYS": los if los is not None else "",
            }
        )
    enc_df = pd.DataFrame(enc_rows)

    proc_catalog = [
        ("80053", "Comprehensive metabolic panel"),
        ("83036", "Hemoglobin A1c"),
        ("71046", "Chest X-ray"),
        ("99285", "ED visit high severity"),
        ("99213", "Office visit est level 3"),
    ]
    orders = []
    for oid in range(1, 4500):
        code, name = random.choice(proc_catalog)
        orders.append(
            {
                "ORDER_ID": oid,
                "PAT_ENC_CSN_ID": random.randint(1, N_ENCOUNTERS),
                "PROC_CODE": code,
                "PROC_NAME": name,
                "ORDER_STATUS": random.choice(["Completed", "Completed", "Canceled"]),
                "ORDER_TIME": (date(2024, 6, 1) + timedelta(hours=random.randint(0, 5000))).isoformat(),
            }
        )
    order_df = pd.DataFrame(orders)

    dep_df.to_csv(DATA_DIR / "clarity_dep.csv", index=False)
    pat_df.to_csv(DATA_DIR / "patient.csv", index=False)
    enc_df.to_csv(DATA_DIR / "pat_enc.csv", index=False)
    order_df.to_csv(DATA_DIR / "order_proc.csv", index=False)
    print(f"Wrote departments={len(dep_df)}, patients={len(pat_df)}, enc={len(enc_df)}, orders={len(order_df)}")


if __name__ == "__main__":
    main()
