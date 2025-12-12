# A-star algorithm


The [A-star algorithm](mathematics/A-star algorithm) is a [greedy](mathematics/greedy_algorithm) 
[algorithm](mathematics/algorithm) that finds the shortest [path](mathematics/path) between two 
[nodes](mathematics/node) in a weighted [graph](mathematics/graph). It extends 
[Dijkstra's algorithm](mathematics/dijkstras_algorithm) by using a [heuristic function](mathematics/heuristic) 
to estimate the [distance](mathematics/graph_distance) from the current node to the goal node, 
allowing it to prioritize more promising paths and find the shortest path more efficiently. 
The algorithm maintains two costs: the actual cost from the start node (g-score) and the estimated 
total cost through the current node to the goal (f-score = g-score + heuristic). 
It requires the heuristic to be admissible (never overestimating the actual cost) to guarantee 
finding the optimal path.

