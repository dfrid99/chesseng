import chess
import chess.pgn
import numpy as np

pgn = open(r'\Users\dfrid\Downloads\chessgames\ficsgamesdb_search_208912.pgn')

first_game = chess.pgn.read_game(pgn)
board = first_game.board()



file_to_row = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

def update_arr(piece, location, arr):
    if piece in ['P','p']:
        if piece == 'P':
            arr[0][location[0]][location[1]] = 1
        else:
            arr[0][location[0]][location[1]] = -1
    elif piece in ['N', 'n']:
        if piece == 'N':
            arr[1][location[0]][location[1]] = 1
        else:
            arr[1][location[0]][location[1]] = -1
    elif piece in ['B', 'b']:
        if piece == 'B':
            arr[2][location[0]][location[1]] = 1
        else:
            arr[2][location[0]][location[1]] = -1
    elif piece in ['R', 'r']:
        if piece == 'R':
            arr[3][location[0]][location[1]] = 1
        else:
            arr[3][location[0]][location[1]] = -1
    elif piece in ['Q', 'q']:
        if piece == 'Q':
            arr[4][location[0]][location[1]] = 1
        else:
            arr[4][location[0]][location[1]] = -1
    else:
        if piece == 'K':
            arr[5][location[0]][location[1]] = 1
        else:
            arr[5][location[0]][location[1]] = -1


def pgn_to_arr(board):
    inp_arr = np.zeros((6,8,8))
    for file in file_to_row.keys():
        for rank in range(1,9):
            piece = board.piece_at(chess.parse_square(file + str(rank)))
            if piece:
                piece = piece.symbol()
                location = (8 - rank, file_to_row[file])
                update_arr(piece, location, inp_arr)
    return inp_arr

#print(pgn_to_arr(board))

for move in first_game.mainline_moves():
    board.push(move)
    print(board)
    print(pgn_to_arr(board))



