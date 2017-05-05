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


class Scores:
    """
    # use this class to keep track of MC scores
    """
    def __init__(self, board):
        self._score = [[[[0 for dummycol in range(board.get_dim())]
                         for dummyrow in range(board.get_dim())]
                        for dummyCOL in range(board.get_dim())]
                       for dummyROW in range(board.get_dim())]
        # score and board need to be consistant

    def __str__(self):
        return self._score

    def update_score(self, board, player):
        # update the score according to the board and player
        for db_i in range(board.get_dim()):
            for db_j in range(board.get_dim()):
                for d_i in range(board.get_dim()):
                    for d_j in range(board.get_dim()):
                        if player == provided.PLAYERX:
                            if board.square(db_i, db_j, d_i, d_j) == provided.PLAYERX:
                                self._score[db_i][db_j][d_i][d_j] += SCORE_CURRENT
                            elif board.square(db_i, db_j, d_i, d_j) == provided.EMPTY:
                                self._score[db_i][db_j][d_i][d_j] += 0
                            else:
                                self._score[db_i][db_j][d_i][d_j] -= SCORE_OTHER
                        elif player == provided.PLAYERO:
                            if board.square(db_i, db_j, d_i, d_j) == provided.PLAYERO:
                                self._score[db_i][db_j][d_i][d_j] += SCORE_OTHER
                            elif board.square(db_i, db_j, d_i, d_j) == provided.EMPTY:
                                self._score[db_i][db_j][d_i][d_j] += 0
                            else:
                                self._score[db_i][db_j][d_i][d_j] -= SCORE_CURRENT
        return self._score

    def get_score(self):
        """
        # use this class to keep track of scores
        """
        return self._score


def mc_trial(board, player):
    """
    This function takes a current board and the next player to move
    then move turn by turn till someone wins or draw
    modify the board
    """
    cnt = 0
    while board.check_win() == None:
        # print ("moves done in a trial: ", cnt)
        # ## shall only consider the board.get_valid_moves()
        # print ("# of valid moves: ", len(board.get_valid_moves())) ### changed to get_all_empty_
        add_pos = random.choice( board.get_valid_moves()) # return list of tuple (boxrow, boxcol, row, col)

        # 4 positions defines a move
        board.move(add_pos[0],add_pos[1], add_pos[2], add_pos[3], player)   # move(self, boxrow, boxcol, row, col, player):
        player = provided.switch_player(player)
        cnt += 1
    return None


def mc_update_scores(scores, board, player):
    """
    update the scores grid according to the board.
    the scores is a reference 
    """
    dim = range(board.get_dim())
    if board.check_win() == provided.PLAYERX:
        # scores.update_score(board, provided.PLAYERX) # to be continued oop design
        for db_i in dim:
            for db_j in dim:
                for d_i in dim:
                    for d_j in dim:
                        if board.square(db_i, db_j, d_i, d_j) == provided.PLAYERX:
                            scores[db_i][db_j][d_i][d_j] += SCORE_CURRENT
                        elif board.square(db_i, db_j, d_i, d_j) == provided.EMPTY:
                            scores[db_i][db_j][d_i][d_j] += 0
                        else:
                            scores[db_i][db_j][d_i][d_j] -= SCORE_OTHER
    elif board.check_win() == provided.PLAYERO:
        # scores.update_score(board, provided.PLAYERO)
        for db_i in dim:
            for db_j in dim:
                for d_i in dim:
                    for d_j in dim:
                        if board.square(db_i, db_j, d_i, d_j) == provided.PLAYERO:
                            scores[db_i][db_j][d_i][d_j] += SCORE_OTHER
                        elif board.square(db_i, db_j, d_i, d_j) == provided.EMPTY:
                            scores[db_i][db_j][d_i][d_j] += 0
                        else:
                            scores[db_i][db_j][d_i][d_j] -= SCORE_CURRENT
    return None


def get_best_move(board, scores):
    """
    The function find all of the valid empty squares with the maximum score 
    and randomly return one of them as a (boxrow, boxcol, row, column) tuple
    """
    # while board.check_win() == None:
    empty_list = board.get_valid_moves()  # ist of length 4 tuple
    empty_val = [scores[i[0]][i[1]][i[2]][i[3]] for i in empty_list] # non-valid moves are 0
    max_score = max(empty_val)

    choice_range = []
    for i in empty_list:
        if scores[i[0]][i[1]][i[2]][i[3]] == max_score:
            choice_range.append(i)
    final_choice = random.choice(choice_range)
    return final_choice

# similar to main function
def mc_move(board, player, trials):
    """
    return the best Monte Carlo simulation move for the machine player.(boxrow, boxcol, row, column) tuple
    """
    score_instance = Scores(board)
    scores = score_instance.get_score() # scores is list in list..
    for i in range(trials):
        # print ("################################attention trial  %d ##############################" %(i))
        copy=board.clone()
        mc_trial(copy, player) # take the copy and simulate to game end. copy is modified
        mc_update_scores(scores, copy, player)
    best_move = get_best_move(board, scores)
    return best_move


# Test game with the console or the GUI.
provided.play_game(mc_move, NTRIALS, False) # two monte carol players test
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)