from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from solver import Solver
from enums import LpSign, LpFunc, LpStatus


app = FastAPI(title="LP Simplex Solver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConstraintInput(BaseModel):
    coefs: list[float]
    rhs: float
    sign: str


class SolveRequest(BaseModel):
    vars_cnt: int
    objective: list[float]
    target: str
    constraints: list[ConstraintInput]
    max_iters: int = 100


@app.post("/solve")
def solve_lp(data: SolveRequest):
    solver = Solver(vars_cnt=data.vars_cnt)

    sign_map = {
        "LESS_OR_EQUAL": LpSign.LESS_OR_EQUAL,
        "GREATER_OR_EQUAL": LpSign.GREATER_OR_EQUAL,
        "EQUAL": LpSign.EQUAL,
    }

    target_map = {
        "MAXIMIZE": LpFunc.MAXIMIZE,
        "MINIMIZE": LpFunc.MINIMIZE,
    }

    for constraint in data.constraints:
        solver.add_constraint(
            constraint.coefs,
            constraint.rhs,
            sign_map[constraint.sign],
        )

    solver.set_objective(data.objective, target_map[data.target])
    status = solver.solve(max_iters=data.max_iters)

    response = {
        "status": status.name,
        "variables": [],
        "objective_value": None,
    }

    if status == LpStatus.OPTIMAL:
        response["variables"] = [
            solver.get_var_value(i) for i in range(data.vars_cnt)
        ]
        response["objective_value"] = solver.get_objective_value()

    return response
