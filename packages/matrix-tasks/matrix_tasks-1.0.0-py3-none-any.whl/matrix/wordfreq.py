# src/matrix/wordfreq.py
import re
from collections import Counter

WORD_RE = re.compile(r"[a-z0-9']+")

def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]

def top_frequencies(text: str, n: int = 10) -> list[tuple[str, int]]:
    words = tokenize(text)
    return Counter(words).most_common(n)