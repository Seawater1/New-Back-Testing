# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 23:34:35 2023

@author: brian
"""

import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestRegressor
from backters import backtest

# Load data
data = pd.read_csv('data.csv')

# Define input and output variables
X = data[['param1', 'param2', 'param3']]
y = data['finish_bal']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the hyperparameter space
param_grid = {
    'stop_loss': [0.01, 0.02, 0.03],
    'take_profit': [0.02, 0.04, 0.06],
    'moving_average_periods': [10, 20, 30]
}

# Define the model and search over the hyperparameter space
model = RandomForestRegressor()
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Retrieve the best hyperparameters and evaluate the model on a holdout dataset
best_params = grid_search.best_params_
best_model = RandomForestRegressor(**best_params)
best_model.fit(X_train, y_train)
best_score = best_model.score(X_test, y_test)

# Use best hyperparameters to perform backtesting
result = backtest(param1=best_params['param1'], param2=best_params['param2'], param3=best_params['param3'])
