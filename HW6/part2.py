import numpy as np

A = np.matrix([[1/2, -1/2, 1], [-1/2, 1/2+1/3+1/5, 0], [1., 0., 0.]])
Ainv = np.linalg.inv(A)

xyz = Ainv * np.matrix([[0], [0], [5.]])
print(f'v1  = {xyz[0, 0]:.3f}')
print(f'v2  = {xyz[1, 0]:.3f}')
print(f'i13 = {xyz[2, 0]:.3f}')

