# Matrix Tasks

## Setup
- python -m venv .venv && .venv\Scripts\activate
- pip install -r requirements.txt

## Usage
- python main.py wordfreq --file sample.txt --top 10
- type text and pipe into wordfreq: type sample.txt | python main.py wordfreq
- python main.py password "Abcdef12!"
- python main.py maze --start 0 0 --goal 4 4 --maze-file maze.txt
- python main.py chatbot

## Maze file format
Each line is space-separated 0/1 values, e.g.:
0 0 1 0
1 0 0 0
0 0 0 1