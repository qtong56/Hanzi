import re
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.models.article import Dictionary

CEDICT_PATH = Path(__file__).parent.parent.parent / "data" / "cedict_1_0_ts_utf-8_mdbg.txt"

# Format: traditional simplified [pinyin] /def1/def2/
_LINE_RE = re.compile(r'^(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+/(.+)/$')


def parse_cedict_file():
    """Yield (simplified, traditional, pinyin, definitions) from the CEDICT file."""
    with open(CEDICT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = _LINE_RE.match(line)
            if m:
                traditional, simplified, pinyin, defs_str = m.groups()
                definitions = [d.strip() for d in defs_str.split("/") if d.strip()]
                yield simplified, traditional, pinyin, definitions


def lookup_word(simplified: str, db: Session) -> Optional[Dictionary]:
    """Look up a word by its simplified Chinese characters."""
    return db.query(Dictionary).filter(Dictionary.simplified == simplified).first()
