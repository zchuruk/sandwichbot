import argparse
import copy
import enum
import math
import pandas
import numpy as np

import pulp
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
    a = 1 # height
    b = 0.5 # x offset
    c = 0.2 # std dev
    d = 0 # y offset
    return a * np.exp(-(heaviness_value - b)**2 / (2 * c**2)) + d

def fr(reliability_value):
    # reliability function
    return reliability_value

def satisfy(q, D, H, R):
    mppl = D.shape[0]
    nsandos = D.shape[1]

    # Create the model
    model = pulp.LpProblem(name="satisfy", sense=pulp.LpMaximize)

    # Initialize the decision variables
    # X = pulp.LpVariable.dicts("X", (names, sandwich_names), lowBound=0, upBound=q, cat='Continuous')
    X = [[pulp.LpVariable(f'X_{m}_{n}', lowBound = 0, upBound = q / mppl, cat='Continuous') \
            for n in range(nsandos)] \
                for m in range(mppl)]
    # X = []
    # for m in range(mppl):
    #     row = []
    #     for n in range(nsandos):
    #         row.append(pulp.LpVariable(f'X_{m}_{n}', lowBound=0, upBound=q, cat='Continuous'))
    #     X.append(row)

    # Add the constraints to the model
    # model += (2 * X + y <= 20, "frequency")
    # model += (4 * X - 5 * y >= -10, "rechage")
    model += (pulp.lpSum([X[m][n] for m in range(mppl) for n in range(nsandos)]) == q, "total")
    # for m in range(mppl):
    #     for n in range(nsandos):
    #         model += (X[m][n] <= q / mppl, f'fair_split_{m}_{n}')

    # Add the objective function to the model
    model  += SIGMA_D * fd(np.mean(np.multiply(X, D))) \
            + SIGMA_H * fd(np.mean(np.multiply(X, H)))**2 \
            + SIGMA_R * fr(np.mean(np.multiply(X, R)))

    # Solve the problem
    # status = model.solve(pulp.GUROBI(msg = 0))
    status = model.solve()
    print(model)


    print(f"status: {model.status}, {pulp.LpStatus[model.status]}")
    print(f"satisfaction: {model.objective.value()}")

    result = [[e.value() for e in row]  for row in X]
    return result, model.objective.value()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A bot to select sandwiches.')
    parser.add_argument('num_sandwiches', type=int, help='The number of sandwiches being ordered')
    parser.add_argument('people', type=str, nargs='+', help='The people ordering the sandwiches')

    args = parser.parse_args()

    D, H, R = make_taste_matrices(args.people)
    
    # optimize
    result, satisfaction = satisfy(args.num_sandwiches, D, H, R)

    # print results
    sandwich_names = list(map(lambda s: s.get_name(), list(Sandwich)))
    out = pandas.DataFrame(result, columns = sandwich_names, index = args.people)
    print(f'\n{"-" * 30} Satisfaction Score: {satisfaction} {"-" * 30}\n')
    print(out)

        