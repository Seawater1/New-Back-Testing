#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:53:50 2023
Maximum Adverse Excursion 
@author: briansheehan
"""
import pandas as pd
import numpy as np
import time
from plots import Plots
from datetime import datetime, timedelta
my_plt = Plots


class Results:
    def __init__(self):
        pass
    
    def cal_results(self,active_value,results_store,risk_per_trade):
        print('Starting calculating returns-----------------------------------------------------------')
        mac = active_value['mac']
        trip_comm = active_value["trip_comm"]
        imaginary_account = active_value["imaginary_account"]
        pm_float_rotations_on = active_value["pm_float_rotations_on"]
        
        
        #dictionarys to store data
        profit_trade_dic = {}
        
        if len(results_store) == 0:
            print('Results dataframe empty')
        else:
            # Strategy 1
            # loss if stop hit
            results_store['stop_p_one'] = results_store['open_price'] - results_store['stop_price']
            results_store['loss_if_stop'] = results_store['stop_p_one'].abs() * results_store['max_shares']
            # profit
            results_store['profit_1'] =   results_store['ticker_return'] * results_store['max_shares']
            
            results_store['profit_win'] = np.nan
            results_store['loss'] = np.nan 
            results_store['total_win_1'] = np.nan
                    
            # Strategy 2
            # loss if stop hit
            results_store['stop_p_one_2'] = results_store['open_price_2'] - results_store['stop_price_2']
            results_store['loss_if_stop_2'] = results_store['stop_p_one_2'].abs() * results_store['max_shares_2']
            # profit_2
            results_store['profit_2'] =   results_store['ticker_return_2'] * results_store['max_shares_2']
            
            results_store['profit_win_2'] = np.nan
            results_store['loss_2'] = np.nan 
            results_store['total_win_2'] = np.nan
            
            results_store['profit'] = results_store['profit_1'] + results_store['profit_2']
            
            # Strategy 1 Commisions and locate fees
            results_store['commission_1'] = results_store['trade_count'] * trip_comm
            
            # Strategy 2 Commisions and locate fees
            results_store['commission_2'] = results_store['trade_count_2'] * trip_comm
            
            results_store['total_commission'] = results_store['commission_1'] + results_store['commission_2']
            
            results_store['total_1'] =  results_store['profit_1'] -  results_store['commission_1']
            results_store['total_2'] =  results_store['profit_2'] -  results_store['commission_2']
            
            
            
            # vectorized calculation for counting locate used one trade or two
            mask1 = (results_store['trade_count'] == 1) & (results_store['trade_count_2'] == 0)
            mask2 = (results_store['trade_count'] == 0) & (results_store['trade_count_2'] == 1)
            mask3 = (results_store['trade_count'] == 1) & (results_store['trade_count_2'] == 1)
            results_store['locat_mult'] = (mask1 | mask2 | mask3).astype(int)
            
            # locate fees calculation
            results_store['locate_fee'] = results_store['locat_mult'] * (results_store['locates_acq'] * results_store['locate_cost_ps'])
            results_store['locate_fee_2'] = results_store['locat_mult'] * (results_store['locates_acq_2'] * results_store['locate_cost_ps_2'])
            # results_store['locate_fee_total'] = results_store['locate_fee'] + results_store['locate_fee_2']
            
            # apply the formula using a vectorized approach
            results_store['locate_fee_total'] = np.where((results_store['locat_mult'] == 1) & (results_store['locate_fee'] != 0) & (results_store['locate_fee_2'] != 0),
                                               results_store['locate_fee'], results_store['locate_fee'] + results_store['locate_fee_2'])

            
            
            
            # results_store['total_1'] =  results_store['profit_1'] - ((results_store['locate_fee_total']*results_store['trade_count']) + results_store['commission_1'])
            # results_store['total_2'] =  results_store['profit_2'] - ((results_store['locate_fee_total']*results_store['trade_count_2']) + results_store['commission_2'])
            results_store['R'] = results_store['total_1'] /  results_store['loss_if_stop']##????????????????????????? this might be wrong!! 
            # Create the new columns based on the values in 'R'
            results_store['R_losser'] = results_store[results_store['R'] < 0]['R']
            results_store['R_winner'] = results_store[results_store['R'] >= 0]['R']
            
            
            results_store['R_2'] = results_store['total_2'] /  results_store['loss_if_stop_2']
            # Create the new columns based on the values in 'R'
            results_store['R_losser_2'] = results_store[results_store['R_2'] < 0]['R_2']
            results_store['R_winner_2'] = results_store[results_store['R_2'] >= 0]['R_2']
            
            # New Total 
            
            results_store['total'] = (results_store['total_1'] + results_store['total_2']) - results_store['locate_fee_total']
           
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
            results_store['start_bal'] = imaginary_account
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
            total_locate_fee = results_store['locate_fee_total'].sum()
            total_comm = results_store['total_commission'].sum()
            total_profit = round(results_store['total'].sum(),2)
            finish_bal = round(results_store['balance'].iloc[-1],2)
            expectancy = round(results_store['R'].mean(),3)

            
            my_plt.plot_results(self,results_store)
            my_plt.scatter_polts(self,results_store)
            my_plt.plot_trades_by_country(self,results_store)
            my_plt.plot_trades_by_day(self,results_store)
            if pm_float_rotations_on == 1:
                my_plt.plot_pm_float_rotations(self, results_store)
            
            my_plt.plot_open_price_Profit(self, results_store)
            
            #####################################################################################

            
            #print('Maximum Drawdown ?????????????????????????', max_dd)
            print('Starting balance',imaginary_account)
            print('Number of trades taken', num_of_trades)
            print('Number of trades won', total_win)
            print('Winning %',win_per)
            print('risk_per_trade',risk_per_trade)
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
        
        # # Load file of tickers and date
        # print('Using filepath', self.file_path)
        # main_df = pd.read_csv(self.file_path , parse_dates=[1], dayfirst=True,index_col=0)# Puts year first

        # results_store.rename(columns = {'date' : 'Date', 'ticker' : 'Ticker'}, inplace = True)
        #Get todays date
        today_dt = datetime.now()
        today = today_dt.strftime("%Y-%m-%d")
        time_now = today_dt.strftime("_%H-%M")

        # joined = pd.merge(results_store, main_df, on=['Date', 'Ticker'], how='left')
        winner_name = today + time_now +  '_winner_losers.csv' #
        if mac == 1:
            results_store.to_csv("/Users/briansheehan/Documents/mac_quant/Backtesting/result_store.csv", index=False)
        if mac == 0:
            results_store.to_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s"% winner_name, index=False)

        # mac = load_parms['mac']
        # if mac == 0:
        #     telegram_send.send(messages=["Back test complete............"])
            
        
        return results_store, num_of_trades, total_win,  gross_profit,total_locate_fee,total_comm,win_per,finish_bal 