import glob
import os
import random

from main import h1, h2, is_solvable, get_moves, solve, GOAL

MIN_DEPTH = 2
MAX_DEPTH = 20
TARGET_CASES = 120  # Test cases I put 120 just for some buffer instead of the 100

# Reads from the original "4200 project1" directory for the Length.txt files
def load_given_puzzles():
    states = []
    # Splits the text by the ////... lines
    for path in glob.glob(os.path.join("4200 project1", "Length*.txt")):
        text = open(path).read()
        for block in text.split("/////////////////////////////////////////////////////"):
            nums = block.split()
            if len(nums) == 9:
                states.append(tuple(int(x) for x in nums))
    return states

# Generates a random puzzle 
def random_puzzle_with_moves(moves):
    state = GOAL
    prev_state = None
    for _ in range(moves):
        options = [s for s in get_moves(state) if s != prev_state]
        prev_state = state
        state = random.choice(options)
    return state

# Turns the random puzzle with the depth range
def collect_puzzles():
    puzzles = []
    seen = set()

    for state in load_given_puzzles():
        if state in seen or not is_solvable(state):
            continue
        seen.add(state)
        path, nodes, t = solve(state, h2)
        depth = len(path) - 1
        if MIN_DEPTH <= depth <= MAX_DEPTH:
            puzzles.append((state, depth))

    while len(puzzles) < TARGET_CASES:
        state = random_puzzle_with_moves(random.randint(2, 25))
        if state in seen:
            continue
        seen.add(state)
        path, nodes, t = solve(state, h2)
        depth = len(path) - 1
        if MIN_DEPTH <= depth <= MAX_DEPTH:
            puzzles.append((state, depth))

    return puzzles

def main():
    puzzles = collect_puzzles()

    rows = []
    for state, depth in puzzles:
        path1, nodes1, time1 = solve(state, h1)
        path2, nodes2, time2 = solve(state, h2)
        rows.append([depth, nodes1, time1, nodes2, time2])

    by_depth = {}
    for depth, nodes1, time1, nodes2, time2 in rows:
        by_depth.setdefault(depth, []).append((nodes1, time1, nodes2, time2))

    agg_rows = []
    for depth in sorted(by_depth):
        group = by_depth[depth]
        n = len(group)
        avg_nodes1 = sum(g[0] for g in group) / n
        avg_time1 = sum(g[1] for g in group) / n
        avg_nodes2 = sum(g[2] for g in group) / n
        avg_time2 = sum(g[3] for g in group) / n
        agg_rows.append([depth, n, avg_nodes1, avg_time1, avg_nodes2, avg_time2])

    print("Total cases:", len(rows))
    print("Depth  #Cases  AvgNodesH1  AvgTimeH1(ms)  AvgNodesH2  AvgTimeH2(ms)")
    for depth, n, avg_nodes1, avg_time1, avg_nodes2, avg_time2 in agg_rows:
        print("%5d %7d %12.2f %14.4f %12.2f %14.4f" % (depth, n, avg_nodes1, avg_time1, avg_nodes2, avg_time2))

if __name__ == "__main__":
    main()
