from tests.performance.mcmf_custom_lp import solve_mfmc_custom_lp
from tests.performance.mcmf_scipy import solve_mfmc_scipy
from tests.performance.mcmf_networkx import solve_mfmc_networkx
from tests.performance.graph_generator import generate_hard_mfmc_graph

import time
import csv
import copy
import matplotlib.pyplot as plt

STYLES = {
    "Custom": "r-o",
    "SciPy": "b-s",
    "NetworkX": "g-^"
}

def compare_results(res1, res2, eps=1e-7):
    if res1 is None or res2 is None:
        return res1 == res2
    if isinstance(res1, (int, float)) and isinstance(res2, (int, float)):
        return abs(res1 - res2) <= eps
    if isinstance(res1, (tuple, list)) and isinstance(res2, (tuple, list)):
        if len(res1) != len(res2):
            return False
        for a, b in zip(res1, res2):
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if abs(a - b) > eps:
                    return False
            else:
                if a != b:
                    return False
        return True
    return res1 == res2

def benchmark_avg_time(solver_func, graphs, k_runs):
    total_duration = 0.0
    m_graphs = len(graphs)
    graph_results = []

    for original_graph in graphs:
        first_run_result = None
        for r in range(k_runs):
            graph_copy = copy.deepcopy(original_graph)
            
            start = time.perf_counter()
            res = solver_func(graph_copy)
            total_duration += time.perf_counter() - start
            
            if r == 0:
                first_run_result = res
                
        graph_results.append(first_run_result)
        
    return total_duration / (m_graphs * k_runs), graph_results


def run_benchmark(benchmark_name, sizes, m_graphs, k_runs, solvers):
    results_time = {name: [] for name in solvers.keys()}
    solver_names = list(solvers.keys())
    
    print(benchmark_name)
    for n in sizes:
        graphs = [generate_hard_mfmc_graph(n, 3, 1000, 1000) for _ in range(m_graphs)]
        all_graph_results = {}
        
        for name, func in solvers.items():
            avg_time, graph_results = benchmark_avg_time(func, graphs, k_runs)
            results_time[name].append(avg_time)
            all_graph_results[name] = graph_results
            
        for i in range(m_graphs):
            base_name = solver_names[0]
            base_res = all_graph_results[base_name][i]
            
            for other_name in solver_names[1:]:
                other_res = all_graph_results[other_name][i]
                if not compare_results(base_res, other_res, eps=1e-7):
                    print(f"  [WARNING] Mismatch on N={n}! {base_name}: {base_res} | {other_name}: {other_res}")
                    
        print(f"N={n} finished.")
    return results_time


def save_to_csv(filename, sizes, results):
    keys = list(results.keys())
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n"] + keys)
        for i, n in enumerate(sizes):
            writer.writerow([n] + [results[key][i] for key in keys])


def plot_results(sizes, results, title, is_log=False):
    plt.figure(figsize=(8, 6))
    
    for name, times in results.items():
        plt.plot(sizes, times, STYLES.get(name, "-"), label=name, lw=2)
        
    if is_log:
        plt.yscale("log")
        plt.grid(True, which="both", alpha=0.3)
    else:
        plt.grid(True, alpha=0.3)
        
    plt.title(title)
    plt.xlabel("Vertices")
    plt.ylabel("Average seconds")
    plt.legend()


def main():
    small_sizes = list(range(2, 31, 2))
    M1, K1 = 10, 5

    large_sizes = list(range(10, 151, 10))
    M2, K2 = 5, 3

    results_small = run_benchmark(
        "Running Custom vs SciPy benchmark...", 
        small_sizes, M1, K1, 
        {"Custom": solve_mfmc_custom_lp, "SciPy": solve_mfmc_scipy}
    )
    
    print()
    
    results_large = run_benchmark(
        "Running SciPy vs NetworkX benchmark...", 
        large_sizes, M2, K2, 
        {"SciPy": solve_mfmc_scipy, "NetworkX": solve_mfmc_networkx}
    )

    save_to_csv("benchmark_small.csv", small_sizes, results_small)
    save_to_csv("benchmark_large.csv", large_sizes, results_large)

    plot_results(small_sizes, results_small, "Custom vs SciPy (linear scale)\nAverage time per run")
    plot_results(small_sizes, results_small, "Custom vs SciPy (log scale)\nAverage time per run", is_log=True)
    
    plot_results(large_sizes, results_large, "SciPy vs NetworkX (linear scale)\nAverage time per run")
    plot_results(large_sizes, results_large, "SciPy vs NetworkX (log scale)\nAverage time per run", is_log=True)

    plt.show()

if __name__ == "__main__":
    main()
