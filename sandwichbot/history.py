import csv
import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

from sandwich import Sandwich

def history_filename(name):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  history_csv_path = os.path.join(dir_path, '../data/users/history')
  return os.path.join(history_csv_path, f'{name}.csv')

def today():
  return datetime.today().strftime('%Y-%m-%d')

def init_history(name):
  filename = history_filename(name)
  headers = [today()] + list(map(lambda s: s.get_name(), list(Sandwich)))
  pd.DataFrame(data=np.array([headers])).to_csv(filename, mode='a', index=False, header=False)

def add_history(name, sandos):
  # Initialize history file
  filename = history_filename(name)
  if (not os.path.exists(filename)):
    init_history(name)

  # Append new row to history
  sandwiches_eaten = list(map(Sandwich.from_name, sandos))
  history = pd.read_csv(history_filename(name))
  new_row = [today()]
  for col in history.columns[1:]: 
    if (Sandwich.from_name(col) in sandwiches_eaten):
      new_row.append(1)
    else:
      new_row.append(0)
  pd.DataFrame(data=np.array([new_row])).to_csv(filename, mode='a', index=False, header=False)

def get_history_matrix(names, days):
  group_history = []
  for name in names:
    history = pd.read_csv(history_filename(name))
    last_n_days = np.array(history.tail(days))
    group_history.append(last_n_days)
  print(np.array(group_history))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add history for a users sandwiches.')
    parser.add_argument('num_people', type=int, help='The number of people who ate sandos today')
    args = parser.parse_args()
    
    for i in range(args.num_people):
      name = input("Identify yourself: ")
      sandos = input("Which sandos did you eat today?: ").split(',')
      add_history(name, sandos)

    print("Thank you for your service")