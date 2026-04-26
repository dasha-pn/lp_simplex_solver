from tests.performance.mcmf_custom_lp import solve_mfmc_custom_lp
from tests.performance.mcmf_scipy import solve_mfmc_scipy
from tests.performance.mcmf_networkx import solve_mfmc_networkx
from tests.performance.graph_generator import generate_hard_mfmc_graph

import time
import csv
import matplotlib.pyplot as plt

STYLES = {
    "Custom": "r-o",
    "SciPy": "b-s",
    "NetworkX": "g-^"
}

def benchmark_avg_time(solver_func, n, m_graphs, k_runs):
    total_duration = 0.0
    for _ in range(m_graphs):
        graph = generate_hard_mfmc_graph(n, 3, 1000, 1000)
        for _ in range(k_runs):
            start = time.perf_counter()
            solver_func(graph)
            total_duration += time.perf_counter() - start
    return total_duration / (m_graphs * k_runs)


def run_benchmark(benchmark_name, sizes, m_graphs, k_runs, solvers):
    results = {name: [] for name in solvers.keys()}
    print(benchmark_name)
    for n in sizes:
        for name, func in solvers.items():
            results[name].append(benchmark_avg_time(func, n, m_graphs, k_runs))
        print(f"N={n} finished.")
    return results


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
