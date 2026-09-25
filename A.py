
from heapq import heappush, heappop

def astar(g, s, goal, h):
    q = [(0 + h[s], 0, s, [s])]
    while q:
        f, cost, node, path = heappop(q)
        if node == goal:
            return path, cost
        for n, c in g[node]:
            new_cost = cost + c
            heappush(q, (new_cost + h[n], new_cost, n, path + [n]))
    return None, float('inf')

# Graph
g = {
    'S': [('A', 1), ('B', 4)],
    'A': [('B', 2), ('C', 5)],
    'B': [('C', 1)],
    'C': []
}

# Heuristic
h = {'S': 7, 'A': 6, 'B': 2, 'C': 0}

path, cost = astar(g, 'S', 'C', h)
print("Path:", path)
print("Cost:", cost)
