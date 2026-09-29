import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from paths import DATA_DIR, OUTPUT_DIR  # noqa: E402
from reporting import run_reports  # noqa: E402


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    results = run_reports(DATA_DIR)
    for name, df in results.items():
        out = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(out, index=False)
        print(f"Wrote {out} ({len(df)} rows)")
        print(df.head().to_string(index=False))
        print()


if __name__ == "__main__":
    main()
