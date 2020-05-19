import json
import copy
class AI:
    def __init__(self):
        with open("engine/ai/ai.json","r") as f:
            data_str = f.read()
        self.win_state = json.loads(data_str)

    def __convert_board_to_str(self ,board, player_id):
        result = ""
        for i in range(3):
            for j in range(3):
                result += str(board[i][j])
        result += str(player_id)
        return result
    def get_move(self,board,player_id):
        board_copy = copy.deepcopy(board)
        board_str = self.__convert_board_to_str(board_copy,player_id)
        if board_str not in self.win_state:
            print("fuck_here")
            return -1
        return self.win_state[board_str]
