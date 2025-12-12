## :1234: SUDOKU SOLVER

### :open_book: OVERVIEW
Date: March 2024\
Developer(s): Ashneet Rathore\
Based on assignment instructions from Prof. Kalev Kask

Sudoku Solver is a program that uses AI-based constraint satisfaction techniques, such as heuristics and backtracking search, to efficiently solve Sudoku boards. Users can supply their own Sudoku board or generate one, select different solving heuristics, and receive the completed board along with statistics tracking the algorithm's solving performance.

### :gear: HOW IT WORKS


### :open_file_folder: PROJECT FILE STRUCTURE
```bash
SudokuSolver/
│── src/
│   │── main.py                 # Takes user input and runs solver
│   │── sudoku_board.py         # Defines SudokuBoard class (represents board)
│   │── bt_solver.py            # Defines BTSolver class (applies heuristics and solves board)
│   │── constraint_network.py   # Defines ConstraintNetwork class (CSP representation of the problem)           
│   │── constraint.py           # Defines Constraint class (represents CSP constraint btwn variables)
│   │── domain.py               # Defines Domain class (represents domain of a variable)
│   │── variable.py             # Defines Variable class (represents variable in CSP)
│   │── trail.py                # Defines Trail class (tracks assignment for backtracking)
│   └── board_generator.py      # Generates random board(s)
│── README.md                   # Project documentation
└── .gitignore                  # Excludes files and folders from version control
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
