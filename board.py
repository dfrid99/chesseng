import chess
import chess.pgn
import numpy as np
import io



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
for move in ["N","NW","NE"]:
    for promote_to in ["r","n","b"]:
        codes[("underpromotion", move, promote_to)] = i
        i += 1

def get_move(num, turn):
    move = num // 64
    for key, value in codes.items():
        if value == move:
            move = key
            break
    square_num = num % 64
    square = [square_num % 8, square_num//8]
    if turn:
        square[1] = 7 - square[1]
    else:
        square[0] = 7 - square[0]
    return square, move

def get_output_simple(move, turn):
    out = np.zeros((2,8,8))
    from_file = chess.square_file(move.from_square)
    from_rank = chess.square_rank(move.from_square)
    to_file = chess.square_file(move.to_square)
    to_rank = chess.square_rank(move.to_square)
    if turn:
        from_location = (7 - from_rank, from_file)
        to_location = (7 - to_rank, to_file)
    else:
        from_location = (from_rank, 7 - from_file)
        to_location = (to_rank, 7 - to_file)
    out[0][from_location[0]][from_location[1]] = 1
    out[1][to_location[0]][to_location[1]] = 1
    return out

def get_output(move, turn):
    out_arr = np.zeros((73,8,8))
    file_diff = chess.square_file(move.to_square) - chess.square_file(move.from_square)
    rank_diff = chess.square_rank(move.to_square) - chess.square_rank(move.from_square)
    if not turn:
        file_diff = file_diff * -1
        rank_diff = rank_diff * -1
    if move.promotion in [2,3,4]:
        promote_piece = chess.piece_symbol(move.promotion)
        if file_diff == 1:
            dir = "E"
        elif file_diff == -1:
            dir = "W"
        else:
            dir = ""
        code = codes[("underpromotion", "N"+dir, promote_piece)]
    elif file_diff == 0:
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
    return out_arr

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
    if board.has_kingside_castling_rights(chess.WHITE):
        white_king_cast = np.ones((1,8,8))
    else:
        white_king_cast = np.zeros((1,8, 8))
    if board.has_queenside_castling_rights(chess.WHITE):
        white_queen_cast = np.ones((1,8, 8))
    else:
        white_queen_cast = np.zeros((1,8, 8))
    if board.has_kingside_castling_rights(chess.BLACK):
        black_king_cast = np.ones((1,8,8))
    else:
        black_king_cast = np.zeros((1,8, 8))
    if board.has_queenside_castling_rights(chess.BLACK):
        black_queen_cast = np.ones((1,8, 8))
    else:
        black_queen_cast = np.zeros((1,8, 8))
    white_cast = np.concatenate((white_king_cast,white_queen_cast))
    black_cast = np.concatenate((black_king_cast,black_queen_cast))
    if board.turn:
        ret_arr = np.concatenate((white_arr,black_arr))
        ret_arr = np.concatenate((ret_arr, np.ones((1,8,8))))
        cast = np.concatenate((white_cast, black_cast))
    else:
        ret_arr = np.concatenate((black_arr, white_arr))
        ret_arr = np.rot90(ret_arr, 2, (1,2))
        ret_arr = np.concatenate((ret_arr, np.zeros((1,8, 8))))
        cast = np.concatenate((black_cast, white_cast))
    ret_arr = np.concatenate((ret_arr, cast))
    return ret_arr









