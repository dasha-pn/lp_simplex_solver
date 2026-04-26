import random
from typing import List, Tuple

def generate_hard_mfmc_graph(
    n: int, 
    sparsity: float, 
    max_edge_cost: int, 
    max_capacity: int
) -> List[List[Tuple[int, int, int]]]:
    if n < 2:
        raise ValueError("Graph must have at least 2 vertices (source and sink).")

    forward_max_cost = max(2, int(max_edge_cost * 0.05))
    spine_min_cost = max(forward_max_cost + 1, int(max_edge_cost * 0.1))
    spine_max_cost = max(spine_min_cost + 1, int(max_edge_cost * 0.2))
    back_min_cost = max(spine_max_cost + 1, int(max_edge_cost * 0.5))
    
    forward_min_cap = max(2, int(max_capacity * 0.2))
    spine_max_cap = max(2, int(max_capacity * 0.05))
    back_max_cap = max(2, int(max_capacity * 0.1))
        
    graph: List[List[Tuple[int, int, int]]] = [[] for _ in range(n)]
    
    target_m = max(n - 1, int(n * sparsity))
    existing_edges = set()
    
    for i in range(n - 1):
        cap = random.randint(1, spine_max_cap)
        cost = random.randint(spine_min_cost, spine_max_cost)
        graph[i].append((i + 1, cap, cost))
        existing_edges.add((i, i + 1))
        
    current_m = n - 1
    
    attempts = 0
    max_attempts = target_m * 10
    
    while current_m < target_m and attempts < max_attempts:
        attempts += 1
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u == v or v == 0 or u == n - 1:
            continue
            
        if (u, v) in existing_edges:
            continue
            
        if u < v:
            cap = random.randint(forward_min_cap, max_capacity)
            cost = random.randint(1, forward_max_cost) 
        else:
            cap = random.randint(1, back_max_cap)
            cost = random.randint(back_min_cost, max_edge_cost) 
            
        graph[u].append((v, cap, cost))
        existing_edges.add((u, v))
        current_m += 1
        
    return graph
