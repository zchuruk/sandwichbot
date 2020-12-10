import csv
import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from sandwich import Sandwich

def history_filename(name):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  history_csv_path = os.path.join(dir_path, '../data/users/history')
  return os.path.join(history_csv_path, f'{name}.csv')

def string_date(datetime):
  return datetime.strftime('%Y-%m-%d')

def from_string_date(stringdate):
  return datetime.strptime(stringdate, '%Y-%m-%d')

def init_history(name):
  filename = history_filename(name)
  headers = [string_date(datetime.today())] + list(map(lambda s: s.get_name(), list(Sandwich)))
  pd.DataFrame(data=np.array([headers])).to_csv(filename, mode='a', index=False, header=False)

def add_history(name, sandos):
  # Initialize history file
  filename = history_filename(name)
  if (not os.path.exists(filename)):
    init_history(name)

  # Append new row to history
  sandwiches_eaten = list(map(Sandwich.from_name, sandos))
  history = pd.read_csv(history_filename(name))
  current_date = string_date(datetime.today())
  new_row = [current_date]
  for col in history.columns[1:]: 
    if (Sandwich.from_name(col) in sandwiches_eaten):
      new_row.append(1)
    else:
      new_row.append(0)
  pd.DataFrame(data=np.array([new_row])).to_csv(filename, mode='a', index=False, header=False)

def get_history_matrix(names, days):
  group_history = []
  for name in names:
    filename = history_filename(name)
    # Initialize history file
    if (not os.path.exists(filename) or os.stat(filename).st_size == 0):
      init_history(name)

    rows_for_name = []
    history = pd.read_csv(filename)
    current_row_num = history.shape[0] - 1
    current_date = datetime.today() - timedelta(days=1)
    for i in range(days):
      rows_for_day = np.zeros(history.shape[1] - 1)
      # move backwards until we reach the following day
      current_row = history.iloc[current_row_num]
      row_date = from_string_date(current_row[0])
      while (row_date >= current_date and current_row_num >= 1):
        # aggregate over all rows who are after current day
        rows_for_day = np.add(rows_for_day, np.array(current_row[1:]))
        # decrement row
        current_row_num -= 1
        current_row = history.iloc[current_row_num]
        row_date = from_string_date(current_row[0])
      # add data for this day, decrement day
      rows_for_name.append(rows_for_day)
      current_date -= timedelta(days=1)
    group_history.append(rows_for_name)
  print(np.array(group_history))

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Add history for a users sandwiches.')
#     parser.add_argument('num_people', type=int, help='The number of people who ate sandos today')
#     args = parser.parse_args()
    
#     for i in range(args.num_people):
#       name = input("Identify yourself: ")
#       sandos = input("Which sandos did you eat today?: ").split(',')
#       add_history(name, sandos)

#     print("Thank you for your service")

# add_history('jeremy', ['blt', 'Valencia'])
# add_history('jeremy', ['mb', 'Valencia'])
# add_history('jeremy', ['blt', 'mb'])
# add_history('jeremy', ['fb', 'ww'])
get_history_matrix(['jeremy'], 3)