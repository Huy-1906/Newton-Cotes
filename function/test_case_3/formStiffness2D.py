# Source code/Function/formStiffness2D.py
import numpy as np
from gaussQuadrature import gaussQuadrature
from shapeFunctionQ4 import shapeFunctionQ4
from Jacobian import Jacobian

def formStiffness2D(GDof, numberElements, elementNodes, numberNodes, nodeCoordinates, C, rho, thickness):
    stiffness = np.zeros((GDof, GDof))
    mass = np.zeros((GDof, GDof))
    
    gaussWeights, gaussLocations = gaussQuadrature('complete')
    
    for e in range(numberElements):
        indice_1based = elementNodes[e, :]
        indice_0based = indice_1based - 1 # 0-based
        
        elementDof = np.concatenate([indice_0based, indice_0based + numberNodes])
        ndof = len(indice_0based) # = 4
        
        for q in range(gaussWeights.shape[0]):
            GaussPoint = gaussLocations[q, :]
            xi, eta = GaussPoint[0], GaussPoint[1]
            
            shape, naturalDerivatives = shapeFunctionQ4(xi, eta)
            
            Jacob, invJacobian, XYDerivatives = Jacobian(nodeCoordinates[indice_0based, :], naturalDerivatives)
            
            B = np.zeros((3, 2 * ndof))
            B[0, 0:ndof] = XYDerivatives[:, 0].T
            B[1, ndof:2*ndof] = XYDerivatives[:, 1].T
            B[2, 0:ndof] = XYDerivatives[:, 1].T
            B[2, ndof:2*ndof] = XYDerivatives[:, 0].T
            
            # Ma trận độ cứng
            ix = np.ix_(elementDof, elementDof)
            detJacob = np.linalg.det(Jacob)
            stiffness[ix] += (B.T @ C * thickness @ B) * gaussWeights[q] * detJacob
            
            # Ma trận khối
            N_w = shape @ shape.T
            ix_m = np.ix_(indice_0based, indice_0based)
            ix_m_theta = np.ix_(indice_0based + numberNodes, indice_0based + numberNodes)
            
            mass[ix_m] += N_w * rho * thickness * gaussWeights[q] * detJacob
            mass[ix_m_theta] += N_w * rho * thickness * gaussWeights[q] * detJacob
            
    return stiffness, mass