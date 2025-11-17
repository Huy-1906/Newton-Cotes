# Source code/Function/drawingMesh.py
import matplotlib.pyplot as plt
import numpy as np
def drawingMesh(ax, nodeCoordinates, elementNodes, elementType, plotStyle):
    """
    Vẽ lưới (chỉ các đường viền) trên một trục (ax) đã cho.
    """
    ax.set_aspect('equal')
    
    if elementType.upper() == 'Q4':
        numberElements = elementNodes.shape[0]
        for e in range(numberElements):
            # Lấy chỉ số 0-based
            indices = elementNodes[e, :] - 1
            
            # Thêm nút đầu tiên vào cuối để khép kín
            draw_indices = np.append(indices, indices[0])
            
            # Lấy tọa độ
            X_coords = nodeCoordinates[draw_indices, 0]
            Y_coords = nodeCoordinates[draw_indices, 1]
            
            ax.plot(X_coords, Y_coords, plotStyle, linewidth=1)
    else:
        # Logic cho phần tử 2 nút (nếu cần)
        pass
    
    ax.set_xlabel('Toa do X')
    ax.set_ylabel('Toa do Y')
    ax.grid(True)