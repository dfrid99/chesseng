import chess.pgn

pgn = open(r'\Users\dfrid\Downloads\chessgames\ficsgamesdb_search_208912.pgn')

first_game = chess.pgn.read_game(pgn)
board = first_game.board()

for move in first_game.mainline_moves():
    board.push(move)
    print(board)
