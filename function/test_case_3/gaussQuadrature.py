# Source code/Function/gaussQuadrature.py
import numpy as np

def gaussQuadrature(option):
    if option.lower() == 'complete': # 2x2
        locations = np.array([
            [-0.577350269189626, -0.577350269189626],
            [ 0.577350269189626, -0.577350269189626],
            [ 0.577350269189626,  0.577350269189626],
            [-0.577350269189626,  0.577350269189626]
        ])
        weights = np.array([1.0, 1.0, 1.0, 1.0])
    elif option.lower() == 'reduced': # 1x1
        locations = np.array([[0.0, 0.0]])
        weights = np.array([4.0])
    else:
        raise ValueError("Tùy chọn không hợp lệ. Chọn 'complete' hoặc 'reduced'.")
        
    return weights, locations