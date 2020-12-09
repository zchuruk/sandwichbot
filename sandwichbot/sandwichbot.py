import argparse
import copy
import enum
import math
import numpy as np

from taste_profile_maker import make_taste_matrices
from sandwich import Sandwich

SIGMA_D = 1.0
SIGMA_H = 1.0
SIGMA_R = 1.0

def fd(deliciousness_value):
    # deliciousness function
    return deliciousness_value

def fh(heaviness_value):
    # heaviness function
    x = heaviness_value
    a = 1 # height
    b = 0.5 # x offset
    c = 0.2 # std dev
    d = 0 # y offset
    return a * np.exp(-(x - b)**2 / (2 * c**2)) + d

def fr(reliability_value):
    # reliability function
    return reliability_value

def satisfaction(x, D, H, R):
    # optimization function

    deliciousness_agg = np.mean(np.matmul(D, x)) / len(x)
    heaviness_agg = np.mean(np.matmul(H, x)) / len(x)
    reliability_agg = np.mean(np.matmul(R, x)) / len(x)

    S = SIGMA_D * fd(deliciousness_agg) + SIGMA_H * fh(heaviness_agg) + SIGMA_R * fr(reliability_agg)
    return S

def rec_optimize(x_curr, n, D, H, R, max_val_in, x_max_in):
    x_max = x_max_in
    max_val = max_val_in
    for i in range(len(x_curr)):
        x = copy.copy(x_curr)
        x[i] += 1
        if sum(x) == n:
            val = satisfaction(x, D, H, R)
            # print(val)
            # print(x)
            if val > max_val:
                x_max = copy.copy(x)
                max_val = val
        else:
            max_val, x_max = rec_optimize(x, n, D, H, R, max_val, x_max)
    # print(max_val)
    return max_val, x_max

def run_optimization(n, D, H, R):
    x0 = np.zeros(len(Sandwich))
    max_val = -100
    x_max = x0

    max_val, x_max = rec_optimize(x0, n, D, H, R, max_val, x_max)
    return x_max

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A bot to select sandwiches.')
    parser.add_argument('num_sandwiches', type=int, help='The number of sandwiches being ordered')
    parser.add_argument('people', type=str, nargs='+', help='The people ordering the sandwiches')

    args = parser.parse_args()

    D, H, R = make_taste_matrices(args.people)

    best_sandwiches = run_optimization(args.num_sandwiches, D, H, R)
    print(best_sandwiches)