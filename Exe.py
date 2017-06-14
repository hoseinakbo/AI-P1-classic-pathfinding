import PSA
import Pathfinding


b = PSA.PSA(Pathfinding.PathFindingProblem())
a = b.bfs_graph_search()
print('BFS: ', 'Final Result: ', a[0], '  created_nodes: ', a[1], '  opened_nodes: ', a[2], '  most_nodes_open_at_once: ', a[3], '  path_cost: ', a[4])

b = PSA.PSA(Pathfinding.PathFindingProblem())
a = b.dfs_iterative_deepening()
print('Iterative Deepening DFS: ', 'Final Result: ', a[0], '  created_nodes: ', a[1], '  opened_nodes: ', a[2], '  most_nodes_open_at_once: ', a[3], '  path_cost: ', a[4])

b = PSA.PSA(Pathfinding.PathFindingProblem())
a = b.bidirectional_graph_search()
print('Bidirectional: ', 'Final Result: ', a[0], '  created_nodes: ', a[1], '  opened_nodes: ', a[2], '  most_nodes_open_at_once: ', a[3], '  path_cost: ', a[4])

b = PSA.PSA(Pathfinding.PathFindingProblem())
a = b.uniform_cost_search()
print('Uniform Cost: ', 'Final Result: ', a[0], '  created_nodes: ', a[1], '  opened_nodes: ', a[2], '  most_nodes_open_at_once: ', a[3], '  path_cost: ', a[4])

b = PSA.PSA(Pathfinding.PathFindingProblem())
a = b.a_star_search()
print('A*: ', 'Final Result: ', a[0], '  created_nodes: ', a[1], '  opened_nodes: ', a[2], '  most_nodes_open_at_once: ', a[3], '  path_cost: ', a[4])

