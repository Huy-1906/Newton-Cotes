# Source code/Function/drawingField.py
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

def drawingField(ax, nodeCoordinates, elementNodes, elementType, valueField):
    """
    Vẽ biểu đồ trường (contour plot) cho các phần tử Q4.
    """
    numberElements = elementNodes.shape[0]
    patches = []
    
    for e in range(numberElements):
        indices = elementNodes[e, :] - 1 # 0-based
        
        # Lấy tọa độ
        element_coords = nodeCoordinates[indices, :]
        
        # Tạo một đa giác (patch)
        polygon = Polygon(element_coords, closed=True)
        patches.append(polygon)

    # Tạo một PatchCollection và đặt dữ liệu màu
    # valueField là giá trị tại các nút, ta lấy trung bình cho mỗi phần tử
    # Lấy giá trị trung bình tại 4 nút của mỗi phần tử
    element_colors = np.mean(valueField[elementNodes - 1], axis=1)
    
    p = PatchCollection(patches, edgecolors='none')
    p.set_array(element_colors)
    ax.add_collection(p)
    
    # Đặt chế độ tô màu
    ax.set_aspect('equal')
