from collections import deque
import sys

from typing import Dict, List, Set, Tuple

def count_orbits(graph: Dict[str,Set[str]], target) -> int:
    if target not in graph:
        return 0
    direct_orbits = len(graph[target])
    indirect_orbits = [count_orbits(graph,t) for t in graph[target]]
    return direct_orbits + sum(indirect_orbits)

def build_directed_graph(pairs: List[Tuple[str,str]]) -> Dict[str,Set[str]]:
    graph = dict()
    for a, b in pairs:
        if b in graph:
            graph[b].add(a)
        else:
            graph[b] = set([a])

    return graph

def build_undirected_graph(pairs: List[Tuple[str,str]]) -> Dict[str,Set[str]]:
    graph = dict()
    for a, b in pairs:
        if a in graph:
            graph[a].add(b)
        else:
            graph[a] = set([b])
        if b in graph:
            graph[b].add(a)
        else:
            graph[b] = set([a])

    return graph

def breadth_first_distance(graph: Dict[str,Set[str]], src: str, dest: str) -> int:
    visited_distances = {src: 0}
    visit_queue = deque([src])
    while len(visit_queue) > 0:
        current_node = visit_queue.popleft()
        if current_node == dest:
            return visited_distances[current_node]
        for next_node in graph[current_node]:
            if next_node not in visited_distances:
                visited_distances[next_node] = visited_distances[current_node] + 1
                visit_queue.append(next_node)

    return visited_distances[dest]

assert len(sys.argv) > 1
raw_map = []
with open(sys.argv[1]) as f:
    raw_map = f.read().strip().split('\n')

orbit_pairs = [tuple(entry.split(')')) for entry in raw_map]

directed_orbit_graph = build_directed_graph(orbit_pairs)
undirected_orbit_graph = build_undirected_graph(orbit_pairs)

total_orbits = sum([count_orbits(directed_orbit_graph,key) for key in directed_orbit_graph.keys()])
print("Total orbits: {}".format(total_orbits))

src = directed_orbit_graph['YOU'].pop()
dest = directed_orbit_graph['SAN'].pop()
transfers = breadth_first_distance(undirected_orbit_graph, src, dest)
print("Transfers from YOU to SAN: {}".format(transfers))
