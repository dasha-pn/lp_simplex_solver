import math

import pytest

from solver import Solver
from enums import LpSign, LpFunc, LpStatus


TOL = 1e-7


def assert_close(actual: float, expected: float, tol: float = TOL) -> None:
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"expected {expected}, got {actual}"
    )


def assert_optimal(status: LpStatus) -> None:
    assert status == LpStatus.OPTIMAL, f"expected OPTIMAL, got {status}"


def test_init_and_basic_maximization_production_planning() -> None:
    """
    Production planning LP.

    Maximize:
        z = 3x + 2y

    Subject to:
        x + y <= 4
        x <= 2
        y <= 3
        x, y >= 0

    Optimal solution:
        x = 2, y = 2, z = 10
    """
    solver = Solver(vars_cnt=2)

    solver.add_constraint([1, 1], 4, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1, 0], 2, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([0, 1], 3, LpSign.LESS_OR_EQUAL)

    solver.set_objective([3, 2], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    assert_optimal(status)
    assert_close(solver.get_var_value(0), 2.0)
    assert_close(solver.get_var_value(1), 2.0)
    assert_close(solver.get_objective_value(), 10.0)


def test_equality_constraint_minimization_blending_problem() -> None:
    """
    Simple blending / allocation LP with equality.

    Minimize:
        z = 2x + y

    Subject to:
        x + y = 5
        x, y >= 0

    Since y is cheaper, optimum is:
        x = 0, y = 5, z = 5
    """
    solver = Solver(vars_cnt=2)

    solver.add_constraint([1, 1], 5, LpSign.EQUAL)

    solver.set_objective([2, 1], LpFunc.MINIMIZE)
    status = solver.solve(max_iters=100)

    assert_optimal(status)
    assert_close(solver.get_var_value(0), 0.0)
    assert_close(solver.get_var_value(1), 5.0)
    assert_close(solver.get_objective_value(), 5.0)


def test_greater_or_equal_constraints_diet_problem() -> None:
    """
    Diet / coverage LP.

    Minimize:
        z = 3x + 5y

    Subject to:
        2x + y >= 8
        x + 3y >= 9
        x, y >= 0

    Optimal solution is at the intersection:
        2x + y = 8
        x + 3y = 9

    Hence:
        x = 3, y = 2, z = 19
    """

    solver = Solver(vars_cnt=2)

    solver.add_constraint([2, 1], 8, LpSign.GREATER_OR_EQUAL)
    solver.add_constraint([1, 3], 9, LpSign.GREATER_OR_EQUAL)

    solver.set_objective([3, 5], LpFunc.MINIMIZE)
    status = solver.solve(max_iters=100)

    assert_optimal(status)
    assert_close(solver.get_var_value(0), 3.0)
    assert_close(solver.get_var_value(1), 2.0)
    assert_close(solver.get_objective_value(), 19.0)


def test_infeasible_problem() -> None:
    """
    Infeasible LP.

    Constraints:
        x <= 1
        x >= 3
        x >= 0

    No feasible solution exists.
    """

    solver = Solver(vars_cnt=1)

    solver.add_constraint([1], 1, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1], 3, LpSign.GREATER_OR_EQUAL)

    solver.set_objective([1], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    assert status == LpStatus.INFEASIBLE


def test_unbounded_problem() -> None:
    """
    Unbounded LP.

    Maximize:
        z = x

    Subject to:
        x >= 0

    The objective can grow without bound.
    """

    solver = Solver(vars_cnt=1)

    solver.add_constraint([1], 0, LpSign.GREATER_OR_EQUAL)

    solver.set_objective([1], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    assert status == LpStatus.UNBOUNDED


def test_iteration_limit_status() -> None:
    """
    The solver should report ITERATION_LIMIT
    when max_iters is too small to finish.
    """

    solver = Solver(vars_cnt=2)

    solver.add_constraint([1, 1], 4, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1, 0], 2, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([0, 1], 3, LpSign.LESS_OR_EQUAL)

    solver.set_objective([3, 2], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=0)

    assert status == LpStatus.ITERATION_LIMIT


def test_fixed_demand_min_cost_flow_problem() -> None:
    """
    Fixed-demand minimum-cost flow LP.

    Network:
        s -> a  capacity 2, cost 1
        s -> b  capacity 2, cost 3
        a -> t  capacity 2, cost 1
        b -> t  capacity 2, cost 1
        a -> b  capacity 1, cost 1

    Send exactly 3 units from s to t at minimum cost.

    Variables:
        x0 = f_sa
        x1 = f_sb
        x2 = f_at
        x3 = f_bt
        x4 = f_ab

    Constraints:
        capacities
        flow conservation at a and b
        total outflow from source = 3

    Optimal solution:
        f_sa = 2
        f_sb = 1
        f_at = 2
        f_bt = 1
        f_ab = 0

        objective = 1*f_sa + 3*f_sb + 1*f_at + 1*f_bt + 1*f_ab = 8
    """

    solver = Solver(vars_cnt=5)

    solver.add_constraint([1, 0, 0, 0, 0], 2, LpSign.LESS_OR_EQUAL)  #f_sa <= 2
    solver.add_constraint([0, 1, 0, 0, 0], 2, LpSign.LESS_OR_EQUAL)  #f_sb <= 2
    solver.add_constraint([0, 0, 1, 0, 0], 2, LpSign.LESS_OR_EQUAL)  #f_at <= 2
    solver.add_constraint([0, 0, 0, 1, 0], 2, LpSign.LESS_OR_EQUAL)  #f_bt <= 2
    solver.add_constraint([0, 0, 0, 0, 1], 1, LpSign.LESS_OR_EQUAL)  #f_ab <= 1

    solver.add_constraint([1, 0, -1, 0, -1], 0, LpSign.EQUAL)  #node a
    solver.add_constraint([0, 1, 0, -1, 1], 0, LpSign.EQUAL)   #node b

    solver.add_constraint([1, 1, 0, 0, 0], 3, LpSign.EQUAL)

    solver.set_objective([1, 3, 1, 1, 1], LpFunc.MINIMIZE)
    status = solver.solve(max_iters=200)

    assert_optimal(status)
    assert_close(solver.get_var_value(0), 2.0)
    assert_close(solver.get_var_value(1), 1.0)
    assert_close(solver.get_var_value(2), 2.0)
    assert_close(solver.get_var_value(3), 1.0)
    assert_close(solver.get_var_value(4), 0.0)
    assert_close(solver.get_objective_value(), 8.0)
