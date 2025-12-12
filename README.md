## :1234: SUDOKU SOLVER

### :open_book: OVERVIEW
Date: March 2024\
Developer(s): Ashneet Rathore\
Based on assignment instructions from Prof. Kalev Kask

Sudoku Solver is a program that solves Sudoku boards using AI-based constraint satisfaction techniques, such as heuristics and backtracking search, to efficiently explore the solution space and compute valid solutions for any given board. Users can supply their own Sudoku board or generate one, select different solving heuristics, and receive the completed board along with statistics tracking the algorithm's solving performance.

### :gear: HOW IT WORKS


### :open_file_folder: PROJECT FILE STRUCTURE
```bash
SudokuSolver/
│── src/
│   │── main.py
│   │── sudoku_board.py              
│   │── bt_solver.py                 
│   │── constraint_network.py                
│   │── constraint.py           
│   │── domain.py
│   │── variable.py
│   │── trail.py
│   └── board_generator.py
│── README.md                 # Project documentation
└── .gitignore                # Excludes files and folders from version control
```
### :rocket: SET UP & EXECUTION
**1. Clone the repository**
```bash
git clone https://github.com/ashneetrathore/SudokuSolver.git
cd SudokuSolver/src
```

**2. Run the program**
```bash
python3 main.py
```

### :wrench: TRY IT OUT
