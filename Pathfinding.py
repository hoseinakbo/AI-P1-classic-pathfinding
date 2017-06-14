import PSA
import queue


class PathFindingState(PSA.State):
    def __init__(self, board_array):
        self.board_array = list(board_array)

    def __eq__(self, other):
        if len(self.board_array) != len(other.board_array):
            return False
        for i in range(0, len(self.board_array)):
            if self.board_array[i] != other.board_array[i]:
                return False
        return True

    def heuristic_to_goal(self):
        return 0


class PathFindingAction(PSA.Action):
    def __init__(self, first_num, second_num):
        self.first_num = first_num
        self.second_num = second_num


class PathFindingProblem(PSA.Problem):
    def get_initial_state(self):
        return PathFindingState([1, 6, 2, 5, 3, 9, 4, 7, 8])

    def get_final_state(self):
        return PathFindingState([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def get_actions(self, state):
        actions = []
        for i in range(0, len(state.board_array)):
            if state.board_array[i] == 9:
                if is_in_table(i - 3):
                    actions.append(PathFindingAction(i, i - 3))
                if i % 3 != 0:
                    if is_in_table(i - 1):
                        actions.append(PathFindingAction(i, i - 1))
                if i % 3 != 2:
                    if is_in_table(i + 1):
                        actions.append(PathFindingAction(i, i + 1))
                if is_in_table(i + 3):
                    actions.append(PathFindingAction(i, i + 3))
        return actions

    def get_result_of_action(self, action, state):
        new_state = PathFindingState(state.board_array)
        temp = new_state.board_array[action.first_num]
        new_state.board_array[action.first_num] = new_state.board_array[action.second_num]
        new_state.board_array[action.second_num] = temp
        return new_state

    def is_goal(self, state):
        if state.board_array == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False

    def get_cost(self, state1, state2, action):
        return 1


def is_in_table(i):
    if i < 0:
        return False
    if i > 8:
        return False
    return True
