from pydantic import BaseModel
from typing import Optional, List


class DictionaryResponse(BaseModel):
    found: bool
    simplified: Optional[str] = None
    traditional: Optional[str] = None
    pinyin: Optional[str] = None
    definitions: Optional[List[str]] = None
    hsk_level: Optional[int] = None
