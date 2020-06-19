import random

"""
*Pieces and players
Two players: P1-White, P2-Brown
White will be distinguished by negative numbers, Brown will be positive
White choses starting position, Brown follows
Pieces per player: 3 Square, 2 Circle
Square can push, Circle can't
Square will be -2 & 2
Circle will be -1 & 1
When a an anchor is placed on a Square -3 & 3
Anchor pieces are made after a push and can't be pushed the following turn

*A starting board could look like
    [] []
|[] [] []
|-1 [] [] []|
|-2 -2 -2 -1|
|-----------| Middle line 
| 1  2  2  2|
|[] [] []  1|
    [] [] []|
    [] []

"""

"""
Each player takes a turn after the other
Board.turn is -3, -2, -1, 3, 2, 1, or 0
turn < 0 is p1's turn
    turn == -3 is p1's first chance to move
    turn == -2 is p1's last chance to move
    turn == -1 is p1's turn to push
turn > 0 is p2's turn
    turn == 3 is p1's first chance to move (or skip to turn == 1)
    turn == 2 is p1's last chance to move (or skip to turn == 1)
    turn == 1 is p1's turn to push
turn == 0 is a finished game

On their turn, a player can:
    Make 0, 1, or 2 moves (optional)
    Push other piece(s) using their square piece (mandatory)
    
Movement of a piece is legal to any free space on the board as long as
there is a connection between it and the piece's space. A connection
exists if you can make orthogonal movements through free spaces to reach it.
Once movement is finished, a player uses a square piece to push.

A player can push either player's piece(s) and can push a line of pieces
in direct contact so long as the piece or line is not blocked (either by 
the side rails or by an anchor)

Board.push_dict tells us the resulting board position for a piece
being pushed, given its current position and direction as a tuple.
Direction is 0, 1, 2, 3, meaning up, right, down, left, respectively
For example, if a piece at position 11 is being pushed left, look up
(11, 3) in push_dict. This tells us the new position of that piece 
will be 10. If a push results in the piece going off, push_dict
for that tuple will be associated with "END", and will similarly
be associated with "BLOCKED" if a push tuple is blocked by the rails.

"""

#Board print helper function
def space(piece):
    if piece == 0: return '[]' 
    else: return " {}".format(piece) if piece > 0 else piece


#board positions
def print_board_positions():
    print('\n')
    print('      0    1      ')
    print('|2    3    4      ')
    print('|5    6    7    8|')
    print('|9   10   11   12|')
    print('|----------------|')
    print('|13  14   15   16|')
    print('|17  18   19   20|')
    print('     21   22   23|')
    print('     24   25      ')

