# Source code/Function/stresses2D.py
import numpy as np
import matplotlib.pyplot as plt
from shapeFunctionQ4 import shapeFunctionQ4
from Jacobian import Jacobian
from drawingField import drawingField
from drawingMesh import drawingMesh

def stresses2D(GDof, numberElements, elementNodes, numberNodes, nodeCoordinates,
               displacements, UX, UY, C, scaleFactor):
    
    stressPoints = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    numberStressPoints = stressPoints.shape[0]
    
    # [số pt, số điểm, 3 thành phần (xx, yy, xy)]
    stress = np.zeros((numberElements, numberStressPoints, 3))
    
    for e in range(numberElements):
        indice_1based = elementNodes[e, :]
        indice_0based = indice_1based - 1
        elementDof = np.concatenate([indice_0based, indice_0based + numberNodes])
        nn = len(indice_0based) # = 4
        
        for q in range(numberStressPoints):
            pt = stressPoints[q, :]
            xi, eta = pt[0], pt[1]
            
            shape, naturalDerivatives = shapeFunctionQ4(xi, eta)
            Jacob, invJacobian, XYDerivatives = Jacobian(nodeCoordinates[indice_0based, :], naturalDerivatives)
            
            B = np.zeros((3, 2 * nn))
            B[0, 0:nn] = XYDerivatives[:, 0].T
            B[1, nn:2*nn] = XYDerivatives[:, 1].T
            B[2, 0:nn] = XYDerivatives[:, 1].T
            B[2, nn:2*nn] = XYDerivatives[:, 0].T
            
            strain = B @ displacements[elementDof]
            stress[e, q, :] = (C @ strain).flatten()
            
    # Tính trung bình ứng suất tại các nút
    nodalStress_xx = np.zeros(numberNodes)
    nodeCount = np.zeros(numberNodes)
    
    for e in range(numberElements):
        indice_1based = elementNodes[e, :]
        indice_0based = indice_1based - 1
        for q in range(numberStressPoints):
            node_index = indice_0based[q] # Chỉ số nút tổng thể (0-based)
            stress_value = stress[e, q, 0] # Lấy sigma_xx
            
            nodalStress_xx[node_index] += stress_value
            nodeCount[node_index] += 1
            
    # Tính trung bình (tránh chia cho 0)
    non_zero_nodes = np.where(nodeCount > 0)[0]
    nodalStress_xx[non_zero_nodes] = nodalStress_xx[non_zero_nodes] / nodeCount[non_zero_nodes]

    # Vẽ biểu đồ ứng suất
    fig, ax = plt.subplots(figsize=(12, 5))
    deformed_coords = nodeCoordinates + scaleFactor * np.hstack((UX, UY))
    
    # 1. Vẽ trường màu
    # Dùng vmin, vmax để khớp thang màu của sách
    vmin = -2.5e7
    vmax = 2.5e7
    drawingField(ax, deformed_coords, elementNodes, 'Q4', nodalStress_xx)
    
    # 2. Đặt bảng màu (colormap)
    plt.set_cmap('jet')
    
    # 3. Vẽ lưới
    drawingMesh(ax, deformed_coords, elementNodes, 'Q4', 'k-')
    drawingMesh(ax, nodeCoordinates, elementNodes, 'Q4', 'k--')
    
    # 4. Thêm thanh màu (colorbar)
    cbar = plt.colorbar(ax.collections[0], ax=ax)
    cbar.set_label('Sigma XX stress')
    
    ax.set_title('Sigma XX stress (on deformed shape)')
    ax.axis('off')
    plt.show()