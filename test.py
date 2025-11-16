import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import simpson # Import thư viện chuẩn Scipy để so sánh
from matplotlib.colors import Normalize
from matplotlib import cm # Import 'cm' để dùng colormap và ScalarMappable
from mpl_toolkits.mplot3d import Axes3D # Import thư viện vẽ 3D

# ==============================================================================
# PHẦN 1: THƯ VIỆN HÀM TÍNH TOÁN (Không thay đổi)
# ==============================================================================

def trapezoidal_composite(y_values, h):
    """Tính tích phân tổng hợp bằng Quy tắc Hình thang."""
    n = len(y_values) - 1
    if n < 1:
        return 0
    integral = (h / 2) * (y_values[0] + 2 * np.sum(y_values[1:-1]) + y_values[-1])
    return integral

def simpson_1_3_composite(y_values, h):
    """Tính tích phân tổng hợp bằng Quy tắc Simpson 1/3."""
    n = len(y_values) - 1
    if n < 2:
        return np.nan
    if n % 2 != 0:
        print(f"Lỗi Simpson 1/3: Số khoảng chia 'n'={n} phải là số chẵn.")
        return np.nan
    sum_odd_indices = np.sum(y_values[1:-1:2])
    sum_even_indices = np.sum(y_values[2:-1:2])
    integral = (h / 3) * (y_values[0] + 4 * sum_odd_indices + 2 * sum_even_indices + y_values[-1])
    return integral

def simpson_3_8_composite(y_values, h):
    """Tính tích phân tổng hợp bằng Quy tắc Simpson 3/8."""
    n = len(y_values) - 1
    if n < 3:
        return np.nan
    if n % 3 != 0:
        print(f"Lỗi Simpson 3/8: Số khoảng chia 'n'={n} phải là bội số của 3.")
        return np.nan
    total_integral = 0.0
    for i in range(0, n, 3):
        y0 = y_values[i]
        y1 = y_values[i+1]
        y2 = y_values[i+2]
        y3 = y_values[i+3]
        segment_integral = (3 * h / 8) * (y0 + 3*y1 + 3*y2 + y3)
        total_integral += segment_integral
    return total_integral

# ==============================================================================
# PHẦN 2: CÁC HÀM VẼ ĐỒ THỊ (Sửa đổi Test Case 2, bỏ Test Case 3)
# ==============================================================================

