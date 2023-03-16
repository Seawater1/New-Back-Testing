# -*- coding: utf-8 -*-
"""
sharep ration
max drawdown
loaddata df3 need a good looking at
"""


# Import libraries

import pandas as pd
import time
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from time import sleep
import time
import math
import matplotlib as mpl
import random
from datetime import datetime, timedelta
import telegram_send
import pytz
import requests

from main import Backtester
import main

indc = main.Indicators()






plt.style.use('ggplot')#Data Viz

start = time.time()
pd.options.mode.chained_assignment = None # wprloing with copy warning disable
# so annoying cant figure out copy not 

#Get todays date
today_dt = datetime.now()
today = today_dt.strftime("%Y-%m-%d")
time_now = today_dt.strftime("_%H-%M")





def polygon_interday(symbol,date):
    api_key = 'Or7vNE5Zw48s7lVMH5vecZJnUd7Ntgcd'
    # Set the URL for the API request
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{date}/{date}?adjusted=true&limit=50000&apiKey={api_key}'#https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2021-07-22/2021-07-22?adjusted=false&sort=asc&limit=50000&apiKey=R8G47SaJzsO0NS5JoorpojbyMcOHmur5
    # Send the request and store the response
    response = requests.get(url)
    # Convert the response to a JSON object
    data = response.json()
    # Extract the OHLC data from the JSON object
    df = pd.DataFrame(data['results'])[['t', 'o', 'h', 'l', 'c', 'v', 'vw']]
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_weighted']
    df.drop(columns='volume_weighted', axis=1, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(pytz.timezone('UTC')).dt.tz_convert(pytz.timezone('US/Eastern'))
    df.set_index('timestamp', inplace=True)
    # VWAP Calculations 
    df['vwap'] = (df['volume']*(df['high']+df['low']+df['close'])/3).cumsum() / df['volume'].cumsum() 

    return df



def plt_chart(active_value,date, ticker, ohlc_intraday,outcome,ticker_return,outcome_2,ticker_return_2):
    longshort = active_value['longshort']
    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8))
    
    ax[0].plot(ohlc_intraday[date,ticker].index, ohlc_intraday[date,ticker].close,ohlc_intraday[date,ticker].vwap)
    ax[1].bar(ohlc_intraday[date,ticker].index, ohlc_intraday[date,ticker].volume, width=1/(5*len(ohlc_intraday[date,ticker].index)))
    ax[0].plot(ohlc_intraday[date,ticker]['st'], color = 'green', linewidth = 2, label = 'ST UPTREND')
    ax[0].plot(ohlc_intraday[date,ticker]['st_dt'], color = 'r', linewidth = 2, label = 'ST DOWNTREND')
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
####################################################################################################################
####################################################################################################################
###########################################             The big picture          ###################################
####################################################################################################################





####################################################################################################################
####################################################################################################################

