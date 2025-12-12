# ds/graph_algorithms.py
from __future__ import annotations
from typing import Dict, Generic, List, Optional, Sequence, Tuple, TypeVar
import heapq

T = TypeVar("T")
Weight = float

# Minimal Union-Find (Disjoint Set) for Kruskal
class UnionFind(Generic[T]):
    def __init__(self):
        self.parent: Dict[T, T] = {}
        self.rank: Dict[T, int] = {}

    def make(self, x: T) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x: T) -> T:
        # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: T, b: T) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True


# -------------------------
# Path reconstruction helper
# -------------------------
def reconstruct_path(parent: Dict[T, Optional[T]], src: T, dest: T) -> List[T]:
    """
    Reconstruct path from src to dest given a parent map (node -> parent).
    Returns list [src, ..., dest]; empty list if dest not reachable / parent missing.
    """
    if dest not in parent:
        return []
    path: List[T] = []
    cur = dest
    while cur is not None:
        path.append(cur)
        if cur == src:
            break
        cur = parent.get(cur)
    path.reverse()
    if path and path[0] == src:
        return path
    return []


# -------------------------
# Dijkstra wrapper with path
# -------------------------
def shortest_path_dijkstra(graph, src: T, dest: Optional[T] = None) -> Tuple[Dict[T, Weight], Dict[T, Optional[T]]]:
    """
    Runs Dijkstra on `graph` (must support graph.neighbors(u) -> List[(v, weight)]).
    If graph.weighted is False, edges are treated as weight 1.
    Returns (distances, parent). Use reconstruct_path(parent, src, dest) to get path.
    """
    # delegate to Graph.dijkstra if available
    if hasattr(graph, "dijkstra"):
        dist, parent = graph.dijkstra(src)
        return dist, parent

    # Generic implementation
    dist: Dict[T, Weight] = {}
    parent: Dict[T, Optional[T]] = {}
    pq: List[Tuple[Weight, T]] = []
    heapq.heappush(pq, (0.0, src))
    dist[src] = 0.0
    parent[src] = None
    weighted = getattr(graph, "weighted", True)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if dest is not None and u == dest:
            break
        for v, w in graph.neighbors(u):
            wt = w if weighted else 1.0
            nd = d + wt
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent


# -------------------------
# Bellman-Ford wrapper with path (supports negative weights)
# -------------------------
def shortest_path_bellman_ford(graph, src: T) -> Tuple[Dict[T, Weight], Dict[T, Optional[T]]]:
    """
    Returns (dist, parent). Raises ValueError on negative cycle.
    """
    # delegate if exists
    if hasattr(graph, "bellman_ford"):
        return graph.bellman_ford(src)

    nodes = list(getattr(graph, "_nodes", []))
    dist: Dict[T, Weight] = {u: float("inf") for u in nodes}
    parent: Dict[T, Optional[T]] = {u: None for u in nodes}
    dist[src] = 0.0
    weighted = getattr(graph, "weighted", True)

    for _ in range(len(nodes) - 1):
        changed = False
        for u in nodes:
            for v, w in graph.neighbors(u):
                wt = w if weighted else 1.0
                if dist[u] + wt < dist[v]:
                    dist[v] = dist[u] + wt
                    parent[v] = u
                    changed = True
        if not changed:
            break

    # check negative cycles
    for u in nodes:
        for v, w in graph.neighbors(u):
            wt = w if weighted else 1.0
            if dist[u] + wt < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")
    # filter unreachable
    return {k: v for k, v in dist.items() if v != float("inf")}, parent


# -------------------------
# Prim's algorithm (MST)
# -------------------------
def prim_mst(graph, start: Optional[T] = None) -> Tuple[float, List[Tuple[T, T, Weight]]]:
    """
    Prim's algorithm for MST on undirected weighted graph.
    Returns (total_weight, edges_list) where edges_list is [(u,v,w), ...] chosen by Prim.
    Raises ValueError if graph is directed.
    """
    if getattr(graph, "directed", False):
        raise ValueError("Prim's algorithm requires undirected graph")
    nodes = list(getattr(graph, "_nodes", []))
    if not nodes:
        return 0.0, []

    if start is None:
        start = nodes[0]

    visited = set()
    pq: List[Tuple[Weight, T, T]] = []  # (weight, from, to)
    total = 0.0
    mst_edges: List[Tuple[T, T, Weight]] = []

    def push_edges(u: T):
        visited.add(u)
        for v, w in graph.neighbors(u):
            if v not in visited:
                heapq.heappush(pq, (w if getattr(graph, "weighted", True) else 1.0, u, v))

    push_edges(start)
    while pq and len(visited) < len(nodes):
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        total += w
        mst_edges.append((u, v, w))
        push_edges(v)

    if len(visited) != len(nodes):
        # Graph not connected -> no spanning tree covering all nodes
        raise ValueError("Graph is not connected; MST not possible for whole graph")
    return total, mst_edges


