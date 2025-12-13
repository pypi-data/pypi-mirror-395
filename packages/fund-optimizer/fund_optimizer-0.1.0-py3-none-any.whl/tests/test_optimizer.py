import unittest
from fund_optimizer import FundOptimizer
from fund_optimizer.utils import generate_sample_data

class TestFundOptimizer(unittest.TestCase):
    def test_basic_functionality(self):
        N = 3
        J = 5
        d1 = 2
        d2 = 3
        R, A, C, B, D = generate_sample_data(N, J, d1, d2)
        
        optimizer = FundOptimizer(N, J, d1, d2)
        optimizer.set_data(R, A, C, B, D)
        solution, total_j = optimizer.solve()
        
        self.assertEqual(len(solution), N)  # 解的长度应与基金数量一致

if __name__ == "__main__":
    unittest.main()