# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 02:36:44 2023

@author: brian
"""


  
#New DF to store data
resistance_ticker = []
resistance_date_list = []
resistance_date_list_default = []
resistance_vol_list = []
# New  Dataframes to store results
resistance_y_n_store = pd.DataFrame() 
resistance_info_store = pd.DataFrame()
    
print('--------------------Resistance started get daily close --------------------------------------------------')

    

# try:
print('---------------------------------------------For loop resistance get daily close')
print('Ticker ',Ticker)
print('Resistance price',R_price)
print('Date one half year', One_half_Year_ago)
print('Date in use',yesterday)
print('Pre market vol X 5', VolX)

df = polygon_day(Ticker,One_half_Year_ago,yesterday)
print('Testing ----',df)
df = df.reset_index()
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
        
        
        #pd.set_option('display.max_rows', None) 
        print('Historic closes')
        print(df)

        # Add Index
        df.reset_index(inplace=True)

        #Adjusted High calculations
        #df['Adj High'] = df['High'] / (df['Close'] / df['Adj Close']) 
        #Adjust volume calculations do I need to do this ##################################################################################################


        #filter by price
        df_date_price = df.loc[df['high'] >= R_price]#PM_resistancePriceList] 

        #filter by Volume 
        df_date_price_vol = df_date_price.loc[df_date_price['volume'] >= VolX]
        print('Filtered by price and volume',df_date_price_vol)
        
        print('First try started')
        
        # Get resistance Date   
        if df_date_price_vol.empty:
            print('If 1')
            print('DataFrame is empty!')
            resistance_speedbird = 'df empty after price vol filter'
        else:
            print('else 1')
            Resistance_date1 = df_date_price_vol.iloc[0,0]
            
            #Get Date only
            Resistance_date = Resistance_date1.strftime('%Y-%m-%d')
            print(Resistance_date,' Resistance date')

            # For Data Frame
            resistance_speedbird =  Resistance_date    

            #Get day after resistance Date
            day_after_resistance = Resistance_date1 + DateOffset(days=1)
            print(day_after_resistance,' Day after resistance')
            
            #Get middle of resistance price
            mid = df_date_price_vol.iloc[0]  #get only first row
            df_r_mid_price = mid['high'] - (mid['high'] * resis_can_perc_below)# get mid price
            print(df_r_mid_price, ' Resistance canceled price')  
                    
            #filter df by dates
            df.set_index('timestamp', inplace=True)# Set time as index
            df_r_day = df.loc[day_after_resistance:yesterday_dt]#filter by dates
            
            #print('Filtered by date',df_r_day)
            
            # Is the Adj High Greater that Resistance mid price
            resistance_greater = df_r_day['high'] > df_r_mid_price#?????????????????????? this maybe should vwap claose???
            #print('Is the Adj High Greater that Resistance mid price',resistance_greater)
        
            if resistance_greater.any(axis=None):
                print('if 2')
                print('Resistance Canceled')
                resistance_speedbird = 'Resistance Canceled'

            else: 
                print("Resistance not canceled continuing with code")
                print('else 2')

                # Get resistance volume
                resistance_vol = df_date_price_vol.iloc[0,5]
                print('Resistance Volume',resistance_vol)
                    
                # Get volume since ResResistance_date
                df.reset_index(inplace = True, drop = False)#add index back in 
                        
                df_vol_since = df.loc[df['timestamp'] >= Resistance_date]
                df_vol_since = df_vol_since.drop(df_vol_since.head(1).index,inplace=False) # drop last n rows
                ## Sum Volume
                df_vol_since = df_vol_since['volume'].sum()
                print('Vol since resistance',df_vol_since) 

                ###############################################################################
                
                
                
                # get five days before
                five_days = timedelta(
                                days=-5,
                )
                five_days_ago1 = yesterday_dt + five_days
                five_days_ago = five_days_ago1.strftime("%Y-%m-%d")
                print("5 days ago",five_days_ago)
                # Volume last five days
                df_vol_five_days = df.loc[df['timestamp'] >= five_days_ago]
                df_vol_five_days = df_vol_five_days.drop(df_vol_five_days.head(1).index,inplace=False) # drop last n rows
                # Add Volume
                df_vol_five_days = df_vol_five_days['volume'].sum()
                print('Vol last five days Vol ',df_vol_five_days)
                            
                #Create Ticker List
                resistance_ticker.append(Ticker)
                #resistance_ticker += resistance_ticker
                
                #resistance_ticker = resistance_ticker.append(Ticker, ignore_index=True)
                #Create resistance date list
                resistance_date_list.append(Resistance_date) 
                

                resistance_date_list_default.append(Resistance_date1)

                resistance_vol_list.append(resistance_vol)


                # Zip lists for For loop
                zip(resistance_ticker,resistance_date_list,resistance_date_list_default,resistance_vol_list )
                list(zip(resistance_ticker,resistance_date_list,resistance_date_list_default,resistance_vol_list ))

                ############################## Get tick data of resistance ##################################################################
               
                # Get extended price data
                df = polygon_interday(Ticker,Resistance_date)
                print('sleep .001 sec')
                time.sleep(.001)
                
                print('Extended price df',Ticker,df)
                # Set time as index 
                #df.set_index('timestamp', inplace=True) ##(failing hear 1?????????????????????????????????????????????)
                if df.empty:
                    print('Interday resistance empty')
                    df_hod = '0'
                    mean_vwap = '0'
                    price_by_vol = '0'
                    poc1 = '0'
                    poc2= '0'

                else:
                
                    #Save Resistance data for ticker for the future analysis
                    dateticker_R =Resistance_date + ' ' + Ticker +'.csv' # adds ticker to date
                    df.to_csv(r'C:\Users\brian\Desktop\PythonProgram\Intraday_Ticker_Database\Resistance\%s'% dateticker_R )
                    df.to_csv(r'B:\2T_Quant\Intraday_Ticker_Database_2T\Resistance_2T\%s'% dateticker_R )
                    # If the script fails here then the slice is probably off because its not yesterday
                    # Get High of day                    
                    df_sort = df.sort_values(by=['close'] ,ascending=False)
                    print('df_sort',df_sort)
                    df_hod = df_sort.iloc[0,3]
                    print('Resistance HOD price is ',df_hod)
                    
                    # Get VWAP average price
                    mean_vwap = df['vwap'].mean(axis=0)
                    mean_vwap = round(mean_vwap, 2)
                    print('VWAP mean ',mean_vwap)

                    # Get average price by volume
                    price_by_vol = mean_vwap * resistance_vol
                    price_by_vol = round(price_by_vol, 2) 
                    print('Resistance dollar volume is ',price_by_vol)

                    # Get  Volume profile https://medium.com/swlh/how-to-analyze-volume-profiles-with-python-3166bb10ff24
                    volume = df['volume']
                    close = df['close']

                    
                    kde_factor = 0.05
                    num_samples = 500
                    kde = stats.gaussian_kde(close,weights=volume,bw_method=kde_factor)
                    xr = np.linspace(close.min(),close.max(),num_samples)
                    kdy = kde(xr)
                    ticks_per_sample = (xr.max() - xr.min()) / num_samples

                    def get_dist_plot(c, v, kx, ky):
                        fig = go.Figure()
                        fig.add_trace(go.Histogram(name='Vol Profile', x=c, y=v, nbinsx=150, 
                                                histfunc='sum', histnorm='probability density',
                                                marker_color='#B0C4DE'))
                        fig.add_trace(go.Scatter(name='KDE', x=kx, y=ky, mode='lines', marker_color='#D2691E'))
                        return fig

                    #get_dist_plot(close, volume, xr, kdy).show()

                    peaks,_ = signal.find_peaks(kdy)
                    pkx = xr[peaks]
                    pky = kdy[peaks]

                    pk_marker_args=dict(size=10)
                    fig = get_dist_plot(close, volume, xr, kdy)
                    fig.add_trace(go.Scatter(name="Peaks", x=pkx, y=pky, mode='markers', marker=pk_marker_args))

                    min_prom = kdy.max() * 0.3
                    peaks, peak_props = signal.find_peaks(kdy, prominence=min_prom)
                    pkx = xr[peaks]
                    pky = kdy[peaks]

                    fig = get_dist_plot(close, volume, xr, kdy)
                    fig.add_trace(go.Scatter(name='Peaks', x=pkx, y=pky, mode='markers', marker=pk_marker_args))

                    # Draw prominence lines
                    left_base = peak_props['left_bases']
                    right_base = peak_props['right_bases']
                    line_x = pkx
                    line_y0 = pky
                    line_y1 = pky - peak_props['prominences']

                    pf1 = pd.DataFrame()
                    for x, y0, y1 in zip(line_x, line_y0, line_y1):
                        
                        #Create Df
                        pf = pd.DataFrame([[x,y0,y1]],
                        columns=['Price', 'Length', 'Not sure?'])
                        #Adds new line to data frame each loop
                        pf1 = pf1.append(pf, ignore_index=True)
                        
                        fig.add_shape(type='line',
                            xref='x', yref='y',
                            x0=x, y0=y0, x1=x, y1=y1,
                            line=dict(
                                color='red',
                                width=2,
                            )
                        )
                    #fig.show()#/////////////here to see results
                    # Get Point of control value
                    try:
                        pf1= pf1.sort_values(by=['Length'],ascending=False)#??? Failed her
                        print('pf1~~~~~~~~~~~~~~~',pf1)
                        poc= pf1.iloc[0,0]
                        poc1 = round(poc,2) 
                        poc2= pf1.iloc[1,0]
                        poc2 = round(poc,2)
                    except :
                        print('Only one point of control')
                        poc1 ='0'
                        poc2 ='0'

                    print(pf1)
                    print('Point of control',poc1)
                    print('Point of control 2',poc2)



                    # timing for alpha vanatage
                    api_call_count+=2
                    # if api_call_count==5:
                    #     api_call_count = 1
                    #     print('Sleep 60sec')
                    #     time.sleep(10 - ((time.time() - start_time) % 10.0))
                    print('---------------------------------------------------------------------------------------------------------------------------------') 
                    # might have to move this        
                    resistance_info = pd.DataFrame([[Ticker, resistance_vol,price_by_vol, df_vol_since, df_vol_five_days,df_hod,mean_vwap,poc1,poc2]],
                                columns=['Ticker2','R Vol','Dollar vol','Vol since R','Vol last 5 days','R HOD','R Mean VWAP', 'POC 1','POC 2' ] )  
                    resistance_info_store = resistance_info_store.append(resistance_info,ignore_index=True)

                
        resistance_y_n = pd.DataFrame([[Ticker, resistance_speedbird]],
                    columns=['Ticker1','Resistance',])
        resistance_y_n_store = resistance_y_n_store.append(resistance_y_n, ignore_index=True)
        # except:
        #     print('Error finding resistance for ',Ticker)
    if 'Ticker2' in resistance_info_store:
        print('Ticker2 found')
        resistance_results = resistance_y_n_store.merge(resistance_info_store,how='left',left_on='Ticker1',right_on='Ticker2' )
        print('test2',resistance_results)
        # Drop Ticker2 from Df
        resistance_results = resistance_results.drop(columns=['Ticker1','Ticker2'])
        print('Resistance Results',resistance_results)
    else:
        print('Ticker2 not found')
        resistance_results = resistance_y_n_store
        resistance_results = resistance_results.drop(columns=['Ticker1'])



    #Join Dataframes
    interday_r_r = pd.concat([interday_df,resistance_results], axis=1)
    # Drop Second Ticker2 
    print('Interday and Resistance ',interday_r_r)