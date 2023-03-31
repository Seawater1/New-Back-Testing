# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:11:04 2023

@author: brian
"""

conditions = [    (price_between_on != 1) or ohlc_intraday[date, ticker]['price_between'][i],
    (buytime_on != 1) or ohlc_intraday[date, ticker]['buy_time'][i],
    (selltime_on != 1) or not ohlc_intraday[date, ticker]['sell_time'][i],
    (buy_between_time_on != 1) or ohlc_intraday[date, ticker]['buy_between_time'][i],
    (buy_between_time_on_2 != 1) or ohlc_intraday[date, ticker]['buy_between_time_2'][i],
    (volume_sum_cal_on != 1) or ohlc_intraday[date, ticker]['vol_sum_greater'][i],
    (pm_volume_sum_cal_on != 1) or ohlc_intraday[date, ticker]['pm_vol_sum_greater'][i],
    (pm_gap_on != 1) or ohlc_intraday[date, ticker]['pm_gap_greater'][i],
    (per_change_first_tick_on != 1) or ohlc_intraday[date, ticker]['first_tick_greater'][i],
    (per_change_open_on != 1) or ohlc_intraday[date, ticker]['open_greater'][i],
    (per_change_open_on_2 != 1) or ohlc_intraday[date, ticker]['open_greater'][i],
    (vwap_above_on != 1) or ohlc_intraday[date, ticker]['vwap_above'][i],
    (vwap_below_on != 1) or ohlc_intraday[date, ticker]['vwap_below'][i],
    (last_close_change_on != 1) or ohlc_intraday[date, ticker]['last_close_change_test'][i],
    (day_greater_than_pm_on != 1) or ohlc_intraday[date, ticker]['dh>pmh'][i],
    (pm_greater_than_day_on != 1) or ohlc_intraday[date, ticker]['pmg>dy'][i],
    (st_close_lessthan_on != 1) or ohlc_intraday[date, ticker]['st_long'][i],
    (st_close_greaterthan_on != 1) or ohlc_intraday[date, ticker]['st_short'][i],
    (st_close_greaterthan_on_2 != 1) or ohlc_intraday[date, ticker]['st_short'][i],
    (sharesfloat_on != 1) or ohlc_intraday[date, ticker]['shares_float_test'][i],
    (market_cap_on != 1) or ohlc_intraday[date, ticker]['market_cap_test'][i],
    (drop_acquistions_on != 1) or ohlc_intraday[date, ticker]['acq_test'][i],
    (percent_from_pmh_on != 1) or ohlc_intraday[date, ticker]['from_pmh_test'][i],
    (longshort == 'long'),
    (open_price == 0)
]

if all(conditions):
    
for i in range(10):
    if sharesfloat_on == 1:
        df = indc.float_share_between(df,sharesfloat_min,sharesfloat_max)
    if market_cap_on == 1:
        df = indc.market_cap_between(df, market_cap_min, market_cap_max)
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
    if buy_between_time_on == 1:
        four = ohlc_intraday[date,ticker]["buy_between_time"][i]
    else:
        four = False
    if buy_between_time_on_2 == 1:
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
    if day_greater_than_pm_on == 1:   
        twelve = ohlc_intraday[date,ticker]['dh>pmh'][i]
    else:
        twelve = True 
    if pm_greater_than_day_on == 1: 
        thirteen = ohlc_intraday[date,ticker]['pmh<dh'][i]
    else:
        thirteen = True
    if st_close_lessthan_on == 1:
        fourteen = ohlc_intraday[date,ticker]["st_close_lessthan"][i]
    else:
        fourteen = True
    if st_close_greaterthan_on == 1:
        fifteen = ohlc_intraday[date,ticker]["st_close_greaterthan"][i]
    elif st_close_greaterthan_on_2 == 1:
        fifteen = ohlc_in

