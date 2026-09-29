"""Clarity-inspired operational reports using DuckDB + pandas."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def register_csvs(con: duckdb.DuckDBPyConnection, data_dir: Path) -> None:
    for table in ("PAT_ENC", "CLARITY_DEP", "ORDER_PROC", "PATIENT"):
        path = data_dir / f"{table.lower()}.csv"
        con.execute(
            f"CREATE OR REPLACE VIEW {table} AS SELECT * FROM read_csv_auto('{path.as_posix()}')"
        )


def average_length_of_stay(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql = """
    SELECT
        d.DEPARTMENT_NAME,
        COUNT(*) AS inpatient_encounters,
        ROUND(AVG(e.LENGTH_OF_STAY_DAYS), 2) AS avg_los_days,
        ROUND(MEDIAN(e.LENGTH_OF_STAY_DAYS), 2) AS median_los_days
    FROM PAT_ENC e
    JOIN CLARITY_DEP d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
    WHERE e.ENC_TYPE = 'Inpatient'
      AND e.LENGTH_OF_STAY_DAYS IS NOT NULL
    GROUP BY 1
    ORDER BY inpatient_encounters DESC
    """
    return con.execute(sql).df()


def encounter_volume_by_month(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql = """
    SELECT
        DATE_TRUNC('month', CAST(e.CONTACT_DATE AS DATE)) AS month,
        e.ENC_TYPE,
        COUNT(*) AS encounter_count
    FROM PAT_ENC e
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    return con.execute(sql).df()


def order_volume_top_procedures(con: duckdb.DuckDBPyConnection, limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        o.PROC_CODE,
        o.PROC_NAME,
        COUNT(*) AS order_count
    FROM ORDER_PROC o
    GROUP BY 1, 2
    ORDER BY order_count DESC
    LIMIT {limit}
    """
    return con.execute(sql).df()


def run_reports(data_dir: Path) -> dict[str, pd.DataFrame]:
    con = duckdb.connect(database=":memory:")
    register_csvs(con, data_dir)
    return {
        "alos_by_department": average_length_of_stay(con),
        "encounter_volume_by_month": encounter_volume_by_month(con),
        "top_procedures": order_volume_top_procedures(con),
    }
