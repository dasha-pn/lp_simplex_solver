import math

import pytest
from scipy.optimize import linprog

from solver import Solver
from enums import LpSign, LpFunc, LpStatus


TOL = 1e-6


def assert_close(actual: float, expected: float, tol: float = TOL) -> None:
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"expected {expected}, got {actual}"
    )


def scipy_status_to_lp_status(result) -> LpStatus:
    """
    Map scipy.optimize.linprog status/result to the project's LpStatus.
    """

    if result.success:
        return LpStatus.OPTIMAL

    if result.status == 1:
        return LpStatus.ITERATION_LIMIT
    if result.status == 2:
        return LpStatus.INFEASIBLE
    if result.status == 3:
        return LpStatus.UNBOUNDED

    raise AssertionError(f"Unexpected SciPy status: {result.status}, message: {result.message}")


def build_and_solve_our_solver(
    vars_cnt: int,
    constraints: list[tuple[list[float], float, LpSign]],
    objective: list[float],
    target_func: LpFunc,
    max_iters: int = 500,
) -> tuple[LpStatus, list[float], float]:
    """
    Build and solve the LP using our solver, 
    returning status, variable values, and objective value.
    """

    solver = Solver(vars_cnt=vars_cnt)

    for coefs, rhs, sign in constraints:
        solver.add_constraint(coefs, rhs, sign)

    solver.set_objective(objective, target_func)
    status = solver.solve(max_iters=max_iters)

    values = [solver.get_var_value(i) for i in range(vars_cnt)]
    objective_value = solver.get_objective_value()

    return status, values, objective_value


def solve_with_scipy(
    vars_cnt: int,
    constraints: list[tuple[list[float], float, LpSign]],
    objective: list[float],
    target_func: LpFunc,
):
    """
    Convert the project LP representation into scipy.optimize.linprog format.
    Assumes all variables are nonnegative.
    """

    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []

    for coefs, rhs, sign in constraints:
        if sign == LpSign.LESS_OR_EQUAL:
            A_ub.append(coefs)
            b_ub.append(rhs)
        elif sign == LpSign.GREATER_OR_EQUAL:
            A_ub.append([-x for x in coefs])
            b_ub.append(-rhs)
        elif sign == LpSign.EQUAL:
            A_eq.append(coefs)
            b_eq.append(rhs)
        else:
            raise AssertionError(f"Unsupported sign: {sign}")

    c = objective[:]
    if target_func == LpFunc.MAXIMIZE:
        c = [-x for x in c]

    result = linprog(
        c=c,
        A_ub=A_ub if A_ub else None,
        b_ub=b_ub if b_ub else None,
        A_eq=A_eq if A_eq else None,
        b_eq=b_eq if b_eq else None,
        bounds=[(0, None)] * vars_cnt,
        method="highs",
    )

    status = scipy_status_to_lp_status(result)

    if status == LpStatus.OPTIMAL:
        values = result.x.tolist()
        objective_value = float(result.fun)
        if target_func == LpFunc.MAXIMIZE:
            objective_value = -objective_value
    else:
        values = [0.0] * vars_cnt
        objective_value = 0.0

    return status, values, objective_value


def compare_with_scipy(
    vars_cnt: int,
    constraints: list[tuple[list[float], float, LpSign]],
    objective: list[float],
    target_func: LpFunc,
    max_iters: int = 500,
    compare_vars: bool = True,
) -> None:
    """Compare our solver's results with SciPy's linprog."""

    our_status, our_values, our_obj = build_and_solve_our_solver(
        vars_cnt, constraints, objective, target_func, max_iters=max_iters
    )
    scipy_status, scipy_values, scipy_obj = solve_with_scipy(
        vars_cnt, constraints, objective, target_func
    )

    assert our_status == scipy_status, (
        f"Status mismatch: our solver = {our_status}, scipy = {scipy_status}"
    )

    if our_status == LpStatus.OPTIMAL:
        assert_close(our_obj, scipy_obj)

        if compare_vars:
            for i in range(vars_cnt):
                assert_close(our_values[i], scipy_values[i])


