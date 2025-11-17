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

  ## Đồ thị và đầu ra

  - `plot_results(x, y, title)` lưu đồ 2D (vùng tô tích phân và điểm nút) cho mỗi test case.
  - `plot_heat_transfer_3D_and_integrand(...)` tạo mô phỏng 3D (khi có) và đồng thời vẽ hàm integrand `y(x)` với vùng tô, lưu ảnh `Mo_phong_truyen_nhiet_3D_va_tich_phan.png`.

  Kiểm tra thư mục `pic/` hoặc thư mục làm việc để lấy ảnh đầu ra.

  ## Cách chạy nhanh

  1) Cài thư viện (nếu chưa có):

  ```bash
  pip install numpy matplotlib scipy
  ```

  2) Chạy chương trình:

  ```bash
  python main.py
  ```

  3) Mở ảnh được lưu để xem đồ thị và mô phỏng 3D.

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

