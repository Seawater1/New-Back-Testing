#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:28:41 2023

@author: briansheehan
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mpl_dates

import numpy as np


import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

import matplotlib.dates as mdates
import matplotlib.ticker as mpl_ticker

import mplfinance as mpf

plt.style.use('ggplot')#Data Viz
class Plots:
    def __init__(self):
        pass
    
    def plot_all(self, longshort, date, ticker, ohlc_intraday, outcome, ticker_return, outcome_2, ticker_return_2, gains, gains_2, new_new_gain, results_store):
        self.plt_chart(longshort, date, ticker, ohlc_intraday, outcome, ticker_return, outcome_2, ticker_return_2)
        self.plot_fips(gains, gains_2, new_new_gain)
        self.plot_results(results_store)
        self.scatter_plots(results_store)
        self.plot_trades_by_country(results_store)
        self.plot_trades_by_day(results_store)
        self.plot_pm_float_rotations(results_store)

    def plt_chart(self,longshort, date, ticker, ohlc_intraday,outcome,ticker_return,outcome_2,ticker_return_2):
        # filter by trade day
        df = ohlc_intraday[date,ticker]
        filtered_df = df[df.index.date == date.date()]
        
        
        # fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8))
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8), gridspec_kw={'height_ratios': [0.7, 0.3]})

        
        ax[0].plot(filtered_df.index, filtered_df.close,filtered_df.vwap)
        ax[1].bar(filtered_df.index, filtered_df.volume, width=1/(5*len(filtered_df.index)))
        # ax[0].plot(filtered_df['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
        # ax[0].plot(filtered_df['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
        
        # Add shaded background before 14:30
        start_time = date.replace(hour=4, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=9, minute=30, second=0, microsecond=0)
        ax[0].axvspan(mpl_dates.date2num(start_time), mpl_dates.date2num(end_time), alpha=0.3, color='gray')

        if longshort == 'long':
            ax[0].plot(filtered_df['cover_sig'], marker = '^', color = 'r', markersize = 12, linewidth = 0, label = 'Sell SIGNAL')
            ax[0].plot(filtered_df['trade_sig'], marker = 'v', color = 'green', markersize = 12, linewidth = 0, label = 'BUY SIGNAL')
        if longshort == 'short':
            ax[0].plot(filtered_df['cover_sig'], marker = '^', color = 'green', markersize = 12, linewidth = 0, label = 'COVER SIGNAL')
            ax[0].plot(filtered_df['trade_sig'], marker = 'v', color = 'r', markersize = 12, linewidth = 0, label = 'SHORT SIGNAL')
            ax[0].plot(filtered_df['trade_sig_2'], marker = 'v', color = 'b', markersize = 12, linewidth = 0, label = 'SHORT SIGNAL 2')
            ax[0].plot(filtered_df['cover_sig_2'], marker = '^', color = 'y', markersize = 12, linewidth = 0, label = 'COVER SIGNAL')
    
        strdate = date.strftime("%Y-%m-%d")
        t = ticker + ' ' + strdate + ' ' + outcome + ' Returns ' + str(ticker_return) + ' ' + outcome_2 + ' Returns_2 ' + str(ticker_return_2)
    
        plt.title(t)#('df ST TRADING SIGNALS')
        ax[0].legend(loc = 'upper left')
        
        xfmt = mpl.dates.DateFormatter('%H:%M')
        ax[1].xaxis.set_major_locator(mpl.dates.HourLocator(interval=3))#???
       
        ax[1].xaxis.set_major_formatter(xfmt)
        
        ax[1].xaxis.set_minor_locator(mpl.dates.HourLocator(interval=1))
        ax[1].xaxis.set_minor_formatter(xfmt)
        
        ax[1].get_xaxis().set_tick_params(which='major', pad=25)
        
        fig.autofmt_xdate()
        
        return plt.show()
    

   
    
        
    def plot_fips(self, gains, gains_2,new_new_gain):
        
        fig, ax1 = plt.subplots(figsize=(15,10), dpi=150)
        color1 = 'tab:red'
        color2 = 'tab:blue'
        color3 = 'tab:green'
        ax1.set_xlabel('Flips')
        ax1.set_ylabel('gains', color=color1)
        ax1.plot(gains, color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('gains_2', color=color2)
        ax2.plot(gains_2, color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('new_new_gain', color=color2)
        ax2.plot(new_new_gain, color=color3)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        fig.tight_layout()
        return plt.show()
    
    def plot_results(self,results_store):
        fig, ax = plt.subplots(figsize=(15,10), dpi=150)#?
        results_store.plot(x='date',  y=['balance', 'balance_no_fee'], color=['red', 'blue'],ax=ax,linewidth=0.25)
        
        
        return plt.show()
    
    def scatter_polts(self,results_store):
        # Filter the DataFrame by profit_win and loss
        profit_df = results_store[results_store['profit_win'] == 1]
        loss_df = results_store[results_store['loss'] == 1]
        
        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.scatter(profit_df.index, profit_df['shares_float'], color='green', label='Profit')
        ax.scatter(loss_df.index, loss_df['shares_float'], color='red', label='Loss')
        
        ax.set_xlabel('Index')
        ax.set_ylabel('Shares Float')
        ax.set_title('Shares Float vs. Index with Profit/Loss Highlighted')
        
        ax.legend()
        # Set the y-axis limits to be between 250 and 10,000,000
        ax.set_ylim(-100, 10000000)
        # Format the y-axis tick labels with commas
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        
        # Add grid lines every 1 million units on the y-axis
        ax.yaxis.grid(True, which='major', linestyle='--', color='gray', alpha=0.5, linewidth=0.5)
        ax.set_yticks(range(0, 10000001, 1000000))

        
        plt.show()
        
        # profit_df = results_store[results_store['profit_win'] == 1]
        # loss_df = results_store[results_store['loss'] == 1]
        
        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.scatter(profit_df.index, profit_df['market_cap'], color='green', label='Profit')
        ax.scatter(loss_df.index, loss_df['market_cap'], color='red', label='Loss')
        
        ax.set_xlabel('Index')
        ax.set_ylabel('market_cap')
        ax.set_title('market_cap vs. Index with Profit/Loss Highlighted')
        
        ax.legend()
        # Set the y-axis limits to be between 250 and 10,000,000
        ax.set_ylim(1000000, 1000000000)
        # Format the y-axis tick labels with commas
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        
        # # Add grid lines every 1 million units on the y-axis
        # ax.yaxis.grid(True, which='major', linestyle='--', color='gray', alpha=0.5, linewidth=0.5)
        # ax.set_yticks(range(0, 10000001, 10000000))
        
        
        plt.show()
        
        # profit_df = results_store[results_store['profit_win'] == 1]
        # loss_df = results_store[results_store['loss'] == 1]
        
        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.scatter(profit_df.index, profit_df['pm_volume'], color='green', label='Profit')
        ax.scatter(loss_df.index, loss_df['pm_volume'], color='red', label='Loss')
        
        ax.set_xlabel('Index')
        ax.set_ylabel('pm_volume')
        ax.set_title('pm_volume vs. Index with Profit/Loss Highlighted')
        
        ax.legend()
        # Set the y-axis limits to be between 250 and 10,000,000
        ax.set_ylim(-100000, 10000000)
        # Format the y-axis tick labels with commas
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        
        
        plt.show()

        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.scatter(profit_df.index, profit_df['number_of_employees'], color='green', label='Profit')
        ax.scatter(loss_df.index, loss_df['number_of_employees'], color='red', label='Loss')
        
        ax.set_xlabel('Index')
        ax.set_ylabel('number_of_employees')
        ax.set_title('number_of_employees vs. Index with Profit/Loss Highlighted')
        
        ax.legend()
        # Set the y-axis limits to be between 250 and 10,000,000
        ax.set_ylim(0, 150)
        # Format the y-axis tick labels with commas
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        
        # # Add grid lines every 1 million units on the y-axis
        # ax.yaxis.grid(True, which='major', linestyle='--', color='gray', alpha=0.5, linewidth=0.5)
        # ax.set_yticks(range(0, 10000001, 10000000))
        
        
        
        
        
        plt.show()
        
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
                
                



    def plot_trades_by_country(self,results_store):
        """
        Create a grouped bar chart showing the number of winning and losing trades for each country.
    
        Parameters:
        results_store (pd.DataFrame): The DataFrame containing the trade results.
    
        Returns:
        None
        """
    
        # Filter results_store to include both winning and losing trades
        winning_df = results_store[results_store['profit_win'] == 1]
        losing_df = results_store[results_store['loss'] == 1]
    
        # Group the results by country and count the number of winning and losing trades for each country
        winning_counts = winning_df.groupby('country')['profit_win'].count()
        losing_counts = losing_df.groupby('country')['loss'].count()
    
        # Combine the winning and losing counts into a single dataframe
        combined_counts = pd.concat([winning_counts, losing_counts], axis=1, keys=['Winning', 'Losing'])
    
        # Create a bar chart
        sns.set(style="whitegrid")
        ax = combined_counts.plot(kind='bar')
        ax.set_title('Winning and Losing Trades by Country')
        ax.set_xlabel('Country')
        ax.set_ylabel('Number of Trades')
        plt.show()
        
    def plot_trades_by_day(self,results_store):
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

    
    def plot_pm_float_rotations( self, data):
        # Grouping ranges for pm_float_rotations
        ranges = [0, 1, 2, 3, 6, 10, 20, 40, float('inf')]
        labels = ['0', '1', '2', '3-6', '6-10', '10-20', '20-40', '+40']
    
        # Grouping and aggregating data
        data['pm_float_rotations_group'] = pd.cut(data['pm_float_rotations'], ranges, labels=labels)
        grouped_data = data.groupby('pm_float_rotations_group').sum()[['profit_win', 'loss']]
    
        # Calculate winning percentage
        grouped_data['win_percentage'] = grouped_data['profit_win'] / (
                    grouped_data['profit_win'] + grouped_data['loss']) * 100
    
        # Set a larger figure size
        plt.figure(figsize=(10, 6))
    
        # Plotting the bar graph
        bar_width = 0.4  # Adjust the bar width as needed
        index = np.arange(len(grouped_data))
    
        plt.bar(index, grouped_data['profit_win'], bar_width, label='profit_win', align='center')
        plt.bar(index + bar_width, grouped_data['loss'], bar_width, label='loss', align='center')
    
        plt.xlabel('pm_float_rotations_group')
        plt.ylabel('win_percentage')
        plt.title('Profit and Loss by pm_float_rotations Group')
        plt.xticks(index + bar_width / 2, grouped_data.index)
    
        # Adding winning percentage above each group with adjusted positioning and font size
        for i, win_percentage in enumerate(grouped_data['win_percentage']):
            bar_x = index[i] + bar_width / 2
            bar_y = max(grouped_data['profit_win'][i], grouped_data['loss'][i]) + 10  # Adjust the positioning as needed
            plt.text(bar_x, bar_y, f'Win %: {win_percentage:.2f}%', ha='center', fontsize=8)
    
        # Plotting a line for the winning percentages
        plt.plot(index + bar_width / 2, grouped_data['win_percentage'], marker='o', color='r', linestyle='--')
    
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_open_price_Profit(self,  data):
        # Grouping ranges for pm_float_rotations
        ranges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, float('inf')]
        labels = ['0', '1', '2', '3', '4', '5', '6','7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20']
    
        # Grouping and aggregating data
        data['open_price_group'] = pd.cut(data['open_price'], ranges, labels=labels)
        grouped_data = data.groupby('open_price_group').sum()[['profit_win', 'loss']]
    
        # Calculate winning percentage
        grouped_data['win_percentage'] = grouped_data['profit_win'] / (
                    grouped_data['profit_win'] + grouped_data['loss']) * 100
    
        # Set a larger figure size
        plt.figure(figsize=(10, 6))
    
        # Plotting the bar graph
        bar_width = 0.4  # Adjust the bar width as needed
        index = np.arange(len(grouped_data))
    
        plt.bar(index, grouped_data['profit_win'], bar_width, label='profit_win', align='center')
        plt.bar(index + bar_width, grouped_data['loss'], bar_width, label='loss', align='center')
    
        plt.xlabel('open_price_group')
        plt.ylabel('win_percentage')
        plt.title('Open price to Profit/Loss')
        plt.xticks(index + bar_width / 2, grouped_data.index)
    
        # Adding winning percentage above each group with adjusted positioning and font size
        for i, win_percentage in enumerate(grouped_data['win_percentage']):
            bar_x = index[i] + bar_width / 2
            bar_y = max(grouped_data['profit_win'][i], grouped_data['loss'][i]) + 10  # Adjust the positioning as needed
            plt.text(bar_x, bar_y, f'Win %: {win_percentage:.2f}%', ha='center', fontsize=8)
    
        # Plotting a line for the winning percentages
        plt.plot(index + bar_width / 2, grouped_data['win_percentage'], marker='o', color='r', linestyle='--')
    
        plt.legend()
        plt.tight_layout()
        plt.show()
        
    def plot_by_marketcap(self,  data):
    
       

        # Grouping ranges for pm_float_rotations
        ranges = [0, 1000000,2000000, 3000000, 4000000, 8000000, 16000000, 32000000, 100000000, 500000000, 1000000000, 5000000000, float('inf')]
        labels = ['0', '1', '2', '3',  '4',    '8',      '16',     '32',    '100',     '500',     '1000',  '5000']
    
        # Grouping and aggregating data
        data['market_cap'] = pd.cut(data['market_cap'], ranges, labels=labels)
        grouped_data = data.groupby('market_cap').sum()[['profit_win', 'loss']]
    
        # Calculate winning percentage
        grouped_data['win_percentage'] = grouped_data['profit_win'] / (
                    grouped_data['profit_win'] + grouped_data['loss']) * 100
    
        # Set a larger figure size
        plt.figure(figsize=(10, 6))
    
        # Plotting the bar graph
        bar_width = 0.4  # Adjust the bar width as needed
        index = np.arange(len(grouped_data))
    
        plt.bar(index, grouped_data['profit_win'], bar_width, label='profit_win', align='center')
        plt.bar(index + bar_width, grouped_data['loss'], bar_width, label='loss', align='center')
    
        plt.xlabel('mmkt cap groups')
        plt.ylabel('win_percentage')
        plt.title('mmkt cap groups to Profit/Loss')
        plt.xticks(index + bar_width / 2, grouped_data.index)
    
        # Adding winning percentage above each group with adjusted positioning and font size
        for i, win_percentage in enumerate(grouped_data['win_percentage']):
            bar_x = index[i] + bar_width / 2
            bar_y = max(grouped_data['profit_win'][i], grouped_data['loss'][i]) + 10  # Adjust the positioning as needed
            plt.text(bar_x, bar_y, f'Win %: {win_percentage:.2f}%', ha='center', fontsize=8)
    
        # Plotting a line for the winning percentages
        plt.plot(index + bar_width / 2, grouped_data['win_percentage'], marker='o', color='r', linestyle='--')
    
        plt.legend()
        plt.tight_layout()
        plt.show()
        
            
    

# csv_path = "/Users/briansheehan/Documents/mac_quant/Backtesting/result_store.csv"
# results_store = pd.read_csv(csv_path)

# # Display the DataFrame
# print(results_store)

# plot_open_price_Profit(results_store)


   