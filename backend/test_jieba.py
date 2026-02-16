import jieba

# Test 1: Basic segmentation
text1 = "我喜欢学习中文"
words1 = list(jieba.cut(text1))

print("=== Test 1: Basic Segmentation ===")
print(f"Original: {text1}")
print(f"Segmented: {' | '.join(words1)}")
print(f"Word count: {len(words1)}")

# Test 2: Longer text
text2 = "中国是一个历史悠久的国家"
words2 = list(jieba.cut(text2))

print("\n=== Test 2: Longer Text ===")
print(f"Original: {text2}")
print(f"Segmented: {' | '.join(words2)}")

# Test 3: Mixed content
text3 = "我在学习Python编程"
words3 = list(jieba.cut(text3))

print("\n=== Test 3: Mixed Chinese/English ===")
print(f"Original: {text3}")
print(f"Segmented: {' | '.join(words3)}")

# Test 4: Check what jieba does with punctuation
text4 = "今天天气很好。明天会下雨吗？"
words4 = list(jieba.cut(text4))

print("\n=== Test 4: With Punctuation ===")
print(f"Original: {text4}")
print(f"Segmented: {' | '.join(words4)}")
print(f"Words: {words4}")

# Test 5: Understand segmentation accuracy
test_cases = [
    ("我爱你", ["我", "爱", "你"]),  # Should be 3 words
    ("北京大学", ["北京大学"]),      # Should be 1 word (proper noun)
    ("中华人民共和国", ["中华人民共和国"]),  # Proper noun
]

print("\n=== Test 5: Segmentation Accuracy ===")
for text, expected in test_cases:
    actual = list(jieba.cut(text))
    match = actual == expected
    status = "MATCH" if match else "NO MATCH"
    print(f"{status} '{text}'")
    print(f"  Expected: {expected}")
    print(f"  Got: {actual}")