#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:35:15 2023

@author: briansheehan
"""


import itertools
import math

# def dict_combinations(default_parms):
#     # Get the values for each key in the dictionary
#     values = list(default_parms.values())
#     # Use itertools.product to get all possible combinations of the values
#     combinations = itertools.product(*values)
#     # Loop through the combinations and print them out (or do whatever you need with them)
#     for combination in combinations:
#         print(combination)
#         my_dict = dict(enumerate(combination))
#         print(my_dict)
#         return combination,my_dict
#         # mac = my_dict['mac']
#         # mac = my_dict['mac']
        
#         import itertools

def dict_combinations(default_parms):
    # Get the keys and values for the dictionary
    keys = list(default_parms.keys())
    values = list(default_parms.values())
    # Use itertools.product to get all possible combinations of the values
    combinations = itertools.product(*values)
    # Loop through the combinations and print them out (or do whatever you need with them)
    result = []
    for combination in combinations:
        # print('combination',combination)
        my_dict = {}
        for i, value in enumerate(combination):
            my_dict[keys[i]] = value
            # print(my_dict)
        # result.append((combination, my_dict))
        print('my_dict',my_dict)
    return my_dict

        

default_parms = {
    "mac": [1],
    "b": [2,],
    "c": [5],
    "e": [1,2],
    "x": [2],
    "t": [2,3],
    "close_stop": [[i / 100 for i in range(1, 21, 2)], 
}

my_dict = dict_combinations(default_parms)


