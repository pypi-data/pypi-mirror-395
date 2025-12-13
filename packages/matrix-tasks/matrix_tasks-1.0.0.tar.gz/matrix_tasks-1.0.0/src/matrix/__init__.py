# src/matrix/__init__.py

"""
Matrix Tasks Package
Provides implementations for:
- Word Frequency Counter
- Password Strength Checker
- Maze Solver
- Chatbot with Memory
"""

__version__ = "1.0.0"

# Optional: expose main functions directly
from .wordfreq import top_frequencies
from .password import evaluate
from .maze import bfs_path, visualize
from .chatbot import load_mem, save_mem, respond

__all__ = [
    "top_frequencies",
    "evaluate",
    "bfs_path",
    "visualize",
    "load_mem",
    "save_mem",
    "respond",
]