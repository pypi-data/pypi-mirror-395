# tests/test_password.py
from src.matrix.password import evaluate
def test_password_strength():
    assert evaluate("abc")["strength"] == "Weak"
    assert evaluate("Abcdef12")["strength"] == "Moderate"
    assert evaluate("Abcdef12!more")["strength"] == "Strong"