# -------------------------
# Kruskal's algorithm (MST)
# -------------------------
def kruskal_mst(graph) -> Tuple[float, List[Tuple[T, T, Weight]]]:
    """
    Kruskal's algorithm: returns (total_weight, edges_list). Works on undirected graphs.
    """
    if getattr(graph, "directed", False):
        raise ValueError("Kruskal requires undirected graph")
    uf = UnionFind[T]()
    edges: List[Tuple[Weight, T, T]] = []
    nodes = list(getattr(graph, "_nodes", []))
    for u in nodes:
        uf.make(u)
    # gather edges uniquely for undirected graphs
    seen = set()
    for u in nodes:
        for v, w in graph.neighbors(u):
            if (v, u) in seen or (u, v) in seen:
                continue
            seen.add((u, v))
            edges.append((w if getattr(graph, "weighted", True) else 1.0, u, v))
    edges.sort(key=lambda x: x[0])
    mst: List[Tuple[T, T, Weight]] = []
    total = 0.0
    for w, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, w))
            total += w
    # Check if MST spans all nodes
    roots = {uf.find(x) for x in nodes}
    if len(roots) > 1:
        raise ValueError("Graph not connected; MST not possible for whole graph")
    return total, mst


# -------------------------
# Directed-cycle detection + return cycle path
# -------------------------
def detect_cycle_directed(graph) -> Optional[List[T]]:
    """
    Detect a cycle in directed graph and return one cycle path (list of nodes in cycle).
    Returns None if no cycle.
    DFS with colors and parent tracking.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[T, int] = {}
    parent: Dict[T, Optional[T]] = {}

    nodes = list(getattr(graph, "_nodes", []))
    for u in nodes:
        color[u] = WHITE
        parent[u] = None

    cycle: List[T] = []

    def dfs(u: T) -> bool:
        color[u] = GRAY
        for v, _ in graph.neighbors(u):
            if color.get(v, WHITE) == WHITE:
                parent[v] = u
                if dfs(v):
                    return True
            elif color.get(v) == GRAY:
                # found back edge u->v; reconstruct cycle
                cur = u
                cycle.append(v)
                while cur != v and cur is not None:
                    cycle.append(cur)
                    cur = parent.get(cur)
                cycle.reverse()
                return True
        color[u] = BLACK
        return False

    for u in nodes:
        if color[u] == WHITE:
            if dfs(u):
                return cycle
    return None


# -------------------------
# Strongly Connected Components (Kosaraju)
# -------------------------
def strongly_connected_components(graph) -> List[List[T]]:
    """
    Kosaraju algorithm: return list of SCCs (each SCC is a list of nodes).
    """
    nodes = list(getattr(graph, "_nodes", []))

    visited = set()
    order: List[T] = []

    def dfs1(u: T):
        visited.add(u)
        for v, _ in graph.neighbors(u):
            if v not in visited:
                dfs1(v)
        order.append(u)

    for u in nodes:
        if u not in visited:
            dfs1(u)

    # build transpose adjacency fast if graph doesn't have reverse neighbor method
    transpose_adj: Dict[T, List[T]] = {u: [] for u in nodes}
    for u in nodes:
        for v, _ in graph.neighbors(u):
            transpose_adj[v].append(u)

    visited.clear()
    sccs: List[List[T]] = []

    def dfs2(u: T, comp: List[T]):
        visited.add(u)
        comp.append(u)
        for v in transpose_adj.get(u, []):
            if v not in visited:
                dfs2(v, comp)

    for u in reversed(order):
        if u not in visited:
            comp: List[T] = []
            dfs2(u, comp)
            sccs.append(comp)
    return sccs
