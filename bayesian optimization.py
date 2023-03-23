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

# Define the objective function that takes in the settings and returns the finish_bal value
@use_named_args([
    Real(0, 200000000000, name='sharesfloat_min'),
    Real(0, 200000000000, name= "sharesfloat_max"),
    Real(0, 200000000000, name='market_cap_min'),
    Real(0, 200000000000, name='market_cap_max')
])
def objective(**params):
    output_dict = {k: v for k, v in params.items()}
    finish_bal = ml_backtester(output_dict)
    return -finish_bal # Return negative value since gp_minimize minimizes the objective function

# Define the search space for each of the settings
search_space = [
    Real(0, 200000000000, name='sharesfloat_min'),
    Real(0, 200000000000, name= "sharesfloat_max"),
    Real(0, 200000000000, name='market_cap_min'),
    Real(0, 200000000000, name='market_cap_max')
]

# Run Bayesian optimization
result = gp_minimize(objective, search_space, n_calls=500, random_state=0, n_jobs=-1)

# Print the optimal settings and finish_bal value
print("Optimal settings: {}".format(dict(zip(['sharesfloat_min', 'sharesfloat_max','market_cap_min','market_cap_max'], result.x))))
print("Optimal finish_bal: {}".format(-result.fun))
telegram_send.send(messages=["Bayesian optimization back test complete............"])



