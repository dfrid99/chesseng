from board import *
import os

#pgn = open(r"\Users\dfrid\Downloads\chessgames2\ficsgamesdb_search_211324.pgn")
directory = r"\Users\dfrid\Downloads\chessgames2"
game_count = 5000
move_count = 80

save_board = "board_arr"
save_move = "movearr"
for num, filename in enumerate(os.listdir(directory)):
    pgn = open(directory +'/' + filename)
    board_arrs = np.zeros((game_count * move_count, 17, 8, 8))
    move_arrs = np.zeros((game_count * move_count, 2, 8, 8))
    i = 0
    for _ in range(game_count):
        try:
            game = chess.pgn.read_game(pgn)
            board = game.board()
        except:
            break
        for count, move in enumerate(game.mainline_moves()):
            if count == move_count:
                break
            inp_arr = pgn_to_arr(board)
            out_arr = get_output_simple(move, board.turn)
            board_arrs[i] = inp_arr
            move_arrs[i] = out_arr
            board.push(move)
            i += 1
    print(i)
    np.save(str(num) + save_board, board_arrs[:i])
    np.save(str(num) + save_move, move_arrs[:i])


