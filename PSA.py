import queue
from random import randint


class Problem:
    def get_initial_state(self):
        pass

    def get_actions(self, state):
        pass

    def get_result_of_action(self, action, state):
        pass

    def is_goal(self, state):
        pass

    def get_cost(self, state1, state2, action):
        pass


class State:
    pass


class Action:
    pass


class Node:
    def __init__(self, current_state, parent_node, cost=0):
        self.current_state = current_state
        self.parent_node = parent_node
        self.cost = cost

    def __eq__(self, other):
        return self.current_state == other.current_state

    def __lt__(self, other):
        return 0


class HeuristicNode:
    def __init__(self, current_state, parent_node, cost=0):
        self.current_state = current_state
        self.parent_node = parent_node
        self.cost = cost

    def __eq__(self, other):
        return self.current_state == other.current_state

    def __lt__(self, other):
        if self.get_total_cost() < other.get_total_cost():
            return 1
        return 0

    def get_total_cost(self):
        return self.cost + self.current_state.heuristic_to_goal()


class PSA:
    def __init__(self, problem):
        self.problem = problem
        self.created_nodes = 0
        self.opened_nodes = 0
        self.most_nodes_open_at_once = 0

    # def final_result(self, node):
    #     return node.current_state.board_array

    def add_to_f_queue(self, node):
        num = 0
        for i in range(len(self.f_queue)):
            if self.f_queue[i].cost > node.cost:
                num = i
                break
        self.f_queue.insert(num, node)

    def bfs_tree_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                # print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    return result_state.board_array
                else:
                    self.f_queue.append(result_node)

    def bfs_graph_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            self.opened_nodes += 1
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                # result_node = Node(result_state, self.current_node)
                result_node = Node(result_state, self.current_node, self.current_node.cost + self.problem.get_cost(self.current_node.current_state, result_state, actions[i]))
                # print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if len(self.f_queue) > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = len(self.f_queue)
                if self.problem.is_goal(result_state):
                    return (result_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once, result_node.cost)
                else:
                    if result_node not in self.f_queue and result_node not in self.e_queue:
                        self.created_nodes += 1
                        self.f_queue.append(result_node)
            self.e_queue.append(self.current_node)

    def dfs_tree_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop()
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                # print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    # print("f_queue size: " + str(len(self.f_queue)))
                    return result_state.board_array
                else:
                    self.f_queue.append(result_node)

    def dfs_graph_search(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop()
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node)
                # print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if self.problem.is_goal(result_state):
                    return result_state.board_array
                else:
                    if result_node not in self.f_queue and result_node not in self.e_queue:
                        self.f_queue.append(result_node)
            self.e_queue.append(self.current_node)

    def uniform_cost_search(self):
        self.f_pqueue = queue.PriorityQueue()
        self.f_pqueue.put((0, Node(self.problem.get_initial_state(), None, 0)))
        self.e_queue = []

        while self.f_pqueue.qsize() != 0:
            self.current_node = self.f_pqueue.get()[1]
            self.opened_nodes += 1
            if self.current_node in self.e_queue:
                continue
            if self.problem.is_goal(self.current_node.current_state):
                return (
                    self.current_node.current_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once,
                    self.current_node.cost)
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_cost = self.current_node.cost + \
                              self.problem.get_cost(result_state, self.current_node.current_state, actions[i])
                # print("cost: " + str(result_cost))
                result_node = Node(result_state, self.current_node, result_cost)
                # print(str(result_state.board_array) + "   f_queue size: " + str(self.f_pqueue.qsize()))
                if self.f_pqueue.qsize() > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = self.f_pqueue.qsize()
                if result_node not in self.e_queue:
                    self.created_nodes += 1
                    self.f_pqueue.put((result_cost, result_node))
            self.e_queue.append(self.current_node)

    def uniform_cost_search_without_priority_queue(self):
        self.f_queue = [Node(self.problem.get_initial_state(), None)]
        self.e_queue = []

        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop(0)
            if self.problem.is_goal(self.current_node.current_state):
                return self.current_node.current_state.board_array
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_cost = self.current_node.cost + \
                              self.problem.get_cost(result_state, self.current_node.current_state, actions[i])
                print("cost: " + str(result_cost))
                result_node = Node(result_state, self.current_node, result_cost)
                # print(str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if result_node not in self.f_queue and result_node not in self.e_queue:
                    # self.f_queue.put((result_cost, result_node))
                    self.add_to_f_queue(result_node)
            self.e_queue.append(self.current_node)

    def bidirectional_graph_search(self):
        self.f_queue_1 = [Node(self.problem.get_initial_state(), None)]
        self.e_queue_1 = []
        self.f_queue_2 = [Node(self.problem.get_final_state(), None)]
        self.e_queue_2 = []
        while len(self.f_queue_1) != 0 and len(self.f_queue_2) != 0:
            self.current_node = self.f_queue_1.pop(0)
            self.opened_nodes += 1
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node, self.current_node.cost + self.problem.get_cost(self.current_node.current_state, result_state, actions[i]))
                # print(str(result_state.board_array) + "   f_queue_1 size: " + str(len(self.f_queue_1)))
                if len(self.f_queue_1)+len(self.f_queue_2) > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = len(self.f_queue_1)+len(self.f_queue_2)
                if self.problem.is_goal(result_state) or result_node in self.f_queue_2:
                    return (
                        result_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once,
                        result_node.cost)
                else:
                    if result_node not in self.f_queue_1 and result_node not in self.e_queue_1:
                        self.created_nodes += 1
                        self.f_queue_1.append(result_node)
            self.e_queue_1.append(self.current_node)

            self.current_node = self.f_queue_2.pop(0)
            self.opened_nodes += 1
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node, self.current_node.cost + self.problem.get_cost(self.current_node.current_state, result_state, actions[i]))
                # print(str(result_state.board_array) + "   f_queue_2 size: " + str(len(self.f_queue_2)))
                if len(self.f_queue_1) + len(self.f_queue_2) > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = len(self.f_queue_1) + len(self.f_queue_2)
                if self.problem.is_goal(result_state) or result_node in self.f_queue_1:
                    return (
                        result_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once,
                        result_node.cost)
                else:
                    if result_node not in self.f_queue_2 and result_node not in self.e_queue_2:
                        self.created_nodes += 1
                        self.f_queue_2.append(result_node)
            self.e_queue_2.append(self.current_node)

    def dfs_depth_limited(self, depth_limit):
        self.f_queue = [Node(self.problem.get_initial_state(), None, 0)]
        self.e_queue = []
        while len(self.f_queue) != 0:
            self.current_node = self.f_queue.pop()
            self.opened_nodes += 1
            if self.current_node.cost >= depth_limit:
                continue
            actions = self.problem.get_actions(self.current_node.current_state)
            for i in range(0, len(actions)):
                result_state = self.problem.get_result_of_action(actions[i], self.current_node.current_state)
                result_node = Node(result_state, self.current_node, self.current_node.cost + self.problem.get_cost(self.current_node.current_state, result_state, actions[i]))
                # print("Depth:" + str(depth_limit) + "  " + str(result_state.board_array) + "   f_queue size: " + str(len(self.f_queue)))
                if len(self.f_queue) > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = len(self.f_queue)
                if self.problem.is_goal(result_state):
                    return (
                    result_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once,
                    result_node.cost)
                else:
                    if result_node not in self.f_queue and result_node not in self.e_queue:
                        self.created_nodes  += 1
                        self.f_queue.append(result_node)
            self.e_queue.append(self.current_node)
        # print('No Result Found')
        return

    def dfs_iterative_deepening(self):
        for i in range(1, 99999999):
            res = self.dfs_depth_limited(i)
            if res is not None:
                # print('Result Found!')
                return res
    # def iterativeDeepeningSearch(startState, actionsF, takeActionF, goalTestF, maxDepth):
    #     for depth in range(maxDepth):
    #         result = depthLimitedSearchHelper(startState, actionsF, takeActionF, goalTestf, depth)
    #         if result is not "cutoff", then
    #         Add startState to front of solution path returned by depthLimitedSearchHelper
    #         return result
    # return "cutoff"


    def a_star_search(self):
        self.f_pqueue = queue.PriorityQueue()
        self.f_pqueue.put(HeuristicNode(self.problem.get_initial_state(), None, 0))
        self.e_queue = []

        while self.f_pqueue.qsize() != 0:
            self.current_node = self.f_pqueue.get()
            self.opened_nodes += 1
            if self.current_node in self.e_queue:
                continue
            self.e_queue.append(self.current_node)
            actions = self.problem.get_actions(self.current_node.current_state)

            for action in actions:
                result_state = self.problem.get_result_of_action(action, self.current_node.current_state)
                if self.f_pqueue.qsize() > self.most_nodes_open_at_once:
                    self.most_nodes_open_at_once = self.f_pqueue.qsize()
                if self.problem.is_goal(result_state):
                    return (result_state.board_array, self.created_nodes, self.opened_nodes, self.most_nodes_open_at_once,
                            self.current_node.cost + self.problem.get_cost(
                                self.current_node.current_state, result_state, action))
                self.created_nodes += 1
                self.f_pqueue.put(HeuristicNode(result_state, self.current_node,
                                                self.current_node.cost + self.problem.get_cost(
                                                    self.current_node.current_state, result_state, action)))
        return
