# Source code/Function/rectangularMesh.py
import numpy as np

def rectangularMesh(Lx, Ly, numberElementsX, numberElementsY):
    xx = np.linspace(0, Lx, numberElementsX + 1)
    yy = np.linspace(0, Ly, numberElementsY + 1)
    
    XX, YY = np.meshgrid(xx, yy)
    nodeCoordinates = np.vstack([XX.ravel(), YY.ravel()]).T
    
    numberNodesInRow = numberElementsX + 1
    numberNodes = nodeCoordinates.shape[0]
    numberElements = numberElementsX * numberElementsY
    elementNodes = np.zeros((numberElements, 4), dtype=int)
    
    counter = 0
    for j in range(numberElementsY):
        for i in range(numberElementsX):
            i1 = (j * numberNodesInRow) + i
            i2 = i1 + 1
            i4 = i1 + numberNodesInRow
            i3 = i2 + numberNodesInRow
            
            # Trả về chỉ số 1-based để khớp với logic MATLAB/Python
            elementNodes[counter, :] = [i1 + 1, i2 + 1, i3 + 1, i4 + 1]
            counter += 1
            
    return nodeCoordinates, elementNodes