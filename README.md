# CS4200-Project1

8-puzzle solver using A\* with two heuristics (h1 = misplaced tiles, h2 =
Manhattan distance).

## Requirements

Python 3, no extra packages needed.

## Files

- `main.py` - board setup, both heuristics, the A\* search, and the
  interactive program (run this one for the assignment's required I/O)
- `testing_harness.py` - generates 100+ solvable puzzles across depth 2-20,
  runs both heuristics on each, and prints a summary table averaged by depth

## Running the solver

```
python3 main.py
```

It will prompt:

```
[1] Random
[2] Manual Input
```

For Manual Input, type the puzzle as 3 rows of 3 numbers (0 = blank), e.g.:

```
1 2 3
4 5 6
8 7 0
```

Then pick a heuristic:

```
Select H Function:
[1] H1 (Misplaced Tiles)
[2] H2 (Manhattan Distance)
```

It prints every step to the goal (`0 1 2 / 3 4 5 / 6 7 8`), then
`Search Cost:` (nodes generated) and `Time:` (ms).

## Running the test harness

```
python3 testing_harness.py
```

Generates 100+ random solvable puzzles (plus the given `4200
project1/Length*.txt` boards) spanning depth 2-20, solves each with both
heuristics, and prints the per-depth table (# cases, avg nodes, avg time)
to the terminal
