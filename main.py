import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import sliders

class SliderPuzzle(QWidget):
    def __init__(self):
        super().__init__()
        self.size = 3  # Default size
        self.ai_solution = []  # List of moves from AI solver
        self.ai_index = 0      # Index for animating moves
        self.ai_timer = QTimer()  # Timer for animation
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Slider Puzzle")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #2c3e50;")
        
        self.layout = QVBoxLayout()
        
        # Size selection buttons
        self.size_layout = QHBoxLayout()
        self.size_label = QLabel("Choose Size:")
        self.size_label.setStyleSheet("color: white; font-size: 16px;")
        self.size_layout.addWidget(self.size_label)
        
        for size in [3, 4, 5]:
            btn = QPushButton(f"{size}x{size}")
            btn.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 5px;")
            btn.clicked.connect(lambda _, s=size: self.set_size(s))
            self.size_layout.addWidget(btn)
        
        self.layout.addLayout(self.size_layout)
        
        # Grid for tiles
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        
        # AI Solve Button
        self.ai_button = QPushButton("AI Solve")
        self.ai_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 16px; padding: 10px;")
        self.ai_button.clicked.connect(self.solve_with_ai)
        self.layout.addWidget(self.ai_button)
        
        self.setLayout(self.layout)
        self.set_size(3)  # Initialize with 3x3 board
    
    def set_size(self, size):
        self.size = size
        self.board = sliders.initial_board(size ** 2)
        self.update_board()
    
    def update_board(self):
        # Clear any existing widgets in the grid
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # For a consistent style, we use fixed size buttons.
        # For larger boards, the board may extend beyond 100x100 per tile.
        # You can adjust tile size if desired.
        tile_size = 100  
        for i in range(self.size):
            for j in range(self.size):
                tile = self.board[i * self.size + j]
                btn = QPushButton(tile if tile else "")
                btn.setFixedSize(tile_size, tile_size)
                btn.setFont(QFont("Arial", 18, QFont.Bold))
                btn.setStyleSheet("background-color: #ecf0f1; color: black; border-radius: 10px;")
                btn.clicked.connect(lambda _, r=i, c=j: self.tile_clicked(r, c))
                self.grid_layout.addWidget(btn, i, j)
    
    def tile_clicked(self, row, col):
        empty_pos = sliders.find_empty(self.board)
        empty_row, empty_col = divmod(empty_pos, self.size)
        
        if abs(empty_row - row) + abs(empty_col - col) == 1:
            # Determine direction based on relative position
            if row < empty_row:
                direction = 'U'
            elif row > empty_row:
                direction = 'D'
            elif col < empty_col:
                direction = 'L'
            else:
                direction = 'R'
            
            self.board = sliders.move(self.board, direction)
            self.update_board()
            if sliders.is_solved(self.board):
                QMessageBox.information(self, "Congratulations!", "You solved the puzzle!")
    
    def solve_with_ai(self):
        # Call the A* solver from sliders.py.
        solution = sliders.a_star_solver(self.board)
        if solution:
            self.ai_solution = solution
            self.ai_index = 0
            self.ai_button.setEnabled(False)  # Disable AI button during animation
            self.ai_timer.timeout.connect(self.animate_ai_move)
            self.ai_timer.start(300)  # 300ms delay between moves
        else:
            QMessageBox.warning(self, "No Solution", "The puzzle is unsolvable.")
    
    def animate_ai_move(self):
        if self.ai_index < len(self.ai_solution):
            move_direction = self.ai_solution[self.ai_index]
            self.board = sliders.move(self.board, move_direction)
            self.update_board()
            self.ai_index += 1
        else:
            self.ai_timer.stop()
            self.ai_timer.timeout.disconnect(self.animate_ai_move)
            self.ai_button.setEnabled(True)
            if sliders.is_solved(self.board):
                QMessageBox.information(self, "AI Solved!", "The AI has solved the puzzle!")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SliderPuzzle()
    ex.show()
    sys.exit(app.exec_())
