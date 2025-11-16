import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path.append('./function')  # Thêm thư mục 'function' vào đường dẫn hệ thống

from scipy.integrate import simpson 
from simpson_1_3_composite import * 
from simpson_3_8_composite import * 
from plot_results import * 
from trapezoidal_composite import * 
from plot_heat_transfer_3D_and_integrand import * 

# ==============================================================================
# TEST CASE 2: BÀI TOÁN TRUYỀN NHIỆT (Ứng dụng thực tế)
# (Thực hiện yêu cầu i, v: "real-world relevance", "applications section")
# ==============================================================================
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
    
if __name__ == "__main__":
    test_case_2_heat_transfer()