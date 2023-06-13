# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 23:55:09 2023

@author: brian
"""

# from sklearn.model_selection import ParameterGrid
# import subprocess

# Define the parameter grid
param_grid = {
    'mac': [0, 5, 10],
    'main_or_all': ['main', 'all'],
    'filter_by_dates_on': [0, 1],
    'start_date': ['2020-01-01', '2021-01-01', '2022-01-01'],
    'end_date': ['2021-12-31', '2022-12-31', '2023-12-31'],
    'insample_per_on': [0, 1],
    'split_per': [0.5, 0.6, 0.7],
    'return_start': [0, 1],
    'random_insample_on': [0, 1],
    'random_insample_start': [0, 1],
    'random_insample_per': [0.1, 0.2, 0.25],
    'volume_min': [-999999, 0],
    'pm_vol_set': [0, 1],
    'yclose_to_open_percent_filter': [20, 40, 60],
}

# Generate all possible combinations of parameter values
param_list = list(ParameterGrid(param_grid))

# Loop over all parameter combinations
results = []
for params in param_list:
    # Run the backtester with the current parameter values
    command = ['python', 'backtester.py'] + [f"--{key}={value}" for key, value in params.items()]
    output = subprocess.check_output(command, universal_newlines=True)
    finish_bal = float(output.strip())
    
    # Store the results for the current parameter combination
    results.append((params, finish_bal))

# Find the parameter combination with the highest finish_bal
best_params, best_finish_bal = max(results, key=lambda x: x[1])
print(f"The best combination of parameters is: {best_params}")
print(f"The highest finish_bal is: {best_finish_bal}")
