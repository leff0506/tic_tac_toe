import  json
board = [[1,1,0],[1,2,0],[0,2,2]]
def convert_board_to_str(board,player_id):
    result = ""
    for i in range(3):
        for j in range(3):
            result+=str(board[i][j])
    result +=str(player_id)
    return result

win_move = {}
win_score = {}
def check_for_win(player):
    # hor
    for i in range(3):
        done = True
        for j in range(3):
            if board[i][j] != player:
                done = False
        if done:
            return True

    # vert
    for i in range(3):
        done = True
        for j in range(3):
            if board[j][i] != player:
                done = False
        if done:
            return True

    # main diag
    done = True
    for i in range(3):
        if board[i][i] != player:
            done = False
    if done:
        return True
    done = True
    for i in range(3):
        if board[i][2 - i] != player:
            done = False

    if done:
        return True
    return False

def get_result(player_id):
    state = convert_board_to_str(board,player_id)
    if state in win_score:
        return win_score[state]
    if check_for_win(player_id):
        return 1
    if check_for_win(3-player_id):
        return -1

    score = -2
    move =-1
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player_id

                win = -get_result(3-player_id)
                if win > score:
                    score = win
                    move = i*3 + j
                board[i][j] = 0

    if move == -1:
        win_move[state] = 10
        win_score[state] = 0
        return 0

    win_move[state] = move
    win_score[state] = score
    return score

get_result(2)
# get_result(2)
#
# print(len(win_move))
# result = json.dumps(win_move)
# with open("ai.json","w") as f:
#     f.write(result)