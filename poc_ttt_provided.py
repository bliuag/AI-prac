"""
poc_ttt_provided.py
Provided Code for Tic-Tac-Toe
@author Rice university, revised by Jiahan Yan and Boyu Liu
"""

from time import time

# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}


class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """
    def __init__(self, dim, reverse=False, board = None, lastmove = None):
        self._dim = dim # now dim is 3. but represent 9x9 board
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[[[EMPTY for dummycol in range(dim)]
                           for dummyrow in range(dim)]
                           for dummyCOL in range(dim)]
                           for dummyROW in range(dim)]
        else:
            # Copy board grid
            self._board = [[[[board[boxr][boxc][row][col] for col in range(dim)]
                           for row in range(dim)]
                           for boxc in range(dim)]
                           for boxr in range(dim)]
        self._lastmove = lastmove

    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for boxrow in range(self._dim):
            for row in range(self._dim):
                for boxcol in range(self._dim):
                    for col in range(self._dim):
                        rep += STRMAP[self._board[boxrow][boxcol][row][col]]
                        if col == self._dim - 1 and boxcol == self._dim - 1:
                            rep += "\n"
                        elif col == self._dim - 1:
                            rep += " || "
                        else:
                            rep += " | "
                if row != self._dim - 1:
                    rep += "-" * (4 * self._dim * self._dim - 3)
                elif boxrow != self._dim - 1:
                    rep += "=" * (4 * self._dim * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim

    def square(self, boxrow, boxcol, row, col):
        """
        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
        position (row, col).
        """
        return self._board[boxrow][boxcol][row][col]

    def get_all_empty_squares(self):
        """
        Return a list of (boxrow, boxcol, row, col) tuples for all empty squares
        """
        empty = []
        for boxrow in range(self._dim):
            for boxcol in range(self._dim):
                for row in range(self._dim):
                    for col in range(self._dim):
                        if self._board[boxrow][boxcol][row][col] == EMPTY:
                            empty.append((boxrow, boxcol, row, col))
        return empty

    def check_full(self, boxrow, boxcol):
        """
        check whether a box is full
        """
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[boxrow][boxcol][row][col] == EMPTY:
                    return False
        return True

    def get_valid_moves(self):
        """
        Return a list of (boxrow, boxcol, row, col) tuples for all empty squares
        """
        lastmove = self._lastmove
        if lastmove == None:
            return self.get_all_empty_squares()
        lastboxrow, lastboxcol, lastrow, lastcol = lastmove
        if self.check_full(lastrow,lastcol):
            return self.get_all_empty_squares()
        else:
            boxrow = lastrow
            boxcol = lastcol
            validset = []
            for row in range(self._dim):
                for col in range(self._dim):
                    if self._board[boxrow][boxcol][row][col] == EMPTY:
                        validset.append((boxrow, boxcol, row, col))
            return validset
        

    def move(self, boxrow, boxcol, row, col, player):
        """
        Place player on the board at position (row, col).

        Does nothing if board square is not empty.
        """
        if self._board[boxrow][boxcol][row][col] == EMPTY:
            self._board[boxrow][boxcol][row][col] = player
            self._lastmove = (boxrow, boxcol, row, col)

    def check_win_box(self, boxrow, boxcol):

        box = self._board[boxrow][boxcol]
        lines = []

        # rows
        lines.extend(box)

        # cols
        cols = [[box[rowidx][colidx] for rowidx in range(self._dim)]
                for colidx in range(self._dim)]
        lines.extend(cols)

        # diags
        diag1 = [box[idx][idx] for idx in range(self._dim)]
        diag2 = [box[idx][self._dim - idx - 1]
                 for idx in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                return line[0]

        return EMPTY
    
    def check_win(self):
        """
        If someone has won, return player.
        If game is a draw, return DRAW.
        If game is in progress, return None.
        """
        board = [[self.check_win_box(boxrow,boxcol) for boxcol in range(self._dim)]
                  for boxrow in range(self._dim)]
        lines = []

        # rows
        lines.extend(board)

        # cols
        cols = [[board[rowidx][colidx] for rowidx in range(self._dim)]
                for colidx in range(self._dim)]
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in range(self._dim)]
        diag2 = [board[idx][self._dim - idx - 1]
                 for idx in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_all_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None

    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board, self._lastmove)


def switch_player(player):
    """
    Convenience function to switch players.
    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX


def play_game(ai_func1,ai1_para, ai_func2, ai2_para, reverse=False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None

    # Run game
    while winner == None:
        # Move
        if curplayer == PLAYERX:
            # prev_t = time()
            boxrow, boxcol, row, col = ai_func1(board, curplayer, ai1_para)
            # cur_t = time()
            # diff = cur_t - prev_t
            # print (diff)
        else:
            try:
                prev_t = time()
                boxrow, boxcol, row, col = ai_func2(board, curplayer, ai2_para)
                cur_t = time()
                diff = cur_t - prev_t
                print (diff)
            except:
                raise ValueError
                print("function2 error")
        board.move(boxrow, boxcol, row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        # print (board)
        # print ("\n")

    # Print winner
    if winner == PLAYERX:
        print ("X wins!")
    elif winner == PLAYERO:
        print ("O wins!")
    elif winner == DRAW:
        print ("Tie!")
    else:
        print ("Error: unknown winner")
    return winner