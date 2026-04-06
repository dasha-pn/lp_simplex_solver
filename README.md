# LP simplex solver

A lightweight Python implementation of a **Linear Programming solver based on the Simplex method**.

This project focuses on solving LP problems in standard linear form with support for:
- maximization and minimization;
- constraints of type `<=`, `>=`, and `=`;
- automatic introduction of slack, surplus, and artificial variables;
- Phase I / Phase II simplex workflow;
- detection of **optimal**, **infeasible**, **unbounded**, and **iteration limit** outcomes.

The repository also includes:
- a small `demo.py` example runner;
- unit tests for basic LP scenarios;
- comparison tests against `scipy.optimize.linprog`.

## Features

### Supported problem types
- Linear objective functions
- Nonnegative decision variables
- Constraint signs:
  - `LpSign.LESS_OR_EQUAL`
  - `LpSign.GREATER_OR_EQUAL`
  - `LpSign.EQUAL`
- Objective directions:
  - `LpFunc.MAXIMIZE`
  - `LpFunc.MINIMIZE`

### Solver statuses
The solver returns one of the following values:
- `LpStatus.OPTIMAL`
- `LpStatus.INFEASIBLE`
- `LpStatus.UNBOUNDED`
- `LpStatus.ITERATION_LIMIT`

## How it works

The solver stores the LP model in terms of:
- the number of variables;
- a list of constraints;
- objective coefficients;
- the target optimization direction.

When `solve()` is called, the implementation:

1. **Normalizes constraints** so right-hand sides are nonnegative.
2. **Builds the augmented LP system**, adding:
   - slack variables for `<=` constraints;
   - surplus and artificial variables for `>=` constraints;
   - artificial variables for `=` constraints.
3. Runs **Phase I simplex** to obtain a feasible basis.
4. Detects **infeasibility** if artificial variables remain positive in the basis.
5. Runs **Phase II simplex** using the original objective.
6. Extracts the values of the original decision variables and computes the final objective value.

The simplex loop uses:
- reduced costs;
- basis inverse computation;
- ratio test for leaving variable selection;
- a Bland-style fallback rule to reduce cycling in degenerate cases.

### Installation

```bash
pip install -r requirements.txt
```

## API overview

### `Solver(vars_cnt: int)`
Creates a solver for a problem with `vars_cnt` decision variables.

### `add_constraint(coefs: list[float], rhs: float, sign: LpSign) -> None`
Adds one linear constraint.

Example:

```python
solver.add_constraint([2, 1], 8, LpSign.GREATER_OR_EQUAL)
```

which represents:

```text
2x1 + x2 >= 8
```

### `set_objective(coefs: list[float], target_func: LpFunc) -> None`
Sets the objective function.

Example:

```python
solver.set_objective([3, 5], LpFunc.MINIMIZE)
```

which represents:

```text
min z = 3x1 + 5x2
```

### `solve(max_iters: int) -> LpStatus`
Runs the simplex-based solver.

### `get_var_value(var_ind: int) -> float`
Returns the value of decision variable `x[var_ind]` after a successful solve.

### `get_objective_value() -> float`
Returns the objective value after a successful solve.

## Test coverage

The current tests cover:
- basic maximization;
- equality-constrained minimization;
- `>=` constraints;
- infeasible LPs;
- unbounded LPs;
- iteration-budget behavior;
- a fixed-demand minimum-cost flow formulation;
- cross-checking results with SciPy.

## Notes and limitations

- The solver assumes **nonnegative variables**.
- Matrix inversion is implemented directly inside the solver, so this project is best suited for **educational purposes and small to medium examples**, not for large-scale industrial optimization.
- Numerical behavior depends on floating-point tolerances.
- Getter methods are intended to be used after an `OPTIMAL` result.

# Links to our videos

### Daryna Shevchuk

[Link](https://youtu.be/VvWtTO8Madk)

### Marharyta Paduchak
[Link](https://youtu.be/BdYCHGgArh0?si=exRUMdmbQ_cfeDzm)

### Roman Leshchuk

[Link](https://www.youtube.com/watch?v=6wimI5qQw_Y)
