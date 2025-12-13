# fund_optimizer/core.py
import numpy as np
import kaiwu as kw

class FundOptimizer:
    def __init__(self, N, J, d1, d2, alpha=0.05, target_sum_j=20):
        self.N = N  # 基金数量
        self.J = J  # 选项数量
        self.d1 = d1  # A_i, B维度
        self.d2 = d2  # C_i, D维度
        self.alpha = alpha
        self.target_sum_j = target_sum_j
        self.best_solution = None
        self.best_total_j = None

    def set_data(self, R, A, C, B, D):
        """设置输入数据"""
        self.R = R
        self.A = A
        self.C = C
        self.B = B
        self.D = D
        
        # 预计算内积
        self.A_dot_A = np.dot(A, A.T)
        self.C_dot_C = np.dot(C, C.T)
        self.A_dot_B = np.dot(A, B)
        self.C_dot_D = np.dot(C, D)

    def build_objective(self, lambda_constraint=0.0):
        """构建目标函数"""
        x = self.x  # 从类变量获取决策变量
        objective = 0.0

        # 原始线性项
        for i in range(self.N):
            for j in range(self.J):
                objective += (self.alpha * j * self.R[i]) * x[i, j]

        # 欧氏距离平方项（二次项）
        for i in range(self.N):
            for k in range(self.N):
                coeff_quad = 0.5 * (self.A_dot_A[i, k] + self.C_dot_C[i, k])
                for j in range(self.J):
                    for l in range(self.J):
                        w_ij = self.alpha * j
                        w_kl = self.alpha * l
                        objective += coeff_quad * w_ij * w_kl * x[i, j] * x[k, l]

        # 欧氏距离平方项（线性项）
        for i in range(self.N):
            linear_coeff = -self.alpha * (self.A_dot_B[i] + self.C_dot_D[i])
            for j in range(self.J):
                objective += linear_coeff * j * x[i, j]

        # 总和约束项（拉格朗日方法）
        if lambda_constraint > 0:
            # 二次项
            for i1 in range(self.N):
                for j1 in range(self.J):
                    for i2 in range(self.N):
                        for j2 in range(self.J):
                            objective += lambda_constraint * j1 * j2 * x[i1, j1] * x[i2, j2]
            # 线性项
            for i in range(self.N):
                for j in range(self.J):
                    objective += -2 * lambda_constraint * self.target_sum_j * j * x[i, j]

        return objective

    def build_one_hot_constraint(self):
        """构建one-hot约束"""
        constraint_sum = 0.0
        for i in range(self.N):
            constraint_sum += (kw.core.quicksum([self.x[i, j] for j in range(self.J)]) - 1) **2
        return constraint_sum

    def solve(self, lambda_values=[10.0, 20.0, 50.0, 100.0]):
        """求解优化问题"""
        # 创建变量
        self.x = kw.core.ndarray((self.N, self.J), "x", kw.core.Binary)

        best_constraint_violation = float('inf')
        best_obj_val = float('inf')

        for lambda_val in lambda_values:
            # 构建目标函数和约束
            objective = self.build_objective(lambda_val)
            one_hot_constraint = self.build_one_hot_constraint()

            # 计算惩罚系数
            try:
                penalty = kw.qubo.get_min_penalty_for_equal_constraint(objective, one_hot_constraint)
            except AttributeError:
                try:
                    penalty = kw.qubo.get_min_penalty(objective, one_hot_constraint)
                except AttributeError:
                    max_obj_coeff = max(
                        max([abs(self.alpha * j * self.R[i]) for i in range(self.N) for j in range(self.J)]),
                        max([abs(-self.alpha * (self.A_dot_B[i] + self.C_dot_D[i]) * j) for i in range(self.N) for j in range(self.J)])
                    )
                    penalty = max_obj_coeff * 10

            # 构建QUBO模型并求解
            qubo_expr = objective + penalty * one_hot_constraint
            qubo_model = kw.qubo.QuboModel()
            qubo_model.set_objective(qubo_expr)

            solver = kw.solver.SimpleSolver(kw.classical.SimulatedAnnealingOptimizer())
            sol_dict, qubo_val = solver.solve_qubo(qubo_model)

            # 验证解
            x_val = kw.core.get_array_val(self.x, sol_dict)
            choices = []
            for i in range(self.N):
                selected_js = [j for j in range(self.J) if x_val[i, j] > 0.5]
                choices.append(selected_js[0] if len(selected_js) == 1 else -1)

            total_j = sum(choices)
            j_sum_violation = abs(total_j - self.target_sum_j)
            one_hot_violation = kw.core.get_val(one_hot_constraint, sol_dict)
            total_violation = j_sum_violation + one_hot_violation

            # 更新最优解
            if total_violation < best_constraint_violation or \
               (total_violation == best_constraint_violation and j_sum_violation == 0 and qubo_val < best_obj_val):
                best_constraint_violation = total_violation
                best_obj_val = qubo_val
                self.best_solution = choices[:]
                self.best_total_j = total_j

        return self.best_solution, self.best_total_j

    def heuristic_fix(self):
        """启发式修复约束违反"""
        if self.best_total_j == self.target_sum_j:
            return self.best_solution

        excess = self.best_total_j - self.target_sum_j
        fixed_choices = self.best_solution[:]

        if excess > 0:
            # 按j值降序排列，优先减少大的j值
            sorted_funds = sorted(range(self.N), key=lambda i: fixed_choices[i], reverse=True)
            for i in sorted_funds:
                if excess <= 0:
                    break
                if fixed_choices[i] > 0:
                    reduce_amount = min(fixed_choices[i], excess)
                    fixed_choices[i] -= reduce_amount
                    excess -= reduce_amount

        return fixed_choices