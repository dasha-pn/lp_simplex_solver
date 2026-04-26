from typing import List, Tuple
from solver import Solver
from enums import LpSign, LpFunc, LpStatus

def solve_mfmc_custom_lp(graph: List[List[Tuple[int, int, int]]]) -> Tuple[float, float]:
    n = len(graph)
    
    edges = []
    for u in range(n):
        for v, cap, cost in graph[u]:
            edges.append((u, v, cap, cost))
            
    E = len(edges)

    solver = Solver(E + 1)

    M_val = 1e8

    obj_coefs = [0.0] * (E + 1)
    for i in range(E):
        obj_coefs[i] = -float(edges[i][3])
    obj_coefs[E] = M_val
    
    solver.set_objective(obj_coefs, LpFunc.MAXIMIZE)

    for i in range(E):
        c = [0.0] * (E + 1)
        c[i] = 1.0
        solver.add_constraint(c, float(edges[i][2]), LpSign.LESS_OR_EQUAL)

    for node in range(n):
        c = [0.0] * (E + 1)
        for i, (u, v, _, _) in enumerate(edges):
            if v == node: c[i] = 1.0
            if u == node: c[i] = -1.0
                
        if node == 0:
            c[E] = 1.0
        elif node == n - 1:
            c[E] = -1.0
            
        solver.add_constraint(c, 0.0, LpSign.EQUAL)
        
    status = solver.solve(max_iters=1000000)
    
    if status != LpStatus.OPTIMAL:
        raise RuntimeError(f"Custom solver failed with status: {status}")
        
    max_flow = solver.get_var_value(E)
    min_cost = sum(solver.get_var_value(i) * edges[i][3] for i in range(E))

    return max_flow, min_cost
