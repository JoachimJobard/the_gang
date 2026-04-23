import unittest
import numpy as np
from utils.loss_functions import kendall_tau_b

class TestKendallB(unittest.TestCase):
    def test_kendall_tau_b(self):
        x = np.array([1, 2, 3])
        y = np.array([1, 2, 3])
        result = kendall_tau_b(x, y)
        self.assertEqual(result, 1.0)
    
    def test_kendall_tau_b_discordant(self):
        x = np.array([1, 2, 3])
        y = np.array([3, 2, 1])
        result = kendall_tau_b(x, y)
        print(type(result))
        self.assertEqual(result, -1.0)
    
    def test_broadcast(self):
        x = np.array([1, 2, 3])
        print(x[:, None], x[None, :], x[:, None] - x[None, :])
