import random
import heapq

EMPTY = None

def count_inversions(board):
    """Counts the number of inversions in the board, ignoring the empty tile.
    Converts tile strings to integers to ensure numerical comparison."""
    tiles = [int(tile) for tile in board if tile is not EMPTY]
    inversions = sum(
        1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j]
    )
    return inversions

def is_solvable(board, n):
    """Checks if the board is solvable based on sliding puzzle rules.
    
    For odd-sized grids (e.g. 3×3, 5×5):
      The puzzle is solvable if the inversion count is even.
      
    For even-sized grids (e.g. 4×4):
      The puzzle is solvable if (inversions + blank row from bottom) is odd.
      (Here, blank row from bottom is 1-indexed: bottom row = 1, next = 2, etc.)
    """
    inversions = count_inversions(board)
    empty_row = board.index(EMPTY) // n  # Row index of empty tile (0-based from top)
    empty_row_from_bottom = n - empty_row  # 1-indexed from bottom (e.g., bottom row = 1)
    
    if n % 2 == 1:  # Odd-sized grid
        return inversions % 2 == 0
    else:  # Even-sized grid (e.g., 4×4)
        return (inversions + empty_row_from_bottom) % 2 == 1

def initial_board(n):
    if n not in [9, 16, 25]:
        raise ValueError("Board size must be 9, 16, or 25.")
    
    while True:
        tiles = [str(i) for i in range(1, n)] + [EMPTY]
        random.shuffle(tiles)
        if is_solvable(tiles, int(n ** 0.5)):
            return tiles

def is_solved(board):
    """Check if the board is in a solved state."""
    solved_board = [str(i) for i in range(1, len(board))] + [EMPTY]
    return board == solved_board

def terminal(board):
    """Returns True if the game is over (solved)."""
    return is_solved(board)

def utility(board):
    """Returns 1 if solved, 0 otherwise."""
    return int(is_solved(board))

def find_empty(board):
    """Returns the index of the empty tile."""
    if EMPTY not in board:
        raise ValueError("Empty tile not found in board.")
    return board.index(EMPTY)

def move(board, direction):
    """Returns a new board with the empty tile moved in the specified direction."""
    n = int(len(board) ** 0.5)
    empty_pos = find_empty(board)
    new_board = board[:]
    swap_pos = None
    
    if direction == 'U' and empty_pos >= n:
        swap_pos = empty_pos - n
    elif direction == 'D' and empty_pos < (n - 1) * n:
        swap_pos = empty_pos + n
    elif direction == 'L' and empty_pos % n != 0:
        swap_pos = empty_pos - 1
    elif direction == 'R' and empty_pos % n != (n - 1):
        swap_pos = empty_pos + 1
    
    if swap_pos is not None:
        new_board[empty_pos], new_board[swap_pos] = new_board[swap_pos], new_board[empty_pos]
    
    return new_board

def manhattan_distance(board, n):
    """Calculates the Manhattan distance heuristic."""
    distance = 0
    for i, tile in enumerate(board):
        if tile is not EMPTY:
            correct_pos = int(tile) - 1
            correct_x, correct_y = divmod(correct_pos, n)
            current_x, current_y = divmod(i, n)
            distance += abs(correct_x - current_x) + abs(correct_y - current_y)
    return distance

def a_star_solver(start_board):
    """Solves the puzzle using the A* algorithm."""
    n = int(len(start_board) ** 0.5)
    pq = []
    counter = 0  # Tie-breaker counter
    # Priority: (priority, counter, cost, board, path)
    heapq.heappush(pq, (manhattan_distance(start_board, n), counter, 0, start_board, []))
    visited = set()
    visited.add(tuple(start_board))
    
    while pq:
        _, _, cost, board, path = heapq.heappop(pq)
        if is_solved(board):
            return path  # Return the sequence of moves to solve the puzzle
        
        for direction in ['U', 'D', 'L', 'R']:
            new_board = move(board, direction)
            if new_board != board and tuple(new_board) not in visited:
                counter += 1
                new_cost = cost + 1
                priority = new_cost + manhattan_distance(new_board, n)
                heapq.heappush(pq, (priority, counter, new_cost, new_board, path + [direction]))
                visited.add(tuple(new_board))
    
    return None  # No solution found (shouldn't happen for valid puzzles)

def ai_solve(board):
    """Wrapper function to trigger AI solving the puzzle."""
    solution = a_star_solver(board)
    if solution:
        print("AI Solution:", solution)
    else:
        print("No solution found.")
