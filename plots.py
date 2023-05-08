#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:28:41 2023

@author: briansheehan
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.dates as mpl_dates
import pytz

from mpl_toolkits.mplot3d import Axes3D

import plotly.express as px

import matplotlib.ticker as ticker



plt.style.use('ggplot')#Data Viz
class Plots:
    def __init__(self):
        pass

    def plt_chart(self,longshort,date, ticker, ohlc_intraday,outcome,ticker_return,outcome_2,ticker_return_2):
        
        # fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8))
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8), gridspec_kw={'height_ratios': [0.7, 0.3]})

        
        ax[0].plot(ohlc_intraday[date,ticker].index, ohlc_intraday[date,ticker].close,ohlc_intraday[date,ticker].vwap)
        ax[1].bar(ohlc_intraday[date,ticker].index, ohlc_intraday[date,ticker].volume, width=1/(5*len(ohlc_intraday[date,ticker].index)))
        # ax[0].plot(ohlc_intraday[date,ticker]['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
        # ax[0].plot(ohlc_intraday[date,ticker]['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
        
        # Add shaded background before 14:30
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=9, minute=30, second=0, microsecond=0)
        ax[0].axvspan(mpl_dates.date2num(start_time), mpl_dates.date2num(end_time), alpha=0.3, color='gray')

        if longshort == 'long':
            ax[0].plot(ohlc_intraday[date,ticker]['cover_sig'], marker = '^', color = 'r', markersize = 12, linewidth = 0, label = 'Sell SIGNAL')
            ax[0].plot(ohlc_intraday[date,ticker]['trade_sig'], marker = 'v', color = 'green', markersize = 12, linewidth = 0, label = 'BUY SIGNAL')
        if longshort == 'short':
            ax[0].plot(ohlc_intraday[date,ticker]['cover_sig'], marker = '^', color = 'green', markersize = 12, linewidth = 0, label = 'COVER SIGNAL')
            ax[0].plot(ohlc_intraday[date,ticker]['trade_sig'], marker = 'v', color = 'r', markersize = 12, linewidth = 0, label = 'SHORT SIGNAL')
            ax[0].plot(ohlc_intraday[date,ticker]['trade_sig_2'], marker = 'v', color = 'b', markersize = 12, linewidth = 0, label = 'SHORT SIGNAL 2')
            ax[0].plot(ohlc_intraday[date,ticker]['cover_sig_2'], marker = '^', color = 'y', markersize = 12, linewidth = 0, label = 'COVER SIGNAL')
    
        strdate = date.strftime("%Y-%m-%d")
        t = ticker + ' ' + strdate + ' ' + outcome + ' Returns ' + str(ticker_return) + ' ' + outcome_2 + ' Returns_2 ' + str(ticker_return_2)
    
        plt.title(t)#('df ST TRADING SIGNALS')
        ax[0].legend(loc = 'upper left')
        
        xfmt = mpl.dates.DateFormatter('%H:%M')
        ax[1].xaxis.set_major_locator(mpl.dates.HourLocator(interval=3))
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
    
    def scatter_polts(self, results_store):
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
        ax.set_ylim(1000000, 10000000)
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
                
                


        
    
      
    # def plot_results(self, results_store):
    #     fig, ax = plt.subplots(figsize=(15, 10), dpi=150)
    
    #     # Scatter plot
    #     profit_df = results_store[results_store['profit_win'] == 1]
    #     loss_df = results_store[results_store['loss'] == 1]
    #     ax.scatter(results_store.index, results_store['shares_float'], color='grey', label='No Profit/Loss')
    #     ax.scatter(profit_df.index, profit_df['shares_float'], color='green', label='Profit')
    #     ax.scatter(loss_df.index, loss_df['shares_float'], color='red', label='Loss')
    
    #     # Line plot
    #     results_store.plot(x='date', y=['balance', 'balance_no_fee'], color=['red', 'blue'], ax=ax, linewidth=0.25)
    
    #     ax.set_xlabel('Date')
    #     ax.set_ylabel('Balance')
    #     ax.set_title('Balance vs. Date with Shares Float Highlighted')
    #     ax.legend()
        
    #     return plt.show()
    #     import matplotlib.pyplot as plt

# # Filter the DataFrame by profit_win and loss
# profit_df = results_store[results_store['profit_win'] == 1]
# loss_df = results_store[results_store['loss'] == 1]

# # Create the scatter plot
# fig, ax = plt.subplots(figsize=(10, 8))

# ax.scatter(results_store.index, results_store['shares_float'], color='grey', label='No Profit/Loss')
# ax.scatter(profit_df.index, profit_df['shares_float'], color='green', label='Profit')
# ax.scatter(loss_df.index, loss_df['shares_float'], color='red', label='Loss')

# ax.set_xlabel('Index')
# ax.set_ylabel('Shares Float')
# ax.set_title('Shares Float vs. Index with Profit/Loss Highlighted')
# ax.legend()

# plt.show()
# 

