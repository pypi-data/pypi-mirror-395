# # graph.py

import heapq
from collections import deque


# ---------------------------
# DIJKSTRA (Already Correct)
# ---------------------------
import heapq

def dijkstra_shortest_path(adj, start):
    dist = {n: float("inf") for n in adj}
    prev = {n: None for n in adj}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in adj.get(u, []):  # v is just an int
            nd = d + 1            # default weight = 1
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev



# ----------------------------------------------------------
# FIXED BFS — SUPPORTS BOTH WEIGHTED AND UNWEIGHTED GRAPHS
# ----------------------------------------------------------
def bfs_distance(adj, start):
    from collections import deque
    q = deque([start])
    dist = {start: 0}
    visited = {start}
    while q:
        u = q.popleft()
        for v in adj.get(u, []):  # v is just an int
            if v not in visited:
                visited.add(v)
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

