import sys
import time
import random
import heapq

GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)

# Prints 3x3 board
def print_board(state):
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])

def read_board():
    nums = []
    while len(nums) < 9:
        line = sys.stdin.readline()
        if line == "":
            break
        nums += line.split()
    return tuple(int(x) for x in nums[:9])

# Ignores the blanks
def count_inversions(state):
    tiles = [t for t in state if t != 0]
    inv = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inv += 1
    return inv

# Checks if it is a 3x3 puzzle
def is_solvable(state):
    return count_inversions(state) % 2 == 0

# Moves the board by swapping the blanks
def swap(state, i, j):
    lst = list(state)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)

def get_moves(state):
    blank = state.index(0)
    row = blank // 3
    col = blank % 3
    moves = []
    if row > 0:
        moves.append(swap(state, blank, blank - 3))
    if row < 2:
        moves.append(swap(state, blank, blank + 3))
    if col > 0:
        moves.append(swap(state, blank, blank - 1))
    if col < 2:
        moves.append(swap(state, blank, blank + 1))
    return moves

def make_random_puzzle():
    state = GOAL
    prev_state = None
    num_moves = random.randint(10, 40)
    for _ in range(num_moves):
        options = [s for s in get_moves(state) if s != prev_state]
        prev_state = state
        state = random.choice(options)
    return state

def h1(state):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != GOAL[i]:
            count += 1
    return count

def h2(state):
    total = 0
    for i in range(9):
        tile = state[i]
        if tile == 0:
            continue
        row1, col1 = i // 3, i % 3
        row2, col2 = tile // 3, tile % 3 
        total += abs(row1 - row2) + abs(col1 - col2)
    return total

# A* search
def solve(start, h):
    frontier = [(h(start), 0, start)]
    g_score = {start: 0}
    parent = {}
    visited = set()
    counter = 0
    nodes_generated = 1

    start_time = time.time()
    while frontier:
        f, c, state = heapq.heappop(frontier)

        if state in visited:
            continue
        visited.add(state)

        if state == GOAL:
            break

        for next_state in get_moves(state):
            if next_state in visited:
                continue
            new_g = g_score[state] + 1
            if next_state not in g_score or new_g < g_score[next_state]:
                g_score[next_state] = new_g
                parent[next_state] = state
                counter += 1
                heapq.heappush(frontier, (new_g + h(next_state), counter, next_state))
                nodes_generated += 1
    elapsed_ms = (time.time() - start_time) * 1000

    path = [GOAL]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return path, nodes_generated, elapsed_ms

def main():
    print("[1] Random")
    print("[2] Manual Input")
    choice = input().strip()

    if choice == "2":
        print("Please enter your puzzle:")
        state = read_board()
        if sorted(state) != list(range(9)):
            print("Invalid puzzle: must contain each of 0-8 exactly once.")
            return
    else:
        state = make_random_puzzle()
        print("Puzzle:")
        print_board(state)

    if not is_solvable(state):
        print("This puzzle is not solvable.")
        return

    print("Select H Function:")
    print("[1] H1 (Misplaced Tiles)")
    print("[2] H2 (Manhattan Distance)")
    h_choice = input().strip()
    h = h1 if h_choice == "1" else h2

    path, nodes_generated, elapsed_ms = solve(state, h)

    step = 1
    for board in path[1:]:
        print("Step:", step)
        print_board(board)
        step += 1

    print("Search Cost:", nodes_generated)
    print("Time: %f ms" % elapsed_ms)

if __name__ == "__main__":
    main()
