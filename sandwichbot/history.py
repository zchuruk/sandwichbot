import csv
import os
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

def add_history(name, sando):
  # Initialize history file
  filename = history_filename(name)
  if (not os.path.exists(filename)):
    init_history(name)

  # Append new row to history
  history = pd.read_csv(history_filename(name))
  new_row = [today()]
  for col in history.columns[1:]: 
    if (Sandwich.from_name(col) == Sandwich.from_name(sando)):
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

# init_history('zach')
add_history('zach', 'v')
# get_history_matrix(['pat'], 2)