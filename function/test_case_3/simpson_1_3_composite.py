import numpy as np

"""
    Tính tích phân tổng hợp bằng Quy tắc Simpson 1/3.
    
    Args:
        y_values (np.array): Mảng các giá trị f(x) tại các điểm nút.
        h (float): Khoảng cách đều giữa các điểm (step size).
        
    Returns:
        float: Giá trị tích phân xấp xỉ.
"""
def simpson_1_3_composite(y_values, h):
    n = len(y_values) - 1
    if n < 2:
        return np.nan # Không thể thực hiện

    # Yêu cầu: n phải là số chẵn (số điểm n+1 là số lẻ)
    if n % 2 != 0:
        print(f"Lỗi Simpson 1/3: Số khoảng chia 'n'={n} phải là số chẵn.")
        return np.nan

    # Công thức: h/3 * (f0 + 4*f1 + 2*f2 + 4*f3 + ... + 4*f(n-1) + fn)
    integral = 0
    
    # Lấy các điểm hệ số 4 (1, 3, 5, ...)
    sum_odd_indices = np.sum(y_values[1:-1:2])
    
    # Lấy các điểm hệ số 2 (2, 4, 6, ...)
    sum_even_indices = np.sum(y_values[2:-1:2])
    
    integral = (h / 3) * (y_values[0] + 4 * sum_odd_indices + 2 * sum_even_indices + y_values[-1])
    
    return integral