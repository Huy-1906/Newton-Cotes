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
# TEST CASE 1: HÀM ĐA THỨC (Để kiểm tra độ chính xác và so sánh)
# (Thực hiện yêu cầu iv: "multiple test cases, comparative studies")
# ==============================================================================
def test_case_1_polynomial():
    print("="*70)
    print(" TEST CASE 1: HÀM ĐA THỨC ĐƠN GIẢN (ĐỂ KIỂM TRA SAI SỐ)")
    print("="*70)
    
    # 1. Định nghĩa bài toán
    L = 6.0       # Chiều dài
    n = 60        # Số khoảng chia (Phải là bội của 2 VÀ 3 để chạy cả 3 PP)
    h = L / n     # Bước nhảy (kích thước "phần tử")
    
    # 2. Tạo "Lưới" (Tương tự 'nodeCoordinates')
    # Tạo n+1 điểm nút
    x_nodes = np.linspace(0, L, n + 1)
    
    # 3. Tạo Dữ liệu
    # Định nghĩa hàm f(x) = x^3 + 0.5*x^2 + 10
    def ham_f(x):
        return x**3 + 0.5*x**2 + 10
        
    y_values = ham_f(x_nodes)
    
    # 4. Tính kết quả chính xác bằng Giải tích
    # Nguyên hàm F(x) = (1/4)x^4 + (0.5/3)x^3 + 10x
    def ham_F(x):
        return (1/4)*x**4 + (0.5/3)*x**3 + 10*x
        
    Q_exact = ham_F(L) - ham_F(0)
    
    # 5. Gọi các hàm từ thư viện 
    Q_trapezoidal = trapezoidal_composite(y_values, h)
    Q_simpson_1_3 = simpson_1_3_composite(y_values, h)
    Q_simpson_3_8 = simpson_3_8_composite(y_values, h)
    
    # 6. In kết quả 
    print(f"Khoảng tích phân: [0, {L}], Số khoảng chia n = {n}, h = {h:.4f}")
    print("\n--- Bảng so sánh kết quả (Test Case 1) ---")
    print(f"Kết quả GIẢI TÍCH (Chính xác): {Q_exact:<20.8f}")
    print("-" * 50)
    print(f"Q (Hình thang):   {Q_trapezoidal:<20.8f} | Sai số: {abs(Q_trapezoidal - Q_exact):.2e}")
    print(f"Q (Simpson 1/3):  {Q_simpson_1_3:<20.8f} | Sai số: {abs(Q_simpson_1_3 - Q_exact):.2e}")
    print(f"Q (Simpson 3/8):  {Q_simpson_3_8:<20.8f} | Sai số: {abs(Q_simpson_3_8 - Q_exact):.2e}")
    
    # 7. Vẽ đồ thị (Phần "Visual Elements" cho báo cáo)
    plot_results(x_nodes, y_values, "Test Case 1 - Ham Da Thuc")
    print("\nĐã lưu hình ảnh 'Test_Case_1_Ham_Da_Thuc.png'.")
    
if __name__ == "__main__":
    test_case_1_polynomial()