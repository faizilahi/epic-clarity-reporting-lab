from src.night_service import run_night_extract


def test_orphan_rejected_when_data_present():
    # Relies on generated synthetic slice including MISSING_PAT orphan
    from pathlib import Path
    import subprocess
    import sys

    gen = Path(__file__).resolve().parents[1] / "scripts" / "generate_clarity_slice.py"
    subprocess.check_call([sys.executable, str(gen)])
    result = run_night_extract()
    assert result.orphan_results >= 1
