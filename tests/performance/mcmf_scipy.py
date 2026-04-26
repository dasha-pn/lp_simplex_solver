import numpy as np
import warnings
from scipy.optimize import linprog, OptimizeWarning
from typing import List, Tuple

warnings.filterwarnings("ignore", category=OptimizeWarning)

def solve_mfmc_scipy(graph: List[List[Tuple[int, int, int]]]) -> Tuple[float, float]:
    n = len(graph)
    
    edges = []
    for u in range(n):
        for v, cap, cost in graph[u]:
            edges.append((u, v, cap, cost))
            
    E = len(edges)
    
    total_vars = E + 1

    M_val = 1e8
    c = np.zeros(total_vars)
    for i in range(E):
        c[i] = edges[i][3]
    c[E] = -M_val

    A_eq = np.zeros((n, total_vars))
    b_eq = np.zeros(n)
    
    for i, (u, v, _, _) in enumerate(edges):
        A_eq[u, i] = -1.0
        A_eq[v, i] =  1.0 
        
    A_eq[n - 1, E] = -1.0
    A_eq[0, E] = 1.0
    
    bounds = []
    for i in range(E):
        bounds.append((0, edges[i][2]))
    
    bounds.append((0, None))

    res = linprog(
        c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="revised simplex",
        options={
            "presolve": False,
            "parallel": False
        }
    )
    
    if not res.success:
        raise RuntimeError(f"SciPy failed to find optimal solution: {res.message}")
        
    max_flow = res.x[E]
    min_cost = sum(res.x[i] * edges[i][3] for i in range(E))
    
    return float(max_flow), float(min_cost)
