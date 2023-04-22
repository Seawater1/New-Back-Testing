# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:28:50 2023

@author: brian

"""

from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker


today_dt = datetime.now()
today = today_dt.strftime("%Y-%m-%d")
time_now = today_dt.strftime("_%H-%M")

# joined = pd.merge(results_store, main_df, on=['Date', 'Ticker'], how='left')
# winner_name = today + time_now +  '_winner_losers.csv' #
winner_name = today +   '_winner_losers.csv' #

results_store = pd.read_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s" % winner_name)


profit_df = results_store[results_store['profit_win'] == 1]
loss_df = results_store[results_store['loss'] == 1]

# Create the scatter plot
fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(profit_df.index, profit_df['open_price'], color='green', label='Profit')
ax.scatter(loss_df.index, loss_df['open_price'], color='red', label='Loss')

ax.set_xlabel('Index')
ax.set_ylabel('open_price')
ax.set_title('open_price vs. Index with Profit/Loss Highlighted')

ax.legend()
# Set the y-axis limits to be between 250 and 10,000,000
ax.set_ylim(0, 20)
# Format the y-axis tick labels with commas
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))



plt.show()