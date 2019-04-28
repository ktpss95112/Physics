import sys
import numpy as np

# assume that there are 10 nodes
# and there are 4 batteries
"""
matrix:
    + v1 = 0
    | node b
    | node c
    | ...
    | battery 1
    | battery 2
    + ...
"""
matrix = np.matrix([ [ 0. for _ in range(14) ] for _ in range(14) ])
values = np.matrix([ [0.] for _ in range(14) ])
battery_index = 10

# v1 = 0
matrix[0, 0] = 1

count = 1
for line in sys.stdin:
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
        if ni != 0:
            matrix[ni, battery_index] += 1
        matrix[nj, battery_index] -= 1
        matrix[battery_index, ni] += 1
        matrix[battery_index, nj] -= 1
        values[battery_index, 0] = value
        battery_index += 1

# print(matrix)

ans = np.matmul(np.linalg.inv(matrix), values)
print(ans)



