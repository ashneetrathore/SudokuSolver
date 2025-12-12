## :1234: SUDOKU SOLVER

### :open_book: OVERVIEW
Date: March 2024\
Developer(s): Ashneet Rathore\
Based on assignment instructions from Prof. Kalev Kask

Sudoku Solver is a program that uses AI-based constraint satisfaction techniques, such as heuristics and backtracking search, to efficiently solve Sudoku boards. Users can supply their own Sudoku board or generate one, select different solving heuristics, and receive the completed board along with statistics tracking the algorithm's solving performance.

### :gear: HOW IT WORKS
Written in **Python**, the program models a Sudoku board as a **Constraint Satisfaction Problem (CSP)**. A CSP is a type of problem where variables must be assigned values from specificied domains such that all constraints, or rules, are satisfied. In Sudoku, each cell is represented as a variable, and its domain consists of all digits still allowed based on the current state of its row, column, or subgrid. The constraints are simply the rules of Sudoku - each digit can appear exactly once per row, column, and subgrid. As the solver progresses and neighboring assignments are made, the domain for each cell is continually reduced, thus shrinking the search space and moving the solver to a consistent, or legal, completed state.

The solver uses **backtracking search** to explore assignments by systematically attempting a value, checking consistency, and undoing the assignment if it violates Sudoku constraints. This search incrementally builds possible solutions, retracting steps whenever a constraint is violated and effectively performing a depth-first exploration of the search space while avoiding invalid paths. To improve efficiency, combinations of different **heuristics** can be applied (if specified by the user) to reduce the search space, prioritize assignments that are less likely to cause constraint violations, and eliminate invalid solutions earlier. The following details the types of heuristics applied:

1. Variable selection heuristics determine which unassigned variable to assign next
    - **Minimum Remaining Value (MRV)** selects the unassigned variable with the smallest domain (with the fewest legal values)
    - **Minimum Remaining Value with Maximum Degree (MAD)** extends the MRV heuristic by applying a tie-breaking rule that selects the most constrained variable (with the most unassigned neighbors) when multiple variables share the smallest domain

2. Value selection heuristics determine which value, for a selected variable, to assign next
    - **Least Constraining Value (LCV)** chooses the value that restricts the fewest options for neighboring variables

3. Consistency checking verifies that an assignment does not violate any constraints
    - **Forward Checking (FC)** eliminates illegal values from neighbors after each assignment
    - **Norvig Checking (NOR)** extends the FC heuristic by additionally assigning values that have only one possible position within a constraint.

By combining CSP modeling, backtracking, and heuristics, the program efficiently prunes the search space to find a completed board.

### :open_file_folder: PROJECT FILE STRUCTURE
```bash
SudokuSolver/
│── src/
│   │── main.py                 # Takes user input and runs solver
│   │── sudoku_board.py         # Defines SudokuBoard class (represents board)
│   │── bt_solver.py            # Defines BTSolver class (applies heuristics and solves board)
│   │── constraint_network.py   # Defines ConstraintNetwork class (represents board as CSP)           
│   │── constraint.py           # Defines Constraint class (represents CSP constraint btwn cells)
│   │── domain.py               # Defines Domain class (represents domain of a cell)
│   │── variable.py             # Defines Variable class (represents variable, or cell, in CSP)
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
