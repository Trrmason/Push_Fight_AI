from game import Board
import random
import pandas as pd
import joblib
import numpy as np

def randomPlaythrough(board, whichPlayer):
    if len(board.get_boards_move_options(whichPlayer)) == 0:
        return whichPlayer * -1
    board.make_move(random.choice(board.get_boards_move_options(whichPlayer)))
    # prevent suicidal state by using this move to recover from a suicidal position eg has no push targets
    if len(board.get_boards_push_options(whichPlayer)) == 0:
        move = None
        # We want to find any move we can make that let's us make a push. The first option we find is good enough, but we do look in an advantageous order
        # first, try and move next to opponent's piece
        for opponentPiece in [x for x in range(26) if board.board[x] in ((-1, -2) if whichPlayer > 0 else (1, 2))]: # for every one of opponent's pieces that isn't anchored
            for ownSquare in [x for x in range(26) if board.board[x] == (-2 if whichPlayer < 0 else 2)]: # for every one of player's own squares
                for spc in board.adj_spaces[opponentPiece]:
                    if board.board[spc] == 0 and board.check_valid_move(ownSquare, spc):
                        move = (ownSquare, spc)
                        break
                if move is not None: break
            if move is not None: break
        # if that is impossible, try and move next to own piece
        # (NOTE: we may want to add an additional check so that this doesn't result in setting up suicidal pushes)
        if move is None:
            for ownPiece in [x for x in range(26) if board.board[x] in ((-1, -2) if whichPlayer < 0 else (1, 2))]: # for every one of own pieces that isn't anchored
                for ownSquare in [x for x in range(26) if board.board[x] == (-2 if whichPlayer < 0 else 2) and x != ownPiece]: # for every one of player's own squares (that isn't the piece we want to be near)
                    for spc in board.adj_spaces[ownPiece]:
                        if board.board[spc] == 0 and board.check_valid_move(ownSquare, spc):
                            move = (ownSquare, spc)
                            break
                    if move is not None: break
                if move is not None: break
        if move is not None:
            board.make_move(move)
        else:
            board.make_move(random.choice(board.get_boards_move_options(whichPlayer)))
    else:
        board.make_move(random.choice(board.get_boards_move_options(whichPlayer)))
    #assert len(board.get_boards_push_options(whichPlayer)) != 0
    if len(board.get_boards_push_options(whichPlayer)) == 0: # if you cannot push, you lose
        return whichPlayer * -1
    board.make_move(random.choice(board.get_boards_push_options(whichPlayer)), push=True)
    if (board.turn == 0):
        return whichPlayer
    else:
        randomPlaythrough(board, whichPlayer * -1)

# Performs the MCTS algorithm on a node
# Returns the odds that this node results in a victory
# This function should not change the board at all by the end
def MCTS(board, whichPlayer, numSimulations):
    # Remember len of board history so we can go back to earlier version using undo_moves_to_depth(boardHistDepth, whichPlayer)
    boardHistDepth = len(board.board_history) - 1 if len(board.board_history) != 0 else 0
    # tracks wins
    wins = 0
    # Expansion: do numSimulations playthroughs, randomly
    for i in range(numSimulations):
        playthruResult = randomPlaythrough(board, whichPlayer)
        if playthruResult == whichPlayer:
            # increase win chances for this node
            wins += 1
        # reset values of the board
        board.undo_moves_to_depth(whichPlayer, boardHistDepth)

    return wins / numSimulations

"""
def monteCarloPlayer(board, whichPlayer, numSim, s):
    values = []
    move_sets = []
    for move1 in board.get_boards_move_options(whichPlayer):
        print(move1)
        board.make_move(move1)
        for move2 in board.get_boards_move_options(whichPlayer):
            print(move2)
            board.make_move(move2)
            if len(board.get_boards_push_options(whichPlayer)) > 0:
                for push1 in board.get_boards_push_options(whichPlayer):
                    board.make_move(push1, True)
                    values.append(MCTS(board, whichPlayer, numSim))
                    move_sets.append((move1, move2, push1))
                    print(board.trace)
                    board.undo_move(whichPlayer, 2)
    moveSet = move_sets[values.index(max(values))]
    board.make_move(moveSet[0])
    board.make_move(moveSet[1])
    board.make_move(moveSet[2], True)
"""



