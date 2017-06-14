def theAStarer(self, problem):
    frontier = queue.PriorityQueue()
    closed_list = []
    c_node = HyperNode(problem.get_initial_state(), None, 0)
    frontier.put(c_node)
    problem.goal_test(c_node.current_state)
    # print(c_node.current_state.__str__())

    while not frontier.empty():
        c_node = frontier.get()
        # checking for the nodes that has been seen before
        if c_node.current_state in closed_list:
            continue
        closed_list.append(c_node.current_state)
        actions = problem.get_actions(c_node.current_state)

        for action in actions:
            # print("closed list: " + str(len(closed_list)))
            # print("frontier list: " + str(frontier.qsize()))
            next_state = problem.get_result_of_action(c_node.current_state, action)

            if next_state not in closed_list:
                # print(next_state.__str__() + "\n")
                if problem.goal_test(next_state):
                    print("closed list: " + str(len(closed_list)))
                    print("frontier list: " + str(frontier.qsize()))
                    self.print_statistics(HyperNode(next_state, c_node,
                                                    c_node.cost_until_now + problem.path_cost(c_node.current_state,
                                                                                              next_state)))
                    return
                frontier.put(
                    HyperNode(next_state, c_node,
                              c_node.cost_until_now + problem.path_cost(c_node.current_state,
                                                                        next_state)))
    return



class MetaNode:
    def __init__(self, c, p, cost_until_now):  # c:state, p:MetaNode, cost:Int
        self.current_state = c  # current state
        self.previous_node = p  # previous node
        self.cost_until_now = cost_until_now

    def __lt__(self, other):
        if self.cost_until_now < other.cost_until_now:
            return 1
        return 0


class HyperNode:
    def __init__(self, c, p, cost_until_now):  # c:state, p:MetaNode, cost:Int
        self.current_state = c  # current state
        self.previous_node = p  # previous node
        self.cost_until_now = cost_until_now

    def the_total_cost(self):
        return self.cost_until_now + self.current_state.the_heuristic_future_cost_speculator()

    def __lt__(self, other):
        if self.the_total_cost() < other.the_total_cost():
            return 1
        return 0





    def theDepthLimitedGraphDFSer(self, problem: SuperProblem, depth_limit):
        frontier = []
        closed_list = []
        c_node = MetaNode(problem.get_initial_state(), None, 0)
        frontier.append(c_node)
        problem.goal_test(c_node.current_state)
        # print(c_node.current_state.__str__())

        while len(frontier) != 0:
            c_node = frontier.pop(0)
            closed_list.append(c_node.current_state)
            if c_node.cost_until_now >= depth_limit:
                continue
            actions = problem.get_actions(c_node.current_state)

            for action in actions:
                # print("closed list: " + str(len(closed_list)))
                # print("frontier list: " + str(len(frontier)))
                next_state = problem.get_result_of_action(c_node.current_state, action)

                if next_state not in closed_list:
                    # print(next_state.__str__() + "\n")
                    if problem.goal_test(next_state):
                        print("closed list: " + str(len(closed_list)))
                        print("frontier list: " + str(len(frontier)))
                        self.print_statistics(MetaNode(next_state, c_node,
                                                       c_node.cost_until_now + problem.path_cost(c_node.current_state,
                                                                                                 next_state)))
                        return
                    frontier.append(
                        MetaNode(next_state, c_node,
                                 c_node.cost_until_now + problem.path_cost(c_node.current_state, next_state)))
        return