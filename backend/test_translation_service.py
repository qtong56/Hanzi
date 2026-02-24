"""
Tests for the translation service (parse_cedict_file + lookup_word).

Run from backend/ directory:
    python test_translation_service.py
"""
import sys
sys.path.insert(0, '.')

PASS = "✓"
FAIL = "✗"
results = []

def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    msg = f"  {status} {label}"
    if not condition and detail:
        msg += f"\n      → {detail}"
    print(msg)
    results.append(condition)
    return condition


# ─────────────────────────────────────────────
# 1. CEDICT file parsing
# ─────────────────────────────────────────────
print("\n=== 1. CEDICT Parsing ===\n")

from app.services.translation import parse_cedict_file, CEDICT_PATH

check("CEDICT file exists", CEDICT_PATH.exists(), str(CEDICT_PATH))

entries = list(parse_cedict_file())
check("Parses > 100,000 entries", len(entries) > 100_000, f"got {len(entries)}")
check("Parses > 0 entries (basic sanity)", len(entries) > 0)

# Spot-check known words
words_by_simplified = {e[0]: e for e in entries}

ni_hao = words_by_simplified.get("你好")
check("你好 is present", ni_hao is not None)
if ni_hao:
    _, traditional, pinyin, definitions = ni_hao
    check("你好 traditional is 你好", traditional == "你好", repr(traditional))
    check("你好 pinyin contains 'ni'", "ni" in pinyin.lower(), repr(pinyin))
    check("你好 has definitions", len(definitions) > 0, repr(definitions))
    check("你好 first definition is english", all(ord(c) < 128 for c in definitions[0]),
          repr(definitions[0]))

zhongguo = words_by_simplified.get("中国")
check("中国 is present", zhongguo is not None)
if zhongguo:
    _, _, _, defs = zhongguo
    china_def = any("China" in d for d in defs)
    check("中国 definition contains 'China'", china_def, repr(defs))

# Check no comment lines leaked through
comment_entries = [e for e in entries if e[0].startswith("#")]
check("No comment lines in output", len(comment_entries) == 0,
      f"found {len(comment_entries)} comment entries")

# Check all entries have non-empty fields
bad = [(s, t, p, d) for s, t, p, d in entries if not s or not p or not d]
check("All entries have simplified/pinyin/definitions",
      len(bad) == 0, f"{len(bad)} bad entries")


# ─────────────────────────────────────────────
# 2. DB lookup
# ─────────────────────────────────────────────
print("\n=== 2. DB lookup (lookup_word) ===\n")

from app.database import SessionLocal, Base, engine
from app.models.article import Dictionary
from app.services.translation import lookup_word

# Ensure table exists
Base.metadata.create_all(engine)
db = SessionLocal()

try:
    # Clean up any leftover test entry
    existing = db.query(Dictionary).filter(Dictionary.simplified == "测试词").first()
    if existing:
        db.delete(existing)
        db.commit()

    # Insert a test word
    test_word = Dictionary(
        simplified="测试词",
        traditional="測試詞",
        pinyin="ce4 shi4 ci2",
        definitions=["test word", "sample entry"],
    )
    db.add(test_word)
    db.commit()

    found = lookup_word("测试词", db)
    check("lookup_word finds inserted entry", found is not None)
    if found:
        check("correct simplified returned", found.simplified == "测试词",
              repr(found.simplified))
        check("correct traditional returned", found.traditional == "測試詞",
              repr(found.traditional))
        check("definitions is a list", isinstance(found.definitions, list),
              type(found.definitions).__name__)
        check("correct definitions returned", found.definitions == ["test word", "sample entry"],
              repr(found.definitions))

    not_found = lookup_word("不存在的词", db)
    check("lookup_word returns None for unknown word", not_found is None,
          repr(not_found))

    # Clean up test entry
    db.delete(found)
    db.commit()
    check("test entry cleaned up", lookup_word("测试词", db) is None)

except Exception as e:
    print(f"  {FAIL} DB error: {e}")
    db.rollback()
    results.append(False)
finally:
    db.close()


# ─────────────────────────────────────────────
# 3. Integration: dictionary in DB (if loaded)
# ─────────────────────────────────────────────
print("\n=== 3. Dictionary DB integration ===\n")

db = SessionLocal()
try:
    count = db.query(Dictionary).count()
    print(f"  Dictionary entries in DB: {count}")

    if count > 0:
        check("Dictionary has > 10,000 entries (fully loaded)", count > 10_000,
              f"got {count} — run scripts/load_dictionary.py to load the full dictionary")

        # Look up a few common words
        for word in ["你好", "中国", "学习", "北京", "汉字"]:
            entry = lookup_word(word, db)
            check(f"lookup '{word}' in loaded dictionary", entry is not None,
                  "not found — dictionary may be partially loaded")
    else:
        print(f"  ⚠  Dictionary is empty. Run: python scripts/load_dictionary.py")
        print(f"     Skipping DB integration checks.")

except Exception as e:
    print(f"  {FAIL} DB error: {e}")
    results.append(False)
finally:
    db.close()


# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
print(f"\n{'='*50}")
passed = sum(results)
total = len(results)
print(f"Results: {passed}/{total} passed")
if passed == total:
    print("All translation service tests passed!")
else:
    print(f"{total - passed} test(s) failed.")
    sys.exit(1)
