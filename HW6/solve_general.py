import sys
import numpy as np
np.set_printoptions(precision=3, linewidth=120)

# assume nodes are consecutive integers start from 1 to N
# assume the input is a valid circuit diagram
# assume all inputs are integer (i.e. no float)

inputs = sys.stdin.read().split('\n')[:-1]
node_exist = {}
battery_exist = {}
for line in inputs:
    ni, nj, is_resistor, value = map(int, line.split())
    node_exist[ni] = node_exist.get(ni, 0)
    node_exist[nj] = node_exist.get(nj, 0)
    if not is_resistor: battery_exist[(ni, nj)] = 0

matrix_size = len(node_exist) + len(battery_exist)

"""
matrix:
    + v1 = 0
    | node 2
    | node 3
    | ...
    | battery 1
    | battery 2
    + ...
"""
matrix = np.matrix([ [ 0. for _ in range(matrix_size) ] for _ in range(matrix_size) ])
values = np.matrix([ [0.] for _ in range(matrix_size) ])
labels = [f'V{i}' for i in range(1, len(node_exist)+1)]
battery_index = len(node_exist)

# v1 = 0
matrix[0, 0] = 1

for line in inputs:
    ni, nj, is_resistor, value = map(int, line.split())
    ni -= 1 # zero base
    nj -= 1 # zero base

    if is_resistor:
        if ni != 0:
            matrix[ni, ni] += (1 / value)
            matrix[ni, nj] -= (1 / value)
        matrix[nj, ni] -= (1 / value)
        matrix[nj, nj] += (1 / value)
    else:
        labels.append(f'I{ni},{nj}')
        if ni != 0:
            matrix[ni, battery_index] += 1
        matrix[nj, battery_index] -= 1
        matrix[battery_index, ni] += 1
        matrix[battery_index, nj] -= 1
        values[battery_index, 0] = value
        battery_index += 1
    # print(matrix, '\n')

# print(matrix)

ans = np.matmul(np.linalg.inv(matrix), values)
for i in range(matrix_size):
    print(f'{labels[i]}\t= {ans[i, 0]:.3f}')



