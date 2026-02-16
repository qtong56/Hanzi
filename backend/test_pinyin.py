import pypinyin

# Test 1: Basic pinyin
word1 = "中国"
pinyin1 = pypinyin.pinyin(word1, style=pypinyin.TONE)

print("=== Test 1: Basic Pinyin ===")
print(f"Word: {word1}")
print(f"Pinyin (raw): {pinyin1}")
print(f"Pinyin (joined): {' '.join([p[0] for p in pinyin1])}")

# Test 2: Different tones
word2 = "你好"
pinyin_with_tone = pypinyin.pinyin(word2, style=pypinyin.TONE)
pinyin_with_numbers = pypinyin.pinyin(word2, style=pypinyin.TONE2)
pinyin_no_tone = pypinyin.pinyin(word2, style=pypinyin.NORMAL)

print("=== Test 2: Different tones ===")
print(f"Word: {word2}")
print(f"With tone marks: {' '.join([p[0] for p in pinyin_with_tone])}")   
print(f"With numbers: {' '.join([p[0] for p in pinyin_with_numbers])}")
print(f"No tones: {' '.join([p[0] for p in pinyin_no_tone])}")

# Test 3: Multicharacter words
word3 = "学习"
pinyin3 = pypinyin.pinyin(word3, style=pypinyin.TONE)

print("=== Test 3: Multicharacter words ===")
print(f"Word: {word3}")
print(f"Pinyin: {' '.join([p[0] for p in pinyin3])}")

# Test 4: Full sentence
sentence = "我喜欢学习中文"
pinyin_sentence = pypinyin.pinyin(sentence, style=pypinyin.TONE)

print("=== Test 4: Full sentence ===")
print(f"Sentence: {sentence}")
print(f"Pinyin: {' '.join([p[0] for p in pinyin_sentence])}")

# Test 5: Which style to use?
sentence = "我喜欢学习中文"
pinyin_sentence = pypinyin.pinyin(sentence, style=pypinyin.TONE)

print("=== Test 5: Recommended style ===")
print(f"For tooltips, use TONE style:")
print(f"    {word2} -> {' '.join([p[0] for p in pypinyin.pinyin(word2, style=pypinyin.TONE)])}")

