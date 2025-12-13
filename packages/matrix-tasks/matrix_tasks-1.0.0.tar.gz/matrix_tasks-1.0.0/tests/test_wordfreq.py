# tests/test_wordfreq.py
from src.matrix.wordfreq import top_frequencies
def test_top_frequencies_basic():
    text = "Hello, hello! World world world."
    top = top_frequencies(text, 2)
    assert top[0] == ("world", 3)
    assert top[1] == ("hello", 2)