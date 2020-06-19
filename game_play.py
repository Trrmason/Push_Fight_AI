#players = int(input("0 or 1 or 2 player: "))
from game import Board, print_board_positions
import player

#Check to see if board has a winner
def check_winner(board):
    winner = 0
    if type(board) == int:
        winner = 1 if board == 1 else 2
        print("Player {} lost, couldn't push".format(2 if board == 1 else 1))
    elif board.turn == 0:
        winner = 2 if board.board[board.anchor_pos] > 0 else 1
        print("Player {} wins!".format(winner))
        print("Game Over")
    return winner

#Runs through a game a certain amount of times
#Displays each play and prints the amount of wins at the end
#Init both players
def play_game(p1, p2, num_sims=1):
    p1_wins = 0
    p2_wins = 0
    for i in range(num_sims):
        #New board
        board = Board(False, False)
        board.build_board()
        board.print()
        #If a player wins break 
        while True:
            board = p1.sim_turn(board)
            winner = check_winner(board)
            if winner == 1:
                p1_wins += 1
                break
            elif winner == 2:
                p2_wins += 1
                break
            board = p2.sim_turn(board)
            winner = check_winner(board)
            if winner == 1:
                p1_wins += 1
                break
            elif winner == 2:
                p2_wins += 1
                break
    print("{} :player 1 wins".format(p1_wins))
    print("{} :player 2 wins".format(p2_wins))

#Simulation #1
p1_sim_1 = player.ModelPlayer(player = -1)
p2_sim_1 = player.MCTSPlayer(player = 1, num_sim=10)
play_game(p1_sim_1, p2_sim_1)
#Simulation #2
# p1_sim_2 = player.MCTSPlayer(player = -1, num_sim=10)
# p2_sim_2 = player.ModelPlayer(player = 1)
# play_game(p1_sim_2, p2_sim_2)
# #Simulation #3
# p1_sim_3 = player.UserPlayer(player = -1)
# p2_sim_3 = player.ModelPlayer(player = 1)
# play_game(p1_sim_3, p2_sim_3)


