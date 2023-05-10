# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:28:50 2023

@author: brian

"""

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt



today_dt = datetime.now()
today = today_dt.strftime("%Y-%m-%d")
time_now = today_dt.strftime("_%H-%M")

# joined = pd.merge(results_store, main_df, on=['Date', 'Ticker'], how='left')
# winner_name = today + time_now +  '_winner_losers.csv' #
winner_name = today +   '_winner_losers.csv' #

results_store = pd.read_csv("/Users/briansheehan/Documents/mac_quant/Backtesting/result_store.csv")


import seaborn as sns

import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_trades_by_day(results_store):
    """
    Create grouped bar charts showing the number of winning and losing trades by day of the week.

    Parameters:
    results_store (pd.DataFrame): The DataFrame containing the trade results.

    Returns:
    None
    """

    # Convert date column to datetime format
    results_store['date'] = pd.to_datetime(results_store['date'])

    # Filter results_store to include both winning and losing trades
    winning_df = results_store[results_store['profit_win'] == 1]
    losing_df = results_store[results_store['loss'] == 1]

    # Group the results by day of the week and count the number of winning and losing trades for each day
    winning_counts = winning_df.groupby(winning_df['date'].dt.day_name())['profit_win'].count()
    losing_counts = losing_df.groupby(losing_df['date'].dt.day_name())['loss'].count()

    # Combine the winning and losing counts into a single DataFrame
    counts_df = pd.concat([winning_counts, losing_counts], axis=1)
    counts_df.columns = ['Winning Trades', 'Losing Trades']

    # Sort the days of the week in the order Monday to Sunday
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts_df.index = pd.Categorical(counts_df.index, categories=days_of_week, ordered=True)
    counts_df.sort_index(inplace=True)

    # Create a bar chart for trades by day of the week
    sns.set(style="whitegrid")
    ax = counts_df.plot(kind='bar', rot=0)
    ax.set_title('Trades by Day of Week')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Number of Trades')
    plt.show()

plot_trades_by_day(results_store)