from game import Board
import random
import player
import pandas as pd

inp1 = -1
inp1 = -1

#For simulating data
for _ in range(500):
    out = []
    print("Game")
    print(_)
    win_percent_history = []
    board = Board(False, False)
    board.build_board()
    win_percent_history = player.simulate_game(board, -1, 10)
    for sim in win_percent_history:
        for turn in sim:
            for play in turn:
                out.append(play)
    df = pd.DataFrame(out, columns=['player','board', 'win_percent'])
    df.to_csv('game_data2.csv', mode='a' ,index=False)
