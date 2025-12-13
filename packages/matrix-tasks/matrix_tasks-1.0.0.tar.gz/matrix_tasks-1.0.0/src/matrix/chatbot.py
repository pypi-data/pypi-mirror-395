# src/matrix/chatbot.py
import json, os

MEM_PATH = os.path.join("data","memory.json")

def load_mem():
    if os.path.exists(MEM_PATH):
        with open(MEM_PATH, "r", encoding="utf-8") as f: return json.load(f)
    return {"name": None, "favorite_color": None, "visits": 0}

def save_mem(mem): 
    os.makedirs("data", exist_ok=True)
    with open(MEM_PATH, "w", encoding="utf-8") as f: json.dump(mem, f, indent=2)

def respond(text: str, mem: dict) -> str:
    t = text.strip().lower()
    if any(g in t for g in ["hello","hi"]):
        mem["visits"] += 1
        return f"Hello{' again' if mem['visits']>1 else ''}{', '+mem['name'] if mem['name'] else ''}!"
    if t.startswith("my name is"):
        name = text.strip()[len("my name is"):].strip()
        if name: mem["name"] = name; return f"Nice to meet you, {name}!"
        return "I didn't catch your name."
    if "how are you" in t: return "I'm good. How are you?"
    if "my favorite color is" in t:
        color = text.lower().split("my favorite color is")[-1].strip()
        mem["favorite_color"] = color
        return f"{color.capitalize()} is a lovely color."
    if "what's my name" in t or "what is my name" in t:
        return f"You're {mem['name']}." if mem["name"] else "I don't know your name yet."
    if "what's my favorite color" in t or "what is my favorite color" in t:
        return f"Your favorite color is {mem['favorite_color']}." if mem["favorite_color"] else "You haven't told me yet."
    if "bye" in t or "goodbye" in t: return "Bye! I'll remember our chat."
    return "I can remember your name and favorite color. Try: 'My name is ...' or 'My favorite color is ...'."