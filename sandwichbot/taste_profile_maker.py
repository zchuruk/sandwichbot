import csv
import pandas as pd
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
profile_csv_path = os.path.join(dir_path, '../data/users/profiles')

## Load pat.csv to determine the number of sando types
pat_csv_path = os.path.join(profile_csv_path, 'pat.csv')

with open(pat_csv_path, 'r') as f:
    data = csv.reader(f, delimiter=',', quotechar='|')
    NUM_SANDO_TYPES = -1
    for row in data:
        NUM_SANDO_TYPES += 1

NUM_SANDO_TYPES = 10

def make_taste_matrices(names):
    ''' Make taste matrices for a given list of names

    Parameters
    ------------
    names : list
        List of names.

    Returns
    -----------
    deliciousness :

    '''
    ## Create empty arrays of number of rows = number of sando types
    ## number of columns = number of names
    global NUM_SANDO_TYPES
    deliciousness = np.zeros((len(names), NUM_SANDO_TYPES))
    heaviness = np.zeros((len(names), NUM_SANDO_TYPES))
    reliability = np.zeros((len(names), NUM_SANDO_TYPES))

    for name in names:
        n_index = names.index(name)
        csv_path = os.path.join(profile_csv_path, (name + '.csv'))
        with open(csv_path, 'r') as f:
            df = pd.read_csv(csv_path)
            deliciousness[n_index] = df['deliciousness'].transpose()
            heaviness[n_index] = df['heaviness'].transpose()
            reliability[n_index] = df['reliability'].transpose()

    return deliciousness, heaviness, reliability

if __name__ == "__main__":
    d, h, r = make_taste_matrices(['pat', 'jeremy'])
    print(d, h, r)
