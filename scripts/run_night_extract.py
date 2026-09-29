#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import OUTPUT
from src.night_service import run_night_extract
from src.reconcile import control_totals


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    result = run_night_extract()
    totals = control_totals(result)
    print("=== Night extract control totals ===")
    print(json.dumps(totals, indent=2))
    result.fact_result.to_csv(OUTPUT / "fact_result_nightly.csv", index=False)
    result.fact_adt.to_csv(OUTPUT / "fact_adt_nightly.csv", index=False)
    result.rejected.to_csv(OUTPUT / "rejected_orphans.csv", index=False)
    print(f"Wrote fact_result rows={len(result.fact_result)} census_delta={result.census_delta}")


if __name__ == "__main__":
    main()
