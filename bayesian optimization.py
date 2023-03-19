#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 07:08:52 2023

@author: briansheehan
"""



from Backtester_load_par import backtester_load_par

from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.utils import use_named_args



from skopt.utils import use_named_args

# Define the objective function that takes in the settings and returns the finish_bal value
@use_named_args([
    Real(0.01, 1.0, name='close_stop'),
    Real(0.01, 1.0, name= "open_greater")
])
def objective(**params):
    output_dict = {k: v for k, v in params.items()}
    finish_bal = backtester_load_par(output_dict)
    return -finish_bal # Return negative value since gp_minimize minimizes the objective function

# Define the search space for each of the settings
search_space = [
    Real(0.01, 1.0, name='close_stop'),
    Real(0.01, 1.0, name='open_greater')
]

# Run Bayesian optimization
result = gp_minimize(objective, search_space, n_calls=100, random_state=0, n_jobs=-1)

# Print the optimal settings and finish_bal value
print("Optimal settings: {}".format(dict(zip(['close_stop', 'open_greater'], result.x))))
print("Optimal finish_bal: {}".format(-result.fun))