def plot_function_and_integral(x_nodes, y_values, title, integral_value=None):
    """Hàm vẽ đồ thị đơn giản cho Test Case 1."""
    plt.figure(figsize=(10, 6))
    plt.plot(x_nodes, y_values, 'o-', label='Hàm f(x) được tích phân', 
             markersize=3, linewidth=1, color='blue')
    plt.fill_between(x_nodes, y_values, alpha=0.3, color='skyblue',
                     label=f'Diện tích tích phân Q = {integral_value:.4f}' if integral_value is not None else 'Diện tích tích phân Q')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title(title, fontsize=16)
    plt.xlabel('Biến độc lập x', fontsize=12)
    plt.ylabel('Giá trị hàm f(x)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{title.replace(' ', '_')}.png") 
    plt.show()


# Hàm plot_volume_of_revolution đã bị XÓA

# ==============================================================================
# PHẦN 3: CODE CHẠY CHÍNH (Bỏ Test Case 3)
# ==============================================================================

def test_case_1_polynomial():
    """Test Case 1: Dùng 1 hàm đa thức đơn giản để kiểm tra sai số."""
    print("="*70)
    print(" TEST CASE 1: HÀM ĐA THỨC ĐƠN GIẢN (ĐỂ KIỂM TRA SAI SỐ)")
    print("="*70)
    
    L = 6.0       # Chiều dài
    n = 60        # Số khoảng chia (Phải là bội của 2 VÀ 3)
    h = L / n     # Bước nhảy
    x_nodes = np.linspace(0, L, n + 1)
    
    def ham_f(x):
        return x**3 + 0.5*x**2 + 10
    y_values = ham_f(x_nodes)
    
    def ham_F(x):
        return (1/4)*x**4 + (0.5/3)*x**3 + 10*x
    Q_exact = ham_F(L) - ham_F(0)
    
    Q_trapezoidal = trapezoidal_composite(y_values, h)
    Q_simpson_1_3 = simpson_1_3_composite(y_values, h)
    Q_simpson_3_8 = simpson_3_8_composite(y_values, h)
    
    print(f"Khoảng tích phân: [0, {L}], Số khoảng chia n = {n}, h = {h:.4f}")
    print("\n--- Bảng so sánh kết quả (Test Case 1) ---")
    print(f"Kết quả GIẢI TÍCH (Chính xác): {Q_exact:<20.8f}")
    print("-" * 50)
    print(f"Q (Hình thang):   {Q_trapezoidal:<20.8f} | Sai số: {abs(Q_trapezoidal - Q_exact):.2e}")
    print(f"Q (Simpson 1/3):  {Q_simpson_1_3:<20.8f} | Sai số: {abs(Q_simpson_1_3 - Q_exact):.2e}")
    print(f"Q (Simpson 3/8):  {Q_simpson_3_8:<20.8f} | Sai số: {abs(Q_simpson_3_8 - Q_exact):.2e}")
    
    plot_function_and_integral(x_nodes, y_values, 
                               "Test Case 1 - Ham Da Thuc (Tich phan Q)", 
                               integral_value=Q_simpson_3_8)
    print("\nĐã lưu hình ảnh 'Test_Case_1_Ham_Da_Thuc_(Tich_phan_Q).png'.")

def test_case_2_heat_transfer():
    """Test Case 2: Ứng dụng thực tế vào bài toán truyền nhiệt."""
    print("\n" + "="*70)
    print(" TEST CASE 2: BÀI TOÁN TRUYỀN NHIỆT (ỨNG DỤNG THỰC TẾ)")
    print("="*70)
    
    L = 10.0      # Chiều dài tấm vật liệu (m)
    n = 90        # Số khoảng chia (Phải là bội của 2 VÀ 3)
    h = L / n     # Bước nhảy
    x_nodes = np.linspace(0, L, n + 1)
    
    # Định nghĩa hàm k(x) và dT/dx(x)
    def k_func(x):
        return 20 * (1 + 0.1 * x**2)
    def dT_dx_func(x):
        return -5 * (10 - x)
        
    k_values = k_func(x_nodes)
    dT_dx_values = dT_dx_func(x_nodes)
    y_values = k_values * dT_dx_values # Hàm f(x) cần tích phân
    
    Q_trapezoidal = trapezoidal_composite(y_values, h)
    Q_simpson_1_3 = simpson_1_3_composite(y_values, h)
    Q_simpson_3_8 = simpson_3_8_composite(y_values, h)
    Q_scipy = simpson(y_values, x=x_nodes) 
    
    print(f"Khoảng tích phân: [0, {L}], Số khoảng chia n = {n}, h = {h:.4f}")
    print("\n--- Bảng so sánh kết quả (Test Case 2) ---")
    print("Lưu ý: Hàm f(x) là đa thức bậc 3, Simpson 1/3 và 3/8 cho kết quả chính xác.")
    print(f"Q (Hình thang):   {Q_trapezoidal:<20.8f}")
    print(f"Q (Simpson 1/3):  {Q_simpson_1_3:<20.8f}")
    print(f"Q (Simpson 3/8):  {Q_simpson_3_8:<20.8f}")
    print(f"Q (Scipy Simpson):{Q_scipy:<20.8f}")
    print(f"Sự khác biệt (Scipy vs Của bạn): {abs(Q_simpson_3_8 - Q_scipy):.2e}")
    
    # Gọi hàm vẽ 3D MỚI
    plot_heat_transfer_3D_and_integrand(x_nodes, k_values, y_values, L, 
                                        k_func, dT_dx_func)
    print("\nĐã lưu hình ảnh 'Mo_phong_truyen_nhiet_3D_va_tich_phan.png'.")

# Hàm test_case_3_volume_of_revolution đã bị XÓA

# ==============================================================================
# PHẦN 4: CHẠY CHÍNH
# ==============================================================================
if __name__ == "__main__":
    
    test_case_1_polynomial()
    test_case_2_heat_transfer()
    # test_case_3_volume_of_revolution() # Đã XÓA