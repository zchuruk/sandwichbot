import argparse
import enum
import math
import numpy as np

from taste_profile_maker import make_taste_matrices

SIGMA_D = 1.0
SIGMA_H = 1.0
SIGMA_R = 1.0

class Sandwich(enum.IntEnum):
    GUS_SPECIAL = 0
    WILD_WEST = 1
    VALENCIA = 2
    PANHANDLE = 3
    KEZAR = 4
    QUAKE = 5
    FLASHBACK_REUBEN = 6
    MEATBALL = 7
    BLT = 8
    PALL_MALL = 9

def construct_sandwich_str(opt_output):
    sandwich_choices = []
    for i, val in enumerate(best_sandwiches):
        if val == 1:
            sandwich_choices.append(Sandwich(i))
    len(sandwich_choices)

    sandwich_choices_str = str(sandwich_choices[0])
    for i, enum_val in enumerate(sandwich_choices[1:]):
        if (i + 1) == len(sandwich_choices):
            sandwich_choices_str += ' and'
        sandwich_choices_str += ' '
        sandwich_choices_str += str(enum_val)
    return sandwich_choices_str

def fd(deliciousness_value):
    # deliciousness function
    return 2 * deliciousness_value - 1

def fh(heaviness_value):
    # heaviness function
    x = heaviness_value
    a = 1 # height
    b = 0.5 # x offset
    c = 0.2 # std dev
    d = 0 # y offset
    return a * np.exp(-(x - b)**2 / (2 * c**2)) - d

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


def run_optimization(n, m, D, H, R):
    max_val = 0
    best_sandwiches = np.zeros(len(Sandwich))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                x = np.zeros(len(Sandwich))
                x[i] += 1
                x[j] += 1
                x[k] += 1
                satisfaction_val = satisfaction(x, D, H, R)
                if satisfaction_val > max_val:
                    best_sandwiches = x
                    max_val = satisfaction_val
    return best_sandwiches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A bot to select sandwiches.')
    parser.add_argument('num_sandwiches', type=int, help='The number of sandwiches being ordered')
    parser.add_argument('people', type=str, nargs='+', help='The people ordering the sandwiches')

    args = parser.parse_args()

    print(args.num_sandwiches)
    print(args.people)

    D, H, R = make_taste_matrices(args.people)

    best_sandwiches = run_optimization(args.num_sandwiches, len(args.people), D, H, R)
    sandwich_str = construct_sandwich_str(best_sandwiches)

    print(f'Your optimal sandwiches are {sandwich_str}. Happy eatin!')
