import re

def parse_cedict_line(line):
    """Parse one line of CC-CEDICT"""
    # Skip comments and empty lines
    if line.startswith('#') or not line.strip():
        return None
    
    # Pattern: simplified traditional [pinyin] /def1/def2/
    pattern = r'^(\S+) (\S+) \[([^\]]+)\] /(.+)/$'
    
    match = re.match(pattern, line.strip())
    if not match:
        return None
    
    simplified, traditional, pinyin, definitions = match.groups()
    
    # Split definitions by /
    def_list = definitions.split('/')
    
    return {
        'simplified': simplified,
        'traditional': traditional,
        'pinyin': pinyin,
        'definitions': def_list
    }


# Test parsing
print("=== Testing CC-CEDICT Parsing ===\n")

test_lines = [
    "你好 你好 [ni3 hao3] /hello/hi/how do you do/",
    "中国 中國 [Zhong1 guo2] /China/Middle Kingdom/",
    "学习 學習 [xue2 xi2] /to learn/to study/",
    "# This is a comment",
    "",
]

for line in test_lines:
    result = parse_cedict_line(line)
    if result:
        print(f"Simplified: {result['simplified']}")
        print(f"Traditional: {result['traditional']}")
        print(f"Pinyin: {result['pinyin']}")
        print(f"Definitions: {result['definitions']}")
        print()
    else:
        print(f"Skipped: {line[:50]}")
        print()

# Now test on real file
print("\n=== Testing on Real File ===\n")

with open('data/cedict_1_0_ts_utf-8_mdbg.txt', 'r', encoding='utf-8') as f:
    count = 0
    parsed = 0
    
    for line in f:
        count += 1
        result = parse_cedict_line(line)
        if result:
            parsed += 1
            
            # Show first 5 entries
            if parsed <= 5:
                print(f"{result['simplified']} ({result['pinyin']})")
                print(f"  {result['definitions'][0]}")
                print()
    
    print(f"Total lines: {count}")
    print(f"Parsed entries: {parsed}")