import sys
import os
from sudoku_board import SudokuBoard
from bt_solver import BTSolver
from trail import Trail

"""
    Main driver file, which is responsible for interfacing with the
    command line and properly starting the backtrack solver.
"""

def main ( ):
    args = sys.argv

    file   = "";
    var_sh = "";
    val_sh = "";
    cc     = "";

    for arg in [args[i] for i in range(1, len(args))]:
        if arg == "MRV":
            var_sh = "MinimumRemainingValue"

        elif arg == "MAD":
            var_sh = "MRVwithTieBreaker"

        elif arg == "LCV":
            val_sh = "LeastConstrainingValue"

        elif arg == "FC":
            cc = "forwardChecking"

        elif arg == "NOR":
            cc = "norvigCheck"

        else:
            file = arg;

    trail = Trail();

    unfinished_board = None

    # If file is actually a specified directory
    if os.path.isdir(file):
        listOfBoards = None

        try:
            listOfBoards = os.listdir ( file )
        except:
            print ( "[ERROR] Failed to open directory." )
            return

        numSolutions = 0
        for f in listOfBoards:
            print ( "Running board: " + str(f) )
            board_path = os.path.join(file, f)
            unfinished_board = SudokuBoard( filepath=board_path)

            solver = BTSolver( unfinished_board, trail, val_sh, var_sh, cc )
            if cc in ["forwardChecking","norvigCheck"]:
                solver.checkConsistency()
            solver.solve()

            if solver.hassolution:
                numSolutions += 1
                solution = solver.getSolution()
                with open(board_path, "a") as board_file:
                    board_file.write("\n\n# Solution:\n")
                    board_file.write(str(solution))

        print ( "Solutions Found: " + str(numSolutions) )
        print ( "Trail Pushes: " + str(trail.getPushCount()) )
        print ( "Backtracks: "  + str(trail.getUndoCount()) )
        return
    
    # If file providing a board is specified
    if os.path.isfile(file):
        unfinished_board = SudokuBoard( filepath=os.path.abspath( file ) )
    # If no file providing a board is specified, generate a random board
    elif file == "":
        unfinished_board = SudokuBoard( 3, 3, 7 )
    
    if unfinished_board != None:
        print(unfinished_board)

        solver = BTSolver( unfinished_board, trail, val_sh, var_sh, cc )
        if cc in ["forwardChecking","norvigCheck"]:
            solver.checkConsistency()
        
        solver.solve()

        if solver.hassolution:
            print( solver.getSolution() )
            print( "Trail Pushes: " + str(trail.getPushCount()) )
            print( "Backtracks: " + str(trail.getUndoCount()) )
        else:
            print( "Failed to find a solution" )

if __name__== "__main__":
    main()