class Board:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.p1_pieces = [-1,-1,-2,-2,-2]
        self.p2_pieces = [ 1, 1, 2, 2, 2]
        self.board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.board_history = []
        self.trace = []
        self.turn = -3

        self.push_dict = {(0, 0) : "END", (0, 1) : 1, (0, 2) : 3, (0, 3) : "END",
                            (1, 0) : "END", (1, 1) : "END", (1, 2) : 4, (1, 3) : 3,
                            (2, 0) : "END", (2, 1) : 3, (2, 2) : 6, (2, 3) : "BLOCKED",
                            (3, 0) : 0, (3, 1) : 4, (3, 2) : 6, (3, 3) : 2,
                            (4, 0) : 1, (4, 1) : "END", (4, 2) : 7, (4, 3) : 3,
                            (5, 0) : 2, (5, 1) : 6, (5, 2) : 9, (5, 3) : "BLOCKED",
                            (6, 0) : 3, (6, 1) : 7, (6, 2) : 10, (6, 3) : 5,
                            (7, 0) : 4, (7, 1) : 8, (7, 2) : 11, (7, 3) : 6,
                            (8, 0) : "END", (8, 1) : "BLOCKED", (8, 2) : 12, (8, 3) : 7,
                            (9, 0) : 5, (9, 1) : 10, (9, 2) : 13, (9, 3) : "BLOCKED",
                            (10, 0) : 6, (10, 1) : 11, (10, 2) : 14, (10, 3) : 9,
                            (11, 0) : 7, (11, 1) : 12, (11, 2) : 15, (11, 3) : 10,
                            (12, 0) : 8, (12, 1) : "BLOCKED", (12, 2) : 16, (12, 3) : 11,
                            (13, 0) : 9, (13, 1) : 14, (13, 2) : 18, (13, 3) : "BLOCKED",
                            (14, 0) : 10, (14, 1) : 15, (14, 2) : 18, (14, 3) : 13,
                            (15, 0) : 11, (15, 1) : 16, (15, 2) : 19, (15, 3) : 14,
                            (16, 0) : 12, (16, 1) : "BLOCKED", (16, 2) : 20, (16, 3) : 15,
                            (17, 0) : 13, (17, 1) : 18, (17, 2) : "END", (17, 3) : "BLOCKED",
                            (18, 0) : 14, (18, 1) : 19, (18, 2) : 21, (18, 3) : 17,
                            (19, 0) : 15, (19, 1) : 20, (19, 2) : 22, (19, 3) : 18,
                            (20, 0) : 16, (20, 1) : "BLOCKED", (20, 2) : 23, (20, 3) : 19,
                            (21, 0) : 18, (21, 1) : 22, (21, 2) : 24, (21, 3) : "END",
                            (22, 0) : 19, (22, 1) : 23, (22, 2) : 25, (22, 3) : 21,
                            (23, 0) : 20, (23, 1) : "BLOCKED", (23, 2) : "END", (23, 3) : 22,
                            (24, 0) : 21, (24, 1) : 25, (24, 2) : "END", (24, 3) : "END",
                            (25, 0) : 22, (25, 1) : "END", (25, 2) : "END", (25, 3) : 24}
        self.adj_spaces = {0:[1,3],1:[4,0],2:[3,5],3:[0,4,6,2],4:[1,7,3],5:[2,6,9],6:[3,7,10,5],7:[4,8,11,10],8:[12,7],9:[5,10,13],10:[6,11,14,9],11:[7,12,15,10],12:[8,16,11],13:[9,14,17],14:[10,15,18,13],15:[11,16,19,14],16:[12,20,15],17:[13,18],18:[14,19,21,17],19:[15,20,22,18],20:[16,23,19],21:[18,22,24],22:[19,23,25,21],23:[20,22],24:[21,25],25:[22,24]}

    #Returns all p1 positions
    @property
    def p1_pos(self):
        return [i for i in range(len(self.board)) if self.board[i] < 0]

    #Returns all p2 positions
    @property
    def p2_pos(self):
        return [i for i in range(len(self.board)) if self.board[i] > 0]

    #Returns anchor position
    @property
    def anchor_pos(self):
        pos = [i for i in range(len(self.board)) if self.board[i] > 2 or self.board[i] < -2]
        return None if len(pos) == 0 else pos[0]

    #Set anchor position with error handling
    def set_anchor(self, pos):
        if pos < 0 or pos > 25 or self.board[pos] == 0: raise Exception('Invalid anchor position')
        if self.board[pos] == 1 or self.board[pos] == -1: raise Exception('Circles cant be anchored')
        if self.board[pos] == 2: self.board[pos] += 1
        else: self.board[pos] -= 1
     

    #if p1 or p2 is false it will count as randomly selected spaces
    def build_board(self):
        #Player One || White Pieces
        if self.p1:
            while len(self.p1_pieces) != 0:
                piece = self.p1_pieces.pop()
                move = input("Place your {} in spaces {}: \n".format('square' if piece == -2 else 'circle', 
                                                                     [i for i in range(0,13) if self.board[i] == 0]))
                if self.check_free_space(move) and int(move) < 13:
                    self.board[int(move)] = piece
                    self.print()
                else:
                    print("{} is not a valid move".format(move))
                    self.p1_pieces.append(piece)
        else:
            
            for i in range(5):
                if i == 4:
                    self.board[12-7] = self.p1_pieces.pop()
                else:    
                    self.board[12-i] = self.p1_pieces.pop()
            """
            while len(self.p1_pieces):
                move = random.randint(0,12)
                if self.board[move] == 0: 
                    self.board[move] = self.p1_pieces.pop()
            """
            
            
        
        #Player Two || Brown Pieces
        if self.p2:
            while len(self.p2_pieces) != 0:
                piece = self.p2_pieces.pop()
                move = input("Place your {} in spaces {}: ".format('square' if piece == 2 else 'circle', 
                                                                   [i for i in range(13,26) if self.board[i] == 0]))
                if self.check_free_space(move) and int(move) > 12:
                    self.board[int(move)] = piece
                    self.print()
                else:
                    print("{} is not a valid move".format(move))
                    self.p2_pieces.append(piece)
        else:
            
            for i in range(5):
                if i == 4:
                    self.board[13+7] = self.p2_pieces.pop()
                else:
                    self.board[13+i] = self.p2_pieces.pop()
            """
            while len(self.p2_pieces) != 0:
                move = random.randint(13,25)
                if self.board[move] == 0:
                    self.board[move] = self.p2_pieces.pop()
            """
            
            
    

    #Check if Space is free
    #Players can move wherever a space is free after INIT
    def check_free_space(self, move):
        try: 
            move = int(move) 
            if self.board[move] != 0: return False
            if move < 0 or move > 25: return False
        except:
            return False
        return True


    # Check that a move is valid
    # A valid move must go from a piece to a free space
    # and have an orthogonal path between
    def check_valid_move(self, curr, final):
        if not self.check_free_space(final): return False
        queue = [x for x in self.adj_spaces[curr] if self.board[x] == 0]
        seen = []
        while queue:
            if final in queue:
                return True
            queue += [x for x in self.adj_spaces[queue[0]] if x not in seen and self.board[x] == 0]
            seen.append(queue[0])
            queue = queue[1:]
        return False
            

    # Get all spaces curr can move to
    # Does not check if curr is empty, in which case curr
    # would be included in the otherwise valid result list
    def get_all_valid_moves(self, curr):
        candidates = [x for x in range(26) if self.board[x] == 0]
        result = []
        for spc in candidates:
            if self.check_valid_move(curr, spc):
                result.append(spc)
        return result


    # Check if a push on curr in direction d is valid
    # The destination must not be blocked
    # If another piece is in destination, it must
    # also be pushed; otherwise the push is valid
    # When first==True, the pushing square is pushing
    # itself, so the destination MUST have a piece
    # Recursive
    # 0 - Up
    # 1 - Right
    # 2 - Down
    # 3 - Left
    def check_valid_push(self, curr, d, first=False):
        final = self.push_dict[(curr, d)]
        if final == "BLOCKED":
            return False
        elif final == "END":
            if first:
                return False
            else:
                return True
        else:
            if abs(self.board[final]) == 3:
                return False
            if self.board[final] == 0:
                if first:
                    return False
                else:
                    return True
            else:
                return self.check_valid_push(final, d)


    # Get all valid pushes from a piece at curr
    # Returns list of tuples
    def get_all_valid_pushes(self, curr):
        candidates = [x for x in self.push_dict.keys() if x[0] == curr]
        result = []
        for psh in candidates:
            if self.check_valid_push(psh[0], psh[1], first=True):
                result.append(psh)
        return result

    # whichPlayer == -1 for p1, or == 1 for p2
    # Return a list of tuples. Each tuple is two locations.
    # The first loc is loc of one of the player's pieces (that can be moved)
    # The second loc is loc where that piece could be moved
    # Used for random decision
    # Use example, making a random move for p1: 
    # board.make_move(random.choice(board.get_boards_move_options(-1)))
    def get_boards_move_options(self, whichPlayer):
        playersPiecesLocs = [x for x in range(26) if self.board[x] == whichPlayer or self.board[x] == whichPlayer*2]
        moveOptions = []
        for curr in playersPiecesLocs:
            for final in [x for x in range(26) if self.check_valid_move(curr, x) and x != curr]:
                moveOptions.append((curr, final))
        return moveOptions

    # whichPlayer == -1 for p1, or == 1 for p2
    # Return a list of tuples. Each tuple is a location and a direction
    # The first loc is loc of one of the player's squares that has pieces it could push
    # The direction is the direction of an adjacent piece that can be pushed
    # Used for random decision
    # Use example, making a random push for p2: 
    # board.make_move(random.choice(board.get_boards_push_options(1)), push=True)
    # If prevent_suicide==True, restricts returned pushes to pushes that do not cause this player to lose
    def get_boards_push_options(self, whichPlayer, prevent_suicide=True):
        playersSquaresLocs = [x for x in range(26) if self.board[x] == (-2 if whichPlayer < 0 else 2)]
        for sq in playersSquaresLocs:
            assert abs(self.board[sq]) == 2
        pushOptions = []
        for curr in playersSquaresLocs:
            for d in range(4):
                if self.check_valid_push(curr, d, first=True):
                    pushOptions.append((curr, d))

        if prevent_suicide:
            viable_options = []
            # A viable push is a push that, if the last piece it pushes is on its own team, doesn't end the game
            # In short, prevents a random player from making pushes that makes itself lose
            for opt in pushOptions:
                # We want to find out the identity of the last piece in a "push chain"
                # to prevent a random player from pushing their own pieces IF that causes the game to end 
                # e.g. When -2 pushes a line of -1, -2, 2, 1, we want to get 1
                lastPushedPiece = 0 # tracks identity
                curr_tmp = opt[0] # tracks location
                while self.board[self.push_dict[(curr_tmp, opt[1])]] != 0: # while piece at curr_tmp's new loc isn't zero (i.e. another piece being pushed)
                    curr_tmp = self.push_dict[(curr_tmp, opt[1])]
                    lastPushedPiece = self.board[curr_tmp] # keep updating the identity to most recently pushed piece
                    if type(self.push_dict[(curr_tmp, opt[1])]) == str: break
                if (lastPushedPiece < 0 and whichPlayer < 0) or (lastPushedPiece > 0 and whichPlayer > 0):
                    # pushing own piece, so we need to make sure this doesn't end the game
                    self.make_move(opt, push=True)
                    if self.turn != 0:
                        viable_options.append(opt)
                    self.undo_move(whichPlayer, 1)
                else:
                    viable_options.append(opt)
            return viable_options

        return pushOptions


    def move_piece(self, curr, final):
        self.board[final] = self.board[curr]
        self.board[curr] = 0

    """
    def push_piece(self, curr, d):
        pieces = queue.LifoQueue()
        check = True
        index = curr
        pieces.put(curr)
        print(curr, d)
        while check:
            if len(self.adj_spaces[index]) >= d+1:
                print(self.adj_spaces[d])
                place = self.board[self.adj_spaces[index][d]]
                print(place)
                if place is not 0:
                    pieces.put(place)
                    index = place
                else:
                    check = False
            else:
                check = False
        for i in range(0, pieces.qsize()):
            place = pieces.get()
            print(place)
            self.move_piece(place, self.adj_spaces[place][d])
        """
    #Sets and updates anchor
    #Sets turn = 0 for game over
    #cur = current piece position, d = direction being pushed
    #directions = 0 up, 1 right, 2 down, 3 left
    #Moves the furthest piece first and ends on the initial push piece
    def push_piece(self, curr, d):
        pieces_to_push = [(curr, self.push_dict[(curr, d)])]
        if self.anchor_pos != None:
            if self.board[self.anchor_pos] < 0:
                self.board[self.anchor_pos] += 1
            else:
                self.board[self.anchor_pos] -= 1
        if self.turn < 0:
            self.board[curr] -= 1
        else:
            self.board[curr] += 1
        while True:
            if self.board[curr] == 0:
                break
            new_curr_pos = self.push_dict[(curr, d)]
            if type(new_curr_pos) == str:
                self.turn = 0
                return new_curr_pos
            if self.board[new_curr_pos] == 0:
                break
            piece_to_push_pos = self.push_dict[(new_curr_pos, d)]
            pieces_to_push.append((new_curr_pos,piece_to_push_pos))
            curr = new_curr_pos
        self.turn = 3 if self.turn == -1 else -3
        for _ in range(len(pieces_to_push)):
             move = pieces_to_push.pop()
             self.move_piece(move[0], move[1])


    """
    # Calls checks and moves pieces back in event of failure
    # push_move is a tuple of 2 (current and direction)
    # piece1_move is a tuple of 2 (current and final)
    # piece2_move is a tuple of 2 (current and final)
    """
    #Editing make move to allow every move to be stored in board history
    #Takes a move , tuple
    #if push is True, move will be piece & direction
    #else move is piece & new board spot
    def make_move(self, move, push = False):
        if push:
            if abs(self.board[move[0]]) == 1: raise Exception('Circles cant push')
            if not self.check_valid_push(move[0], move[1]): raise Exception('Invalid push')
            else: 
                self.board_history.append(self.board[:])
                self.trace.append(["push",move])
                self.push_piece(move[0], move[1])
        else:
            if not self.check_valid_move(move[0], move[1]): raise Exception('Invalid move')
            else: 
                self.board_history.append(self.board[:])
                self.trace.append(["move",move])
                self.move_piece(move[0], move[1])
                self.turn = self.turn + 1 if self.turn < 0 else self.turn - 1
            

    # Revert a board to its state movesMade moves ago, setting board.turn to 3 * whichPlayer
    def undo_move(self, whichPlayer, movesMade=3):
        self.board = self.board_history[len(self.board_history) - movesMade]
        self.board_history = self.board_history[:len(self.board_history) - movesMade]
        self.trace = self.trace[:len(self.trace) - movesMade]
        self.turn = 3 * whichPlayer


    # Resets board to an earlier state, where nothing after depth in board's history has happened
    def undo_moves_to_depth(self, whichPlayer, depth):
        self.board = self.board_history[depth] # if depth > 0 else self.board
        self.board_history = self.board_history[:depth]
        self.trace = self.trace[:depth]
        self.turn = 3 * whichPlayer



    #current board
    def print(self):
        print('\n')
        print('    {} {}    '.format(space(self.board[0]), space(self.board[1])))
        print('|{} {} {}    '.format(space(self.board[2]), space(self.board[3]), space(self.board[4])))
        print('|{} {} {} {}|'.format(space(self.board[5]), space(self.board[6]), space(self.board[7]), space(self.board[8])))
        print('|{} {} {} {}|'.format(space(self.board[9]), space(self.board[10]), space(self.board[11]), space(self.board[12])))
        print('|-----------|')
        print('|{} {} {} {}|'.format(space(self.board[13]), space(self.board[14]), space(self.board[15]), space(self.board[16])))
        print('|{} {} {} {}|'.format(space(self.board[17]), space(self.board[18]), space(self.board[19]), space(self.board[20])))
        print('    {} {} {}|'.format(space(self.board[21]), space(self.board[22]), space(self.board[23])))
        print('    {} {}    '.format(space(self.board[24]), space(self.board[25])))

        
if __name__ == "__main__":
    board = Board(False, False)
    board.build_board()
    board.print()
    print(board.p1_pos)
    print(board.p2_pos)
    print(board.check_valid_move(1, 24))
    print(board.get_all_valid_moves(1))
    print(board.get_all_valid_pushes(3))
    print_board_positions()
