from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class _Config:
    DATA_PATH_MD = Path(__file__).parent / "data_md"


CONFIG = _Config()
