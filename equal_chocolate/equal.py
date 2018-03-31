#!/bin/python3

"""
Python script for solving the equal chocolate problem on Hackerrank:
https://www.hackerrank.com/challenges/equal/problem
"""

import sys

def equal(n,arr,baseline_adjustment=0):
    arr_sorted = sorted(arr)
    arr_sorted[0] -= baseline_adjustment
    count = (baseline_adjustment > 0)
    i = 0
    while True:
        i += 1
        if i == n:
            break
        if arr_sorted[i-1] == arr_sorted[i]:
            continue

        for k in [5,2,1]:
            rounds = (arr_sorted[i] - arr_sorted[i-1]) // k
            count += rounds
            # giving everyone else chocolate is the same as taking away chocolate from the remaining person in terms of equality
            arr_sorted[i] -= k*rounds

    return count

if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename,"r")
    fout = open('results_' + filename, "w")
    t = int(f.readline().strip())
    for a0 in range(t):
        n = int(f.readline().strip())
        arr = list(map(int, f.readline().strip().split(' ')))
        result = min([equal(n,arr,baseline_adjustment=i) for i in [0,1,2]])
        fout.write(str(result) + '\n')
    f.close()
    fout.close()

    # t = int(input().strip())
    # for a0 in range(t):
    #     n = int(input().strip())
    #     arr = list(map(int, input().strip().split(' ')))
    #     result = min([equal(n,arr,baseline_adjustment=i) for i in [0,1,2]])
    #     print(result)
