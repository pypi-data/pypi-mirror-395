# src/matrix/cli.py
import argparse
import sys
import json
from .wordfreq import top_frequencies
from .password import evaluate
from .maze import bfs_path, visualize
from .chatbot import load_mem, save_mem, respond

def main():
    parser = argparse.ArgumentParser(prog="matrix", description="Matrix Internship Tasks CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Word Frequency
    wf = subparsers.add_parser("wordfreq", help="Count word frequencies")
    wf.add_argument("--file", help="Path to text file")
    wf.add_argument("--top", type=int, default=10, help="Number of top words to display")

    # Password Checker
    pw = subparsers.add_parser("password", help="Check password strength")
    pw.add_argument("password", help="Password string to evaluate")

    # Maze Solver
    mz = subparsers.add_parser("maze", help="Solve a maze")
    mz.add_argument("--maze-file", help="Path to maze file (rows of 0/1)")
    mz.add_argument("--start", nargs=2, type=int, metavar=("R", "C"), required=True)
    mz.add_argument("--goal", nargs=2, type=int, metavar=("R", "C"), required=True)

    # Chatbot
    cb = subparsers.add_parser("chatbot", help="Run chatbot with memory")

    args = parser.parse_args()

    if args.command == "wordfreq":
        text = open(args.file, "r", encoding="utf-8").read() if args.file else sys.stdin.read()
        for word, count in top_frequencies(text, args.top):
            print(f"{word}\t{count}")

    elif args.command == "password":
        result = evaluate(args.password)
        print(json.dumps(result, indent=2))

    elif args.command == "maze":
        if args.maze_file:
            with open(args.maze_file, "r") as f:
                maze = [[int(x) for x in line.strip().split()] for line in f if line.strip()]
        else:
            maze = [
                [0,0,1,0,0],
                [1,0,1,0,1],
                [0,0,0,0,0],
                [0,1,1,1,0],
                [0,0,0,1,0],
            ]
        start = tuple(args.start)
        goal = tuple(args.goal)
        path = bfs_path(maze, start, goal)
        if path:
            print("Path:", path)
            print(visualize(maze, path))
        else:
            print("No path found.")

    elif args.command == "chatbot":
        mem = load_mem()
        print("Chatbot ready. Type 'bye' to exit.")
        while True:
            try:
                line = input("> ")
            except KeyboardInterrupt:
                print("\nExiting.")
                break
            reply = respond(line, mem)
            print(reply)
            save_mem(mem)
            if reply.lower().startswith("bye"):
                break

if __name__ == "__main__":
    main()