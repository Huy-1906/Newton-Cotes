import numpy as np

def trapezoidal_composite(y_values, h):
    """
    Tính tích phân tổng hợp bằng Quy tắc Hình thang.
    
    Args:
        y_values (np.array): Mảng các giá trị f(x) tại các điểm nút.
        h (float): Khoảng cách đều giữa các điểm (step size).
        
    Returns:
        float: Giá trị tích phân xấp xỉ.
    """
    n = len(y_values) - 1
    if n < 1:
        return 0
        
    # Công thức: h/2 * (f0 + 2*f1 + 2*f2 + ... + 2*f(n-1) + fn)
    integral = (h / 2) * (y_values[0] + 2 * np.sum(y_values[1:-1]) + y_values[-1])
    
    return integral