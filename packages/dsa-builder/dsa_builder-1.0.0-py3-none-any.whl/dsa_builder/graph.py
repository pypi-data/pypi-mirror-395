# ds/graph.py
from __future__ import annotations
from typing import Dict, Generic, Iterable, Iterator, List, Optional, Tuple, TypeVar
from collections import deque, defaultdict
import heapq

T = TypeVar("T")
Weight = float
Edge = Tuple[T, T]            # (u, v)
WeightedEdge = Tuple[T, T, Weight]  # (u, v, w)


class Graph(Generic[T]):
    """
    Adjacency-list graph.
    - directed: if True, edges are directed (u->v). If False, edges are undirected.
    - weighted: if True, edges carry weights (float). If False, weight is ignored.
    """

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self.directed = directed
        self.weighted = weighted
        # adjacency: node -> list of (neighbor, weight) (weight ignored if not weighted)
        self._adj: Dict[T, List[Tuple[T, Weight]]] = defaultdict(list)
        self._nodes: set[T] = set()

    # ---------- construction ----------
    def add_node(self, node: T) -> None:
        self._nodes.add(node)
        self._adj.setdefault(node, [])

    def add_edge(self, u: T, v: T, w: Weight = 1.0) -> None:
        """Add edge u->v (or undirected both ways)."""
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, w))
        if not self.directed:
            self._adj[v].append((u, w))

    def nodes(self) -> List[T]:
        return list(self._nodes)

    def edges(self) -> List[WeightedEdge]:
        out: List[WeightedEdge] = []
        for u, nbrs in self._adj.items():
            for v, w in nbrs:
                if self.directed:
                    out.append((u, v, w))
                else:
                    # For undirected, include each edge once: u <= v by ordering
                    if u <= v:
                        out.append((u, v, w))
        return out

    def neighbors(self, u: T) -> List[Tuple[T, Weight]]:
        return list(self._adj.get(u, []))

    # ---------- utilities ----------
    def to_adj_list(self) -> Dict[T, List[Tuple[T, Weight]]]:
        return {u: list(nbrs) for u, nbrs in self._adj.items()}

    def to_adj_matrix(self) -> Tuple[List[T], List[List[Optional[Weight]]]]:
        """
        Return (nodes_order, matrix) where matrix[i][j] is weight or None if no edge.
        Node order is deterministic: sorted(nodes) if nodes comparable, otherwise insertion order.
        """
        nodes = list(self._nodes)
        idx = {node: i for i, node in enumerate(nodes)}
        n = len(nodes)
        mat: List[List[Optional[Weight]]] = [[None] * n for _ in range(n)]
        for u in nodes:
            for v, w in self._adj.get(u, []):
                mat[idx[u]][idx[v]] = w
        return nodes, mat

    # ---------- BFS ----------
    def bfs(self, start: T) -> Tuple[Dict[T, int], Dict[T, Optional[T]]]:
        """
        Breadth-first search (unweighted distances).
        Returns (distances, parents) where distance is number of edges from start.
        Unvisited nodes are absent from distances.
        """
        dist: Dict[T, int] = {}
        parent: Dict[T, Optional[T]] = {}
        q = deque([start])
        dist[start] = 0
        parent[start] = None
        while q:
            u = q.popleft()
            for v, _ in self._adj.get(u, []):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
        return dist, parent

    # ---------- DFS ----------
    def dfs(self, start: Optional[T] = None) -> Tuple[List[T], Dict[T, int], Dict[T, int]]:
        """
        Depth-first-search.
        If start is None, runs full-graph DFS (may produce forest) in arbitrary node order.
        Returns (order, discovery_time, finish_time)
        - order: nodes in order they were first discovered
        - discovery_time/finish_time map nodes -> timestamps (1-based)
        """
        visited = set()
        disc: Dict[T, int] = {}
        fin: Dict[T, int] = {}
        order: List[T] = []
        time = 0

        def _visit(u: T):
            nonlocal time
            visited.add(u)
            time += 1
            disc[u] = time
            order.append(u)
            for v, _ in self._adj.get(u, []):
                if v not in visited:
                    _visit(v)
            time += 1
            fin[u] = time

        nodes_iter = [start] if start is not None else list(self._nodes)
        for node in nodes_iter:
            if node is None:
                continue
            if node not in visited:
                _visit(node)
        # If start provided, we may still want to visit other nodes for full map:
        if start is not None:
            for node in self._nodes:
                if node not in visited:
                    _visit(node)
        return order, disc, fin

    # ---------- Connected components (undirected) ----------
    def connected_components(self) -> List[List[T]]:
        """
        For undirected graphs: list of connected components as lists of nodes.
        For directed graphs, this returns weakly-connected components (ignores direction).
        """
        seen = set()
        comps: List[List[T]] = []
        for node in self._nodes:
            if node in seen:
                continue
            comp = []
            q = deque([node])
            seen.add(node)
            while q:
                u = q.popleft()
                comp.append(u)
                for v, _ in self._adj.get(u, []):
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
                # for directed graphs we should also walk reverse edges to get weak components:
                if self.directed:
                    # walk reverse neighbors
                    for x, nbrs in self._adj.items():
                        for y, _ in nbrs:
                            if y == u and x not in seen:
                                seen.add(x)
                                q.append(x)
            comps.append(comp)
        return comps

    # ---------- Topological sort ----------
    def topological_sort(self) -> List[T]:
        """
        Kahn's algorithm. Raises ValueError if cycle detected.
        Works only for directed acyclic graphs (DAGs).
        """
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph")

        indeg: Dict[T, int] = {u: 0 for u in self._nodes}
        for u in self._nodes:
            for v, _ in self._adj.get(u, []):
                indeg[v] = indeg.get(v, 0) + 1

        q = deque([u for u, d in indeg.items() if d == 0])
        out: List[T] = []
        while q:
            u = q.popleft()
            out.append(u)
            for v, _ in self._adj.get(u, []):
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        if len(out) != len(self._nodes):
            raise ValueError("Graph has at least one cycle; topological order not possible")
        return out

    # ---------- Shortest paths ----------
    def dijkstra(self, src: T) -> Tuple[Dict[T, Weight], Dict[T, Optional[T]]]:
        """
        Dijkstra's algorithm for non-negative weights. Returns (distances, parents).
        Distances for unreachable nodes are absent.
        """
        if not self.weighted:
            # For unweighted, BFS gives shortest paths in edges; still works if weights assumed 1.
            # We'll still run Dijkstra treating w as 1 for neighbors.
            pass

        dist: Dict[T, Weight] = {}
        parent: Dict[T, Optional[T]] = {}
        pq: List[Tuple[Weight, T]] = []
        heapq.heappush(pq, (0.0, src))
        dist[src] = 0.0
        parent[src] = None

        while pq:
            d, u = heapq.heappop(pq)
            # stale entry
            if d > dist.get(u, float("inf")):
                continue
            for v, w in self._adj.get(u, []):
                # treat w as float; if graph not weighted, w may be default 1
                nd = d + (w if self.weighted else 1.0)
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, parent

    def bellman_ford(self, src: T) -> Tuple[Dict[T, Weight], Dict[T, Optional[T]]]:
        """
        Bellman-Ford: supports negative weights; will raise ValueError on negative cycle.
        O(V * E)
        """
        dist: Dict[T, Weight] = {u: float("inf") for u in self._nodes}
        parent: Dict[T, Optional[T]] = {u: None for u in self._nodes}
        dist[src] = 0.0

        for _ in range(len(self._nodes) - 1):
            changed = False
            for u in self._nodes:
                for v, w in self._adj.get(u, []):
                    if dist[u] + (w if self.weighted else 1.0) < dist[v]:
                        dist[v] = dist[u] + (w if self.weighted else 1.0)
                        parent[v] = u
                        changed = True
            if not changed:
                break

        # check negative cycle
        for u in self._nodes:
            for v, w in self._adj.get(u, []):
                if dist[u] + (w if self.weighted else 1.0) < dist[v]:
                    raise ValueError("Graph contains a negative-weight cycle")
        # remove unreachable infinities
        return {k: v for k, v in dist.items() if v != float("inf")}, parent
