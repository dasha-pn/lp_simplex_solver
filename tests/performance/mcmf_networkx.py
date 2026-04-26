from typing import List, Tuple
import networkx as nx

def solve_mfmc_networkx(graph: List[List[Tuple[int, int, int]]]) -> Tuple[float, float]:
    n = len(graph)
    
    G = nx.DiGraph()
    for u in range(n):
        for v, cap, cost in graph[u]:
            G.add_edge(u, v, capacity=cap, weight=cost)

    flow_dict = nx.max_flow_min_cost(G, 0, n - 1)
    
    min_cost = nx.cost_of_flow(G, flow_dict)
    
    max_flow = sum(flow_dict[0][v] for v in flow_dict[0]) 
        
    return float(max_flow), float(min_cost)
