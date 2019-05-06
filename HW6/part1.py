import numpy as np

A = np.matrix([[1., 1., 1.], [2., 3., -1], [3., -1., -2.]])
Ainv = np.linalg.inv(A)

xyz = Ainv * np.matrix([[8.], [2.], [-5.]])
print(f'x = {xyz[0, 0]:.1f}')
print(f'y = {xyz[1, 0]:.1f}')
print(f'z = {xyz[2, 0]:.1f}')

