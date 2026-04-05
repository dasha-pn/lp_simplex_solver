"helper math functions"

import copy
EPS = 1e-9

def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def mat_vec_mul(A: list[list[float]], x: list[float]) -> list[float]:
    return [dot(row, x) for row in A]

def transpose(A: list[list[float]]) -> list[list[float]]:
    return list(map(list, zip(*A)))

def identity(n: int) -> list[list[float]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def deep_copy_matrix(A):
    return copy.deepcopy(A)

def is_zero(x: float) -> bool:
    return abs(x) < EPS


def is_positive(x: float) -> bool:
    return x > EPS


def is_negative(x: float) -> bool:
    return x < -EPS

def argmax_positive(values: list[float]):
    best_idx = None
    best_val = 0
    for i, v in enumerate(values):
        if v > best_val:
            best_val = v
            best_idx = i
    return best_idx
