#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:28:33 2023

@author: briansheehan
"""
import pandas as pd
import numpy as np


class Indicators:
    def __init__(self):
        pass

    def float_share_between(self, df, sharesfloat_min, sharesfloat_max):
        test = (df['shares_float'] >= sharesfloat_min) & (df['shares_float'] <= sharesfloat_max)
        df['shares_float_test'] = test
        return df
    
    def market_cap_between(self, df, market_cap_min, market_cap_max):
        test = (df['market_cap'] >= market_cap_min) & (df['market_cap'] <= market_cap_max)
        df['market_cap_test'] = test
        return df
    
    def price_greater(self, df,min_price):
        val = min_price <= df['close']
        df['min_price'] = val
        return df
    
    def price_between(self, df,min_between_price, max_between_price ):
        "price between"
        test = (min_between_price <= df['close']) & (df['close'] <= max_between_price)
        df['price_between'] = test
        return df
    
    def buytime(self, df,date,buy_time):
        date = date.strftime("%Y-%m-%d")
        datetest = date + ' ' + buy_time
        df.reset_index(inplace = True, drop = False)
        timetest = df['timestamp'] >= datetest
        df['buy_time'] = timetest
        df.set_index('timestamp', inplace=True)   
        return df
    
    def buylocatecondition(self, df, date, buy_locate_time, last_close, last_close_per_locate):
        df['last_close_change'] = ((df['close'] - last_close) / last_close) 
        df['last_close_change_locate'] = df['last_close_change'] >= last_close_per_locate 
        date = date.strftime("%Y-%m-%d")
        datetest = date + ' ' + buy_locate_time
        df.reset_index(inplace=True, drop=False)
        df['buy_locate_time'] = df['timestamp'] >= datetest
        # df.loc[(df['buy_locate_time'] == True) & (df['last_close_change_locate'] == True), 'buy_locate_condition'] = Truedf.loc[(df['buy_locate_time'] == True) & (df['last_close_change_locate'] == True), 'buy_locate_condition'] = True
        df['buy_locate_condition'] = df.apply(lambda x: True if x['buy_locate_time'] and x['last_close_change_locate'] else False, axis=1)

        df.set_index('timestamp', inplace=True)
        # create binary mask for start of each group
        mask = df['buy_locate_condition'].cumsum() != 0

        # set all rows in each group to True
        df['buy_locate_condition'] = mask.cumsum().astype(bool)

        return df

    
    
    
    def selltime(self, df,date, sell_time):
        date = date.strftime("%Y-%m-%d")
        datetest = date + ' ' + sell_time
        df.reset_index(inplace = True, drop = False)
        timetest = df['timestamp'] >= datetest
        df['sell_time'] = timetest
        df.set_index('timestamp', inplace=True)   
        return df
    
    def buy_between_time(self, df,date, buy_after ,buy_before):
        date = date.strftime("%Y-%m-%d")
        datebuy = date + ' ' + buy_after
        datesell = date + ' ' + buy_before
        df.reset_index(inplace = True, drop = False)
        timetest = (df['timestamp'] >= datebuy) & (df['timestamp'] <= datesell)
        df['buy_between_time'] = timetest
        df.set_index('timestamp', inplace=True)   
        return df
    
    def buy_between_time_2(self, df,date, buy_after_2 ,buy_before_2):
        
        date = date.strftime("%Y-%m-%d")
        datebuy = date + ' ' + buy_after_2
        datesell = date + ' ' + buy_before_2
        df.reset_index(inplace = True, drop = False)
        timetest = (df['timestamp'] >= datebuy) & (df['timestamp'] <= datesell)
        df['buy_between_time_2'] = timetest
        df.set_index('timestamp', inplace=True)    
        return df
    
    # Price below VWAP 
    def vwap_above(self, df):
        vwap = df['vwap'] >= df['close']
        df['vwap_above'] = vwap
        return df
    
    # Price above VWAP 
    def vwap_below(self, df):
        vwap = df['vwap'] <= df['close']
        df['vwap_below'] = vwap
        return df
    
    # % Change from first tick of my data greater than
    def per_change_first_tick(self, df,precent_greater):
        close = df.iloc[0,3]# get open price
        df['start_change'] = ((df['close'] - close) / close)
        test = df['start_change'] >= precent_greater
        df['first_tick_greater'] = test
        return df

    def last_close_change(self, df,last_close,last_close_per):
        'is the percent from yesterdays close greater than set amount'
        df['last_close_change'] = ((df['close'] - last_close) / last_close) 
        df['last_close_change_test'] = df['last_close_change'] >= last_close_per   
        return df
    
    
    # % Change from Open
    def per_change_open(self, df,date,open_greater):
        try:
            "change from the open. open bar to each open bar"
            str_date = date.strftime("%Y-%m-%d")#convert datetime to string
            Date0930 = str_date + ' 09:30:00'
            Date1600 = str_date + ' 16:00:00'
            day = df.loc[Date0930:Date1600]
            open_price = day.iloc[0,0]# get open price
            df['open_change'] = ((df['open'] - open_price) / open_price)
            df['open_greater'] = df['open_change'] >= open_greater# returns true false
            return df
        except :
            df['open_greater'] = False
            print('Error in per_change_open indicator')
            return df
    
    # Pre market gap PMG
    def pm_gap(self, df,date,last_close, pmg_greater):
        "y_close to PMH"
        try:
            str_date = date.strftime("%Y-%m-%d")#convert datetime to string
            Date0400 = str_date + ' 04:00:00'
            Date0930 = str_date + ' 09:29:00'
            dfpm = df.loc[Date0400:Date0930]##get pre-market date only
            pmh_time = dfpm['close'].idxmax()#get pmh time
            pmh_price = df.loc[pmh_time]['high']# get pmh price
            df['pm_gap_y_c'] = ((pmh_price - last_close) / last_close)
            
            test = df['pm_gap_y_c'] >= pmg_greater
            df['pm_gap_greater'] = test
            df = df.fillna(method='ffill')#fill nan with last value#
        except:
            print('pmg fail--------------------------------------')
            df['pm_gap_greater'] = False
            print(df)
        return df

    def volume_sum_cal(self, df,vol_sum_greaterthan):
        df['vol sum'] = df['volume'].cumsum()
        vol = df['vol sum'] >= vol_sum_greaterthan
        df['vol_sum_greater'] = vol
        return df  
    
    def pm_volume_sum_cal(self, df, date, pm_vol_sum_greaterthan):
        str_date = date.strftime("%Y-%m-%d")#convert datetime to string
        Date0400 = str_date + ' 04:00:00'
        Date0930 = str_date + ' 09:29:00'
        dfpm = df.loc[Date0400:Date0930]##get pre-market date only
        df['pm_vol_sum'] = dfpm['volume'].cumsum()
        df = df.fillna(method='ffill')
        vol = df['pm_vol_sum'] >= pm_vol_sum_greaterthan
        df['pm_vol_sum_greater'] = vol
        return df   
    
    def day_greater_than_pm(self, df,date):
        print('dfsd')
        str_date = date.strftime("%Y-%m-%d")#convert datetime to string
        Date0400 = str_date + ' 04:00:00'
        Date0930 = str_date + ' 09:29:00'
        premarket1 = df.loc[Date0400:Date0930]##get pre-market date only
        pmh_time = premarket1['high'].idxmax()#get pmh time 
        pmh_price = df.loc[pmh_time]['high']# get pmh price
        val = df.close >=  pmh_price# true false test
        df['dh>pmh'] = val# add new tst column
        return df
    
    def pm_greater_than_day(self, df,date):
        "pmh greater than day"
        str_date = date.strftime("%Y-%m-%d")#convert datetime to string
        Date0400 = str_date + ' 04:00:00'
        Date0930 = str_date + ' 09:29:00'
        premarket1 = df.loc[Date0400:Date0930]#get pre-market date only
        pmh_time = premarket1['high'].idxmax()#get pmh time 
        pmh_price = df.loc[pmh_time]['high']# get pmh price
        val = df.close <=  pmh_price# true false test
        df['pmg>dy'] = val# add new tst column
        return df
    
    def get_pmh_price(self, df,date):
        "if day price goes above pmh stop out"
        str_date = date.strftime("%Y-%m-%d")#convert datetime to string
        Date0400 = str_date + ' 04:00:00'
        Date0930 = str_date + ' 09:29:00'
        premarket1 = df.loc[Date0400:Date0930]#get pre-market date only
        pmh_time = premarket1['high'].idxmax()#get pmh time 
        pmh_price = df.loc[pmh_time]['high']# get pmh price
        return pmh_price
    
    def percent_from_pmh(self, df,date,per_pmh_val):
        try:
            'if price is percentage from pmh'
            str_date = date.strftime("%Y-%m-%d")#convert datetime to string
            Date0400 = str_date + ' 04:00:00'
            Date0929 = str_date + ' 09:29:00'
            premarket1 = df.loc[Date0400:Date0929]#get pre-market date only
            pmh_time = premarket1['high'].idxmax()#get pmh time 
            pmh_price = df.loc[pmh_time]['high']# get pmh price
            df['%_from_pmh'] = pmh_price  - (per_pmh_val * pmh_price) 
            val = df.high >= df['%_from_pmh']# true false test
            df['from_pmh_test'] = val# add new tst column
        except :
            df['from_pmh_test'] = False
            print('Getting PMH fail')
        return df
        
    
    def drop_acquistions(self, df,date,aq_value):    
        ' Drop Acquistions '
        str_date = date.strftime("%Y-%m-%d")#convert datetime to string
        Date0400 = str_date + ' 08:00:00'
        Date0930 = str_date + ' 09:29:00'
        df1 = df.loc[Date0400:Date0930]#get pre-market date only
        df['acquistions'] = ((df1['high'] / df1['low']))
        df['acq_test'] = df['acquistions'].gt(aq_value).cumsum().gt(0)
        # Fill remaining values with last value
        df['acq_test'] = df['acq_test'].fillna(method='ffill')
        return df
    
    #Super trend less than close
    def st_close_lessthan(self, df):
        df['st_long'] = ''
        df.loc[df.st < df.close, 'st_long'] = True
      
        return df
    
    #Super trend greater than close
    def st_close_greaterthan(self, df):
        df['st_short'] = ''
        df.loc[df.st > df.close, 'st_short'] = True
        return df
        
    # ATF with shift calculations
    def ATR(self, DF,lenth, lessthan,shift):
        "function to calculate True Range and Average True Range"
        df = DF.copy()
        df['H-L']=abs(df['high']-df['low'])
        df['H-PC']=abs(df['high']-df['close'].shift(1))
        df['L-PC']=abs(df['low']-df['close'].shift(1))
        df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
        df['atr'] = df['TR'].rolling(lenth).mean()
        #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
        df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
        df['atr'] = df2
        # True false agrument
        # shift atr
        df2['atr shift'] = df2['atr'].shift(+shift)
        df3 = df2['atr'] <= lessthan
        df2['atr >'] = df3
        return df2
    
    def get_supertrend(self, high, low, close, lookback, multiplier):
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
        atr = tr.ewm(lookback).mean()
        
        # H/L AVG AND BASIC UPPER & LOWER BAND
        hl_avg = (high + low) / 2
        upper_band = (hl_avg + multiplier * atr).dropna()
        lower_band = (hl_avg - multiplier * atr).dropna()
        
        # FINAL UPPER BAND
        final_bands = pd.DataFrame(columns = ['upper', 'lower'])
        final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
        final_bands.iloc[:,1] = final_bands.iloc[:,0]
       
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i,0] = 0
            else:
                if (upper_band[i] < final_bands.iloc[i-1,0]) | (close[i-1] > final_bands.iloc[i-1,0]):
                    final_bands.iloc[i,0] = upper_band[i]
                else:
                    final_bands.iloc[i,0] = final_bands.iloc[i-1,0]#??//
        
        # FINAL LOWER BAND
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i, 1] = 0
            else:
                if (lower_band[i] > final_bands.iloc[i-1,1]) | (close[i-1] < final_bands.iloc[i-1,1]):
                    final_bands.iloc[i,1] = lower_band[i]
                else:
                    final_bands.iloc[i,1] = final_bands.iloc[i-1,1]
        
        # SUPERTREND
        supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
        supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
        
        for i in range(len(supertrend)):
            if i == 0:
                supertrend.iloc[i, 0] = 0
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] < final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] > final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] > final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] < final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        
        supertrend = supertrend.set_index(upper_band.index)
        supertrend = supertrend.dropna()[1:]
        
        # ST UPTREND/DOWNTREND
        upt = []
        dt = []
        close = close.iloc[len(close) - len(supertrend):]
    
        for i in range(len(supertrend)):
            if close[i] > supertrend.iloc[i, 0]:
                upt.append(supertrend.iloc[i, 0])
                dt.append(np.nan)
            elif close[i] < supertrend.iloc[i, 0]:
                upt.append(np.nan)
                dt.append(supertrend.iloc[i, 0])
            else:
                upt.append(np.nan)
                dt.append(np.nan)
                
        st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
        upt.index, dt.index = supertrend.index, supertrend.index
        
        return st, upt,  dt
    
    def round_to_nearest_100(self, number):
        return ((number + 99) // 100) * 100