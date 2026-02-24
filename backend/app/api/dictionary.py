from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.translation import lookup_word
from app.schemas.dictionary import DictionaryResponse

router = APIRouter()


@router.get("/{word}", response_model=DictionaryResponse)
def get_translation(word: str, db: Session = Depends(get_db)):
    """
    Look up a word's translation from CC-CEDICT.

    Returns definitions and pinyin if found, or `found: false` if not in dictionary.
    """
    entry = lookup_word(word, db)

    if not entry:
        return DictionaryResponse(found=False)

    return DictionaryResponse(
        found=True,
        simplified=entry.simplified,
        traditional=entry.traditional,
        pinyin=entry.pinyin,
        definitions=entry.definitions,
        hsk_level=entry.hsk_level,
    )