def test_compare_scipy_production_planning() -> None:
    """
    Maximize:
        z = 3x + 2y

    Subject to:
        x + y <= 4
        x <= 2
        y <= 3
        x, y >= 0
    """

    constraints = [
        ([1, 1], 4, LpSign.LESS_OR_EQUAL),
        ([1, 0], 2, LpSign.LESS_OR_EQUAL),
        ([0, 1], 3, LpSign.LESS_OR_EQUAL),
    ]
    objective = [3, 2]

    compare_with_scipy(
        vars_cnt=2,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MAXIMIZE,
    )


def test_compare_scipy_equality_minimization() -> None:
    """
    Minimize:
        z = 2x + y

    Subject to:
        x + y = 5
        x, y >= 0
    """

    constraints = [
        ([1, 1], 5, LpSign.EQUAL),
    ]
    objective = [2, 1]

    compare_with_scipy(
        vars_cnt=2,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MINIMIZE,
    )


def test_compare_scipy_greater_or_equal_diet_problem() -> None:
    """
    Minimize:
        z = 3x + 5y

    Subject to:
        2x + y >= 8
        x + 3y >= 9
        x, y >= 0
    """

    constraints = [
        ([2, 1], 8, LpSign.GREATER_OR_EQUAL),
        ([1, 3], 9, LpSign.GREATER_OR_EQUAL),
    ]
    objective = [3, 5]

    compare_with_scipy(
        vars_cnt=2,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MINIMIZE,
    )


def test_compare_scipy_infeasible_problem() -> None:
    """
    x <= 1
    x >= 3
    """

    constraints = [
        ([1], 1, LpSign.LESS_OR_EQUAL),
        ([1], 3, LpSign.GREATER_OR_EQUAL),
    ]
    objective = [1]

    compare_with_scipy(
        vars_cnt=1,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MAXIMIZE,
        compare_vars=False,
    )


def test_compare_scipy_unbounded_problem() -> None:
    """
    Maximize:
        z = x

    Subject to:
        x >= 0
    """

    constraints = [
        ([1], 0, LpSign.GREATER_OR_EQUAL),
    ]
    objective = [1]

    compare_with_scipy(
        vars_cnt=1,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MAXIMIZE,
        compare_vars=False,
    )


def test_compare_scipy_fixed_demand_min_cost_flow() -> None:
    """
    Fixed-demand minimum-cost flow LP.

    Variables:
        x0 = f_sa
        x1 = f_sb
        x2 = f_at
        x3 = f_bt
        x4 = f_ab

    Minimize:
        z = 1*f_sa + 3*f_sb + 1*f_at + 1*f_bt + 1*f_ab

    Subject to:
        f_sa <= 2
        f_sb <= 2
        f_at <= 2
        f_bt <= 2
        f_ab <= 1

        f_sa - f_at - f_ab = 0
        f_sb - f_bt + f_ab = 0

        f_sa + f_sb = 3

        all variables >= 0
    """

    constraints = [
        ([1, 0, 0, 0, 0], 2, LpSign.LESS_OR_EQUAL),
        ([0, 1, 0, 0, 0], 2, LpSign.LESS_OR_EQUAL),
        ([0, 0, 1, 0, 0], 2, LpSign.LESS_OR_EQUAL),
        ([0, 0, 0, 1, 0], 2, LpSign.LESS_OR_EQUAL),
        ([0, 0, 0, 0, 1], 1, LpSign.LESS_OR_EQUAL),
        ([1, 0, -1, 0, -1], 0, LpSign.EQUAL),
        ([0, 1, 0, -1, 1], 0, LpSign.EQUAL),
        ([1, 1, 0, 0, 0], 3, LpSign.EQUAL),
    ]
    objective = [1, 3, 1, 1, 1]

    compare_with_scipy(
        vars_cnt=5,
        constraints=constraints,
        objective=objective,
        target_func=LpFunc.MINIMIZE,
    )
