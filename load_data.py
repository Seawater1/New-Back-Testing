#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:15:34 2023

@author: briansheehan
"""

import pandas as pd
from indicators import Indicators
import pytz
import time
# from polygon  import PolygonData
# create an instance of the Polygon class
# polygon = PolygonData()

from plots import Plots


############################################################################################################
## Functions to load data
############################################################################################################

class Load_date():
    def __init__(self):
        pass
        
        
    def loadmaindata(self,load_parms):
        # mac = load_parms[0]['mac'][0]
        # mac = load_parms['mac']
        # print('test',load_parms[0]['mac'])
        mac = load_parms['mac']

        print('mac',mac)
        main_or_all = load_parms['main_or_all']
        filter_by_dates_on = load_parms['filter_by_dates_on']
        start_date = load_parms['start_date']
        end_date = load_parms['end_date']
        insample_per_on = load_parms['insample_per_on']
        split_per = load_parms['split_per']
        return_start = load_parms['return_start']
        random_insample_on = load_parms['random_insample_on']
        random_insample_per = load_parms['random_insample_per']
        random_insample_start = load_parms['random_insample_start']
        volume_min = load_parms['volume_min']
        pm_vol_set = load_parms['pm_vol_set']
        yclose_to_open_percent = load_parms['yclose_to_open_percent']
        Gap_per = load_parms['Gap_per']
        Pre_market_Gap = load_parms['Pre_market_Gap']
        Change_from_Open = load_parms['Change_from_Open']
        Change_per = load_parms['Change_per']
        
        if mac == 1:
            if main_or_all == 'all':
                file_path = "/Users/briansheehan/Documents/mac_quant/Intraday_Ticker_Database/download_all_database/main_database_april_2023.csv"
                print('mac: all file')
            if main_or_all == 'main':
                file_path = "/Users/briansheehan/Documents/mac_quant/Intraday_Ticker_Database/2021DataBase.csv"   
                print('mac: main file')
            
            
        if mac == 0:
            if main_or_all == 'all': 
                file_path = r'C:\Users\brian\Desktop\PythonProgram\Intraday_Ticker_Database\download_all_database\main_database_april_2023.csv'
                print('win: all file')
            if main_or_all == 'main':
                file_path = r'C:\Users\brian\Desktop\PythonProgram\MainTickerDataBase\2021DataBase.csv'
                print('win: main file')
            
        # Load file of tickers and date
        # df = pd.read_csv(file_path, index_col='Date')
        df = pd.read_csv(file_path, parse_dates=['Date'], infer_datetime_format=True)
        # df = pd.read_csv(file_path, parse_dates=['Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%y'))
        # df = df.drop('Unnamed: 0', axis=1)

        # df = df.reset_index()
        print(df)
        # for index, row in df.iterrows():
        #     print(row['Date'])
        #     time.sleep(.1)


        
        df['Date'] = pd.to_datetime(df.Date)#Change time object to datetime
        print('Ticker Database no filter',df)
        
        #Filter by dates
        if filter_by_dates_on == 1:
            # print('Flitering by dates -----------------------------------------------------------------------------------------------')
            date_filter = (df['Date'] >= start_date) & (df['Date'] <= end_date )
            df = df.loc[date_filter]
            print('DF filtered by Date', df)
        # Split insample and out of sample
        if insample_per_on == 1: 
            print('split %',split_per)
            # print('Spliting insample and out of smaple -----------------------------------------------------------------',split_per)
            num_rows = len(df)
            split_index = int(num_rows * split_per)
            if return_start == 1:
                df = df[:split_index]
                # print('start --- split')
            else:
                df = df[split_index:]
                # print('start --- split')
            # print('Split Percent ', split_per)
            # print('In sample df ',df)
            
        #Random OOS not for training for test afterwards
        if random_insample_on == 1:
            # print('Random insample is on -----------------------------------------------------------------------------------------')
            pos = ((df.index[-1])* random_insample_per)
            pos1 = round(pos)
            start_df = df.iloc[:pos1,:]
            end_df = df.iloc[pos1:,:]
            if random_insample_start ==1:
                df = start_df
                print('Random insample start')
                print(df)
            else:
                df = end_df
                print('Random insample end')
                print(df)        

        
        if main_or_all == 'all':
            df = df.loc[(df['Yclose_to_open_percent'] >= yclose_to_open_percent) |
                        (df['Gap %'] >= Gap_per) |
                        (df['Pre-market Gap %'] >= Pre_market_Gap) |
                        (df['Change from Open %'] >= Change_from_Open) |
                        (df['Change %'] >= Change_per)]
            print('All Gap filters')
            print(df)
        
        if main_or_all == 'main':                                    
             df = df.loc[(df['Volume'] > volume_min) &
                               (df['Pre-market Volume'] >= pm_vol_set)] # &
                               # (df['Shares Float'] > sharesfloat_min) &
                               # (df['Shares Float'] < sharesfloat_max) &
                               # (df['Market Capitalization'] > market_cap_min) & 
                               # (df['Market Capitalization'] < market_cap_max))
                             
         
        
        df1 = df.set_index('Date')
        # print('Ticker database after filters',df1)     
        if main_or_all == 'all':
        # Dictionary for storing Date Ticker yesterdaysclose          
         top_gap_by_date ={top_gap_by_date: dict(zip(sub_df['Ticker'], sub_df['last_close_price']))
               for top_gap_by_date, sub_df in df1.groupby(df1.index)}
            
        if main_or_all == 'main': 
           # Dictionary for storing Date Ticker yesterdaysclose          
            top_gap_by_date ={top_gap_by_date: dict(zip(sub_df['Ticker'], sub_df['Yesterdays Close']))
                  for top_gap_by_date, sub_df in df1.groupby(df1.index)}
            
        return top_gap_by_date, file_path, df
    
    # function to load interday data
    def load_interday(self, date, ticker, mac, flt_database):
        """
        Parameters
        ----------
        date : TYPE
            symbol date.
        ticker : TYPE
            filter by symbol.
        mac : TYPE
           mac or win.
        flt_database : TYPE
            main database, already filtered .
    
        Returns
        -------
        data : TYPE
            DESCRIPTION.
    
        """
        # try:
        # take filtered database from loadmaindata and retreave float and market cap 
        date_string = date.strftime('%Y-%m-%d')
        
        mc = flt_database.loc[(flt_database['Ticker'] == ticker) & (flt_database['Date'] == date_string), 'Market Capitalization'].values[0]
        sf = flt_database.loc[(flt_database['Ticker'] == ticker) & (flt_database['Date'] == date_string), 'Shares Float'].values[0]



         
        year = date.strftime("%Y") 
        
        if mac == 1:
            date = date.strftime("/%Y-%m-%d")# convert datetime to string
            dateticker = year + date + ' ' + ticker +'.csv' # adds ticker to date
            data = pd.read_csv('/Users/briansheehan/Documents/mac_quant/Intraday_Ticker_Database/download_all_%s'% dateticker )
        
        if mac == 0:
            date = date.strftime("\%Y-%m-%d")# convert datetime to string
            dateticker = year + date + ' ' + ticker +'.csv' # adds ticker to date
            data = pd.read_csv(r'C:\Users\brian\Desktop\PythonProgram\Intraday_Ticker_Database\download_all_%s'% dateticker )
            
        data.columns = ['timestamp','open','high','low','close','volume','vwap']
        data['shares_float'] = sf
        data['market_cap'] = mc 
        print('sf',sf)
        print('mc',mc)
        
        data['timestamp'] = pd.to_datetime(data['timestamp'])# change column to datetime
        # Remove the time offset
        data['timestamp'] = data['timestamp'].apply(lambda x: x.replace(tzinfo=None))
        data.set_index('timestamp', inplace=True)# set datetime as index s i can filter time
        # except:
            # print('Interday file not found will i get polygon to get it for you?', date, ticker)  
            # df = polygon.interday(ticker, date)
            # if mac == 0:
            #     date = date.strftime("\%Y-%m-%d")# convert datetime to string
            #     dateticker = year + date + ' ' + ticker +'.csv' # adds ticker to date
            #     data = pd.to_csv(r'C:\Users\brian\Desktop\PythonProgram\Intraday_Ticker_Database\download_all_%s'% dateticker )
            # if mac == 1:
            #     date = date.strftime("/%Y-%m-%d")# convert datetime to string
            #     dateticker = year + date + ' ' + ticker +'.csv' # adds ticker to date
            #     data = pd.to_csv('/Users/briansheehan/Documents/mac_quant/Intraday_Ticker_Database/download_all_%s'% dateticker )
            
       
        return data 