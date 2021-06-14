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

codes, i = {}, 0
for nSquares in range(1, 8):
    for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
        codes[(nSquares, direction)] = i
        i += 1
for two in ["N","S"]:
    for one in ["E","W"]:
        codes[("kn", two, one)] = i
        i += 1
for two in ["E","W"]:
    for one in ["N","S"]:
        codes[("kn", two, one)] = i
        i += 1


def get_output(move, turn):
    out_arr = np.zeros((73,8,8))
    file_diff = chess.square_file(move.to_square) - chess.square_file(move.from_square)
    rank_diff = chess.square_rank(move.to_square) - chess.square_rank(move.from_square)
    if not turn:
        file_diff = file_diff * -1
        rank_diff = rank_diff * -1
    if file_diff == 0:
        if rank_diff > 0:
            code = codes[(rank_diff, "N")]
        else:
            code = codes[(abs(rank_diff), "S")]
    elif rank_diff == 0:
        if file_diff > 0:
            code = codes[(file_diff, "E")]
        else:
            code = codes[(abs(file_diff), "W")]
    elif abs(rank_diff) == abs(file_diff):
        if rank_diff > 0 and file_diff > 0:
            code = codes[(abs(rank_diff), "NE")]
        elif rank_diff > 0 and file_diff < 0:
            code = codes[(abs(rank_diff), "NW")]
        elif rank_diff < 0 and file_diff < 0:
            code = codes[(abs(rank_diff), "SW")]
        else:
            code = codes[(abs(rank_diff), "SE")]
    elif (abs(rank_diff) + abs(file_diff)) == 3:
        if rank_diff == 2:
            dirL = "N"
        elif rank_diff == -2:
            dirL = "S"
        elif file_diff == 2:
            dirL = "E"
        else:
            dirL = "W"
        if rank_diff == 1:
            dirS = "N"
        elif rank_diff == -1:
            dirS = "S"
        elif file_diff == 1:
            dirS = "E"
        else:
            dirS = "W"
        code = codes[("kn", dirL, dirS)]

    sq_location = (7 - chess.square_rank(move.from_square), chess.square_file(move.from_square))
    out_arr[code][sq_location[0]][sq_location[1]] = 1
    if not turn:
        out_arr[code] = np.rot90(out_arr[code], 2,(0,1))
    return out_arr[code], code

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
    if board.turn:
        ret_arr = np.concatenate((white_arr,black_arr))
    else:
        ret_arr = np.concatenate((black_arr, white_arr))
        ret_arr = np.rot90(ret_arr, 2, (1,2))
    return ret_arr



for move in first_game.mainline_moves():
    # print(board.has_kingside_castling_rights(chess.BLACK))
    print(board)
    print(board.turn)
    print(chess.square_name(move.from_square))
    print(chess.square_name(move.to_square))
    out_arr, code = get_output(move, board.turn)
    print(out_arr)
    print(code)
    board.push(move)
    #print(pgn_to_arr(board))








