#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 07:08:52 2023

@author: briansheehan
"""

import itertools


from Backtester_load_par import backtester_load_par

from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.utils import use_named_args



from skopt.utils import use_named_args

# Define the objective function that takes in the settings and returns the finish_bal value
@use_named_args([
    Real(0.01, 1.0, name='close_stop'),
    Real(0.5, 10.0, name='min_between_price'),
    Real(5.0, 50.0, name='max_between_price')
])
def objective(**params):
    output_dict = {k: v for k, v in params.items()}
    finish_bal = backtester_load_par(output_dict)
    return -finish_bal # Return negative value since gp_minimize minimizes the objective function

# Define the search space for each of the settings
search_space = [
    Real(0.01, .5, name='close_stop'),
    Real(0.5, 5.0, name='min_between_price'),
    Real(5.0, 20.0, name='max_between_price')
]

# Run Bayesian optimization
result = gp_minimize(objective, search_space, n_calls=50, random_state=0)

# Print the optimal settings and finish_bal value
print("Optimal settings: {}".format(dict(zip(['close_stop', 'min_between_price', 'max_between_price'], result.x))))
print("Optimal finish_bal: {}".format(-result.fun))


