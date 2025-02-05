# AI Slider Puzzle 🎮🤖

A sliding puzzle game (8-puzzle, 15-puzzle, and 24-puzzle) with an AI solver powered by the A* algorithm. The project uses PyQt5 to provide a sleek graphical user interface with board size selection and animated AI moves.

---

## ✨ Features

- **Multiple Board Sizes:**  
  Choose between **3×3**, **4×4**, or **5×5** puzzles.
  
- **Stylish UI:**  
  Enjoy a modern interface with custom colors, fonts, and animations.

- **AI Solver:**  
  Let the AI solve the puzzle for you using the A* algorithm with the Manhattan distance heuristic.

- **Solvability Check:**  
  Only generates puzzles that are guaranteed to be solvable. ✅

---

## 📂 Project Structure

```
├── main.py        # Main GUI application using PyQt5
├── sliders.py     # Game logic including board generation, move logic, and AI solver (A* algorithm)
└── README.md      # Project documentation
```

---

## 🚀 Installation

1. **Clone the repository:**
   

2. **Create a virtual environment (optional but recommended):**
  

3. **Install dependencies:**
   ```bash
   pip install PyQt5
   ```

---

## 🎮 Usage

Run the main application with:

```bash
python main.py
```

### How to Play

- **Choose Board Size:**  
  Click one of the size buttons (3×3, 4×4, or 5×5) to generate a new puzzle.

- **Make Moves:**  
  Click on any tile adjacent to the empty space to slide it.

- **AI Solve:**  
  Click the **"AI Solve"** button to see the AI animate a solution using the A* algorithm.

---

## 🛠️ Code Highlights

### Board Generation & Solvability

The game logic in `sliders.py` ensures that only solvable boards are generated. For example, the `count_inversions` function converts tile strings to integers to accurately count inversions:

```python
def count_inversions(board):
    tiles = [int(tile) for tile in board if tile is not EMPTY]
    inversions = sum(
        1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j]
    )
    return inversions
```

> **Note:** This function is crucial for ensuring that generated puzzles are solvable. Removing it could lead to unsolvable puzzles.

### AI Solver (A* Algorithm)

The AI solver in `sliders.py` uses a priority queue and the Manhattan distance heuristic to find the optimal solution:

```python
def a_star_solver(start_board):
    n = int(len(start_board) ** 0.5)
    pq = []
    counter = 0  # Tie-breaker counter
    heapq.heappush(pq, (manhattan_distance(start_board, n), counter, 0, start_board, []))
    visited = set([tuple(start_board)])
    # ...
```

### Stylish PyQt5 Interface

The `main.py` file uses PyQt5 with custom styles to create a modern look:

```python
self.setStyleSheet("background-color: #2c3e50;")
...
btn.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 5px;")
...
self.ai_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 16px; padding: 10px;")
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute to the project.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Enjoy playing and coding! 🚀😊
