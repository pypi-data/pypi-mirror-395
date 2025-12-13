# src/matrix/password.py
import re

def evaluate(password: str) -> dict:
    checks = {
        "length_ok": len(password) >= 8,
        "has_upper": bool(re.search(r"[A-Z]", password)),
        "has_lower": bool(re.search(r"[a-z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_special": bool(re.search(r"[^\w\s]", password)),
    }
    categories = sum(checks[k] for k in ["has_upper","has_lower","has_digit","has_special"])
    if checks["length_ok"] and categories == 4 and len(password) >= 12:
        strength = "Strong"
    elif checks["length_ok"] and categories >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"
    tips = []
    if not checks["length_ok"]: tips.append("Use at least 8 characters.")
    if not checks["has_upper"]: tips.append("Add uppercase letters.")
    if not checks["has_lower"]: tips.append("Add lowercase letters.")
    if not checks["has_digit"]: tips.append("Add digits.")
    if not checks["has_special"]: tips.append("Add special characters.")
    if strength == "Moderate" and len(password) < 12: tips.append("Aim for 12+ characters.")
    return {"strength": strength, "length": len(password), "checks": checks, "tips": tips}