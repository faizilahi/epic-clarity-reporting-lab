"""Loaders for Clarity-shaped CSVs used by the night extract."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import DATA


def load_patient(path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(path or DATA / "PATIENT.csv")
    need = {"PAT_ID", "PAT_MRN_ID", "BIRTH_DATE", "SEX"}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f"PATIENT missing {missing}")
    return df


def load_pat_enc(path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(path or DATA / "PAT_ENC.csv")
    for col in ("HOSP_ADMSN_TIME", "HOSP_DISCH_TIME"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def load_order_proc(path: Path | None = None) -> pd.DataFrame:
    return pd.read_csv(path or DATA / "ORDER_PROC.csv")


def load_order_results(path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(path or DATA / "ORDER_RESULTS.csv")
    df["RESULT_TIME"] = pd.to_datetime(df["RESULT_TIME"], errors="coerce")
    return df


def load_clarity_adt(path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(path or DATA / "CLARITY_ADT.csv")
    df["EFFECTIVE_TIME"] = pd.to_datetime(df["EFFECTIVE_TIME"], errors="coerce")
    return df
