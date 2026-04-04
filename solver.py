from enum import Enum

class LpSign(Enum):
    EQUAL = 0
    LESS_OR_EQUAL = 1
    GREATER_OR_EQUAL = 2

class LpFunc(Enum):
    MINIMIZE = 0
    MAXIMIZE = 1

class LpStatus(Enum):
    OPTIMAL = 0
    INFEASIBLE = 1
    UNBOUNDED = 2
    ITERATION_LIMIT = 3

class Solver:
    def __init__(vars_cnt: int):
        pass

    def add_constraint(coefs: list[float], rhs: float, sign: LpSign) -> None:
        pass

    def set_objective(coefs: list[float], target_func: LpFunc) -> None:
        pass

    def solve(max_iters: int) -> LpStatus:
        pass

    def get_var_value(var_ind: int) -> float:
        pass

    def get_objective_value(self) -> float:
        pass
