import os
import sys
from sudoku_board import SudokuBoard


def genBoard ( p, q, m, filename ):
    filepath = os.path.join(output_dir, filename)
    sudoku_board = SudokuBoard(p, q, m)
    with open(filepath, "w") as file:
            file.write( str(p) + " " + str(q) + "\n" )
            for i in range(sudoku_board.N):
                for j in range(sudoku_board.N):
                    file.write( sudoku_board.intToOdometer( sudoku_board.board[i][j] ) + " " )
                file.write("\n")

if __name__== "__main__":
    if len(sys.argv) != 6:
        print ( "Usage: python3 board_generator.py <base_file_name> <#ofBoards. <p> <q> <m>" )
        exit(0)

    baseFileName = sys.argv[1]
    numOfFiles = int(sys.argv[2])
    p = int(sys.argv[3])
    q = int(sys.argv[4])
    m = int(sys.argv[5])

    output_dir = "../boards"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(numOfFiles):
        print ( "Creating board file: " + str(i) + "." )
        genBoard( p, q, m, baseFileName + "_" + str(i) + ".txt" )