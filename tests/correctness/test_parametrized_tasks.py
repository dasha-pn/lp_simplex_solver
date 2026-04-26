import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from solver import Solver
from enums import LpSign, LpFunc, LpStatus


TOL = 1e-7


def assert_close(actual: float, expected: float, tol: float = TOL) -> None:
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"expected {expected}, got {actual}"
    )


def solve_production(profit_a, profit_b, shared_resource, max_a, max_b):
    solver = Solver(vars_cnt=2)

    solver.add_constraint([1, 1], shared_resource, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1, 0], max_a, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([0, 1], max_b, LpSign.LESS_OR_EQUAL)

    solver.set_objective([profit_a, profit_b], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    return status, [solver.get_var_value(0), solver.get_var_value(1)], solver.get_objective_value()


def solve_reddy_mikks(profit_exterior, profit_interior):
    solver = Solver(vars_cnt=2)

    solver.add_constraint([6, 4], 24, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1, 2], 6, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([-1, 1], 1, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([0, 1], 2, LpSign.LESS_OR_EQUAL)

    solver.set_objective([profit_exterior, profit_interior], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    return status, [solver.get_var_value(0), solver.get_var_value(1)], solver.get_objective_value()


def solve_floating_point_lp(profit_a, profit_b, resource_1_limit, resource_2_limit):
    solver = Solver(vars_cnt=2)

    solver.add_constraint([0.5, 1.25], resource_1_limit, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1.2, 0.8], resource_2_limit, LpSign.LESS_OR_EQUAL)

    solver.set_objective([profit_a, profit_b], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    return status, [solver.get_var_value(0), solver.get_var_value(1)], solver.get_objective_value()


def solve_resource_allocation(profit_a, profit_b, profit_c, resource_1_limit, resource_2_limit, max_c):
    solver = Solver(vars_cnt=3)

    solver.add_constraint([2, 1, 3], resource_1_limit, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([1, 2, 1], resource_2_limit, LpSign.LESS_OR_EQUAL)
    solver.add_constraint([0, 0, 1], max_c, LpSign.LESS_OR_EQUAL)

    solver.set_objective([profit_a, profit_b, profit_c], LpFunc.MAXIMIZE)
    status = solver.solve(max_iters=100)

    return (
        status,
        [solver.get_var_value(0), solver.get_var_value(1), solver.get_var_value(2)],
        solver.get_objective_value(),
    )


def solve_blending(cost_a, cost_b, total_amount, quality_requirement):
    solver = Solver(vars_cnt=2)

    solver.add_constraint([1, 1], total_amount, LpSign.EQUAL)
    solver.add_constraint([0.3, 0.7], quality_requirement, LpSign.GREATER_OR_EQUAL)

    solver.set_objective([cost_a, cost_b], LpFunc.MINIMIZE)
    status = solver.solve(max_iters=100)

    return status, [solver.get_var_value(0), solver.get_var_value(1)], solver.get_objective_value()


def test_production_multiple_inputs():
    status, values, obj = solve_production(3, 2, 4, 2, 3)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 2.0)
    assert_close(values[1], 2.0)
    assert_close(obj, 10.0)

    status, values, obj = solve_production(5, 1, 6, 4, 5)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 4.0)
    assert_close(values[1], 2.0)
    assert_close(obj, 22.0)


def test_reddy_mikks_multiple_inputs():
    status, values, obj = solve_reddy_mikks(5, 4)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 3.0)
    assert_close(values[1], 1.5)
    assert_close(obj, 21.0)

    status, values, obj = solve_reddy_mikks(4, 6)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 3.0)
    assert_close(values[1], 1.5)
    assert_close(obj, 21.0)


def test_floating_point_lp_multiple_inputs():
    status, values, obj = solve_floating_point_lp(2.75, 3.4, 7.5, 6.4)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 1.8181818181818181)
    assert_close(values[1], 5.2727272727272725)
    assert_close(obj, 22.927272727272726)

    status, values, obj = solve_floating_point_lp(3.0, 2.0, 7.5, 6.4)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 5.3333333333)
    assert_close(values[1], 0.0)
    assert_close(obj, 16.0)


def test_resource_allocation_multiple_inputs():
    status, values, obj = solve_resource_allocation(6, 4, 5, 60, 40, 15)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 26.6666666667)
    assert_close(values[1], 6.6666666667)
    assert_close(values[2], 0.0)
    assert_close(obj, 186.6666666667)

    status, values, obj = solve_resource_allocation(3, 4, 10, 60, 40, 15)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 1.6666666667)
    assert_close(values[1], 11.6666666667)
    assert_close(values[2], 15.0)
    assert_close(obj, 201.6666666667)


def test_blending_multiple_inputs():
    status, values, obj = solve_blending(4, 6, 10, 5)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 5.0)
    assert_close(values[1], 5.0)
    assert_close(obj, 50.0)

    status, values, obj = solve_blending(6, 4, 10, 5)

    assert status == LpStatus.OPTIMAL
    assert_close(values[0], 0.0)
    assert_close(values[1], 10.0)
    assert_close(obj, 40.0)
