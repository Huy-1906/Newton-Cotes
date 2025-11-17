# .....................................................................
# Code Python cho phương pháp phần tử hữu hạn
# Tệp hàm: solution.py
# Chức năng: Bộ giải hệ phương trình tuyến tính [K][U] = [F]
# .....................................................................

# .....................................................................
# Thêm các thư viện cần thiết
# .....................................................................
import numpy as np
import sys # Dùng sys để thoát nếu có lỗi nghiêm trọng

# .....................................................................
# Định nghĩa hàm
# .....................................................................
def solution(GDof, prescribedDof, stiffness, force):
    """
    Giải hệ phương trình K*U = F sau khi áp dụng điều kiện biên.
    Phiên bản này sửa lỗi 'shape mismatch' và dùng np.linalg.solve.
    """
    
    # .................................................................
    # Tìm các bậc tự do (DOF)
    # .................................................................
    
    # Lấy danh sách tất cả các bậc tự do (0-based)
    all_dof = np.arange(GDof)
    
    # Chuyển các bậc tự do bị chặn (1-based, từ file MATLAB) về 0-based
    # và làm phẳng (flatten) thành mảng 1D
    try:
        prescribedDof_1d = prescribedDof.flatten() - 1
    except Exception as e:
        print(f"LỖI trong solution.py: 'prescribedDof' có vẻ không phải là mảng số.")
        print(f"Chi tiết: {e}")
        sys.exit()
    
    # Tìm các bậc tự do đang hoạt động (active) (0-based)
    activeDof = np.setdiff1d(all_dof, prescribedDof_1d)
    
    # .................................................................
    # Trích xuất ma trận con (Sub-matrixing)
    # .................................................................
    
    # Lấy ma trận độ cứng K của các DOF active
    try:
        stiffness_ff = stiffness[np.ix_(activeDof, activeDof)]
    except IndexError as e:
        print(f"LỖI trong solution.py: Lỗi Index khi lấy stiffness_ff.")
        print(f"Chi tiết: {e}")
        sys.exit()
        
    # Lấy vector lực F của các DOF active
    # Đảm bảo F_active là 1D (dạng (N,))
    force_f = force[activeDof].flatten()
    
    # .................................................................
    # Giải hệ phương trình
    # .................................................................
    
    try:
        # Giải K_active * U_active = F_active
        # displacements_f trả về là 1D array (ví dụ: shape (499,))
        displacements_f = np.linalg.solve(stiffness_ff, force_f)
    
    except np.linalg.LinAlgError:
        print("LỖI trong solution.py: Ma trận độ cứng suy biến (Singular Matrix).")
        print("Hệ phương trình không thể giải được.")
        return np.zeros((GDof, 1)) # Trả về mảng 0
    except ValueError as e:
        print(f"LỖI trong solution.py: Lỗi giá trị khi gọi np.linalg.solve.")
        print(f"Kiểm tra kích thước K_active ({stiffness_ff.shape}) và F_active ({force_f.shape}).")
        print(f"Chi tiết: {e}")
        sys.exit()

    # .................................................................
    # Lắp ráp lại vector chuyển vị đầy đủ
    # .................................................................
    
    # Khởi tạo vector chuyển vị 0 (dạng 2D column (GDof, 1))
    displacements = np.zeros((GDof, 1))
    
    # === SỬA LỖI SHAPE MISMATCH TẠI ĐÂY ===
    # 'displacements_f' là 1D (N,), 
    # nhưng 'displacements[activeDof]' là 2D (N, 1).
    # Chúng ta cần reshape 'displacements_f' thành vector cột (2D).
    
    displacements_f_column = displacements_f.reshape(-1, 1)
    
    # Gán kết quả (đã reshape) vào đúng vị trí
    # (N, 1) = (N, 1) -> OK
    displacements[activeDof] = displacements_f_column
    
    return displacements