#MCTS player
class MCTSPlayer:

    #init num_simulations for MCTS and player
    #-1 = player 1 , 1 = player 2
    def __init__(self, player = -1, num_sim=10):
        self.which_player = player
        self.num_sim = num_sim

    #First_move for MCTS.
    #This takes a player and attempts every move in move_options
    #It creates a move_dict with the highest win percent as the key and the move as the value
    #Since this function doesn't have an optimal tie breaking solution it could be improved
    def first_move(self, board):
        move_dict = {}
        for move in board.get_boards_move_options(self.which_player):
            #Make move for new board state, MCTS converts it back to original board after simulations
            board.make_move(move)
            win_percent = MCTS(board, self.which_player, self.num_sim)
            move_dict[win_percent] = move
        return move_dict[max(move_dict)]

    #Second move is the same as first move
    def second_move(self, board):
        move_dict = {}
        for move in board.get_boards_move_options(self.which_player):
            board.make_move(move)
            win_percent = MCTS(board, self.which_player, self.num_sim)
            move_dict[win_percent] = move
        return move_dict[max(move_dict)]

    #Push tries every push available for the current board state
    #It goes through the same process as the previous two functions
    def push(self, board):
        move_dict = {}
        for push in board.get_boards_push_options(self.which_player):
            board.make_move(push, push=True)
            win_percent = MCTS(board, self.which_player, self.num_sim)
            move_dict[win_percent] = push
        if len(move_dict) == 0:
            board.turn = 0
            return None
        return move_dict[max(move_dict)]

    #Sim turn simulates and entire turn and moves based on the highest win percent
    def sim_turn(self, board):
        first = self.first_move(board)
        board.make_move(first)
        print("MCTS first move")
        board.print()
        second = self.second_move(board)
        board.make_move(second)
        print("MCTS second move")
        board.print()
        last = self.push(board)
        if last == None: return self.which_player 
        board.make_move(last, push=True)
        print("MCTS push")
        board.print()
        return board

#Model Player
class ModelPlayer:

    #Based on the player, a certain trained GBR model is imported
    def __init__(self, player = -1):
        self.which_player = player
        self.player_decision = joblib.load('player_1.1_model.pkl') if player == -1 else joblib.load('player_2.1_model.pkl')
    
    #First move works the same as MCTSPlayer, but calls the model for a prediction
    def first_move(self, board):
        move_dict = {}
        for move in board.get_boards_move_options(self.which_player):
            board.make_move(move)
            win_percent = self.player_decision.predict([board.board])[0]
            move_dict[win_percent] = move
            board.undo_move(self.which_player, 1)
        return move_dict[max(move_dict)]

    #Second move is the same as first move
    def second_move(self, board):
        move_dict = {}
        for move in board.get_boards_move_options(self.which_player):
            board.make_move(move)
            win_percent = self.player_decision.predict([board.board])[0]
            move_dict[win_percent] = move
            board.undo_move(self.which_player, 1)
        return move_dict[max(move_dict)]
    
    #Push tries every push available for the current board state
    #Same as the previous two functions, but for push
    def push(self, board):
        move_dict = {}
        for push in board.get_boards_push_options(self.which_player):
            board.make_move(push, push=True)
            win_percent = self.player_decision.predict([board.board])[0]
            move_dict[win_percent] = push
            board.undo_move(self.which_player, 1)
        if len(move_dict) == 0:
            board.turn = 0
            return None
        return move_dict[max(move_dict)]

    #Sim turn simulates and entire turn and moves based on the highest win percent
    def sim_turn(self, board):
        first = self.first_move(board)
        board.make_move(first)
        print("GBR first move")
        board.print()
        second = self.second_move(board)
        board.make_move(second)
        print("GBR second move")
        board.print()
        last = self.push(board)
        #If no push player loses
        if last == None: return self.which_player
        board.make_move(last, push=True)
        print("GBR push")
        board.print()
        return board


