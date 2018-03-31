#!/bin/python3

"""
Python script for solving the Frog in Maze challenge on Hackerrank:
https://www.hackerrank.com/challenges/frog-in-maze/problem
"""

import sys
sys.setrecursionlimit(10001)

obstacle = '#'
start = 'A'
mine = '*'
exitcode = '%'
freecell = 'O'
tunnel = 'T'

n, m, k = input().strip().split(' ')
n, m, k = [int(n), int(m), int(k)]

maze = {}
for i in range(n):
    row = input().strip()
    for j in range(m):
        maze[(i,j)] = row[j]
        # remember start
        if maze[(i,j)] == start:
            alef_start = (i,j)
            maze[(i,j)] = freecell

tunnels = {}
for i in range(k):
    i1, j1, i2, j2 = input().strip().split(' ')
    i1, j1, i2, j2 = [int(i1)-1, int(j1)-1, int(i2)-1, int(j2)-1]
    tunnels[(i1, j1)] = (i2, j2)
    tunnels[(i2, j2)] = (i1, j1)
    # mark tunnels
    maze[(i1, j1)] = tunnel
    maze[(i2, j2)] = tunnel

def gauss(A):
    # Gaussian elimination
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x

def get_valid_adjacent_cells(p):
    # returns all adjacent cells Alef can go to
    i,j = p
    adj = []

    if i > 0 and maze[(i-1,j)] != obstacle:
        adj.append((i-1,j))
    if i < n-1 and maze[(i+1,j)] != obstacle:
        adj.append((i+1,j))
    if j > 0 and maze[(i,j-1)] != obstacle:
        adj.append((i,j-1))
    if j < m-1 and maze[(i,j+1)] != obstacle:
        adj.append((i,j+1))

    return adj

def index(p):
    # return matrix index for coordinate
    return m*p[0] + p[1]

# generate coefficient matrix via BFS
mat = [[0 for j in range(n*m+1)] for i in range(n*m)]
for i in range(n*m):
    mat[i][i] = 1

queue = [alef_start]
num_exits = 0
while queue:
    pos = queue.pop(0)
    i = index(pos)
    if mat[i][i] == -1:
        continue
    mat[i][i] = -1

    if maze[pos] == mine:
        continue
    if maze[pos] == exitcode:
        mat[i][n*m] = -1
        num_exits += 1
        continue

    adj_cells = get_valid_adjacent_cells(pos)
    num_adj_cells = len(adj_cells)

    # Alef is stuck
    if num_adj_cells == 0:
        continue

    # free cell with valid adjacent cells, build equation
    for c in adj_cells:
        if maze[c] == tunnel:
            mat[i][index(tunnels[c])] = 1.0/num_adj_cells
            queue.append(tunnels[c])
        else:
            mat[i][index(c)] = 1.0/num_adj_cells
            queue.append(c)

# retrieve result
if num_exits == 0:
    print(0)
else:
    x = gauss(mat)
    print(x[index(alef_start)])
