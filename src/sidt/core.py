from __future__ import annotations
import math
import numpy as np
import networkx as nx

def gf2_rank(A):
    A = np.asarray(A, dtype=np.uint8).copy() & 1
    if A.ndim != 2:
        raise ValueError("A must be a 2D binary matrix")
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i, c]), None)
        if pivot is None:
            continue
        if pivot != r:
            A[[r, pivot]] = A[[pivot, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return int(r)

def affine_sid(A):
    A = np.asarray(A, dtype=np.uint8)
    return int(A.shape[1] - gf2_rank(A))

def locality_lower_bound(n, supports):
    touched = set()
    for s in supports:
        touched.update(int(x) for x in s)
    return int(n - len(touched))

def domain_collapse_lower_bound(n, transcript_bits):
    return int(max(0, n - int(sum(transcript_bits))))

def interaction_graph(n, supports):
    G = nx.Graph(); G.add_nodes_from(range(int(n)))
    for s in supports:
        s = sorted(set(int(x) for x in s))
        for i, u in enumerate(s):
            for v in s[i+1:]:
                G.add_edge(u, v)
    return G

def approx_treewidth(n, supports):
    G = interaction_graph(n, supports)
    if G.number_of_edges() == 0:
        return 0
    w, _ = nx.algorithms.approximation.treewidth_min_fill_in(G)
    return int(w)

def exact_solution_count(n, predicate):
    return sum(1 for x in range(1 << int(n)) if predicate(x))

def sid_from_count(count):
    if count < 1:
        return float("nan")
    return float(math.log2(count))
