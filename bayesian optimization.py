#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 07:08:52 2023

@author: briansheehan
"""



from ML_backtester import ml_backtester

from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.utils import use_named_args
import telegram_send

from skopt.utils import use_named_args
import time

# Start the timer
start_time = time.time()

# Define the objective function that takes in the settings and returns the finish_bal value
# @use_named_args([
#     Real(0.01, 1.0, name='close_stop'),
#     Real(0.01, 1.0, name= "last_close_per"),
# ])
# def objective(**params):
#     output_dict = {k: v for k, v in params.items()}
#     finish_bal = ml_backtester(output_dict)
#     return -finish_bal # Return negative value since gp_minimize minimizes the objective function

# # Define the search space for each of the settings
# search_space = [
#     Real(0.01, 1.0, name='close_stop'),
#     Real(0.01, 1.0, name= "last_close_per"),
# ]
@use_named_args([
    Real(0.01, .1, name='open_greater')
])
def objective(**params):
    output_dict = {k: v for k, v in params.items()}
    finish_bal = ml_backtester(output_dict)
    return -finish_bal # Return negative value since gp_minimize minimizes the objective function

# Define the search space for each of the settings
search_space = [
    Real(0.01, .1, name='open_greater')
]

# Run Bayesian optimization
result = gp_minimize(objective, search_space, n_calls=100, random_state=0, n_jobs=-1)

# Print the optimal settings and finish_bal value
print("Optimal settings: {}".format(dict(zip(['open_greater'], result.x))))
print("Optimal finish_bal: {}".format(-result.fun))
telegram_send.send(messages=["Bayesian optimization back test complete............"])
end_time = time.time()
execution_time = end_time - start_time
print("Execution time: {:.2f} seconds".format(execution_time))



