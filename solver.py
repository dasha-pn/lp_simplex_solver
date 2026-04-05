"Solver"

from enums import LpSign, LpFunc, LpStatus

class Solver:
    def __init__(self, vars_cnt: int):
        pass

    def add_constraint(self, coefs: list[float], rhs: float, sign: LpSign) -> None:
        pass

    def set_objective(self, coefs: list[float], target_func: LpFunc) -> None:
        pass

    def solve(self, max_iters: int) -> LpStatus:
        pass

    def get_var_value(self, var_ind: int) -> float:
        pass

    def get_objective_value(self) -> float:
        pass
