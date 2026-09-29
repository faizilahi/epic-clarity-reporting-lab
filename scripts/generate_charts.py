import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from reporting import run_reports  # noqa: E402

DATA_DIR = ROOT / "data"
IMG_DIR = ROOT / "docs" / "images"


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    results = run_reports(DATA_DIR)
    alos = results["alos_by_department"]
    vol = results["encounter_volume_by_month"]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(alos["DEPARTMENT_NAME"], alos["avg_los_days"], color="#006BA6")
    ax.set_title("Average Length of Stay by Department (Synthetic Inpatient)")
    ax.set_ylabel("Days")
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    fig.savefig(IMG_DIR / "alos_by_department.png", dpi=120)
    plt.close(fig)

    amb = vol[vol["ENC_TYPE"] == "Ambulatory"].copy()
    amb["month"] = pd.to_datetime(amb["month"])
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(amb["month"], amb["encounter_count"], marker="o", color="#0496FF")
    ax.set_title("Ambulatory Encounter Volume by Month (2024 Synthetic)")
    ax.set_ylabel("Encounters")
    fig.tight_layout()
    fig.savefig(IMG_DIR / "ambulatory_volume_by_month.png", dpi=120)
    plt.close(fig)
    print(f"Charts saved under {IMG_DIR}")


if __name__ == "__main__":
    main()
