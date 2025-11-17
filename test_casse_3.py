import numpy as np
import matplotlib.pyplot as plt
import sys 
sys.path.append('./function/test_case_3')  # Thêm thư mục 'function' vào đường dẫn hệ thống

# --- 1. IMPORT CÁC HÀM GIẢI BÀI TOÁN ỨNG SUẤT DẦM ---
from plot_results import * 
from drawingMesh import drawingMesh
from rectangularMesh import rectangularMesh
from formStiffness2D import formStiffness2D
from drawingField import drawingField
from stresses2D import stresses2D
from solution import solution
from gaussQuadrature import gaussQuadrature
from shapeFunctionQ4 import shapeFunctionQ4
from Jacobian import Jacobian

# --- 2. IMPORT CÁC HÀM NEWTON-COTES ---
from simpson_1_3_composite import * 
from simpson_3_8_composite import * 
from trapezoidal_composite import * 

# ==============================================================================
# PHẦN A: TÍNH TỔNG LỰC P
# ==============================================================================
print("\n" + "="*70)
print(" PHẦN A: TÍNH TỔNG TẢI TRỌNG (P)")
print("="*70)

# Định nghĩa hàm tải trọng phân bố q(y) dọc theo mép dầm
# Giả sử tải trọng là Parabolic, đạt đỉnh 1.5e6 N/m ở giữa
Ly_fem = 1.0 # Chiều cao dầm (từ problem18.py)
P_peak = -1.5e6 # Tải trọng đỉnh (N/m), âm để hướng xuống

def q_y_func(y):
    # Hàm parabolic: q(y) = P_peak * (1 - ( (y - Ly/2) / (Ly/2) )^2)
    mid = Ly_fem / 2.0
    return P_peak * (1 - ((y - mid) / mid)**2)

# Thiết lập lưới tích phân cho Newton-Cotes
n_integral = 90  # Số khoảng chia (phải chẵn cho Simpson 1/3)
h_integral = Ly_fem / n_integral
y_nodes_integral = np.linspace(0, Ly_fem, n_integral + 1)

# Lấy giá trị q(y) tại các nút
q_values = q_y_func(y_nodes_integral)

# Dùng Simpson 1/3 để tính tổng lực P
P_calculated = simpson_1_3_composite(q_values, h_integral)

print(f"Hàm tải trọng: Parabolic (đỉnh {P_peak} N/m)")
print(f"Tổng lực P tính bằng Simpson 1/3: {P_calculated:.2f} N")
print(f"(Đây sẽ là giá trị 'P' cho mô phỏng FEM)")

# ==============================================================================
# PHẦN B: MÔ PHỎNG FEM (DỰA TRÊN problem18.py)
# ==============================================================================
print("\n" + "="*70)
print(" PHẦN B: CHẠY MÔ PHỎNG FEM VỚI TẢI TRỌNG P ĐÃ TÍNH")
print("="*70)

# 1. Khai báo vật liệu
E = 10e7
poisson = 0.30
C = E / (1 - poisson**2) * np.array([
    [1, poisson, 0],
    [poisson, 1, 0],
    [0, 0, (1 - poisson) / 2]
])
# SỬ DỤNG PHẦN  TỪ NEWTON-COTES
P = P_calculated 

# 2. Tạo lưới (giống problem18.py)
Lx = 5.0
Ly = 1.0 # Phải khớp với Ly_fem ở trên
numberElementsX = 20
numberElementsY = 10
numberElements = numberElementsX * numberElementsY

nodeCoordinates, elementNodes = rectangularMesh(Lx, Ly, numberElementsX, numberElementsY)
xx = nodeCoordinates[:, 0]
yy = nodeCoordinates[:, 1]
numberNodes = xx.shape[0]

# 3. Khởi tạo hệ thống
GDof = 2 * numberNodes
rho = 1.0
thickness = 1.0

# 4. Phân tích
print("1. Dang lap rap ma tran do cung...")
stiffness, mass = formStiffness2D(GDof, numberElements, elementNodes, numberNodes, 
                                  nodeCoordinates, C, rho, thickness)

# 5. Điều kiện biên (Ngàm tại x=0)
fixedNodes_0based = np.where(nodeCoordinates[:, 0] == 0)[0]
prescribedDof_X = fixedNodes_0based
prescribedDof_Y = fixedNodes_0based + numberNodes
prescribedDof_0based = np.concatenate([prescribedDof_X, prescribedDof_Y])
prescribedDof = (prescribedDof_0based + 1).reshape(-1, 1)

# 6. Véc-tơ lực (tải phân bố ở mép phải, x=Lx)
# Code FEM sẽ phân bố tổng lực P này về các nút
force = np.zeros((GDof, 1))
rightBord_0based = np.where(nodeCoordinates[:, 0] == Lx)[0]
dofs_Y_right = rightBord_0based + numberNodes # DOF theo phương Y

# Phân bố tải P (giống problem18.py, dùng quy tắc Hình thang)
force[dofs_Y_right] = P * Ly / numberElementsY
force[dofs_Y_right[0]] = P * Ly / numberElementsY / 2.0
force[dofs_Y_right[-1]] = P * Ly / numberElementsY / 2.0

# 7. Giải hệ phương trình
print("2. Dang giai he phuong trinh...")
displacements = solution(GDof, prescribedDof, stiffness, force)

# 8. Xuất kết quả (giống problem18.py)
UX = displacements[0:numberNodes].reshape(-1, 1)
UY = displacements[numberNodes:GDof].reshape(-1, 1)
scaleFactor = 0.1 # Tăng hệ số khuếch đại để thấy võng

print("3. Dang ve bieu do chuyen vi UX...")
fig2, ax2 = plt.subplots(figsize=(10, 4))
deformed_coords = nodeCoordinates + scaleFactor * np.hstack((UX, UY))

drawingField(ax2, deformed_coords, elementNodes, 'Q4', UX.flatten())
plt.set_cmap('jet')
if ax2.collections:
    ax2.collections[0].set_cmap('jet')
drawingMesh(ax2, deformed_coords, elementNodes, 'Q4', 'k-')
drawingMesh(ax2, nodeCoordinates, elementNodes, 'Q4', 'k--')
cbar = plt.colorbar(ax2.collections[0], ax=ax2)
cbar.set_label('Chuyen vi UX')
ax2.set_title(f'FEM voi P = {P:.2f} N tai mep phai (x={Lx} m)')
ax2.axis('off')

#plot_results(y_nodes_integral, q_values, "Test Case 3 - Ham Tai Trong Parabolic")
#print("\nĐã lưu hình ảnh 'Test Case 3 - Mo_phong_ung_suat_phang.png'.")
fig2.savefig('Test_Case_3_Mo_phong_ung_suat_phang.png', dpi=300)
plt.show()