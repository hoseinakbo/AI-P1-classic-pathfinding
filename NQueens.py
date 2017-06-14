import PSA
import queue


class NQueensState(PSA.State):
    def __init__(self, board_array):
        self.board_array = list(board_array)

    def __eq__(self, other):
        if len(self.board_array) != len(other.board_array):
            return False
        for i in range(0, len(self.board_array)):
            if self.board_array[i] != other.board_array[i]:
                return False
        return True


class NQueensAction(PSA.Action):
    def __init__(self, first_num, second_num):
        self.first_num = first_num
        self.second_num = second_num


class NQueensProblem(PSA.Problem):
    def get_initial_state(self):
        return NQueensState([0, 1, 2, 3, 4, 5, 6, 7])
        # return NQueensState([0, 1, 2, 3])

    def get_actions(self, state):
        actions = []
        for i in range(0, len(state.board_array)-1):
            for j in range(i+1, len(state.board_array)):
                actions.append(NQueensAction(i, j))
        return actions

    def get_result_of_action(self, action, state):
        new_state = NQueensState(state.board_array)
        temp = new_state.board_array[action.first_num]
        new_state.board_array[action.first_num] = new_state.board_array[action.second_num]
        new_state.board_array[action.second_num] = temp
        return new_state

    def is_goal(self, state):
        for i in range(0, len(state.board_array)-1):
            for j in range(i+1, len(state.board_array)):
                # if i != j and abs(state.board_array[i] - state.board_array[j]) == abs(i - j):
                if has_conflict(i, state.board_array[i], j, state.board_array[j]):
                    return False
        return True

    def get_cost(self, state1, state2, action):
        return 1


def has_conflict(column1, row1, column2, row2):
    if column1 == column2 or row1 == row2:
        return True
    if abs(column1 - column2) == abs(row1 - row2):
        return True
    return False


b = PSA.PSA(NQueensProblem())
a = b.dfs_graph_search()
print("Final Result: " + str(a))


