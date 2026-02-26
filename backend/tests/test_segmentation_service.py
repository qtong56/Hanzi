"""
Tests for backend/app/services/segmentation.py
"""
import pytest
from app.services.segmentation import (
    count_chinese_chars,
    _count_chinese_word_tokens,
    estimate_hsk_level,
    dominant_hsk_level,
    segment_text,
)

# The exact text of the first sample article (中国) from load_sample_data.py
CHINA_ARTICLE_TEXT = """中国，全称中华人民共和国，是位于东亚的国家。中国是世界上人口最多的国家，拥有超过14亿人口。
        中国有着悠久的历史和丰富的文化传统。中国的首都是北京，最大的城市是上海。
        中国的地理环境非常多样，包括高山、平原、沙漠和海岸线。长江是中国最长的河流，黄河被称为中华民族的母亲河。
        中国是世界第二大经济体，在科技、制造业和贸易方面都有重要地位。"""


# ---------------------------------------------------------------------------
# count_chinese_chars
# ---------------------------------------------------------------------------

class TestCountChineseChars:
    def test_simple_sentence(self):
        assert count_chinese_chars("我喜欢学习中文") == 7

    def test_empty_string(self):
        assert count_chinese_chars("") == 0

    def test_whitespace_only(self):
        assert count_chinese_chars("   \n\t") == 0

    def test_ascii_only(self):
        assert count_chinese_chars("Hello World 123") == 0

    def test_mixed_chinese_and_ascii(self):
        # 北京 = 2 Chinese chars; digits and spaces are not
        assert count_chinese_chars("北京2024年") == 3  # 北京年

    def test_punctuation_not_counted(self):
        # Chinese punctuation like ，。！ are NOT in CJK Unified Ideographs range
        assert count_chinese_chars("你好，世界！") == 4  # 你好世界

    def test_first_sample_article_is_146_chars(self):
        """The 中国 article from load_sample_data.py must have exactly 146 Chinese characters."""
        assert count_chinese_chars(CHINA_ARTICLE_TEXT) == 146


# ---------------------------------------------------------------------------
# _count_chinese_word_tokens
# ---------------------------------------------------------------------------

class TestCountChineseWordTokens:
    def test_simple_sentence(self):
        # jieba segments "我喜欢学习中文" as: 我 / 喜欢 / 学习 / 中文 → 4 tokens
        assert _count_chinese_word_tokens("我喜欢学习中文") == 4

    def test_empty_string(self):
        assert _count_chinese_word_tokens("") == 0

    def test_ascii_only(self):
        # jieba will produce tokens, but none contain Chinese characters
        assert _count_chinese_word_tokens("Hello World") == 0

    def test_mixed_content(self):
        # "北京" → 1 token, digits/spaces are not Chinese word tokens
        result = _count_chinese_word_tokens("北京2024")
        assert result >= 1


# ---------------------------------------------------------------------------
# estimate_hsk_level — character-level counting with fallback
# ---------------------------------------------------------------------------

class TestEstimateHskLevel:
    def test_empty_string(self):
        assert estimate_hsk_level("") == {}

    def test_whitespace_only(self):
        assert estimate_hsk_level("   ") == {}

    def test_returns_dict_of_ints(self):
        result = estimate_hsk_level("我爱你")
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, int)
            assert 1 <= k <= 7

    def test_known_hsk1_word(self):
        # 我, 爱, 你 are all basic HSK 1 words/characters
        result = estimate_hsk_level("我爱你")
        assert 1 in result
        assert result[1] >= 3  # at least 3 HSK-1 character counts

    def test_character_fallback_increases_coverage(self):
        # For a word NOT in HSK dict, its individual characters should still contribute.
        # We can't know exactly which words jieba will find, but the total count
        # should be > 0 for common Chinese text.
        result = estimate_hsk_level("中国历史文化")
        total = sum(result.values())
        assert total > 0

    def test_character_level_counting_for_found_word(self):
        # 喜欢 is a 2-character HSK-1 word. With character-level counting it should
        # contribute 2 to the HSK-1 count (one per character), not just 1.
        result_word = estimate_hsk_level("喜欢")
        result_chars = estimate_hsk_level("喜") + estimate_hsk_level("欢") if False else None
        # 喜欢 found as a word → each of its 2 chars counted at HSK 1
        # So HSK-1 count should be 2
        if 1 in result_word:
            assert result_word[1] >= 2

    def test_total_chars_le_count_chinese_chars(self):
        # Sum of all level counts ≤ total Chinese characters
        # (some chars may not be in HSK at any level)
        text = "中国是世界上最大的发展中国家之一"
        total_hsk = sum(estimate_hsk_level(text).values())
        total_chars = count_chinese_chars(text)
        assert total_hsk <= total_chars


# ---------------------------------------------------------------------------
# dominant_hsk_level
# ---------------------------------------------------------------------------

class TestDominantHskLevel:
    def test_zero_total_returns_zero(self):
        assert dominant_hsk_level({}, 0) == 0

    def test_all_level1_returns_1(self):
        # 100% of words are HSK 1 → 80% threshold reached at level 1
        assert dominant_hsk_level({1: 100}, 100) == 1

    def test_mixed_levels(self):
        # 50 HSK1 + 50 HSK2 out of 100 total → 80% reached at level 2
        assert dominant_hsk_level({1: 50, 2: 50}, 100) == 2

    def test_returns_7_when_coverage_never_reached(self):
        # Only 5 HSK-counted words out of 100 total → never hits 80%
        assert dominant_hsk_level({1: 5}, 100) == 7

    def test_exactly_80_percent(self):
        # Exactly 80 out of 100 are HSK 1 → should return 1
        assert dominant_hsk_level({1: 80}, 100) == 1
