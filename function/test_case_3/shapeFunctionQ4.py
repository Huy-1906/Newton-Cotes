# Source code/Function/shapeFunctionQ4.py
import numpy as np

def shapeFunctionQ4(xi, eta):
    # shape: Hàm dạng (4, 1)
    # naturalDerivatives: Đạo hàm (4, 2)
    
    shape = 0.25 * np.array([
        (1 - xi) * (1 - eta),
        (1 + xi) * (1 - eta),
        (1 + xi) * (1 + eta),
        (1 - xi) * (1 + eta)
    ]).reshape(-1, 1) # Đảm bảo là vector cột (4,1)
    
    naturalDerivatives = 0.25 * np.array([
        [-(1 - eta), -(1 - xi)],
        [ (1 - eta), -(1 + xi)],
        [ (1 + eta),  (1 + xi)],
        [-(1 + eta),  (1 - xi)]
    ]) # Kích thước (4,2)
    
    return shape, naturalDerivatives