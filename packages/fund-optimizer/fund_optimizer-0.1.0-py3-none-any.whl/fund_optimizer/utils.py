# fund_optimizer/utils.py
import numpy as np

def generate_sample_data(N, J, d1, d2, seed=42):
    """生成示例数据用于测试"""
    np.random.seed(seed)
    R = np.random.rand(N) * 10
    A = np.random.randn(N, d1)
    C = np.random.randn(N, d2)
    B = np.random.randn(d1)
    D = np.random.randn(d2)
    return R, A, C, B, D

def calculate_metrics(solution, alpha, A, B, C, D):
    """计算优化结果的评估指标"""
    w_actual = np.array([alpha * j if j != -1 else 0.0 for j in solution])
    A_weighted = np.dot(w_actual, A)
    C_weighted = np.dot(w_actual, C)
    dist_AB_sq = np.sum((A_weighted - B)** 2)
    dist_CD_sq = np.sum((C_weighted - D) **2)
    return {
        "w_actual": w_actual,
        "dist_AB_sq": dist_AB_sq,
        "dist_CD_sq": dist_CD_sq
    }