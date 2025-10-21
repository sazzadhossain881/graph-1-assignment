from collections import deque, defaultdict
import copy
import pprint

class GraphFlow:
    def __init__(self, is_directed=True):
        self.graph = defaultdict(dict)
        self.is_directed = is_directed

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        if not self.is_directed:
            self.graph[v][u] = capacity

    def bfs(self, residual, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in residual[u]:
                if v not in visited and residual[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def max_flow(self, source, sink, visualize=False):
        residual = copy.deepcopy(self.graph)
        parent = {}
        max_flow = 0
        step = 0

        while self.bfs(residual, source, sink, parent):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, residual[parent[s]][s])
                s = parent[s]

            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= path_flow
                if v not in residual:
                    residual[v] = {}
                residual[v][u] = residual[v].get(u, 0) + path_flow
                v = parent[v]

            max_flow += path_flow
            step += 1
            if visualize:
                print(f"\n Residual Graph after augmentation {step} (flow = {path_flow}):")
                pprint.pprint(dict(residual))

        return max_flow

g1 = GraphFlow(is_directed=True)
g1.add_edge('S', 'A', 10)
g1.add_edge('S', 'C', 10)
g1.add_edge('A', 'B', 4)
g1.add_edge('A', 'C', 2)
g1.add_edge('C', 'D', 9)
g1.add_edge('D', 'B', 6)
g1.add_edge('B', 'T', 10)
g1.add_edge('D', 'T', 10)

print("\n Max Flow (Directed):", g1.max_flow('S', 'T', visualize=True))


g2 = GraphFlow(is_directed=False)
g2.add_edge('S', 'A', 3)
g2.add_edge('A', 'B', 4)
g2.add_edge('B', 'T', 2)

print("\n Max Flow (Undirected):", g2.max_flow('S', 'T', visualize=True))

g_empty = GraphFlow()
print("\n Max Flow (Empty Graph):", g_empty.max_flow('A', 'B'))

g_single = GraphFlow()
g_single.add_edge('A', 'A', 5)
print("\n Max Flow (Single Node):", g_single.max_flow('A', 'A'))

g_disconnected = GraphFlow()
g_disconnected.add_edge('A', 'B', 3)
print("\n Max Flow (Disconnected Sink):", g_disconnected.max_flow('A', 'C'))
