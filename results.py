#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:53:50 2023

@author: briansheehan
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from plots import Plots
my_plt = Plots
class Results:
    def __init__(self):
        pass
    def cal_results(self,active_value,results_store,total_risk):
        print('Starting calculating returns-----------------------------------------------------------')
        mac = active_value['mac']
        trip_comm = active_value["trip_comm"]
        locate_fee = active_value["locate_fee"]
        start_balance = active_value["start_balance"]
        #dictionarys to store data
        profit_trade_dic = {}
        
        if len(results_store) == 0:
            print('Results dataframe empty')
        else:
            # First trade
            results_store['stop_p_one'] = results_store['open_price'] - results_store['stop_price']
            results_store['loss_if_stop'] = results_store['stop_p_one'].abs() * results_store['max_shares']
            results_store['profit_1'] =   results_store['ticker_return'] * results_store['max_shares']
            
            results_store['profit_win'] = np.nan
            results_store['loss'] = np.nan 
            results_store['total_win_1'] = np.nan
                    
            # Second trade
            results_store['stop_p_one_2'] = results_store['open_price_2'] - results_store['stop_price_2']
            results_store['loss_if_stop_2'] = results_store['stop_p_one_2'].abs() * results_store['max_shares_2']
            results_store['profit_2'] =   results_store['ticker_return_2'] * results_store['max_shares_2']
            
            results_store['profit_win_2'] = np.nan
            results_store['loss_2'] = np.nan 
            results_store['total_win_2'] = np.nan
            
            # Total commission
            results_store['commission'] = results_store['trade_count'] * trip_comm
            
            
            for i in range(len(results_store)):
                profit_trade_dic[i] = []
                #print(results_store['ticker'][i])
                #if results_store['trade_count'][i] > 0:??? NEED TO COME UP WITH SOMETHING HERE
                results_store['locate_fee'] = results_store['locate'] * locate_fee
                profit_trade_dic[i].append(results_store['locate'] * locate_fee)
        
            
            
            
            results_store['total_1'] =  results_store['profit_1'] - (results_store['locate_fee'] + results_store['commission'])
            results_store['R'] = results_store['total_1'] /  results_store['loss_if_stop']##????????????????????????? this might be wrong!! 
            # Create the new columns based on the values in 'R'
            results_store['R_losser'] = results_store[results_store['R'] < 0]['R']
            results_store['R_winner'] = results_store[results_store['R'] >= 0]['R']
            
            #Second trade no locate or commisions all covered in first trade
            results_store['total_2'] =  results_store['profit_2']
            results_store['R_2'] = results_store['total_2'] /  results_store['loss_if_stop_2']
            # Create the new columns based on the values in 'R'
            results_store['R_losser_2'] = results_store[results_store['R_2'] < 0]['R_2']
            results_store['R_winner_2'] = results_store[results_store['R_2'] >= 0]['R_2']
            
            # New Total 
            results_store['profit'] = results_store['profit_1'] + results_store['profit_2']
            results_store['total'] = results_store['total_1'] + results_store['total_2']
           
            # First trade
            results_store['profit_win'] = 0
            results_store['loss'] = 0
            results_store['total_win_1'] = 0
            # assign 'qualitative_rating' based on 'grade' with .loc
            results_store.loc[results_store.profit > 0, 'profit_win'] = 1
            results_store.loc[results_store.profit < 0, 'loss'] = 1
            results_store.loc[results_store.total > 0, 'total_win'] = 1
            
            # Second trade
            results_store['profit_win_2'] = 0
            results_store['loss_2'] = 0
            results_store['total_win_2'] = 0
            # assign 'qualitative_rating' based on 'grade' with .loc
            results_store.loc[results_store.profit_2 > 0, 'profit_win_2'] = 1
            results_store.loc[results_store.profit_2 < 0, 'loss_2'] = 1
            results_store.loc[results_store.total_2 > 0, 'total_win_2'] = 1
            
            # Exposed Capital
            results_store ['exposed'] = (results_store['max_shares'] * results_store['open_price'])#.cumsum()
              
            # Cal balance
            results_store['start_bal'] = start_balance
            results_store['cum_profit'] =  results_store['profit'].cumsum()
            results_store['balance_no_fee'] = results_store['start_bal'] + results_store['cum_profit']
            results_store['cum_total'] = results_store['total'].cumsum()
            results_store['balance'] = results_store['start_bal'] + results_store['cum_total']
            
            
            
            
            
            #-----------------------------------------------------------------------------------
           
            total_win = results_store['total_win'].sum()
            num_of_trades = results_store['trade_count'].sum()
            if total_win > 0:
                win_per = total_win / num_of_trades
            else:
                win_per = 0 
            # Calculate the averages
            losser_average = round(results_store['R_losser'].mean(),3)
            winner_average = round(results_store['R_winner'].mean(),3)
            gross_profit = round(results_store['profit'].sum(),3)
            total_locate_fee = results_store['locate_fee'].sum()
            total_comm = results_store['commission'].sum()
            total_profit = round(results_store['total'].sum(),2)
            finish_bal = round(results_store['balance'].iloc[-1],2)
            expectancy = round(results_store['R'].mean(),3)

            
            my_plt.plot_results(self,results_store)
            #####################################################################################

            
            #print('Maximum Drawdown ?????????????????????????', max_dd)
            print('Starting balance',start_balance)
            print('Number of trades taken', num_of_trades)
            print('Number of trades won', total_win)
            print('Winning %',win_per)
            print('Total risk',total_risk)
            print('Gross profit',gross_profit)
            print('Total locate fees', total_locate_fee)
            print('Total commission', total_comm)
            print('Total Profits',total_profit)
            print('Finishing balance',finish_bal)
            print('expectancy',expectancy)
            print('Loosing R',losser_average)
            print('Winning R',winner_average)
               
        #########################################################################################################################################

        #########################################################################################################################################
        #########################################################################################################################################
        
        # Load file of tickers and date
        print('Using filepath', self.file_path)
        main_df = pd.read_csv(self.file_path , parse_dates=[1], dayfirst=True,index_col=0)# Puts year first

        results_store.rename(columns = {'date' : 'Date', 'ticker' : 'Ticker'}, inplace = True)
        #Get todays date
        today_dt = datetime.now()
        today = today_dt.strftime("%Y-%m-%d")
        time_now = today_dt.strftime("_%H-%M")

        joined = pd.merge(results_store, main_df, on=['Date', 'Ticker'], how='left')
        winner_name = today + time_now +  '_winner_losers.csv' #
        if mac == 1:
            joined.to_csv("/Users/briansheehan/Documents/mac_quant/Backtesting/winners.csv", index=False)
        if mac == 0:
            joined.to_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s"% winner_name, index=False)

        # mac = load_parms['mac']
        # if mac == 0:
        #     telegram_send.send(messages=["Back test complete............"])
            
        
        return results_store, num_of_trades, total_win,  gross_profit,total_locate_fee,total_comm,win_per,finish_bal 