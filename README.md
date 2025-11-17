# Phương Pháp Tính Tích Phân Số: Newton–Cotes

Bài tập lớn này triển khai ba phương pháp tính tích phân số phổ biến:

## Nội dung chính

Mục tiêu: triển khai và so sánh ba phương pháp tích phân lưới đều (composite):
  ---

File mô tả các thuật toán Newton–Cotes (composite closed), giao diện hàm trong thư mục `function/`, cách chạy `main.py`, và nghiệm phân tích cho hai test case.

  ## Những file chính 

  - `test_case_1.py` — Chạy test case 1 và lưu đồ thị
  - `test_case_2.py` — Chạy test case 2 và lưu đồ thị tấm vật liệu truyền nhiệt 
  - `function/trapezoidal_composite.py` — hàm `trapezoidal_composite(y_values, h)`
  - `function/simpson_1_3_composite.py` — hàm `simpson_1_3_composite(y_values, h)`
  - `function/simpson_3_8_composite.py` — hàm `simpson_3_8_composite(y_values, h)`
  - `function/plot_results.py` — hàm `plot_results(x, y, title)` lưu đồ 2D cho mỗi test case
  - `function/plot_heat_transfer_3D_and_integrand.py` — hàm `plot_heat_transfer_3D_and_integrand(x_nodes, k_values, y_values, L, k_func, dT_dx_func)` tạo mô phỏng 3D + đồ thị hàm dưới tích phân và lưu ảnh

  Ảnh kết quả theo code hiện tại sẽ được lưu (ví dụ) dưới tên như `Test_Case_1_Ham_Da_Thuc.png` và `Mo_phong_truyen_nhiet_3D_va_tich_phan.png` trong thư mục làm việc hoặc `pic/` nếu bạn đặt đầu ra ở đó.

  ## Tóm tắt thuật toán (Newton–Cotes closed / composite)

  Chia đoạn [a,b] thành n khoảng đều, h=(b-a)/n, và lấy các nút x_i = a + i h.

  - Composite Trapezoidal:

  $$\int_a^b f(x)\,dx \approx \frac{h}{2}\left(f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n)\right).$$

  - Composite Simpson 1/3 (yêu cầu n chẵn):

  $$\int_a^b f(x)\,dx \approx \frac{h}{3}\left(f(x_0) + 4\sum_{i\;odd} f(x_i) + 2\sum_{i\;even,\;i\ne0,n} f(x_i) + f(x_n)\right).$$

  - Composite Simpson 3/8 (yêu cầu n bội của 3):

  $$\int_a^b f(x)\,dx \approx \frac{3h}{8}\left(f(x_0) + 3\sum_{i\not\equiv0\; (\mathrm{mod}\;3)} f(x_i) + 2\sum_{i\equiv0\; (\mathrm{mod}\;3),\;i\ne0,n} f(x_i) + f(x_n)\right).$$

  Trong repository, mỗi hàm nhận mảng `y_values` (f(x) tại các nút đều) và `h` rồi trả về một số thực là xấp xỉ tích phân.

  ## Contract (giao diện hàm)

  - Input:
    - `y_values`: numpy array chứa f(x_0), ..., f(x_n) (độ dài n+1)
    - `h`: bước lưới (float)
  - Output:
    - float: xấp xỉ tích phân trên [a,b]

  Yêu cầu:

  - `len(y_values) == n+1`
  - Simpson 1/3: `n` chẵn
  - Simpson 3/8: `n` chia hết cho 3

  Nếu muốn hỗ trợ mọi `n`, có thể kết hợp Simpson 1/3 và 3/8 tự động (tùy chọn nâng cấp).

  ## Hai test case (giải tay để đối chứng)

  Phần này tóm tắt nghiệm phân tích dùng trong `main.py` để bạn kiểm tra kết quả số.

  ### Test Case 1 — Hàm đa thức

  - Hàm: $f(x)=x^{3}+0.5x^{2}+10$, khoảng \([0,6]\), chọn \(n=60\) (\(h=0.1\)).

  - Nguyên hàm: $F(x)=\frac{1}{4}x^{4}+\frac{0.5}{3}x^{3}+10x$
  - Giá trị chính xác (tính bằng giải tích):

  $$
  Q_{\mathrm{exact}} = F(6) - F(0) = 324 + 36 + 60 = 420.
  $$

  Khi chạy `main.py` với \(n=60\), các kết quả số (trapezoid / Simpson) phải xấp xỉ \(420\); Simpson thường cho sai số nhỏ hơn.

  ### Test Case 2 — Bài toán truyền nhiệt

  - Định nghĩa trong `main.py`:
    - $k(x)=20(1+0.1x^{2})=20+2x^{2}$
    - $\dfrac{dT}{dx}=-5(10-x)=-50+5x$
    - Hàm dưới tích phân: $y(x)=k(x)\,\dfrac{dT}{dx}=(20+2x^{2})(-50+5x)$

  - Khai triển:

  $$
  y(x) = -1000 + 100x -100x^{2} + 10x^{3}.
  $$

  - Tích phân trên [0,10]:

  $$
  \int_0^{10} y(x)\,dx = -10000 + 5000 - \frac{100000}{3} + 25000 = -\frac{40000}{3}.
  $$

  Vì trong `main.py` ta lấy dấu âm theo luật Fourier ($Q = -∫k \dfrac{dT}{dx}$), nên

  $$
  Q = -\left(-\frac{40000}{3}\right) = \frac{40000}{3} \approx 13333.3333.
  $$

  Đây là nghiệm phân tích dùng để so sánh với kết quả số (khi n đủ lớn).

  ### Test Case 3 — FEM (Tính tổng lực phân bố và mô phỏng 2D)

  - Mục tiêu: sử dụng Newton–Cotes để tích phân hàm tải phân bố theo mép dầm (ví dụ parabolic),
    sau đó dùng tổng lực P tính được làm tải cho mô phỏng phần tử hữu hạn (FEM) 2D. Test Case 3
    minh họa một ứng dụng thực tế của tích phân số: chuyển một phân bố tải liên tục thành một lực
    rời rạc để sử dụng trong lưới phần tử.

  - Tóm tắt quy trình trong `test_casse_3.py`:
    - Tạo phân bố tải `q(y)` parabolic trên mép (ví dụ `P_peak = -1.5e6` N/m), lưới tích phân 1D trên `y in [0, Ly]`.
    - Dùng `simpson_1_3_composite(q_values, h_integral)` để tính tổng lực `P_calculated`.
    - Phân bố `P_calculated` lên các nút mép phải của lưới FEM, ráp ma trận độ cứng, áp điều kiện biên, giải hệ,
      và vẽ lưới biến dạng + trường dịch chuyển.

  - File kết quả: `Test_Case_3_Mo_phong_ung_suat_phang.png` (hình lưới biến dạng với màu biểu diễn dịch chuyển UX).

  ## Mô tả chi tiết các module trong `function/test_case_3/`

  Dưới đây là mô tả ngắn gọn về từng file trong `function/test_case_3/` — vai trò, giao diện chính (inputs/outputs),
  và các phụ thuộc quan trọng.

  - `rectangularMesh.py`:
    - Vai trò: sinh lưới chữ nhật đều cho miền 2D (tạo `nodeCoordinates` và `elementNodes`).
    - Giao diện: `rectangularMesh(Lx, Ly, nx, ny)` → `(nodeCoordinates, elementNodes)`.

  - `shapeFunctionQ4.py`:
    - Vai trò: cung cấp hàm hình dạng và đạo hàm cho phần tử Q4 (4 nút).
    - Giao diện: `shapeFunctionQ4(xi, eta)` → `(N, dN_dxi, dN_deta)`.

  - `gaussQuadrature.py`:
    - Vai trò: trả về điểm Gauss và trọng số cho tích phân trên phần tử (1D hoặc 2D).
    - Giao diện: `gaussQuadrature(order)` → `(points, weights)`.

  - `Jacobian.py`:
    - Vai trò: tính ma trận Jacobian, định thức và nghịch đảo để biến đổi đạo hàm từ hệ xi-eta sang hệ x-y.
    - Giao diện: `Jacobian(dN_dxi, node_coords)` → `(J, detJ, invJ)`.

  - `formStiffness2D.py`:
    - Vai trò: lắp ráp ma trận độ cứng toàn cục (và ma trận khối lượng nếu cần) bằng cách lặp qua các phần tử,
      sử dụng `shapeFunctionQ4`, `gaussQuadrature` và `Jacobian` để tính ma trận phần tử.
    - Giao diện: `formStiffness2D(GDof, numberElements, elementNodes, numberNodes, nodeCoordinates, C, rho, thickness)` → `(stiffness, mass)`.

  - `solution.py`:
    - Vai trò: áp điều kiện biên, giải hệ tuyến tính và trả về vectơ dịch chuyển đầy đủ.
    - Giao diện: `solution(GDof, prescribedDof, stiffness, force)` → `displacements`.

  - `drawingMesh.py` và `drawingField.py`:
    - Vai trò: hàm trợ giúp hiển thị lưới (mesh) và trường (field) trên Matplotlib; thường gọi `drawingMesh(ax, coords, elems, 'Q4', style)`
      và `drawingField(ax, coords, elems, 'Q4', values)`.

  - `stresses2D.py`:
    - Vai trò: tính ứng suất (σ_xx, σ_yy, σ_xy) từ vectơ dịch chuyển và ma trận vật liệu `C` tại điểm Gauss hoặc nút.

  - `plot_results.py` (được tinh chỉnh cho FEM):
    - Vai trò: lưu/hiển thị các hình ảnh hậu xử lý (ví dụ contour, deformed mesh) phù hợp với output của `test_casse_3.py`.

  - `simpson_1_3_composite.py`, `simpson_3_8_composite.py`, `trapezoidal_composite.py` (bản trong `test_case_3`):
    - Vai trò: cùng chức năng Newton–Cotes như các bản chính; sử dụng trực tiếp để tích phân q(y) hoặc các hàm 1D khác.

  - Ghi chú: nhiều module phụ thuộc lẫn nhau — ví dụ `formStiffness2D.py` gọi `gaussQuadrature`, `Jacobian` và `shapeFunctionQ4`.
    Kiểm tra đường dẫn và import khi di chuyển các file hoặc khi chuẩn hóa thư viện.


  ## Đồ thị và đầu ra

  - `plot_results(x, y, title)` lưu đồ 2D (vùng tô tích phân và điểm nút) cho mỗi test case.
  - `plot_heat_transfer_3D_and_integrand(...)` tạo mô phỏng 3D (khi có) và đồng thời vẽ hàm integrand `y(x)` với vùng tô, lưu ảnh `Mo_phong_truyen_nhiet_3D_va_tich_phan.png`.


  ## Gợi ý mở rộng

  - Tự động kết hợp Simpson 1/3 và 3/8 nếu `n` không thỏa yêu cầu.
  - Thêm kiểm tra đầu vào cho `y_values` và `h` để báo lỗi rõ ràng nếu không đúng chuẩn.
  - Tạo một notebook Jupyter minh họa từng bước tính theo ô (trapezoid/Simpson) để dùng trong báo cáo.

  ---



## Lưu ý và mở rộng

- Nếu `n` không phù hợp với Simpson 1/3 hoặc 3/8, có thể kết hợp các quy tắc (ví dụ dùng Simpson 1/3 cho phần lớn và Simpson 3/8 cho phần dư).
- Kiểm tra thứ tự `y_values` và giá trị `h` luôn đúng (h = (b-a)/n).

## Chạy chương trình

1) Cài đặt thư viện:

```bash
pip install numpy matplotlib scipy
```

2) Chạy:

```bash
python main.py
```

3) Các đồ thị sẽ được lưu (xem thư mục làm việc hoặc `pic/`).

