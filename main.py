#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 06:27:52 2023

@author: briansheehan
"""
import time
import telegram_send
import json
import pandas as pd
import numpy as np
from indicators import Indicators
from load_data import Load_date
from plots import Plots
from datetime import datetime, timedelta
from slippage_model import SlippageCalculator
from results import Results
ld = Load_date
indc = Indicators()
my_plt = Plots


# Create an instance of the SlippageCalculator class
sc = SlippageCalculator()




import matplotlib.pyplot as plt

############################################################################################################
## Functions to load data
############################################################################################################
pd.options.mode.chained_assignment = None # wprloing with copy warning disable
# # so annoying cant figure out copy not 
class Backtester():
    def __init__(self,active_value):
        top_gap_by_date,file_path, flt_database = ld.loadmaindata(self,active_value)
        
        super().__init__()
        
        
        self.top_gap_by_date = top_gap_by_date
        self.file_path = file_path
        self.flt_database = flt_database
        
        """
        :load_parms dic that contains all settings

        """
        # super().__init__()
        # self.load_parms = load_parms
        
    def backtester(self,active_value):
        print(json.dumps(active_value, indent=4))   
        start = time.time()
        
        

        ohlc_intraday = {}
        mac = active_value['mac']
        longshort = active_value["longshort"]
        take_second_trade = active_value["take_second_trade"]
        plot = active_value["plot"]
        plot_trades_only = active_value["plot_trades_only"]
        save_winners_df = active_value["save_winners_df"]
        
        
        full_balance = active_value["full_balance"]
        imaginary_account = active_value["imaginary_account"]
        risk_acc = active_value["risk_acc"]
 
        
        max_risk = active_value["max_risk"]
        
        locate_fee = active_value['locate_fee']
        locate_cost_per_on = active_value['locate_cost_per_on']
        max_locate_per_price = active_value["max_locate_per_price"]
        
        
        open_slippage = active_value["open_slippage"]
        close_slippage = active_value["close_slippage"]
        

        lookback = active_value["lookback"]
        multiplier = active_value["multiplier"]

        drop_acquistions_on = active_value["drop_acquistions_on"]
        aq_value = active_value["aq_value"]
        trip_comm = active_value["trip_comm"]
        
        close_stop_on = active_value["close_stop_on"]
        close_stop = active_value["close_stop"]
        close_stop_on_2 = active_value["close_stop_on_2"]
        close_stop_2 = active_value["close_stop_2"]

        pre_market_h_stop_on = active_value["pre_market_h_stop_on"]
        pre_market_h_stop_on = active_value["pre_market_h_stop_on"]
        trail_stop_on = active_value["trail_stop_on"]
        min_reward_then_let_it_run = active_value["min_reward_then_let_it_run"]
        min_reward_then_let_it_run_2 = active_value["min_reward_then_let_it_run_2"]
        reward = active_value["reward"]
        trail_stop_per = active_value["trail_stop_per"]
        
        sharesfloat_on = active_value["sharesfloat_on"]
        sharesfloat_min = active_value["sharesfloat_min"]
        sharesfloat_max = active_value["sharesfloat_max"]
        market_cap_on = active_value["market_cap_on"]
        market_cap_min = active_value["market_cap_min"]
        market_cap_max = active_value["market_cap_max"]

        price_between_on = active_value["price_between_on"]
        min_between_price = active_value["min_between_price"]
        max_between_price = active_value["max_between_price"]
        buytime_on = active_value["buytime_on"]
        buy_time = active_value["buy_time"]
        buylocatecondition_on = active_value["buylocatecondition_on"]
        buy_locate_time = active_value["buy_locate_time"]
        last_close_per_locate = active_value["last_close_per_locate"]
        selltime_on = active_value["selltime_on"]
        sell_time = active_value["sell_time"]
        buy_between_time_on = active_value["buy_between_time_on"]
        buy_after = active_value["buy_after"]
        buy_before = active_value["buy_before"]
        buy_between_time_on_2 = active_value["buy_between_time_on_2"]
        buy_after_2 = active_value["buy_after_2"]
        buy_before_2 = active_value["buy_before_2"]
        volume_sum_cal_on = active_value["volume_sum_cal_on"]
        vol_sum_greaterthan = active_value["vol_sum_greaterthan"]
        pm_volume_sum_cal_on = active_value["pm_volume_sum_cal_on"]
        pm_volume_sum_greaterthat = active_value["pm_volume_sum_greaterthat"]
        pm_gap_on = active_value["pm_gap_on"]
        pmg_greater = active_value["pmg_greater"]
        per_change_first_tick_on = active_value["per_change_first_tick_on"]
        precent_greater = active_value["precent_greater"]
        per_change_open_on = active_value["per_change_open_on"]
        per_change_open_on_2 = active_value["per_change_open_on_2"]
        open_greater = active_value["open_greater"]
        vwap_above_on = active_value["vwap_above_on"]
        vwap_below_on = active_value["vwap_below_on"]
        last_close_change_on = active_value["last_close_change_on"]
        
        last_close_per = active_value["last_close_per"],
        percent_from_pmh_on = active_value["percent_from_pmh_on"]
        per_pmh_val = active_value["per_pmh_val"]
        day_greater_than_pm_on = active_value["day_greater_than_pm_on"]
        pm_greater_than_day_on = active_value["pm_greater_than_day_on"]
        st_close_lessthan_on = active_value["st_close_lessthan_on"]
        st_close_greaterthan_on = active_value["st_close_greaterthan_on"]
        st_close_greaterthan_on_2 = active_value["st_close_greaterthan_on_2"]
        
        last_close_change_on_2 = active_value["last_close_change_on_2"]
        last_close_per_2 = active_value["last_close_per_2"]
         
        percent_from_pmh_on_2 = active_value["percent_from_pmh_on_2"]
        per_pmh_val_2 = active_value["per_pmh_val_2"]
        
        
        
        
        if sharesfloat_on == 1:
            print('float_share_between:', sharesfloat_min, sharesfloat_max)
        if market_cap_on == 1:
            print('market_cap_between:', market_cap_min, market_cap_max)
        if price_between_on == 1:
            print('price_between:', min_between_price, max_between_price)
        if buytime_on == 1:
            print('buytime:', buy_time)
        if selltime_on == 1:
            print('selltime:', sell_time)
        if buy_between_time_on == 1:
            print('buy_between_time:', buy_after, buy_before)
        if buy_between_time_on_2 == 1:
            print('buy_between_time_2:', buy_after_2, buy_before_2)
        if volume_sum_cal_on == 1:
            print('volume_sum_cal:', vol_sum_greaterthan)
        if pm_volume_sum_cal_on == 1:
            print('pm_volume_sum_cal:', pm_volume_sum_greaterthat)
        if pm_gap_on == 1:
            print('pm_gap:', pmg_greater)
        if per_change_first_tick_on == 1:
            print('per_change_first_tick:', precent_greater)
        if per_change_open_on == 1 or per_change_open_on_2 == 1:
            print('per_change_open 1 or two is on?:', open_greater)
        if vwap_above_on == 1:
            print('vwap_above_on')
        if vwap_below_on == 1:
            print('vwap_below_on')
        if last_close_change_on ==1 or last_close_change_on_2 ==1:
            print('last_close_change 1 or 2 is on?:',last_close_per)
        if day_greater_than_pm_on ==1:
            print('day_greater_than_pm:')
        if pm_greater_than_day_on ==1: 
            print('pm_greater_than_day:')
        if st_close_lessthan_on == 1:
            print('st_close_lessthan_on')
        if st_close_greaterthan_on == 1 or st_close_greaterthan_on_2 == 1:
            print('st_close_greaterthan_on')
        if drop_acquistions_on ==1:
            print('drop_acquistions_on:',aq_value)
        if percent_from_pmh_on ==1:
            print('percent_from_pmh_on',per_pmh_val) 
        if buylocatecondition_on == 1:#2
            print('buylocatecondition_on','buy_locate_time:',buy_locate_time,'last_close_per_locate',last_close_per_locate)
       
        if last_close_change_on_2 ==1:
            print('last_close_change_on_2:',last_close_per_2)            
        if percent_from_pmh_on_2 ==1:
            print('percent_from_pmh_on_2:',per_pmh_val_2)
            
        
        
        print('------  Starting Testing strategy  ---------------------------------------------------------')      
        # print('Going ', longshort)
        #dictionarys to store data
        strategy1_equity = imaginary_account
        strategy2_equity = imaginary_account
        combined_equity = imaginary_account
        strategy1_equity_gain = []
        strategy2_equity_gain = []
        combined_equity_gain = []
        
        strategy1_return = 0
        strategy2_return = 0
        gains = [] 
        gains_2 = []
        new_gain ={}
        new_new_gain = []
        total_win = 0
        locate_cost_ps = 0
        date_stats = {} # stores the returns 
        date_stats_2 = {} # stores the returns
        #Data Frame to store data
        results_store = pd.DataFrame()
        for date in self.top_gap_by_date:
            date_stats[date] = {} #store the day return of eash ticker
            date_stats_2[date] = {} #store the day return of eash ticker
            for ticker in self.top_gap_by_date[date]:# the key is date
                #print('Loading data and applying indicator for ',date,ticker)
                # try:
                    risk_per_trade = imaginary_account * risk_acc
                     
                    if risk_per_trade > max_risk:
                        risk_per_trade = max_risk
                        # print('Compounding off ')
                    # print('risk_per_trade',risk_per_trade)
                    # flt_database = self.flt_database
                    try:
                        df = ld.load_interday(self,date,ticker,mac,self.flt_database)# load interday files ??? does this need to be moved to the top of fucntion
                    except:
                        print('Interday file not found for ----------------------------------------------', date, ticker)  
                        # df = polygon.interday(ticker, date)
                        continue
                    # get last close price
                    last_close = self.top_gap_by_date[date][ticker]

                    # apply super trend always for chart
                    df['st'], df['s_upt'], df['st_dt'] = indc.get_supertrend(df['high'], df['low'], df['close'], lookback, multiplier)
                    if sharesfloat_on == 1:
                        df = indc.float_share_between(df,sharesfloat_min,sharesfloat_max)
                    if market_cap_on == 1:
                        df = indc.market_cap_between(df, market_cap_min, market_cap_max)
                    if price_between_on == 1:
                        df = indc.price_between(df,min_between_price, max_between_price )
                    if buytime_on == 1:
                        df = indc.buytime(df,date,buy_time)
                    if selltime_on == 1:
                        df = indc.selltime(df,date,sell_time)
                    if buy_between_time_on == 1:
                        df = indc.buy_between_time(df, date, buy_after, buy_before)
                    if buy_between_time_on_2 == 1:
                        df = indc.buy_between_time_2(df, date, buy_after_2, buy_before_2)
                    if volume_sum_cal_on == 1:
                        df = indc.volume_sum_cal(df,vol_sum_greaterthan)
                    if pm_volume_sum_cal_on == 1:
                        df = indc.pm_volume_sum_cal(df,date, pm_volume_sum_greaterthat)
                    if pm_gap_on == 1:
                        df = indc.pm_gap(df,date,last_close, pmg_greater) 
                    if per_change_first_tick_on == 1:
                        df = indc.per_change_first_tick(df, precent_greater)
                    if per_change_open_on == 1 or per_change_open_on_2 == 1:
                        df = indc.per_change_open(df,date, open_greater)  
                    if vwap_above_on == 1:
                        df = indc.vwap_above(df)# Close below VWAP
                    if vwap_below_on == 1:
                        df = indc.vwap_below(df)
                    if last_close_change_on ==1:
                        df = indc.last_close_change(df,last_close,last_close_per)
                    if day_greater_than_pm_on ==1:
                        df = indc.day_greater_than_pm(df,date)
                    if pm_greater_than_day_on ==1: 
                        df = indc.pm_greater_than_day(df,date)
                    if st_close_lessthan_on == 1:
                        df = indc.st_close_lessthan(df)#Supertrend lessthan
                    if st_close_greaterthan_on == 1 or st_close_greaterthan_on_2 == 1:
                        df = indc.st_close_greaterthan(df)#Supertrend greather than
                    if drop_acquistions_on ==1:
                        df = indc.drop_acquistions(df,date,aq_value)
                    if percent_from_pmh_on ==1:
                        df = indc.percent_from_pmh(df,date,per_pmh_val)
                    if buylocatecondition_on == 1:#2
                        df = indc.buylocatecondition(df,date,buy_locate_time,last_close,last_close_per_locate)# Time Greater tha
                    if last_close_change_on_2 ==1:
                         df = indc.last_close_change_2(df,last_close,last_close_per_2)
                    if percent_from_pmh_on_2 ==1:
                        df = indc.percent_from_pmh_2(df,date,per_pmh_val_2)
                    df['trade_sig'] = np.nan
                    df['trade_sig_2'] = np.nan
                    df['cover_sig'] = np.nan
                    df['cover_sig_2'] = np.nan
                    df['trade_count'] = np.nan
                    df['trade_count_2'] = np.nan
                    direction = '' # Long short
                    date_stats[date][ticker] = (0) # Setting the return to zero to start
                    date_stats_2[date][ticker] = (0)
                    ohlc_intraday[date,ticker] = df # stores interday data in dictionary
                    #Testing
                    open_price = 0
                    open_price_slippage = 0
                    open_price_2 = 0
                    open_price_slippage_2 = 0
                    close_price = 0
                    close_price_slippage  = 0
                    close_price_2 = 0
                    close_price_slippage_2  = 0
                    #sell_price  = 0
                    max_shares  = 0
                    max_shares_2  = 0
                    stop_price  = 0
                    stop_price_2 = 0
                    locates_acq = 0
                    locates_acq_2 = 0
                    ticker_return = 0
                    ticker_return_2 = 0
                    trade_count = 0
                    trade_count_2 = 0
                    outcome = 'no_trade'
                    outcome_2 = 'no_trade_2'
                    last_high = 0
                    system_1_not_trade = True
                    
                    last_low = 99999999
                    last_low_2 = 99999999
                    trail_stop_price_short = 999999999
                    trail_stop_price_short_2 = 999999999
                    take_profit_count = 0
                    take_profit_count_2 = 0
                    for i in range(len(ohlc_intraday[date,ticker])):# he skips the first bar (1,len) do i need to do this 
                        if price_between_on == 1:
                            is_price_between  = ohlc_intraday[date,ticker]['price_between'][i]
                        else:
                            is_price_between = True
                        if buytime_on == 1:
                            is_buy_time  = ohlc_intraday[date,ticker]['buy_time'][i]
                        else:
                            is_buy_time  = True
                        
                        if selltime_on == 1:
                            is_sell_time  = ohlc_intraday[date,ticker]["sell_time"][i]
                        else:
                            is_sell_time  = False
                        if buy_between_time_on ==1:
                            is_buy_between_time  = ohlc_intraday[date,ticker]["buy_between_time"][i]
                        else:
                            is_buy_between_time  = True
                        if buy_between_time_on_2 ==1:
                            is_buy_between_time_2 = ohlc_intraday[date,ticker]["buy_between_time_2"][i]
                        else:
                            is_buy_between_time_2 = False
                        if volume_sum_cal_on == 1:
                            is_volume_sum_greater  = ohlc_intraday[date,ticker]["vol_sum_greater"][i]
                        else:
                            is_volume_sum_greater  = True
                        if pm_volume_sum_cal_on == 1:
                            is_pm_volume_sum_greater  = ohlc_intraday[date,ticker]["pm_vol_sum_greater"][i]
                        else:
                            is_pm_volume_sum_greater  = True
                        if pm_gap_on == 1:
                            is_pm_gap_greater  = ohlc_intraday[date,ticker]["pm_gap_greater"][i] 
                        else:
                            is_pm_gap_greater  = True
                        if per_change_first_tick_on == 1:
                            is_first_tick_greater  = ohlc_intraday[date,ticker]["first_tick_greater"][i]
                        else:
                            is_first_tick_greater  = True
                        if per_change_open_on == 1:
                            is_open_greater  = ohlc_intraday[date,ticker]["open_greater"][i]
                        else:
                            is_open_greater  = True
                        if per_change_open_on_2 == 1:
                            is_open_greater_2  = ohlc_intraday[date,ticker]["open_greater"][i]
                        else:
                            is_open_greater_2 = True
                        if vwap_above_on == 1:
                            is_vwap_above  = ohlc_intraday[date,ticker]["vwap_above"][i]
                        else:
                            is_vwap_above  = True
                        if vwap_below_on == 1:
                            is_vwap_below  = ohlc_intraday[date,ticker]["vwap_below"][i]
                        else:
                            is_vwap_below  = True
                        if last_close_change_on == 1:
                            is_last_close_change  = ohlc_intraday[date,ticker]["last_close_change_test"][i] 
                        else:
                            is_last_close_change  = True
                        if day_greater_than_pm_on ==1:   
                            is_dh_greater_than_pmh  = ohlc_intraday[date,ticker]['dh>pmh'][i]
                        else:
                            is_dh_greater_than_pmh  = True 
                        if pm_greater_than_day_on ==1:   
                            is_pmg_greater_than_dy  = ohlc_intraday[date,ticker]['pmg>dy'][i]
                        else:
                            is_pmg_greater_than_dy  = True 
                        if st_close_lessthan_on == 1:
                            is_st_long  = ohlc_intraday[date,ticker]["st_long"][i]
                        else:
                            is_st_long  = True 
                        if st_close_greaterthan_on == 1:
                            is_st_short  = ohlc_intraday[date,ticker]["st_short"][i]
                        else:
                            is_st_short  = True
                        if st_close_greaterthan_on_2 == 1:
                            is_st_short_2  = ohlc_intraday[date,ticker]["st_short"][i]
                        else:
                            is_st_short_2  = True
                        if sharesfloat_on == 1:
                            is_shares_float_test  = ohlc_intraday[date,ticker]["shares_float_test"][i]                        
                        else:
                            is_shares_float_test  = True
                        if market_cap_on == 1:
                            is_market_cap_test  = ohlc_intraday[date,ticker]["market_cap_test"][i]                        
                        else:
                            is_market_cap_test  = True
                        if drop_acquistions_on ==1:
                            is_drop_acquistions  = ohlc_intraday[date,ticker]["acq_test"][i]
                        else:
                            is_drop_acquistions  = True
                        if percent_from_pmh_on ==1:
                            is_from_pmh_test  = ohlc_intraday[date,ticker]["from_pmh_test"][i]
                        else:
                            is_from_pmh_test  = True
                        if buylocatecondition_on == 1:
                            is_buy_locate_condition  = ohlc_intraday[date,ticker]['buy_locate_condition'][i]
                        else:
                            is_buy_locate_condition  = True
                        if last_close_change_on_2 == 1:
                            is_last_close_change_2  = ohlc_intraday[date,ticker]["last_close_change_test_2"][i] 
                        else:
                            is_last_close_change_2  = True
                        if percent_from_pmh_on_2 == 1:
                            is_from_pmh_test_2  = ohlc_intraday[date,ticker]["from_pmh_test_2"][i]
                        else:
                            is_from_pmh_test_2  = True
                        ########################################################
                        ######## Conditions to open a long trade ###############
                        ########################################################    
                        if (
                            longshort == 'long' and
                            is_price_between == True and
                            is_buy_time == True and
                            is_sell_time == False and
                            is_buy_between_time == True and
                            is_volume_sum_greater  == True and
                            is_pm_volume_sum_greater  == True and
                            is_pm_gap_greater  == True and
                            is_first_tick_greater  == True and 
                            is_open_greater  == True and 
                            is_vwap_above == True and
                            is_vwap_below  == True and
                            is_last_close_change  == True and
                            is_dh_greater_than_pmh  == True and
                            is_pmg_greater_than_dy   == True and
                            is_st_long  == True and
                            is_st_short  == True and
                            is_shares_float_test  == True and
                            is_market_cap_test  == True and
                            is_drop_acquistions  == True and
                            is_from_pmh_test  == True and
                            is_buy_locate_condition == True and
                            open_price == 0 ):
                                trade_count += 1    
                                direction = 'long'
                                open_price = ohlc_intraday[date,ticker]["open"][i+1] # ["high"][i+1] +1 is the next candle. Need to work in slipage here  
                                # Calculate entry price with slippage
                                open_price_slippage = sc.calculate_open_slippage(direction, open_price, open_slippage)
                                ohlc_intraday[date,ticker]["trade_sig"][i+1] = open_price_slippage #  ["trade_sig"][i+1]          
                                if close_stop_on == 1:
                                    stop_price = open_price - (open_price * close_stop)  
                                elif pre_market_h_stop_on ==1 :
                                    pmh_price = indc.get_pmh_price(df,date)
                                    stop_price = pmh_price
                                    
                                loss_per_share = open_price - stop_price
                                #print('loss_per_share', loss_per_share)
                                max_shares = round((risk_per_trade / loss_per_share),0)
                                #print('Max shares', max_shares)
        
                                #print('Going Long ', ticker, ' Open price',open_price)
                                #print('Stop price ', stop_price)
                                
                        
                        #########################################################
                        ######## Conditions to open a short trade ###############
                        #########################################################   
                        
                        if (
                            longshort == 'short' and
                            is_price_between == True and
                            is_buy_time == True and
                            is_sell_time == False and
                            is_buy_between_time == True and
                            is_volume_sum_greater  == True and
                            is_pm_volume_sum_greater  == True and
                            is_pm_gap_greater  == True and
                            is_first_tick_greater  == True and 
                            is_open_greater  == True and 
                            is_vwap_above == True and
                            is_vwap_below  == True and
                            is_last_close_change  == True and
                            is_dh_greater_than_pmh  == True and
                            is_pmg_greater_than_dy   == True and
                            is_st_long  == True and
                            is_st_short  == True and
                            is_shares_float_test  == True and
                            is_market_cap_test  == True and
                            is_drop_acquistions  == True and
                            is_from_pmh_test  == True and
                            is_buy_locate_condition == True and
                            open_price == 0 ):
                                system_1_not_trade = False
                                trade_count += 1    
                                direction = 'short'
                                open_price = ohlc_intraday[date,ticker]["open"][i+1]# ["low"][i+1] +1 is the next candle. Need to work in slipage here  
                                open_price_slippage = sc.calculate_open_slippage(direction, open_price, open_slippage)
                                ohlc_intraday[date,ticker]["trade_sig"][i+1] = open_price_slippage# ["trade_sig"][i+1] 
                                # print('open_price',open_price)
                                # print('close_stop',close_stop)
                                # print('reward',reward)  
                                reward_price = open_price - ((open_price * close_stop) * reward)
                                # print('reward_price',reward_price)
                                          
                                # print('close_stop',close_stop)
                                if close_stop_on == 1:
                                    stop_price = (open_price * close_stop) + open_price
                                if pre_market_h_stop_on == 1:
                                    pmh_price = indc.get_pmh_price(df,date)
                                    #print('PMH price',pmh_price,ticker,date)
                                    stop_price = pmh_price 
                                loss_per_share =   stop_price - open_price
                                #print('loss_per_share', loss_per_share)
                                #max_shares = round((risk_per_trade / loss_per_share),0)
                                max_shares = round((risk_per_trade / loss_per_share),0)
                               
                                if max_shares < 100:
                                    locates_acq = 100   
                                else:
                                    locates_acq =  round(max_shares, -2) # rounds to the nearest 100
                                    max_shares = locates_acq
                                # print('Max Shares',max_shares)
                                # print('locates_acq',locates_acq)  
                                if locate_cost_per_on == 1:
                                    locate_cost_ps = open_price * max_locate_per_price
                                else:
                                    locate_cost_ps = locate_fee # fixed fee
                                # print('Going Short ', ticker, ' open_price',open_price)
                                # print('Stop price ', stop_price)
                        #########################################################
                        ######## Conditions to open second short trade ###############
                        #########################################################   
                        
                        if (
                            longshort == 'short' and
                            take_second_trade == True and
                            is_sell_time == False and
                            is_buy_between_time_2 == True and
                            is_price_between == True and
                            is_open_greater_2 == True and
                            is_last_close_change_2 == True and#
                            is_st_short_2  == True and
                            is_from_pmh_test_2  == True and
                            open_price_2 == 0 and
                            system_1_not_trade == True and
                            trade_count_2 == 0):
                                # print('-------------Starting second trade')
                                # trade_count += 1
                                trade_count_2 += 1
                                direction = 'short'
                                open_price_2 = ohlc_intraday[date,ticker]["open"][i+1] # ["low"][i+1] +1 is the next candle. Need to work in slipage here  
                                open_price_slippage_2 = sc.calculate_open_slippage(direction, open_price_2, open_slippage)
                                ohlc_intraday[date,ticker]["trade_sig_2"][i+1] =  open_price_slippage_2  # ["trade_sig"][i+1]  
                                reward_price_2 = open_price_2 - ((open_price_2 * close_stop_2) * reward)
                                          
                                if close_stop_on_2 == 1:
                                    stop_price_2 = (open_price_2 * close_stop_2) + open_price_2    
                                elif pre_market_h_stop_on == 1:
                                    pmh_price_2 = indc.get_pmh_price(df,date)
                                    #print('PMH price',pmh_price,ticker,date)
                                    stop_price_2 = pmh_price_2    
                                open_price_2 =  open_price_2
                                loss_per_share_2 =   stop_price_2 - open_price_2
                                #print('loss_per_share_2', loss_per_share_2)
                                max_shares_2 = round((risk_per_trade / loss_per_share_2),0)
                                if max_shares_2 < 100:
                                    locates_acq_2 = 100 
                                    #print('1 Max Shares',max_shares)
                                    #print('1 Locates',locate)
                                else:
                                    locates_acq_2 =  round(max_shares_2, -2)
                                    max_shares_2 = locates_acq_2
                                # print('2Max Shares',max_shares_2)  
                                # print('Going Short ', ticker, ' Price',open_price_2)
                                # print('Stop price ', stop_price_2)
                        
                        ###################################################
                        ####### If long trade is open  ###################        
                        #################################################
                        if  open_price != 0 and direction == 'long':
                            # Calculate trailing stop price
                            if (
                                trail_stop_on == 1 and 
                                ohlc_intraday[date,ticker]["open"][i] > last_high):
                                last_high = ohlc_intraday[date,ticker]["open"][i]
                                trail_stop_price_long = last_high * (1 - trail_stop_per)
                                #print('trail_stop_price_long',trail_stop_price_long)
                                #print('current price',ohlc_intraday[date,ticker]["high"][i]) 
                            #########################
                            #Check for take profit###
                            #########################
                            elif(
                                close_price == 0 and 
                                ohlc_intraday[date,ticker]["open"][i] > ((open_price * close_stop) * reward) + open_price) :
                                close_price = ohlc_intraday[date,ticker]["open"][i] #["low"][i+1]
                                close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage#["cover_sig"][i+1] = close_price
                                ticker_return = close_price_slippage - open_price_slippage  
                                date_stats[date][ticker] = ticker_return
                                outcome = 'take_profit'
                                #print('Taking profit',ticker, ' Price',close_price)
                                #print('Ticker return', ticker_return)
                                
                            ##################
                            #Trailing Stop ###
                            ##################
                            elif (
                                    trail_stop_on == 1 and 
                                    close_price == 0 and 
                                    ohlc_intraday[date,ticker]["open"][i] < trail_stop_price_long ) :
                                        close_price = ohlc_intraday[date,ticker]["open"][i]# ["low"][i+1]
                                        close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                        ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                        ticker_return = close_price_slippage - open_price_slippage 
                                        date_stats[date][ticker] = ticker_return
                                        outcome = 'trailing_stop_hit'
                                        #print('trailing_stop_hit',ticker, ' Price',close_price)
                                        #print('Ticker return', ticker_return)
                            
                            ##############
                            #Stop Loss ###
                            ##############
                            elif (
                                    close_price == 0 and 
                                    ohlc_intraday[date,ticker]["open"][i] < stop_price ) :# stop loss
                                        close_price = ohlc_intraday[date,ticker]["open"][i]
                                        close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                        ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                        ticker_return = close_price_slippage - open_price_slippage 
                                        date_stats[date][ticker] = ticker_return
                                        outcome = 'stopped_out'
                                        #print('Stopped out',ticker, ' Price',close_price)
                                        #print('Ticker return', ticker_return)
                           
                            ###############
                            # VWAP above ###
                            ###############
                            # elif (
                            #         close_price == 0 and 
                            #         ohlc_intraday[date,ticker]["vwap_below"][i] == False ) :# stop loss
                            #             close_price = ohlc_intraday[date,ticker]["low"][i+1]
                            #             ohlc_intraday[date,ticker]["cover_sig"][i+1] = close_price
                            #             ticker_return = close_price - open_price 
                            #             date_stats[date][ticker] = ticker_return
                            #             outcome = 'vwaped'
                            #             print('VWAPED',ticker, ' Price',close_price)
                            #             print('Ticker return', ticker_return)
                            #             break
                            ###############
                            # Time stop
                            ###############  
                            elif ( 
                                    close_price == 0 and  
                                    ohlc_intraday[date,ticker]["sell_time"][i] == True):
                                        close_price = ohlc_intraday[date,ticker]["open"][i]
                                        close_price_slippage = close_price
                                        # close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                        ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                        ticker_return = close_price_slippage - open_price_slippage 
                                        date_stats[date][ticker] = ticker_return
                                        outcome = 'time_stop'
                                        #print('Sell time hit',ticker, ' Price',close_price)
                                        #print('Ticker return', ticker_return)
                        
                        ###################################################
                        ####### If short trade is open  ###################        
                        ###################################################
                        if  open_price != 0 and direction == 'short':
                            # Check for 3R  profit, then keep 3R as min, then let it run                       
                            if (
                                min_reward_then_let_it_run == 1 and
                                close_price == 0 and
                                take_profit_count == 0 and
                                ohlc_intraday[date,ticker]["high"][i] <  reward_price): # is 3 times the risk price to get 3R
                                take_profit_count += 1
                                last_low = ohlc_intraday[date,ticker]["high"][i] # keeps track of the lowest price
                                # print('last_low',last_low)
                                trail_stop_price_short = ohlc_intraday[date,ticker]["high"][i] * (1 + .02) # adds a percentage above so dont get stopped stright away
                                # print('Tight stop here of 2 %')
                                # print(reward,'R, Price target hit. New stop price',trail_stop_price_short)
                                # print('Last high price',last_low)
                            
                            # trail stop continues after take profit 3 r     
                            elif(
                                min_reward_then_let_it_run == 1 and
                                close_price == 0 and
                                take_profit_count > 0 and
                                ohlc_intraday[date,ticker]["high"][i] < last_low): #if price keeps dropping
                                last_low = ohlc_intraday[date,ticker]["high"][i] # move last low doun for next loop
                                trail_stop_price_short = ohlc_intraday[date,ticker]["high"][i] * (1 + trail_stop_per)#new trail stop out price
                                #print('New trail stop price',trail_stop_price_short)
                            
                            # check if trail stop stopped out
                            elif(
                                min_reward_then_let_it_run == 1 and
                                close_price == 0 and
                                take_profit_count > 0 and
                                ohlc_intraday[date,ticker]["high"][i] > trail_stop_price_short):# stopped out
                                #close_price = ohlc_intraday[date,ticker]["open"][i]#slipage
                                system_1_not_trade = True
                                close_price = trail_stop_price_short
                                close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                ticker_return = open_price_slippage - close_price_slippage
                                date_stats[date][ticker] = ticker_return
                                outcome = 'trailing_stop_hit'
                                # print('Trail stop hit')
                                # print('min_r_trail_stop_hit',ticker, ' Price',close_price)
                                # print('Ticker return', ticker_return)
                        
                              
                            ##################
                            #Trailing Stop ###
                            ##################
                            elif (
                                  trail_stop_on == 1 and 
                                  close_price == 0 and 
                                  ohlc_intraday[date,ticker]["high"][i] > trail_stop_price_short ) :# stop loss
                                      #close_price = ohlc_intraday[date,ticker]["open"][i]#slipage
                                      system_1_not_trade = True
                                      close_price = trail_stop_price_short 
                                      close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                      ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                      ticker_return = open_price_slippage - close_price_slippage
                                      date_stats[date][ticker] = ticker_return
                                      outcome = 'trailing_stop_hit'
                                      print('trailing_stop_hit',ticker, ' Price',close_price)
                                      print('Ticker return', ticker_return)
                                
                            ###############
                            # Stop Loss ###
                            ###############
                            elif (
                                  close_price == 0 and 
                                  ohlc_intraday[date,ticker]["high"][i] > stop_price) :# stop loss
                                      system_1_not_trade = True
                                      close_price = stop_price
                                      close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                      ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage 
                                      ticker_return = open_price_slippage - close_price_slippage 
                                      date_stats[date][ticker] = ticker_return
                                      outcome = 'stopped_out'
                                      # print('Stopped out',ticker, ' Price',stop_price)
                                      # print('Ticker return', ticker_return)
                            ###############
                            # Time stop
                            ###############  
                            if ( 
                                    close_price == 0 and  
                                    ohlc_intraday[date,ticker]["sell_time"][i+1] == True):
                                        system_1_not_trade = True
                                        close_price = ohlc_intraday[date,ticker]["open"][i]
                                        close_price_slippage = close_price 
                                        # close_price_slippage = sc.calculate_close_slippage(direction, close_price, close_slippage)
                                        ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                        ticker_return = open_price_slippage - close_price_slippage
                                        date_stats[date][ticker] = ticker_return
                                        outcome = 'time_stop'
                                        # print('Sell time hit',ticker, ' Price',close_price)
                                        # print('Ticker return', ticker_return)          
                                    
                            
                            
                        
                        ###################################################
                        ####### If second short trade is open  #############        
                        ###################################################
                        if  open_price_2 != 0 and direction == 'short':                    
                            # Check for 3R  profit, then keep 3R as min, then let it run                       
                            if (
                                min_reward_then_let_it_run_2 == 1 and
                                close_price_2 == 0 and
                                take_profit_count_2 == 0 and
                                ohlc_intraday[date,ticker]["high"][i] <  reward_price_2): # is 3 times the risk price to get 3R
                                take_profit_count_2 += 1
                                last_low_2 = ohlc_intraday[date,ticker]["high"][i] # keeps track of the lowest price
                                
                                trail_stop_price_short_2 = ohlc_intraday[date,ticker]["high"][i] * (1 + .02) # adds a percentage above so dont get stopped stright away
                                # print('Tight stop here of 2 %')
                                # print(reward,'R, Price target hit. New stop price',trail_stop_price_short_2)
                                # print('Last high price',last_low_2)
                            # trail stop continues after take profit 3 r     
                            elif(
                                min_reward_then_let_it_run_2 == 1 and
                                close_price_2 == 0 and
                                take_profit_count_2 > 0 and
                                ohlc_intraday[date,ticker]["high"][i] < last_low_2): #if price keeps dropping
                                last_low_2 = ohlc_intraday[date,ticker]["high"][i] # move last low doun for next loop
                                trail_stop_price_short_2 = ohlc_intraday[date,ticker]["high"][i] * (1 + trail_stop_per)#new trail stop out price
                                #print('New trail stop price-2',trail_stop_price_short_2,'last high',last_low_2)
                            # check if trail stop stopped out
                            elif(
                                min_reward_then_let_it_run_2 == 1 and
                                close_price_2 == 0 and
                                take_profit_count_2 > 0 and
                                ohlc_intraday[date,ticker]["high"][i] > trail_stop_price_short_2):# stopped out
                                #close_price_2 = ohlc_intraday[date,ticker]["open"][i]#slipage
                                close_price_2 = trail_stop_price_short_2
                                close_price_slippage_2 = sc.calculate_close_slippage(direction, close_price_2, close_slippage)
                                ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_slippage
                                ticker_return_2 = open_price_slippage_2 - close_price_slippage_2
                                date_stats[date][ticker] = ticker_return_2
                                outcome_2 = 'trailing_stop_hit_2'
                                # print('Trail stop hit')
                                # print('min_r_trail_stop_hit',ticker, ' Price',close_price_2)
                                # print('Ticker return', ticker_return_2)
                            # Calculate trailing stop price  
                            ###############
                            # Second Time stop
                            ###############  
                            if ( 
                                    close_price_2 == 0 and  
                                    direction == 'short' and
                                    ohlc_intraday[date,ticker]["sell_time"][i] == True):
                                        close_price_2 = ohlc_intraday[date,ticker]["open"][i]  
                                        close_price_slippage_2 = close_price_2
                                        # close_price_slippage_2 = sc.calculate_close_slippage(direction, close_price_2, close_slippage)
                                        ohlc_intraday[date,ticker]["cover_sig_2"][i] = close_price_slippage_2
                                        ticker_return_2 = open_price_slippage_2 - close_price_slippage_2
                                        date_stats_2[date][ticker] = ticker_return_2
                                        outcome_2 = 'time_stop_2'
                                        #print('Sell time hit',ticker, ' Price',close_price)
                                        #print('Ticker return', ticker_return)
                            #####################
                            # Second Stop Loss ##
                            #####################
                            elif (
                                  close_price_2 == 0 and 
                                  ohlc_intraday[date,ticker]["high"][i+1] > stop_price_2) :# stop loss
                                      #close_price_2 = ohlc_intraday[date,ticker]["open"][i+1]
                                      close_price_2 = stop_price_2 
                                      close_price_slippage_2 = sc.calculate_close_slippage(direction, close_price_2, close_slippage)
                                      ohlc_intraday[date,ticker]["cover_sig_2"][i] = close_price_slippage_2 
                                      ticker_return_2 = open_price_slippage_2 - close_price_slippage_2
                                      date_stats_2[date][ticker] = ticker_return_2
                                      outcome_2 = 'stopped_out_2'
                                      # print('Stopped out',ticker, ' Price',close_price)
                                      # print('Ticker return', ticker_return)  
                                      break      
                    system_one_profit = []
                    system_two_profit = []
                    
                    # Calculate returns for strategy one.
                    if ticker_return != 0:
                        payout =  ticker_return * max_shares
                        if locate_cost_per_on == 1:
                            locate_cost_ps = open_price * max_locate_per_price
                        else:
                            locate_cost_ps = locate_fee # fixed fee
                        locate_cost = locate_cost_ps * max_shares
                        
                        strategy1_comm = (trip_comm * trade_count)+locate_cost
                        strategy1_return  = (payout - strategy1_comm)
                        print('strategy1_return',strategy1_return )
                    # Calculate returns for strategy two.
                    if ticker_return_2 != 0:
                        payout_2 =  ticker_return_2 * max_shares_2
                        # Check if shares have already been located
                        if locate_cost != 0:
                            if locate_cost_per_on == 1:
                                locate_cost_ps_2 = open_price_2 * max_locate_per_price
                            else:
                                locate_cost_ps_2 = locate_fee # fixed fee
                            locate_cost_2 = locate_cost_ps_2 * max_shares_2
                            
                        strategy2_comm = (trip_comm * trade_count_2) + locate_cost_2
                        strategy2_return = (payout_2 - strategy2_comm)
                        print('strategy2_return',strategy2_return)
                    
                    # # Calculate the new account balance for each strategy 
                    # strategy1_balance = strategy1_equity + [strategy1_return]

                    strategy1_balance = strategy1_equity + strategy1_return
                    print('strategy1_balance',strategy1_balance)
                    strategy2_balance = strategy2_equity + strategy2_return
                    print('strategy2_balance',strategy2_balance)
                    combined_balance = combined_equity + strategy1_return + strategy2_return
                    print('combined_balance',combined_balance)
                    # # Append the new account balance to each equity curve list
                    strategy1_equity_gain.append(strategy1_balance)
                    strategy2_equity_gain.append(strategy2_balance)
                    combined_equity_gain.append(combined_balance)
                    
                    print(f'Strategy 1 final equity: {strategy1_equity_gain[-1]}')
                    print(f'Strategy 2 final equity: {strategy2_equity_gain[-1]}')
                    print(f'Combined strategy final equity: {combined_equity_gain[-1]}')


                    # new_gain =  (payout - new_commission)  + (payout_2 - new_commission_2)
                    # total_Gain = imaginary_account + full_balance
                    # gains.append(total_Gain)
                    # print('gains',gains)
                    
                    # total_Gain_2 = imaginary_account_2 + full_balance_2
                    # gains_2.append(total_Gain_2)
                    # print('gains_2',gains_2)
                    # new_new_gain.append(new_gain+5000)
                    # print('new_new_gain',new_new_gain)
                    
                    
                    #print('Adding this ticker to Results df        ',date,ticker)
                    results = pd.DataFrame([[date, ticker ,  open_price_slippage, close_price_slippage,   stop_price,  ticker_return,  outcome,  max_shares,  locates_acq, locate_cost_ps,  open_price_slippage_2, close_price_slippage_2,   stop_price_2,  ticker_return_2,  outcome_2,  trade_count, trade_count_2,  max_shares_2,  locates_acq_2]],
                                   columns=['date','ticker',  'open_price',       'close_price',          'stop_price','ticker_return','outcome','max_shares','locates_acq','locate_cost_ps','open_price_2',        'close_price_2',          'stop_price_2','ticker_return_2','outcome_2','trade_count','trade_count_2','max_shares_2','locates_acq_2'] )  
                    #Adds new line to dic each loop 
                    # results_store = results_store.append(results,ignore_index=True) 
                    results_store = pd.concat([results_store, results], ignore_index=True)

                    results_store.reset_index(drop=True)        
                    
                    # print("**********Strategy Performance Statistics**********")
                    # print("total cumulative return = {}".format(round(abs_return(date_stats),4)))
                    # print("total win rate = {}".format(round(win_rate(date_stats),2)))
                    # print("mean return per win trade = {}".format(round(mean_ret_winner(date_stats),4)))
                    # print("mean return per loss trade = {}".format(round(mean_ret_loser(date_stats),4)))
                    
                    # btresults = pd.DataFrame([[longshort,sharesfloat_min, sharesfloat_max, market_cap_min, market_cap_max,last_close_per, open_greater, vol_sum_greaterthan, buy_after, close_stop, vwap_below_on,st_close_lessthan_on, reward,trail_stop_per ,num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal]],
                    #                         columns=['longshort','sharesfloat_min', 'sharesfloat_max', 'market_cap_min', 'market_cap_max','last_close_per','open_greater','vol_sum_greaterthan','buy_after','close_stop','vwap_below_on','st_close_lessthan_on','reward','trail_stop_per','num_of_trades', 'total_win', 'win_per', 'gross_profit','total_locate_fee','total_comm','finish_bal'] )  

                        
                        
        ###########################################################################################################
        ###################################  Plot    ##############################################################
        ###########################################################################################################

                    if plot == 1 and trade_count >= plot_trades_only or trade_count_2 >= plot_trades_only :
                        my_plt.plot_fips(self,strategy1_equity_gain, strategy2_equity_gain,combined_equity_gain)
                        my_plt.plt_chart(self,longshort ,date, ticker, ohlc_intraday,outcome,ticker_return,outcome_2,ticker_return_2)
                    else:
                        pass
                
                
                
                # except (FileNotFoundError,IndexError ) as e:
                #     print(e)
                #     print('Interday file not found for ----------------------------------------------', date, ticker)  
                    # date1 = date.strftime("%Y-%m-%d")
                    # print('Getting interday data for',ticker,date1)
                    # missingdf = polygon_interday(ticker,date1)
                        
                    # #Save Intraday data for each Gapper for the future 
                    # dateticker = date1 + ' ' + ticker +'.csv' # adds ticker to date
                    # missingdf.to_csv(r'C:\Users\brian\Desktop\PythonProgram\Intraday_Ticker_Database\download_all_2022\%s'% dateticker )
                    # missingdf.to_csv(r'B:\2T_Quant\Intraday_Ticker_Database_2T\download_all_2022_2T\%s'% dateticker ) 
                    # print('Missin data retrived')
                    # pass
                
        #####################################################################################################################
        ######  Calculating results ##
        #####################################################################################################################
        # last_value = new_new_gain[-1]
        # print('new_new_gain------',last_value)
        results_store, num_of_trades, total_win,  gross_profit,total_locate_fee,total_comm,win_per,finish_bal  = Results.cal_results(self, active_value, results_store,risk_per_trade)
        print('It took', (time.time()-start)/60, 'minutes.')
        print('Finished')
        btresults = pd.DataFrame([[longshort,sharesfloat_min, sharesfloat_max, market_cap_min, market_cap_max,last_close_per, open_greater, vol_sum_greaterthan, buy_after, close_stop, vwap_below_on,st_close_lessthan_on, reward, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal]],
                                 columns=['longshort','sharesfloat_min', 'sharesfloat_max', 'market_cap_min', 'market_cap_max','last_close_per','open_greater','vol_sum_greaterthan','buy_after','close_stop','vwap_below_on','st_close_lessthan_on','reward','num_of_trades', 'total_win', 'win_per', 'gross_profit','total_locate_fee','total_comm','finish_bal'] )  
                                                #Adds new line to dic each loop 
                                                
        # btresults_store = btresults_store.append(btresults,ignore_index=True) 
        # btresults_store.reset_index(drop=True)
        # Get todays date
        today_dt = datetime.now()
        today = today_dt.strftime("%Y-%m-%d")
        time_now = today_dt.strftime("_%H-%M")
        results_name = today + time_now +  '_backtest_results.csv' #
        if mac == 1:
            btresults.to_csv("/Users/briansheehan/Documents/mac_quant/%s"% results_name, index=False)
            
        if mac == 0:
            btresults.to_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s"% results_name, index=False)
        return ohlc_intraday, results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal ,date_stats, date_stats_2 

