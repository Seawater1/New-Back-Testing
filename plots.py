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