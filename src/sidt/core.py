from __future__ import annotations
import math
import numpy as np
import networkx as nx

def gf2_rank(A):
    A = np.array(A, dtype=np.uint8).copy() & 1
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r,m) if A[i,c]), None)
        if piv is None:
            continue
        A[[r,piv]] = A[[piv,r]]
        for i in range(m):
            if i != r and A[i,c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return int(r)

def affine_sid(A, n=None):
    A = np.array(A, dtype=np.uint8)
    if n is None:
        n = A.shape[1]
    return int(n - gf2_rank(A))

def locality_lower_bound(n, supports):
    U = set()
    for s in supports:
        U |= set(s)
    return int(n - len(U))

def collapse_budget_lower_bound(n, alphabet_bits):
    return int(max(0, n - sum(alphabet_bits)))

def interaction_graph(n, supports):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for s in supports:
        ss = list(s)
        for i in range(len(ss)):
            for j in range(i+1,len(ss)):
                G.add_edge(ss[i], ss[j])
    return G

def approx_treewidth(n, supports):
    G = interaction_graph(n, supports)
    if G.number_of_edges() == 0:
        return 0
    tw, _ = nx.algorithms.approximation.treewidth_min_fill_in(G)
    return int(tw)

def exact_residual_count(n, constraints):
    count = 0
    for x in range(1 << n):
        if all(f(x) for f in constraints):
            count += 1
    return count

def sid_from_count(count):
    if count <= 0:
        return None
    return math.log2(count)
