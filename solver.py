from enums import LpSign, LpFunc, LpStatus
from typing import List, Tuple

class Solver:
    def __init__(self, vars_cnt: int):
        self.n = vars_cnt
        self.constraints: List[Tuple[List[float], float, LpSign]] = []
        self.obj_coefs: List[float] = [0.0] * self.n
        
        self.solution: List[float] = [0.0] * self.n
        self.obj_value = 0.0

    def add_constraint(self, coefs: List[float], rhs: float, sign: LpSign) -> None:
        if len(coefs) != self.n:
            raise ValueError(f"Expected {self.n} coefficients")
        self.constraints.append((list(coefs), float(rhs), sign))

    def set_objective(self, coefs: List[float], target_func: LpFunc) -> None:
        if len(coefs) != self.n:
            raise ValueError(f"Expected {self.n} coefficients")
        self.obj_coefs = list(coefs)
        self.target = target_func

    def _mat_vec_mult(self, M: List[List[float]], v: List[float]) -> List[float]:
        """Multiply matrix by column vector (M * v)"""
        m = len(M)
        n = len(v)
        res = [0.0] * m
        for i in range(m):
            res[i] = sum(M[i][j] * v[j] for j in range(n))
        return res

    def _vec_mat_mult(self, v: List[float], M: List[List[float]]) -> List[float]:
        """Multiply row vector by matrix (v^T * M)"""
        if not M:
            return []
        m = len(v)
        cols = len(M[0])
        res = [0.0] * cols
        for j in range(cols):
            res[j] = sum(v[i] * M[i][j] for i in range(m))
        return res

    def _get_columns(self, A: List[List[float]], indices: List[int]) -> List[List[float]]:
        """Get new matrix from columns of A"""
        return [[row[j] for j in indices] for row in A]

    def _get_column(self, A: List[List[float]], j: int) -> List[float]:
        """Get matrix column"""
        return [row[j] for row in A]

    def _invert_matrix(self, M: List[List[float]]) -> List[List[float]]:
        """Find matrix inverse using elementary row operations"""
        m = len(M)
        aug = [row[:] + [1.0 if i == j else 0.0 for j in range(m)] for i, row in enumerate(M)]
        
        for i in range(m):
            pivot_row = i
            max_val = abs(aug[i][i])
            for k in range(i + 1, m):
                if abs(aug[k][i]) > max_val:
                    max_val = abs(aug[k][i])
                    pivot_row = k
                    
            if max_val < 1e-12:
                raise ValueError("Singular matrix encountered")
                
            aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
            
            pivot = aug[i][i]
            for j in range(i, 2 * m):
                aug[i][j] /= pivot
                
            for k in range(m):
                if k != i:
                    factor = aug[k][i]
                    for j in range(i, 2 * m):
                        aug[k][j] -= factor * aug[i][j]
                        
        return [row[m:] for row in aug]

    def solve(self, max_iters: int) -> LpStatus:
        m = len(self.constraints)
        if m == 0:
            return LpStatus.OPTIMAL

        norm_constraints = []
        for coefs, rhs, sign in self.constraints:
            c = coefs[:]
            r = rhs
            s = sign
            if r < 0:
                c = [-x for x in c]
                r = -r
                if s == LpSign.LESS_OR_EQUAL:
                    s = LpSign.GREATER_OR_EQUAL
                elif s == LpSign.GREATER_OR_EQUAL:
                    s = LpSign.LESS_OR_EQUAL
            norm_constraints.append((c, r, s))

        slack_surplus_cnt = 0
        artificial_cnt = 0
        for _, _, sign in norm_constraints:
            if sign == LpSign.LESS_OR_EQUAL:
                slack_surplus_cnt += 1
            elif sign == LpSign.GREATER_OR_EQUAL:
                slack_surplus_cnt += 1
                artificial_cnt += 1
            elif sign == LpSign.EQUAL:
                artificial_cnt += 1

        total_vars = self.n + slack_surplus_cnt + artificial_cnt
        A = [[0.0] * total_vars for _ in range(m)]
        b = [0.0] * m

        B = []
        N = list(range(self.n))
        art_indices = []

        current_col = self.n

        for i, (coefs, rhs, sign) in enumerate(norm_constraints):
            for j in range(self.n):
                A[i][j] = coefs[j]
            b[i] = rhs
            
            if sign == LpSign.LESS_OR_EQUAL:
                A[i][current_col] = 1.0
                B.append(current_col)
                current_col += 1
            elif sign == LpSign.GREATER_OR_EQUAL:
                A[i][current_col] = -1.0
                N.append(current_col)
                current_col += 1
                A[i][current_col] = 1.0
                B.append(current_col)
                art_indices.append(current_col)
                current_col += 1
            elif sign == LpSign.EQUAL:
                A[i][current_col] = 1.0
                B.append(current_col)
                art_indices.append(current_col)
                current_col += 1

        EPS = 1e-9

        if artificial_cnt > 0:
            c_phase1 = [0.0] * total_vars
            for idx in art_indices:
                c_phase1[idx] = -1.0 
            
            status, B, N = self._run_simplex_loop(c_phase1, A, b, B, N, max_iters, EPS)
            if status != LpStatus.OPTIMAL:
                return status

            B_mat = self._get_columns(A, B)
            B_inv = self._invert_matrix(B_mat)
            x_B = self._mat_vec_mult(B_inv, b)
            
            for i, basic_var_idx in enumerate(B):
                if basic_var_idx in art_indices and x_B[i] > EPS:
                    return LpStatus.INFEASIBLE
            
            N = [j for j in N if j not in art_indices]

        c_phase2 = [0.0] * total_vars
        for i in range(self.n):
            c_phase2[i] = self.obj_coefs[i] if self.target == LpFunc.MAXIMIZE else -self.obj_coefs[i]

        status, B, N = self._run_simplex_loop(c_phase2, A, b, B, N, max_iters, EPS)

        if status == LpStatus.OPTIMAL:
            self.solution = [0.0] * self.n
            B_mat = self._get_columns(A, B)
            B_inv = self._invert_matrix(B_mat)
            x_B = self._mat_vec_mult(B_inv, b)

            for i, var_idx in enumerate(B):
                if var_idx < self.n:
                    self.solution[var_idx] = x_B[i]

            self.obj_value = sum(self.obj_coefs[i] * self.solution[i] for i in range(self.n))

        return status

    def _run_simplex_loop(self, c: List[float], A: List[List[float]], b: List[float], B: List[int], N: List[int], max_iters: int, EPS: float):
        degenerate_iters = 0

        for _ in range(max_iters):
            B_mat = self._get_columns(A, B)
            B_inv = self._invert_matrix(B_mat)

            c_B = [c[i] for i in B]
            y = self._vec_mat_mult(c_B, B_inv)

            N_mat = self._get_columns(A, N)
            y_N = self._vec_mat_mult(y, N_mat)
            
            c_N = [c[i] for i in N]
            c_bar_N = [c_N[i] - y_N[i] for i in range(len(N))]

            use_blands_rule = degenerate_iters > 10

            j_entering_N_idx = -1
            
            if use_blands_rule:
                min_original_index = float("inf")
                for idx, val in enumerate(c_bar_N):
                    if val > EPS:
                        original_var_idx = N[idx]
                        if original_var_idx < min_original_index:
                            min_original_index = original_var_idx
                            j_entering_N_idx = idx
                if j_entering_N_idx == -1:
                    return LpStatus.OPTIMAL, B, N
            else:
                max_c_bar = -float("inf")
                for idx, val in enumerate(c_bar_N):
                    if val > max_c_bar:
                        max_c_bar = val
                        j_entering_N_idx = idx
                
                if max_c_bar <= EPS:
                    return LpStatus.OPTIMAL, B, N

            j = N[j_entering_N_idx]
            A_j = self._get_column(A, j)
            d = self._mat_vec_mult(B_inv, A_j)

            if all(val <= EPS for val in d):
                return LpStatus.UNBOUNDED, B, N

            x_B = self._mat_vec_mult(B_inv, b)
            min_ratio = float("inf")
            leaving_B_idx = -1
            
            if use_blands_rule:
                min_leaving_original_index = float("inf")
                for i in range(len(B)):
                    if d[i] > EPS:
                        ratio = x_B[i] / d[i]
                        if ratio < min_ratio - EPS:
                            min_ratio = ratio
                            leaving_B_idx = i
                            min_leaving_original_index = B[i]
                        elif abs(ratio - min_ratio) <= EPS:
                            if B[i] < min_leaving_original_index:
                                leaving_B_idx = i
                                min_leaving_original_index = B[i]
            else:
                for i in range(len(B)):
                    if d[i] > EPS:
                        ratio = x_B[i] / d[i]
                        if ratio < min_ratio:
                            min_ratio = ratio
                            leaving_B_idx = i

            if min_ratio <= EPS:
                degenerate_iters += 1
            else:
                degenerate_iters = 0

            B[leaving_B_idx], N[j_entering_N_idx] = N[j_entering_N_idx], B[leaving_B_idx]

        return LpStatus.ITERATION_LIMIT, B, N

    def get_var_value(self, var_ind: int) -> float:
        return self.solution[var_ind]

    def get_objective_value(self) -> float:
        return self.obj_value
