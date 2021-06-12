import chess
import chess.pgn
import numpy as np

pgn = open(r'\Users\dfrid\Downloads\chessgames2\games.pgn')

first_game = chess.pgn.read_game(pgn)
board = first_game.board()



file_to_row = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

def update_arr(piece, location, arr):
    if piece in ['P','p']:
        arr[0][location[0]][location[1]] = 1
    elif piece in ['N', 'n']:
        arr[1][location[0]][location[1]] = 1
    elif piece in ['B', 'b']:
        arr[2][location[0]][location[1]] = 1
    elif piece in ['R', 'r']:
        arr[3][location[0]][location[1]] = 1
    elif piece in ['Q', 'q']:
        arr[4][location[0]][location[1]] = 1
    else:
        arr[5][location[0]][location[1]] = 1

def get_output(move):
    out_arr = np.zeros((73,8,8))
    start_square = chess.square_name(move.from_square)
    end_square = chess.square_name(move.to_square)

def pgn_to_arr(board):
    white_arr = np.zeros((6,8,8))
    black_arr = np.zeros((6,8,8))
    for file in file_to_row.keys():
        for rank in range(1,9):
            piece = board.piece_at(chess.parse_square(file + str(rank)))
            if piece:
                piece = piece.symbol()
                location = (8 - rank, file_to_row[file])
                if piece.isupper():
                    update_arr(piece, location, white_arr)
                else:
                    update_arr(piece, location, black_arr)
    ret_arr = None
    if board.turn:
        ret_arr = np.concatenate((white_arr,black_arr))
    else:
        ret_arr = np.concatenate((black_arr, white_arr))
        ret_arr = np.rot90(ret_arr, 2, (1,2))
    return ret_arr



for move in first_game.mainline_moves():
    # print(board.has_kingside_castling_rights(chess.BLACK))
    board.push(move)
    print(chess.square_name(move.from_square))
    print(chess.square_name(move.to_square))
    print(board)
    if not board.has_castling_rights(chess.WHITE):
        break
    print(board.turn)
    #print(pgn_to_arr(board))






