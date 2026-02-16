import jieba
import pypinyin

def segment_text(text):
    """
    Robust segmentation: Chinese text → list of word segments, handles whitespace and punctuation
    """
    words = list(jieba.cut(text))
    segments = []
    position = 0
    
    for word in words:
        # Get pinyin for this word
        if not word:
            continue

        pinyin_list = pypinyin.pinyin(word, style=pypinyin.TONE)
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

# Test it
print("=== Test Basic Segmentation ===\n")

text1 = "我喜欢学习中文"
result1 = segment_text(text1)

print(f"Original text: {text1}")
print(f"Segments ({len(result1)}):\n")

for seg in result1:
    print(f"  {seg['text']:8} | Position: {seg['start']}-{seg['end']} | Pinyin: {seg['pinyin']}")

# Verify positions are correct
print("\n=== Verify Positions ===")
for seg in result1:
    extracted = text1[seg['start']:seg['end']]
    match = extracted == seg['text']
    status = "✓" if match else "✗"
    print(f"{status} text[{seg['start']}:{seg['end']}] = '{extracted}' (expected: '{seg['text']}')")

# Test reconstruction
reconstructed = ''.join([seg['text'] for seg in result1])
print(f"\nReconstructed: {reconstructed}")
print(f"Original:      {text1}")
print(f"Match: {'✓' if reconstructed == text1 else '✗'}")



# Test edge cases
test_cases = [
    "我喜欢学习中文",           # Basic
    "今天天气很好。",          # Period
    "你好吗？",               # Question mark
    "我在学习Python编程",      # English
    "2024年1月1日",          # Numbers
    "我 爱 你",               # Spaces
    "",                       # Empty
    "   ",                    # Just spaces
]

print("=== Testing Edge Cases ===\n")

for i, text in enumerate(test_cases, 1):
    print(f"Test {i}: '{text}'")
    
    if not text.strip():
        print("  (empty/whitespace - skipped)")
        print()
        continue
    
    try:
        segments = segment_text(text)
        print(f"  Segments: {len(segments)}")
        
        for seg in segments:
            print(f"    {seg['text']:10} | {seg['pinyin']}")
        
        # Verify reconstruction
        reconstructed = ''.join([seg['text'] for seg in segments])
        if reconstructed == text:
            print(f"  ✓ Reconstruction matches")
        else:
            print(f"  ✗ Reconstruction mismatch!")
            print(f"    Expected: '{text}'")
            print(f"    Got:      '{reconstructed}'")
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()