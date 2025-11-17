# Source code/Function/Jacobian.py
import numpy as np

def Jacobian(nodeCoordinates_element, naturalDerivatives):
    # nodeCoordinates_element: (4, 2)
    # naturalDerivatives: (4, 2)
    
    JacobianMatrix = nodeCoordinates_element.T @ naturalDerivatives
    invJacobian = np.linalg.inv(JacobianMatrix)
    XYDerivatives = naturalDerivatives @ invJacobian
    
    return JacobianMatrix, invJacobian, XYDerivatives