ohlc_intraday = {}
def backtester(active_value):
    mac = active_value['mac']
    longshort = active_value["longshort"]
    plot = active_value["plot"]
    plot_trades_only = active_value["plot_trades_only"]
    save_winners_df = active_value["save_winners_df"]
    start_balance = active_value["start_balance"]
    risk_acc = active_value["risk_acc"]
    full_balance = active_value["full_balance"]
    imaginary_account = active_value["imaginary_account"]
    full_balance_2 = active_value["full_balance_2"]
    imaginary_account_2 = active_value["imaginary_account_2"]
    bet_percentage = active_value["bet_percentage"]
    max_locate_per_price = active_value["max_locate_per_price"]
    max_risk = active_value["max_risk"]
    open_slippage = active_value["open_slippage"]
    close_slippage = active_value["close_slippage"]
    

    lookback = active_value["lookback"]
    multiplier = active_value["multiplier"]
    lenth = active_value["lenth"]
    lessthan = active_value["lessthan"]
    shift = active_value["shift"]
    drop_acquistions_on = active_value["drop_acquistions_on"]
    aq_value = active_value["aq_value"]
    locate_fee = active_value["locate_fee"]
    trip_comm = active_value["trip_comm"]
    close_stop_on = active_value["close_stop_on"]
    close_stop = active_value["close_stop"]


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
    last_close_change_on_2 = active_value["last_close_change_on_2"]
    last_close_per = active_value["last_close_per"],
    percent_from_pmh_on = active_value["percent_from_pmh_on"]
    per_pmh_val = active_value["per_pmh_val"]
    day_greater_than_pm_on = active_value["day_greater_than_pm_on"]
    pm_greater_than_day_on = active_value["pm_greater_than_day_on"]
    st_close_lessthan_on = active_value["st_close_lessthan_on"]
    st_close_greaterthan_on = active_value["st_close_greaterthan_on"]
    st_close_greaterthan_on_2 = active_value["st_close_greaterthan_on_2"]

    
    print('------  Starting Testing strategy  ---------------------------------------------------------')      
    print('Going ', longshort)
    #dictionarys to store data
    gains = [] 
    gains_2 = []
    total_win = 0
    total_loss = 0
    date_stats = {} # stores the returns 
    date_stats_2 = {} # stores the returns
    #Data Frame to store data
    results_store = pd.DataFrame()
    for date in top_gap_by_date:
        date_stats[date] = {} #store the day return of eash ticker
        date_stats_2[date] = {} #store the day return of eash ticker
        for ticker in top_gap_by_date[date]:# the key is date
            #print('Loading data and applying indicator for ',date,ticker)
            try:
                print()
                total_risk = start_balance * risk_acc
                risk_per_trade = imaginary_account * bet_percentage
                
                if risk_per_trade > max_risk:
                    risk_per_trade = max_risk
                    print('Compounding off ')
                print('risk_per_trade',risk_per_trade)
                df = bt.load_interday(date,ticker,mac,flt_database)# load interday files ??? does this need to be moved to the top of fucntion
                # get last close price
                last_close = top_gap_by_date[date][ticker]

                # apply super trend always for chart
                df['st'], df['s_upt'], df['st_dt'] = indc.get_supertrend(df['high'], df['low'], df['close'], lookback, multiplier)
                
                if sharesfloat_on == 1:
                    df = indc.float_share_between(df,sharesfloat_min,sharesfloat_max)
                if market_cap_on == 1:
                    df = indc.market_cap_between(df, market_cap_min, market_cap_max)
                if price_between_on == 1:#1
                    df = indc.price_between(df,min_between_price, max_between_price )
                if buytime_on == 1:#2
                    df = indc.buytime(df,date,buy_time)# Time Greater than
                if selltime_on == 1:#3
                    df = indc.selltime(df,date,sell_time)
                if buy_between_time_on == 1:#4
                    df = indc.buy_between_time(df, date, buy_after, buy_before)
                if buy_between_time_on_2 == 1:#4
                    df = indc.buy_between_time_2(df, date, buy_after_2, buy_before_2)
                if volume_sum_cal_on == 1:#5
                    df = indc.volume_sum_cal(df,vol_sum_greaterthan)
                if pm_volume_sum_cal_on == 1:#6
                    df = indc.pm_volume_sum_cal(df,date, pm_volume_sum_greaterthat)
                if pm_gap_on == 1:#7
                    df = indc.pm_gap(df,date,last_close, pmg_greater) 
                if per_change_first_tick_on == 1:#8
                    df = indc.per_change_first_tick(df, precent_greater)
                if per_change_open_on == 1 or per_change_open_on_2 == 1:
                    df = indc.per_change_open(df,date, open_greater)                    
                if vwap_above_on == 1:#9
                    df = indc.vwap_above(df)# Close below VWAP
                if vwap_below_on == 1:#10
                    df = indc.vwap_below(df)
                if last_close_change_on ==1 or last_close_change_on_2 ==1:#11
                    df = indc.last_close_change(df,last_close,last_close_per)
                if day_greater_than_pm_on ==1:#12  
                    df = indc.day_greater_than_pm(df,date)
                if pm_greater_than_day_on ==1: 
                    df = indc.pm_greater_than_day(df,date)
                if st_close_lessthan_on == 1:#13
                    df = indc.st_close_lessthan(df)#Supertrend lessthan
                if st_close_greaterthan_on == 1 or st_close_greaterthan_on_2 == 1:#14
                    df = indc.st_close_greaterthan(df)#Supertrend greather than
                if drop_acquistions_on ==1:
                    df = indc.drop_acquistions(df,date,aq_value)
                if percent_from_pmh_on ==1:
                    df = indc.percent_from_pmh(df,date,per_pmh_val)
                
                
                df['trade_sig'] = np.nan
                df['trade_sig_2'] = np.nan
                df['cover_sig'] = np.nan
                df['cover_sig_2'] = np.nan
                df['trade_count'] = np.nan
                df['trade_count_2'] = np.nan
                open_price = '' # price you open a trade
                open_price_2 = '' 
                direction = '' # Long short
                date_stats[date][ticker] = (0) # Setting the return to zero to start
                date_stats_2[date][ticker] = (0)
                ohlc_intraday[date,ticker] = df # stores interday data in dictionary
                #Testing
                open_price = 0
                open_price_2 = 0
                close_price = 0
                close_price_2 = 0
                #sell_price  = 0
                max_shares  = 0
                max_shares_2  = 0
                stop_price  = 0
                stop_price_2 = 0
                locate = 0
                locate_2 = 0
                ticker_return = 0
                ticker_return_2 = 0
                trade_count = 0
                trade_count_2 = 0
                outcome = 'no_trade'
                outcome_2 = 'no_trade_2'
                last_high = 0
                
                last_low = 99999999
                last_low_2 = 99999999
                trail_stop_price_short = 999999999
                trail_stop_price_short_2 = 999999999
                take_profit_count = 0
                take_profit_count_2 = 0
                for i in range(len(ohlc_intraday[date,ticker])):# he skips the first bar (1,len) do i need to do this 
                    if price_between_on == 1:
                        one = ohlc_intraday[date,ticker]['price_between'][i]
                    else:
                        one = True
                    if buytime_on == 1:
                        two = ohlc_intraday[date,ticker]['buy_time'][i]
                    else:
                        two = True
                    if selltime_on == 1:
                        three = ohlc_intraday[date,ticker]["sell_time"][i]
                    else:
                        three = False
                    if buy_between_time_on ==1:
                        four = ohlc_intraday[date,ticker]["buy_between_time"][i]
                    else:
                        four = False
                    if buy_between_time_on_2 ==1:
                        four_2 = ohlc_intraday[date,ticker]["buy_between_time_2"][i]
                    else:
                        four_2 = False
                    if volume_sum_cal_on == 1:
                        five = ohlc_intraday[date,ticker]["vol_sum_greater"][i]
                    else:
                        five = True
                    if pm_volume_sum_cal_on == 1:
                        six = ohlc_intraday[date,ticker]["pm_vol_sum_greater"][i]
                    else:
                        six = True
                    if pm_gap_on == 1:
                        seven = ohlc_intraday[date,ticker]["pm_gap_greater"][i] 
                    else:
                        seven = True
                    if per_change_first_tick_on == 1:
                        eight = ohlc_intraday[date,ticker]["first_tick_greater"][i]
                    else:
                        eight = True
                    if per_change_open_on == 1:
                        pcoo = ohlc_intraday[date,ticker]["open_greater"][i]
                    else:
                        pcoo = True
                    if per_change_open_on_2 == 1:
                        pcoo_2 = ohlc_intraday[date,ticker]["open_greater"][i]
                    else:
                        pcoo_2 = True
                    if vwap_above_on == 1:
                        nine = ohlc_intraday[date,ticker]["vwap_above"][i]
                    else:
                        nine = True
                    if vwap_below_on == 1:
                        ten = ohlc_intraday[date,ticker]["vwap_below"][i]
                    else:
                        ten = True
                    if last_close_change_on == 1:
                        eleven = ohlc_intraday[date,ticker]["last_close_change_test"][i] 
                    else:
                        eleven = True
                    if day_greater_than_pm_on ==1:   
                        twelve = ohlc_intraday[date,ticker]['dh>pmh'][i]
                    else:
                        twelve = True 
                    if pm_greater_than_day_on ==1:   
                        pm_g_t_d = ohlc_intraday[date,ticker]['pmg>dy'][i]
                    else:
                        pm_g_t_d = True 
                    if st_close_lessthan_on == 1:
                        thirteen = ohlc_intraday[date,ticker]["st_long"][i]
                    else:
                        thirteen = True 
                    if st_close_greaterthan_on == 1:
                        fourteen = ohlc_intraday[date,ticker]["st_short"][i]
                    else:
                        fourteen = True
                    if st_close_greaterthan_on_2 == 1:
                        fourteen_2 = ohlc_intraday[date,ticker]["st_short"][i]
                    else:
                        fourteen_2 = True
                    if sharesfloat_on == 1:
                        s_f_test = ohlc_intraday[date,ticker]["shares_float_test"][i]                        
                    else:
                        s_f_test = True
                    if market_cap_on == 1:
                        m_c_test = ohlc_intraday[date,ticker]["market_cap_test"][i]                        
                    else:
                        m_c_test = True
                    if drop_acquistions_on ==1:
                        dacq = ohlc_intraday[date,ticker]["acq_test"][i]
                    else:
                        dacq = True
                    if percent_from_pmh_on ==1:
                        pmh_t = ohlc_intraday[date,ticker]["from_pmh_test"][i]
                    else:
                        pmh_t = True
                    ########################################################
                    ######## Conditions to open a long trade ###############
                    ########################################################    
                    if (
                        longshort == 'long' and
                        one == True and
                        two == True and
                        three == False and
                        four == True and
                        five == True and
                        six == True and
                        seven == True and
                        eight == True and 
                        pcoo == True and 
                        nine == True and
                        ten == True and
                        eleven == True and
                        twelve == True and
                        pm_g_t_d  == True and
                        thirteen == True and
                        fourteen == True and
                        s_f_test == True and
                        m_c_test == True and
                        dacq == True and
                        pmh_t == True and
                        open_price == 0 ):
                            trade_count += 1    
                            direction = 'long'
                            open_price = ohlc_intraday[date,ticker]["open"][i+1] # ["high"][i+1] +1 is the next candle. Need to work in slipage here  
                            ohlc_intraday[date,ticker]["trade_sig"][i+1] = open_price #  ["trade_sig"][i+1]          
                            if close_stop_on == 1:
                                stop_price = open_price - (open_price * close_stop)  
                            elif pre_market_h_stop_on ==1 :
                                pmh_price = indc.get_pmh_price(df,date)
                                stop_price = pmh_price
                                
                            loss_per_share = open_price - stop_price
                            #print('loss_per_share', loss_per_share)
                            max_shares = round((total_risk / loss_per_share),0)
                            #print('Max shares', max_shares)
    
                            #print('Going Long ', ticker, ' Open price',open_price)
                            #print('Stop price ', stop_price)
                            
                    
                    #########################################################
                    ######## Conditions to open a short trade ###############
                    #########################################################   
                    
                    if (
                        longshort == 'short' and
                        one == True and
                        two == True and
                        three == False and
                        four == True and
                        five == True and
                        six == True and
                        seven == True and
                        eight == True and
                        pcoo == True and
                        nine == True and
                        ten == True and
                        eleven == True and
                        twelve == True and
                        pm_g_t_d  == True and
                        thirteen == True and
                        fourteen == True and
                        s_f_test == True and
                        m_c_test == True and
                        dacq == True and
                        pmh_t == True and
                        open_price == 0 ):
                            trade_count += 1    
                            direction = 'short'
                            open_price = ohlc_intraday[date,ticker]["open"][i+1]# ["low"][i+1] +1 is the next candle. Need to work in slipage here  
                            print('open_price',open_price)
                            print('close_stop',close_stop)
                            print('reward',reward)
                            reward_price = open_price - ((open_price * close_stop) * reward)
                            print('reward_price',reward_price)
                            ohlc_intraday[date,ticker]["trade_sig"][i+1] = open_price# ["trade_sig"][i+1]            
                            print('close_stop',close_stop)
                            if close_stop_on == 1:
                                stop_price = (open_price * close_stop) + open_price
                            if pre_market_h_stop_on == 1:
                                pmh_price = indc.get_pmh_price(df,date)
                                #print('PMH price',pmh_price,ticker,date)
                                stop_price = pmh_price 
                            loss_per_share =   stop_price - open_price
                            #print('loss_per_share', loss_per_share)
                            #max_shares = round((total_risk / loss_per_share),0)
                            max_shares = round((risk_per_trade / loss_per_share),0)
                           
                            if max_shares < 100:
                                locate = 100   
                            else:
                                locate =  round(max_shares, -2)
                                max_shares = locate
                            print('Max Shares',max_shares)
                            print('Locates',locate)   
                            print('Going Short ', ticker, ' open_price',open_price)
                            print('Stop price ', stop_price)
                    #########################################################
                    ######## Conditions to open second short trade ###############
                    #########################################################   
                    
                    if (
                        longshort == 'short' and
                        1 == 2 and
                        # one == True and
                        # two == True and
                        # three == False and
                        four_2 == True and
                        # five == True and
                        # six == True and
                        # seven == True and
                        # eight == True and
                        pcoo_2 == True and
                        # nine == True and
                        # ten == True and
                        eleven == True and
                        # twelve == True and
                        # pm_g_t_d  == True and
                        # thirteen == True and
                        fourteen_2 == True and
                        # s_f_test == True and
                        # m_c_test == True and
                        # dacq == True and
                        # pmh_t == True and
                        open_price_2 == 0 and
                        ticker_return != 0 and
                        trade_count == 1):
                            print('-------------Starting second trade')
                            # trade_count += 1
                            trade_count_2 += 1
                            direction = 'short'
                            open_price_2 = ohlc_intraday[date,ticker]["open"][i+1] # ["low"][i+1] +1 is the next candle. Need to work in slipage here  
                            
                            reward_price_2 = open_price_2 - ((open_price_2 * close_stop) * reward)
                            ohlc_intraday[date,ticker]["trade_sig_2"][i+1] =  open_price_2  # ["trade_sig"][i+1]            
                            if close_stop_on == 1:
                                stop_price_2 = (open_price_2 * close_stop) + open_price_2    
                            elif pre_market_h_stop_on == 1:
                                pmh_price_2 = indc.get_pmh_price(df,date)
                                #print('PMH price',pmh_price,ticker,date)
                                stop_price_2 = pmh_price_2    
                            open_price_2 =  open_price_2
                            loss_per_share_2 =   stop_price_2 - open_price_2
                            #print('loss_per_share_2', loss_per_share_2)
                            max_shares_2 = round((total_risk / loss_per_share_2),0)
                            if max_shares_2 < 100:
                                locate_2 = 100 
                                #print('1 Max Shares',max_shares)
                                #print('1 Locates',locate)
                            else:
                                locate_2 =  round(max_shares_2, -2)
                                max_shares_2 = locate_2
                            print('2Max Shares',max_shares_2)
                            print('2Locates',locate_2)   
                            print('Going Short ', ticker, ' Price',open_price_2)
                            print('Stop price ', stop_price_2)
                    
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
                            ohlc_intraday[date,ticker]["cover_sig"][i] = close_price#["cover_sig"][i+1] = close_price
                            ticker_return = close_price - open_price  
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
                                    ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                                    ticker_return = close_price - open_price 
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
                                    ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                                    ticker_return = close_price - open_price 
                                    date_stats[date][ticker] = ticker_return
                                    outcome = 'stopped_out'
                                    #print('Stopped out',ticker, ' Price',close_price)
                                    #print('Ticker return', ticker_return)
                        ####################
                        #Second Stop Loss ##
                        ####################
                        elif (
                                close_price_2 == 0 and 
                                ohlc_intraday[date,ticker]["open"][i] < stop_price ) :# stop loss
                                    close_price_2 = ohlc_intraday[date,ticker]["open"][i]
                                    ohlc_intraday[date,ticker]["cover_sig_2"][i] = close_price_2
                                    ticker_return = close_price_2 - open_price 
                                    date_stats[date][ticker] = ticker_return
                                    outcome = 'stopped_out_2'
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
                                    ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                                    ticker_return = close_price - open_price 
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
                            print('last_low',last_low)
                            trail_stop_price_short = ohlc_intraday[date,ticker]["high"][i] * (1 + .02) # adds a percentage above so dont get stopped stright away
                            print('Tight stop here of 2 %')
                            print(reward,'R, Price target hit. New stop price',trail_stop_price_short)
                            print('Last high price',last_low)
                        
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
                            close_price = trail_stop_price_short
                            ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                            ticker_return = open_price - close_price
                            date_stats[date][ticker] = ticker_return
                            outcome = 'trailing_stop_hit'
                            print('Trail stop hit')
                            print('min_r_trail_stop_hit',ticker, ' Price',close_price)
                            print('Ticker return', ticker_return)
                    
                          
                        ##################
                        #Trailing Stop ###
                        ##################
                        elif (
                              trail_stop_on == 1 and 
                              close_price == 0 and 
                              ohlc_intraday[date,ticker]["high"][i] > trail_stop_price_short ) :# stop loss
                                  #close_price = ohlc_intraday[date,ticker]["open"][i]#slipage
                                  close_price = trail_stop_price_short 
                                  ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                                  ticker_return = open_price - close_price
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
                                  close_price = stop_price
                                  ohlc_intraday[date,ticker]["cover_sig"][i] = stop_price 
                                  ticker_return = open_price - stop_price 
                                  date_stats[date][ticker] = ticker_return
                                  outcome = 'stopped_out'
                                  print('Stopped out',ticker, ' Price',stop_price)
                                  print('Ticker return', ticker_return)
                        ###############
                        # Time stop
                        ###############  
                        if ( 
                                close_price == 0 and  
                                ohlc_intraday[date,ticker]["sell_time"][i+1] == True):
                                    close_price = ohlc_intraday[date,ticker]["open"][i]
                                    ohlc_intraday[date,ticker]["cover_sig"][i] = close_price
                                    ticker_return = open_price - close_price
                                    date_stats[date][ticker] = ticker_return
                                    outcome = 'time_stop'
                                    print('Sell time hit',ticker, ' Price',close_price)
                                    print('Ticker return', ticker_return)          
                                
                        
                        
                    
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
                            print('Tight stop here of 2 %')
                            print(reward,'R, Price target hit. New stop price',trail_stop_price_short_2)
                            print('Last high price',last_low_2)
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
                            ohlc_intraday[date,ticker]["cover_sig"][i] = close_price_2
                            ticker_return_2 = open_price_2 - close_price_2
                            date_stats[date][ticker] = ticker_return_2
                            outcome_2 = 'trailing_stop_hit'
                            print('Trail stop hit')
                            print('min_r_trail_stop_hit',ticker, ' Price',close_price_2)
                            print('Ticker return', ticker_return_2)
                        # Calculate trailing stop price  
                        ###############
                        # Second Time stop
                        ###############  
                        if ( 
                                close_price_2 == 0 and  
                                direction == 'short' and
                                ohlc_intraday[date,ticker]["sell_time"][i] == True):
                                    close_price_2 = ohlc_intraday[date,ticker]["open"][i]  
                                    ohlc_intraday[date,ticker]["cover_sig_2"][i] = close_price_2
                                    ticker_return_2 = open_price_2 - close_price_2
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
                                  ohlc_intraday[date,ticker]["cover_sig_2"][i] = close_price_2 
                                  ticker_return_2 = open_price_2 - close_price_2
                                  date_stats_2[date][ticker] = close_price_2
                                  outcome_2 = 'stopped_out_2'
                                  # print('Stopped out',ticker, ' Price',close_price)
                                  # print('Ticker return', ticker_return)  
                                  break      
                
                # Calculate returns
                # I have the max_shares per trade
                if ticker_return != 0:
                    payout =  ticker_return * max_shares
                    payout_2 =  ticker_return_2 * max_shares_2
                    
                    new_commission = trip_comm * trade_count
                    new_commission_2 = trip_comm * trade_count_2
                   
                    
                    # print('tot_slip',tot_slip)
                    # print('open_price',open_price)
                    print('max_shares',max_shares)
                    locate_cost_ps = open_price * max_locate_per_price
                    locate_cost = locate_cost_ps * max_shares
                    print('locate_cost',locate_cost)
                    # print("new_commission",new_commission)
                    #locate_cost =  locate * locate_fee
                    # print('locate_cost',locate_cost)
                    #gain = payout - (new_commission + locate_cost)
                    #first is percentage for locate fee second is slippage
                    total_payout = payout + payout_2
                    gain = payout - (new_commission + locate_cost)
                    gain_2 = gain + (payout_2 - (new_commission_2))
                    
                    imaginary_account += gain
                    imaginary_account_2 += gain_2
                    
                    #gain_no_fee = payout
                    #imaginary_account_no_fee += gain_no_fee
                    
                total_Gain = imaginary_account + full_balance
                gains.append(total_Gain)
                total_Gain_2 = imaginary_account_2 + full_balance_2
                gains_2.append(total_Gain_2)
                
                
                
                #print('Adding this ticker to Results df        ',date,ticker)
                results = pd.DataFrame([[date, ticker ,  open_price, close_price,   stop_price,  ticker_return,  outcome,  max_shares,  locate, open_price_2,  close_price_2,  stop_price_2,  ticker_return_2,  outcome_2,  trade_count,  max_shares_2,  locate_2]],
                               columns=['date','ticker','open_price','close_price','stop_price','ticker_return','outcome','max_shares','locate','open_price_2','close_price_2','stop_price_2','ticker_return_2','outcome_2','trade_count','max_shares_2','locate_2'] )  
                #Adds new line to dic each loop 
                results_store = results_store.append(results,ignore_index=True) 
                results_store.reset_index(drop=True)        
                
                
                    
                    
    ###########################################################################################################
    ###################################  Plot    ##############################################################
    ###########################################################################################################
                if plot == 1 and trade_count > plot_trades_only:
                    
                    # fig, ax1 = plt.subplots()
                    # color = 'tab:red'
                    # ax1.set_xlabel('Flips')
                    # ax1.set_ylabel('gains', color=color)
                    # ax1.plot(gains, color=color)
                    # ax1.tick_params(axis='y', labelcolor=color)
                    fig, ax1 = plt.subplots()
                    color1 = 'tab:red'
                    color2 = 'tab:blue'
                    ax1.set_xlabel('Flips')
                    ax1.set_ylabel('gains', color=color1)
                    ax1.plot(gains, color=color1)
                    ax1.tick_params(axis='y', labelcolor=color1)
                    
                    ax2 = ax1.twinx()
                    ax2.set_ylabel('gains_2', color=color2)
                    ax2.plot(gains_2, color=color2)
                    ax2.tick_params(axis='y', labelcolor=color2)
                    
                    fig.tight_layout()
                    plt.show()
                    
                    plt_chart(date, ticker, ohlc_intraday,outcome,ticker_return,outcome_2,ticker_return_2)
                else:
                    pass
            except (FileNotFoundError,IndexError ) as e:
                print(e)
                print('Interday file not found for ----------------------------------------------', date, ticker)  
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
    print('Starting calculating returns-----------------------------------------------------------')
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
        
        ax = plt.gca()
    
        #results_store.plot(kind='line',y='balance',x = 'date',ax=ax)
        #Need a new column with balance without fees and plot thatn
        # results_store.plot(kind='line', x='date', y=['balance', 'balance_no_fee'], color=['red', 'blue'], ax=ax)
        fig, ax = plt.subplots(figsize=(15,10), dpi=150)#?
        results_store.plot(x='date',  y=['balance', 'balance_no_fee'], color=['red', 'blue'],ax=ax,linewidth=0.25)
        #results_store.plot(x='date', y='balance', kind='scatter',color=['red'], ax=ax, s=1 )
        #plt.show()
        #####################################################################################
        fig, ax1 = plt.subplots()
        color1 = 'tab:red'
        color2 = 'tab:blue'
        ax1.set_xlabel('Flips')
        ax1.set_ylabel('gains', color=color1)
        ax1.plot(gains, color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('gains_2', color=color2)
        ax2.plot(gains_2, color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        fig.tight_layout()
        plt.show()
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
    print('Using filepath', file_path)
    main_df = pd.read_csv(file_path , parse_dates=[1], dayfirst=True,index_col=0)# Puts year first

    results_store.rename(columns = {'date' : 'Date', 'ticker' : 'Ticker'}, inplace = True)

    joined = pd.merge(results_store, main_df, on=['Date', 'Ticker'], how='left')
    winner_name = today + time_now +  '_winner_losers.csv' #
    if mac == 1:
        joined.to_csv("/Users/briansheehan/Documents/mac_quant/Backtesting/winners.csv", index=False)
    if mac == 0:
        joined.to_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s"% winner_name, index=False)

    
    return results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal ,date_stats, date_stats_2 

                 
##########################################################################################################################################################################################################################
##########################################################################################################################################################################################################################
load_parms = {
    'mac': 1,
    'main_or_all': 'all',
    'filter_by_dates_on': 1,
    'start_date': '2021-10-01',
    'end_date': '2023-03-12',
    
    'insample_per_on': 0,
    'split_per':.5,
    'return_start':0,
    
    'random_insample_on' :0,
    'random_insample_per':.5,
    'random_insample_start':0,
    #Scanner
    'volume_min': -999999,
    'yclose_to_open_percent_filter': 15,# all
    'pm_vol_set': 0, # main

}

##########################################################################################################################################################################################################################
# General Settings                                                  #????????????##############################
#############################################################################################################

default_parms = {
    'mac': 1,
    'main_or_all': 'all',
    'filter_by_dates_on': 1,
    'start_date': '2021-10-01',
    'end_date': '2023-03-12',
    # Scanner Settings
    # Insample out of sample settings
    "insample_per_on": 1,
    "split_per": 0.60,
    "return_start": 1,  # True
    # Random insample out of sample testing
    "random_insample_on": 0,  # Turn on randon insample
    "random_insample_start": 1,  # 1 for start 0 for end
    "random_insample_per": 0.25,
 
    #Scanner
    'volume_min': -999999,
    'pm_vol_set': 0, # main
    'yclose_to_open_percent_filter': 15,# all

    # System settings

    "longshort": "short",  # 'long' or 'short'

    "plot": 0,  # 1 to plot on
    "plot_trades_only": 0,  # 0 or -1
    "save_winners_df": 1,

    # Balance
    "start_balance": 5000,
    # Percent of account to risk
    "risk_acc": 0.01,  # 0.01

    # New Balance for System
    "full_balance": 0,
    "imaginary_account": 5000,
    "full_balance_2": 0,
    "imaginary_account_2": 5000,
    "bet_percentage": 0.01,  # risk per trade of imaginary account
    "max_locate_per_price": 0.01,
    "max_risk": 50,  # set low to prevent compounding
    "open_slippage": 0,
    "close_slippage": 0,

    # Indicator Settings
    # Super T setting
    "lookback": 10,
    "multiplier": 3,
    # ATR settings
    "lenth": 14,
    "lessthan": 0.11,
    "shift": 3,
    # Acquisition filter
    "drop_acquistions_on": 1,
    "aq_value": 1.05,

    # Testing Settings
    # Commissions
    "locate_fee": 0.05,  # per share
    "trip_comm": 2,  # round trip commission
    # Stop loss percent from trade price
    "close_stop_on": 1,
    "close_stop": 0.10,  # percent percent away from open pricee/ .001 is to small dont get even r

    # Pre-market high stop
    "pre_market_h_stop_on": 0,
    #Trailing stop
    "pre_market_h_stop_on": 0,
    "trail_stop_on": 0,
    "min_reward_then_let_it_run": 0,
    "min_reward_then_let_it_run_2": 0,
    "reward": 4,# times the close_stop - 1 R for trailstop
    "trail_stop_per": 0,#.03,.06,.1 if this is greater than close_stop it affects R

    # Both Main and All
    "sharesfloat_on": 0,
    "sharesfloat_min": -9999999,
    "sharesfloat_max": 9999999999,
    "market_cap_on": 0,
    "market_cap_min": -999,
    "market_cap_max": 9999999999999999,

    "price_between_on": 1,
    "min_between_price": 2.5,
    "max_between_price": 20,
    "buytime_on": 0,
    "buy_time": "09:30:00",
    "selltime_on": 1,
    "sell_time": "15:58:00",
    "buy_between_time_on": 1,
    "buy_after": "09:29:00",
    "buy_before": "09:35:00",
    "buy_between_time_on_2": 1,
    "buy_after_2": "09:33:00",
    "buy_before_2": "10:35:00",
    "volume_sum_cal_on": 0,
    "vol_sum_greaterthan": 1000000,
    "pm_volume_sum_cal_on": 0,
    "pm_volume_sum_greaterthat": 1000000,
    "pm_gap_on": 0,
    "pmg_greater": 0.4,
    "per_change_first_tick_on": 0,
    "precent_greater": 0.5,
    "per_change_open_on": 0,
    "per_change_open_on_2": 0,
    "open_greater": -0.1,
    "vwap_above_on": 0,
    "vwap_below_on": 0,
    "last_close_change_on": 1,
    "last_close_change_on_2": 0,
    "last_close_per": 0.3,
    "percent_from_pmh_on": 0,
    "per_pmh_val": 0.3,
    "day_greater_than_pm_on": 0,
    "pm_greater_than_day_on": 0,
    "st_close_lessthan_on": 0,# Long
    "st_close_greaterthan_on": 0, # short
    "st_close_greaterthan_on_2": 0, # short 2
}
###########################################################################################################
# Set up active parameters
active_parms = {
    "per_change_first_tick_on": 0,
    "precent_greater": 0.5,
    "per_change_open_on": 0,
    "per_change_open_on_2": 0,
    "open_greater": -0.1,
}


output_dict = {}
# Loop through parameters
for param_name, default_value in default_parms.items():
    active_value = active_parms.get(param_name, default_value)
    # use active_value here as the value of the parameter
    output_dict[param_name] = active_value
    print(f"{param_name}: {active_value}")
    print(output_dict)
    



########################### Run code here   #############################################################################
# create an instance of the Backtester class
bt = Backtester(output_dict)

# call the loadmaindata method
# lmd = bt.loadmaindata(output_dict)


btresults_store = pd.DataFrame()
#Get list of stocks you want to test
# for sharesfloat_min, sharesfloat_max, market_cap_min, market_cap_max,vwap_below_on,st_close_lessthan_on in zip(sharesfloat_min, sharesfloat_max,market_cap_min,market_cap_max, vwap_below_on, st_close_lessthan_on):
#     #print(sharesfloat_min, sharesfloat_max, market_cap_min, market_cap_max  )
#try:
# top_gap_by_date,file_path, flt_database = loadmaindata(output_dict)
top_gap_by_date,file_path, flt_database = bt.loadmaindata(output_dict)


results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal,date_stats,date_stats_2 = backtester(output_dict)
# 
# btresults = pd.DataFrame([[longshort,sharesfloat_min, sharesfloat_max, market_cap_min, market_cap_max,last_close_per, open_greater, vol_sum_greaterthan, buy_after, close_stop, vwap_below_on,st_close_lessthan_on, reward,trail_stop_per ,num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal]],
#                         columns=['longshort','sharesfloat_min', 'sharesfloat_max', 'market_cap_min', 'market_cap_max','last_close_per','open_greater','vol_sum_greaterthan','buy_after','close_stop','vwap_below_on','st_close_lessthan_on','reward','trail_stop_per','num_of_trades', 'total_win', 'win_per', 'gross_profit','total_locate_fee','total_comm','finish_bal'] )  


# except(UnboundLocalError) as e:
#             print(e,'---------------------------------error----------------------------------------------')
##############################################################################################################



# print("**********Strategy Performance Statistics**********")
# print("total cumulative return = {}".format(round(abs_return(date_stats),4)))
# print("total win rate = {}".format(round(win_rate(date_stats),2)))
# print("mean return per win trade = {}".format(round(mean_ret_winner(date_stats),4)))
# print("mean return per loss trade = {}".format(round(mean_ret_loser(date_stats),4)))


mac = load_parms['mac']
if mac == 0:
    telegram_send.send(messages=["Back test complete............"])
    
print('It took', (time.time()-start)/60, 'minutes.')
print('Finished')

