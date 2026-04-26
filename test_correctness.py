from tests.correctness.test_basic import *
from tests.correctness.test_compare_scipy import *

if __name__ == "__main__":
    test_compare_scipy_equality_minimization()
    test_compare_scipy_fixed_demand_min_cost_flow()
    test_compare_scipy_greater_or_equal_diet_problem()
    test_compare_scipy_infeasible_problem()
    test_compare_scipy_production_planning()
    test_compare_scipy_unbounded_problem()

    test_equality_constraint_minimization_blending_problem()
    test_fixed_demand_min_cost_flow_problem()
    test_greater_or_equal_constraints_diet_problem()
    test_infeasible_problem()
    test_init_and_basic_maximization_production_planning()
    test_small_iteration_budget_does_not_misclassify_problem()
    test_init_and_basic_maximization_production_planning()

    print("OK")
