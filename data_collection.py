from board import *

pgn = open(r'\Users\dfrid\Downloads\chessgames2\games.pgn')

game_count = 5000
board_arrs = np.zeros((game_count*80,17,8,8))
move_arrs = np.zeros((game_count*80,73,8,8))
print('done')
i = 0
for _ in range(game_count):
    game = chess.pgn.read_game(pgn)
    board = game.board()
    for count, move in enumerate(game.mainline_moves()):
        if count == 80:
            break
        inp_arr = pgn_to_arr(board)
        out_arr = get_output(move, board.turn)
        #inp_arr = np.reshape(inp_arr, (-1, 17,8,8))
        #out_arr = np.reshape(out_arr, (-1, 73, 8, 8))
        board_arrs[i] = inp_arr
        move_arrs[i] = out_arr
        board.push(move)
        i += 1

np.save("1boardarr", board_arrs[:i])
np.save("1movearr", move_arrs[:i])
a = np.load("1boardarr.npy")
b = np.load("1movearr.npy")
print(a.shape)
print(b.shape)