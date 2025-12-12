# bellman_ford_algorithm


A [algorithm](mathematics/algorithm) that computes shortest [paths](mathematics/path) from a single source 
[node](mathematics/node) to all other nodes in a weighted [graph](mathematics/graph). The algorithm iteratively 
relaxes all [edges](mathematics/edge) by updating [distances](mathematics/graph_distance) if a 
shorter path is found, repeating this process for each node in the graph. Unlike 
[Dijkstra's algorithm](mathematics/dijkstras_algorithm), Bellman-Ford can handle negative edge weights and 
can detect negative-weight [cycles](mathematics/cycle), making it more versatile for certain applications.

