import numpy as np

def simpson_3_8_composite(y_values, h):
    """
    Tính tích phân tổng hợp bằng Quy tắc Simpson 3/8.
    Hàm này được viết để "mô phỏng" cấu trúc lắp ráp (assembly) của FEM.
    
    Args:
        y_values (np.array): Mảng các giá trị f(x) tại các điểm nút.
        h (float): Khoảng cách đều giữa các điểm (step size).
        
    Returns:
        float: Giá trị tích phân xấp xỉ.
    """
    n = len(y_values) - 1
    if n < 3:
        return np.nan # Không thể thực hiện

    # Yêu cầu: n phải là bội số của 3
    if n % 3 != 0:
        print(f"Lỗi Simpson 3/8: Số khoảng chia 'n'={n} phải là bội số của 3.")
        return np.nan

    total_integral = 0.0

    # Vòng lặp "Lắp ráp" (Assembly loop):
    # Tương tự như 'for i in range(0, numberElements)' trong code FEM.
    # Chúng ta lặp qua từng "siêu phần tử" (gồm 3 khoảng) một.
    # i sẽ là 0, 3, 6, 9, ...
    for i in range(0, n, 3):
        
        # Lấy 4 điểm nút cho "phần tử" này
        y0 = y_values[i]
        y1 = y_values[i+1]
        y2 = y_values[i+2]
        y3 = y_values[i+3]
        
        # Tính "đóng góp" của phần tử này (tương tự 'k1' hoặc 'f1' trong FEM)
        # Đây là công thức Simpson 3/8 cho 1 đoạn (3 khoảng)
        segment_integral = (3 * h / 8) * (y0 + 3*y1 + 3*y2 + y3)
        
        # "Lắp ráp": Cộng đóng góp vào kết quả toàn cục
        # Tương tự 'stiffness[idx] += k1'
        total_integral += segment_integral
        
    return total_integral