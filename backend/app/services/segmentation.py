"""
Text segmentation service for Chinese text
"""
import json
import os
import re
import jieba
import pypinyin
from typing import List, Dict, Optional

# Initialize jieba once module loads
jieba.initialize()

# Matches a single CJK character
_CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def count_chinese_chars(text: str) -> int:
    """Count individual Chinese characters in text (for display as 'word count')."""
    return sum(1 for ch in text if _CHINESE_RE.match(ch))

def _count_chinese_word_tokens(text: str) -> int:
    """Count jieba word-tokens that contain at least one Chinese character (denominator for HSK coverage)."""
    return sum(1 for w in jieba.cut(text) if _CHINESE_RE.search(w))

# HSK word lookup: simplified -> set of new-HSK level ints (1-7)
_HSK_LOOKUP: Optional[Dict[str, List[int]]] = None

def _get_hsk_lookup() -> Dict[str, List[int]]:
    global _HSK_LOOKUP
    if _HSK_LOOKUP is None:
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'complete.json')
        with open(data_path, encoding='utf-8') as f:
            data = json.load(f)
        _HSK_LOOKUP = {}
        for entry in data:
            levels = [
                int(l[4:])  # "new-3" -> 3
                for l in entry.get('level', [])
                if l.startswith('new-')
            ]
            if levels:
                _HSK_LOOKUP[entry['simplified']] = levels
    return _HSK_LOOKUP

def segment_text(text: str) -> List[Dict[str, any]]:
    """
    Segment Chinese text into words with pinyin
    
    :param text: Chinese text to segment
    :type text: str
    :return: list of segments, each containing
        - text: the word
        - start: the start position in original text
        - end: end position in the original text
        - pinyin: pinyin pronunciation with tone marks
    :rtype: List[Dict[str, Any]]
    """

    if not text or not text.strip():
        return []
    
    # Segment text with jieba
    words = list(jieba.cut(text))
    
    segments = []
    position = 0

    for word in words:
        # Skip empty string (can happen with whitespace)
        if not word:
            position += len(word)
            continue
        
        # Skip whitespace characters
        if not word.strip():
            position += len(word)
            continue

        # Get pinyin for the word
        pinyin_list = pypinyin.pinyin(
            word, 
            style=pypinyin.TONE,
            heteronym=False # only use most common pronunciation
        )
        pinyin = ' '.join([p[0] for p in pinyin_list])
        
        # Create segment
        segment = {
            'text': word,
            'start': position,
            'end': position + len(word),
            'pinyin': pinyin
        }

        segments.append(segment)
        position += len(word)
    return segments

def estimate_hsk_level(text: str) -> Dict[int, int]:
    """
    Count Chinese characters by new-HSK level in text.

    Segments the text using jieba. For each word segment:
    - If the word is in the HSK lookup, each Chinese character in the word
      is counted at the word's HSK level(s).
    - If the word is NOT in the HSK lookup, each individual Chinese character
      is looked up separately and counted at its own level.

    This gives a character-based coverage count where the denominator is
    count_chinese_chars(text).

    :param text: Chinese text
    :type text: str
    :return: dict mapping new-HSK level (1-7) to character count
    :rtype: Dict[int, int]
    """
    if not text or not text.strip():
        return {}

    hsk_lookup = _get_hsk_lookup()
    counts: Dict[int, int] = {}

    for word in jieba.cut(text):
        word = word.strip()
        if not word:
            continue
        if word in hsk_lookup:
            # Count each Chinese character in this word at the word's HSK level(s)
            char_count = sum(1 for ch in word if _CHINESE_RE.match(ch))
            for level in hsk_lookup[word]:
                counts[level] = counts.get(level, 0) + char_count
        else:
            # Word not in HSK dict — fall back to per-character lookup
            for char in word:
                if _CHINESE_RE.match(char) and char in hsk_lookup:
                    for level in hsk_lookup[char]:
                        counts[level] = counts.get(level, 0) + 1

    return counts


def dominant_hsk_level(counts: Dict[int, int], total_words: int) -> int:
    """
    Find the minimum new-HSK level L such that words at levels 1..L
    cover >= 80% of all segmented words in the text.

    :param counts: dict mapping new-HSK level (1-7) to word occurrence count
    :param total_words: total number of segmented (non-whitespace) words in text
    :return: minimum level reaching 80% coverage (1-7), or 0 if total_words is 0
    :rtype: int
    """
    if total_words == 0:
        return 0
    target = 0.80 * total_words
    cumulative = 0
    for level in range(1, 8):
        cumulative += counts.get(level, 0)
        if cumulative >= target:
            return level
    return 7


if __name__ == "__main__":
    test_text = "我喜欢学习中文"
    result = segment_text(test_text)

    print(f"Text: {test_text}")
    print(f"Segments: {len(result)}\n")

    for seg in result:
        print(f"    {seg['text']:8} | {seg['start']}--{seg['end']} | {seg['pinyin']}")
