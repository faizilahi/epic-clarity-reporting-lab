from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

WATERMARK_START = datetime(2024, 11, 12, 1, 0, 0)
WATERMARK_END = datetime(2024, 11, 12, 5, 0, 0)


@dataclass(frozen=True)
class ExtractWindow:
    start: datetime
    end: datetime

    @property
    def label(self) -> str:
        return f"{self.start.isoformat()} .. {self.end.isoformat()}"


DEFAULT_WINDOW = ExtractWindow(WATERMARK_START, WATERMARK_END)
