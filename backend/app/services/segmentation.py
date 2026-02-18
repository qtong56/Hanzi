"""
Text segmentation service for Chinese text
"""
import jieba
import pypinyin
from typing import List, Dict

# Initialize jieba once module loads
jieba.initialize()

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

def estimate_hsk_level(text: str) -> int:
    """
    Estimate HSK level based on unique characters
    This is a simple heuristic, can be improved with actual HSK word lists.
    
    :param text: Chinese text
    :type text: str
    :return: Estimated HSK level (1-6)
    :rtype: int
    """

    unique_chars = len(set(text))

    if unique_chars < 300:
        return 1
    elif unique_chars < 600:
        return 2
    elif unique_chars < 900:
        return 3
    elif unique_chars < 1200:
        return 4
    elif unique_chars < 1500:
        return 5
    else: 
        return 6
    
if __name__ == "__main__":
    test_text = "我喜欢学习中文"
    result = segment_text(test_text)

    print(f"Text: {test_text}")
    print(f"Segments: {len(result)}\n")

    for seg in result:
        print(f"    {seg['text']:8} | {seg['start']}--{seg['end']} | {seg['pinyin']}")
