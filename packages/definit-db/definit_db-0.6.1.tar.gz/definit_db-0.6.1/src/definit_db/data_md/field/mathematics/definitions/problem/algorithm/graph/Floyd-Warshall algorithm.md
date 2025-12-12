# Floyd-Warshall algorithm


The [Floyd-Warshall algorithm](mathematics/Floyd-Warshall algorithm) is an [algorithm](mathematics/algorithm) that finds the shortest 
[paths](mathematics/path) between all pairs of [nodes](mathematics/node) in a weighted 
[graph](mathematics/graph). The algorithm uses [dynamic programming](mathematics/dynamic_programming) 
by iteratively considering each node as an intermediate node and updating the 
[distances](mathematics/graph_distance) between all pairs of nodes if a shorter path through 
the intermediate node is found. It can handle negative [edge](mathematics/edge) weights but 
cannot handle negative-weight [cycles](mathematics/cycle). The algorithm has a [time complexity](mathematics/time_complexity) 
of O(V³) where V is the number of nodes, making it efficient for dense graphs or when all-pairs shortest paths are needed.

