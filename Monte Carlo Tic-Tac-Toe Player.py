"""
Monte Carlo Tic-Tac-Toe Player
    @author Jiahan Yan, Boyu Liu
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 20  # Number of trials to run
SCORE_CURRENT = 3.0  # Score for squares played by the machine player
SCORE_OTHER = 2.0  # Score for squares played by the other player


# Add your functions here.
class Scores:
    """
    # use this class to keep track of scores
    """
    def __init__(self, board):
        self._score = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]

    def __str__(self):
        return self._score

    def set_score(self, board):
        """
        # set scores
        """
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                self._score[dummy_row][dummy_col] = board.square(dummy_row, dummy_col)

    def get_score(self):
        """
        # use this class to keep track of scores
        """
        return self._score


def mc_trial(board, player):
    """
    # This function takes a current board 
    # and the next player to move
    """
    while board.check_win()==None:
        add_pos= random.choice( board.get_empty_squares() )
        #print "mc_trial part: add pos: ", add_pos
        board.move(add_pos[0],add_pos[1], player)
        player=provided.switch_player(player)
    #print "mc_trial part: ", "\n",board
    return None


def mc_update_scores(scores, board, player):
    """
    # The function should score the completed board 
    # and update the scores grid.
    # As the function updates the scores grid directly
    """
    dim = range(board.get_dim())
    #    scores=[  [0 for dummy in dim] for dummy in dim ]
    if board.check_win() == provided.PLAYERX:
        for d_i in dim:
            for d_j in dim:
                if board.square(d_i, d_j) == provided.PLAYERX:
                    scores[d_i][d_j] += SCORE_CURRENT
                elif board.square(d_i, d_j) == provided.EMPTY:
                    scores[d_i][d_j] += 0
                else:
                    scores[d_i][d_j] -= SCORE_OTHER
    elif board.check_win() == provided.PLAYERO:
        for d_i in dim:
            for d_j in dim:
                if board.square(d_i, d_j) == provided.PLAYERO:
                    scores[d_i][d_j] += SCORE_OTHER
                elif board.square(d_i, d_j) == provided.EMPTY:
                    scores[d_i][d_j] += 0
                else:
                    scores[d_i][d_j] -= SCORE_CURRENT
    # print "update score part: scores: ", scores
    return None

def get_best_move(board, scores):
    """
    # The function find all of the empty squares with the maximum score 
    # and randomly return one of them as a (row, column) tuple
    """
    while board.check_win() == None:
        e_i = board.get_empty_squares()  # ei is a list of tuple
        # print "ei is: ", ei
        # i is a tuple
        empty_val = [scores[i[0]][i[1]] for i in e_i]
        empty_max = max(empty_val)

        choice_range = []
        # print "get_best_move part: empty ones are: ",board.get_empty_squares()
        for d_i in board.get_empty_squares():
            # mistake: if board.square(i[0],i[1])== tot_max:
            if scores[d_i[0]][d_i[1]] == empty_max:
                choice_range.append(d_i)
                #                print "in loop choice_range is: ", choice_range
        # print "get_best_move part: choice_range is:", choice_range
        final_choice = random.choice(choice_range)
        return final_choice


def mc_move(board, player, trials):
    """
    # The function should use the Monte Carlo simulation 
    #  return a move for the machine player in the form of a (row, column) tuple
    """
    scores=[  [0 for dummy in range(board.get_dim())] for dummy in range(board.get_dim()) ]
    for _ in range(trials):
        copy=board.clone()
        mc_trial(copy, player)#this is for modifying the copy
        mc_update_scores(scores, copy, player)
    #print "mc_move part: scores: ", scores
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(9, provided.PLAYERX, mc_move, NTRIALS, False)