class UserPlayer:

    def __init__(self, player = -1):
        self.player = player

    #Get the pos move
    #Get the pos location
    #return
    def first_move(self, board):
        attempt_move = int(input("Enter the piece you would like to move: "))
        attempt_location = int(input("Enter the location you would like to move: "))
        move = (attempt_move, attempt_location)
        return move

    #Same as first move
    def second_move(self, board):
        attempt_move = int(input("Enter the piece you would like to move: "))
        attempt_location = int(input("Enter the location you would like to move: "))
        move = (attempt_move, attempt_location)
        return move
    
    def push(self, board):
        attempt_push = int(input("Enter the piece you would like to push: "))
        attempt_direction = int(input("Enter the direction you would like to push: "))
        move = (attempt_push, attempt_direction)
        return move

    def sim_turn(self, board):
        while True:
            try:
                first = self.first_move(board)
                board.make_move(first)
                break
            except:
                print("{} is not a valid move".format(first))
        board.print()
        while True:
            try:
                second = self.second_move(board)
                board.make_move(second)
                break
            except:
                print("{} is not a valid move".format(second))
        board.print()
        while True:
            try:
                last = self.push(board)
                board.make_move(last, push=True)
                break
            except:
                print("{} is not a valid push".format(last))
        board.print()
        return board

    

#Was used to simulate game data to train the models
#MCTS Game simulator
#First_move for MCTS.
#This takes a player and attempts every move possible for the first move
#It creates a move_dict with the highest win percent as the key and the move as the value
#Since this function doesn't have an optimal tie breaking solution it could be improved
def first_move(board, whichPlayer, numSim):
    #player_1 = joblib.load('player_1_model.pkl')
    move_dict = {}
    win_percent_history = []
    for move in board.get_boards_move_options(whichPlayer):
        #MCTS resets the board to the original state so no need to update board after a state move
        board.make_move(move)
        board_after_move = board.board
        #win_percent = player_1.predict([board.board])[0]
        win_percent = MCTS(board, whichPlayer, numSim)
        move_dict[win_percent] = move
        win_percent_history.append([whichPlayer, board_after_move, win_percent]) 
    return move_dict[max(move_dict)], win_percent_history

#Second move could have been collapsed to one move function, same functionality as first_move
def second_move(board, whichPlayer, numSim):
    move_dict = {}
    win_percent_history = []
    for move in board.get_boards_move_options(whichPlayer):
        board.make_move(move)
        board_after_move = board.board
        win_percent = MCTS(board, whichPlayer, numSim)
        move_dict[win_percent] = move 
        win_percent_history.append([whichPlayer, board_after_move, win_percent])
    return move_dict[max(move_dict)], win_percent_history

#Push is basically the same as the previous functions, but attempts every push available
#If no push is possible the player loses, MCTS tries to prevent this from happening
def push(board, whichPlayer, numSim):
    move_dict = {}
    win_percent_history = []
    for push in board.get_boards_push_options(whichPlayer):
        board.make_move(push, push=True)
        board_after_move = board.board
        win_percent = MCTS(board, whichPlayer, numSim)
        move_dict[win_percent] = push
        win_percent_history.append([whichPlayer, board_after_move, win_percent])
    if len(move_dict) == 0:
        board.turn = 0
        return None, win_percent_history
    return move_dict[max(move_dict)], win_percent_history



#This function calls each move and plays whatever move is returned.
def monteCarloPlayer(board, whichPlayer, numSim):
    win_percent_history = []
    win_percent = []
    print(whichPlayer)
    board.print()
    move_one, win_percent= first_move(board, whichPlayer, numSim)
    win_percent_history.append(win_percent)
    print(move_one)
    board.make_move(move_one)
    board.print()
    move_two, win_percent = second_move(board, whichPlayer, numSim)
    win_percent_history.append(win_percent)
    print(move_two)
    board.make_move(move_two)
    board.print()
    push_move, win_percent = push(board, whichPlayer, numSim)
    win_percent_history.append(win_percent)
    print(push_move)
    if push_move != None:
        board.make_move(push_move, push=True)
    board.print()
    print(board.turn)
    return win_percent_history
        

#This simulates an entire game between two MCTS players.
def simulate_game(board, whichPlayer, numSim):
    win_percent_history = []
    while board.turn != 0:
        win_percent = monteCarloPlayer(board, whichPlayer, numSim)
        whichPlayer *= -1
        win_percent_history.append(win_percent)
    return win_percent_history
#End of MCTS game simulator




if __name__ == "__main__":
    board = Board(False, False)
    board.build_board()
    