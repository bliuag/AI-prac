"""
Monte Carlo Tic-Tac-Toe Player
    @author Jiahan Yan, Boyu Liu
"""
import numpy as np
import random
import poc_ttt_gui
import poc_ttt_provided as provided

######################    Monte carol method ##############################
NTRIALS = 100  # Number of trials to run
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
    return board.check_win()

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
    empty_list = board.get_valid_moves()  # list of length 4 tuple
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
        copy=board.clone()
        mc_trial(copy, player) # take the copy and simulate to game end. copy is modified
        mc_update_scores(scores, copy, player)
    best_move = get_best_move(board, scores)
    return best_move

############################### minMax recursion #######################
DEPTH = 3
MIN_MAX_MC_ROUND = 10 # huristic rounds
def minMaxRec(d, board, player):
    """
    min-max to certain degree
    """
    if board.check_win() == player:
        return None, 1
    elif board.check_win() == provided.switch_player(player):
        return None, 0
    elif board.check_win() == provided.DRAW:
        return None, 0.5
    if d == 0:
        oppo = provided.switch_player(player)
        # ####### 1. MC as the huristic function
        # winr = 0 # winning rounds
        # loser = 0 # losing rounds
        # for i in range(MIN_MAX_MC_ROUND):
        #     winner = mc_trial(board, player)
        #     if winner == player:
        #         winr += 1
        #     elif winner == oppo:
        #         loser += 1
        # return None, (winr +1)/(winr+loser+1) # smooth

        # ####### 2. feature evaluation as huristic function
        res = huristic(board, player)/10
        if res >1 or res <0:
            print("res %f" %(res))
        # print ("board: ", board.get_valid_moves())
        # print ("res: ", res)
        return None, res

    valid_moves = board.get_valid_moves()
    if len(valid_moves)==0:
        print("No valid moves!")
    best_move, best_win_rate = None, -1 # can't be 0 since heuristic is changed

    for move in valid_moves:
        copy = board.clone()
        copy.move(move[0], move[1], move[2], move[3], player)
        nextplayer = provided.switch_player(player)
        _, r = minMaxRec(d-1, copy, nextplayer)
        # print("%d %f" %(d,r))
        # print("position\t%d\t%d\t%d\t%d\tscore\t%f" %(move[0], move[1], move[2], move[3],1-r))
        if 1-r >= best_win_rate:
            best_win_rate = 1-r
            best_move = move
    return (best_move, best_win_rate)

def minMaxMove(board, player, d):
    return minMaxRec(d, board, player)[0]

############### huristic function (feature function) ##########
def huristic(board, player):
    # board is after the oppo moves, the board
    # the value is for player's reference
    # print(str(board))
    box_vals = [[],[],[]]
    for i in range(3):
        for j in range(3):
            box_vals[i].append( normalize( huristic_small_box(board, i, j, player) ) )
    box_row,box_col,row,col = board._lastmove
    hc = box_vals[box_row][box_col]
    # print ("hc: ", hc)
    hn = box_vals[row][col]
    H = huristic_big_box(box_vals)
    # print (hc, hn, H)
    # print (hc + hn + H)
    return hc + hn + H

NORMAL = 30
def huristic_small_box(board, boxrow, boxcol, player):
    # [[],[],[]] small_box
    score = 0
    small_box = np.array(board._board[boxrow][boxcol])
    oppo = provided.switch_player(player)

    winner = board.check_win_box(boxrow,boxcol)
    if winner == player: # return 1
        return NORMAL/2
    if winner == oppo: # return 0
        return -NORMAL/2
    
    player_pos = (small_box == player) # 3 x 3
    oppo_pos = (small_box == oppo)

    ## score the player
    score += np.sum( (np.sum(player_pos,1)-np.sum(oppo_pos,1)) * (np.sum(player_pos, 1) * np.sum(oppo_pos, 1) == 0) ) # np.sum(player_pos, 1) * np.sum(oppo_pos, 1) == 0  is 3x1 true false matrix. axis=1 sum rows
    score += np.sum( (np.sum(player_pos,0)-np.sum(oppo_pos,0)) * (np.sum(player_pos, 0) * np.sum(oppo_pos, 0) == 0) ) # axis 0 sum columns
    score += (      np.sum(np.diag(player_pos))-np.sum(np.diag(oppo_pos))     ) * (      np.sum(np.diag(player_pos)) * np.sum(np.diag(oppo_pos))==0    ) # np.diag(player_pos) is 3x1 matrix
    score += (np.sum(np.diag(np.fliplr(player_pos)))-np.sum(np.diag(np.fliplr(oppo_pos)))) * (    np.sum(np.diag(np.fliplr(player_pos))) * np.sum(np.diag(np.fliplr(oppo_pos))) == 0   )
    return score

def normalize(score):
    return (score + 15) / NORMAL

# (a^2 + b^2 + c^2)^0.5
def huristic_big_box_2(box_vals):
    # has a 9x9 0~1 matrix already
    big_box = np.array(box_vals)
    big_box = big_box ** 3
    res = 0
    res += np.sum( np.cbrt(np.sum(big_box, 0)) ) # 3 values
    res += np.sum( np.cbrt(np.sum(big_box, 1)) ) # 3 values
    res += np.sum( np.cbrt(np.diag(big_box)) ) # 1 value
    res += np.sum( np.cbrt(np.diag(np.fliplr(big_box))) ) # 1 value
    return res

def huristic_big_box(box_vals):
    # has a 9x9 0~1 matrix already
    big_box = np.array(box_vals)
    res = 0
    res += np.sum( np.cbrt(np.prod(big_box, 0)) ) # 3 values
    res += np.sum( np.cbrt(np.prod(big_box, 1)) ) # 3 values
    res += np.cbrt(np.prod(np.diag(big_box))) # 1 value
    res += np.cbrt(np.prod(np.diag(np.fliplr(big_box)))) # 1 value
    return res


###Test game with the console or the GUI.
AI_VS_AI_GAMES = 10
winners = []
lookup = {provided.PLAYERX: "Monte carol", provided.PLAYERO: "minMax"}
for i in range(AI_VS_AI_GAMES):
    # two AI test
    print("test",i)
    winner = provided.play_game(mc_move, NTRIALS, minMaxMove, DEPTH, False)
    if winner == provided.PLAYERX:
        winners.append("Monte carol")
    elif winner == provided.PLAYERO:
        winners.append("minMax")
    else:
        winners.append("draw")
print (winners)

# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

# just run minmax
# poc_ttt_gui.run_gui(3, provided.PLAYERX, minMaxMove, DEPTH, False)