# tests/test_chatbot.py
from src.matrix.chatbot import respond, load_mem
def test_chatbot_name_memory():
    mem = load_mem()
    assert "Nice to meet you" in respond("my name is Dipaon", mem)
    assert "Dipaon" in respond("what's my name", mem)