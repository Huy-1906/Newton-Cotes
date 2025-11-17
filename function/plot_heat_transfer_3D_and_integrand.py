# BỔ SUNG CÁC IMPORT CẦN THIẾT
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import ScalarMappable 

def plot_heat_transfer_3D_and_integrand(x_nodes, k_values, y_values, L, k_func, dT_dx_func):
    """
    Hàm vẽ NÂNG CẤP cho Test Case 2:
    1. (Trên) Đồ thị 3D mô phỏng tấm vật liệu, với Z=T(x) và màu=k(x).
    2. (Dưới) Đồ thị 2D của hàm f(x) = k(x)*dT/dx(x) và diện tích tích phân Q.
    """
    fig = plt.figure(figsize=(12, 14)) # Tăng chiều cao
    fig.suptitle('Ứng dụng Newton-Cotes cho Truyền nhiệt (3D)', fontsize=18, weight='bold')

    # --- AX1: Mô phỏng 3D vật liệu ---
    ax1 = fig.add_subplot(2, 1, 1, projection='3d')
    ax1.set_title('Mô phỏng 3D: Tấm Vật liệu', fontsize=16)

    # Tính hàm nhiệt độ T(x) bằng cách lấy nguyên hàm của dT/dx
    # dT/dx = -5 * (10 - x) = -50 + 5x
    # T(x) = -50x + (5/2)*x^2 + C. Giả sử T(0) = 100 (C=100)
    def T_func(x, T0=100):
        return T0 - 50*x + 2.5*x**2

    # Tạo lưới 2D (X, Y) cho tấm vật liệu
    y_plate = np.linspace(0, 5, 10) # Tạo chiều rộng 5m cho tấm
    X, Y = np.meshgrid(x_nodes, y_plate)
    
    # Tính giá trị Z (Nhiệt độ) và Màu (Hệ số k)
    T_values_mesh = T_func(X)
    K_values_mesh = k_func(X) # k(x) không đổi theo y
    
    # Thiết lập colormap
    cmap_name = 'jet' 
    cmap = cm.get_cmap(cmap_name)
    norm = Normalize(vmin=np.min(k_values), vmax=np.max(k_values))
    
    # Vẽ bề mặt 3D
    # Z là T(x), màu là k(x)
    surf = ax1.plot_surface(X, Y, T_values_mesh, 
                            facecolors=cmap(norm(K_values_mesh)), 
                            shade=False, rstride=1, cstride=1,
                            antialiased=False)
    
    # Thêm colorbar
    m = ScalarMappable(cmap=cmap, norm=norm) 
    m.set_array(k_values) # Dùng mảng 1D k_values
    cbar = fig.colorbar(m, ax=ax1, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('Hệ số truyền nhiệt k(x) (W/mK)', fontsize=12)

    ax1.set_xlabel('Vị trí x (m)', fontsize=12)
    ax1.set_ylabel('Chiều rộng Y (m)', fontsize=12)
    ax1.set_zlabel('Nhiệt độ T(x) (°C)', fontsize=12)
    ax1.view_init(elev=20., azim=-60) # Đặt góc nhìn

    # --- AX2: Đồ thị Hàm tích phân f(x) = k(x) * dT/dx(x) ---
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(x_nodes, y_values, 'o-', label='Hàm f(x) = k(x) * dT/dx(x)', 
             markersize=3, linewidth=1, color='blue')
    ax2.fill_between(x_nodes, y_values, alpha=0.3, color='skyblue',
                     label='Diện tích tích phân Q (Dòng nhiệt tổng)')
    ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax2.set_xlabel('Vị trí x (m)', fontsize=12)
    ax2.set_ylabel('Giá trị hàm f(x)', fontsize=12)
    ax2.set_title('Hàm Dưới Tích phân và Dòng Nhiệt Q', fontsize=16)
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"Mo_phong_truyen_nhiet_3D_va_tich_phan.png")
    plt.show()