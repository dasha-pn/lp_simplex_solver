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
