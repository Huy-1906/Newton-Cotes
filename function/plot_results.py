from matplotlib import pyplot as plt
"""Hàm trợ giúp để vẽ đồ thị cho báo cáo."""
def plot_results(x_nodes, y_values, title):
    plt.figure(figsize=(10, 6))
    plt.plot(x_nodes, y_values, 'o-', label='Hàm f(x) = k(x) * dT/dx', 
             markersize=3, linewidth=1)
    
    # Tô màu diện tích dưới đường cong
    plt.fill_between(x_nodes, y_values, alpha=0.3, 
                     label='Diện tích tích phân Q')
    
    plt.title(title, fontsize=16)
    plt.xlabel('Vị trí x (dọc theo vật liệu)', fontsize=12)
    plt.ylabel('Giá trị hàm f(x)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{title.replace(' ', '_')}.png") # Lưu hình ảnh cho báo cáo
    plt.show()