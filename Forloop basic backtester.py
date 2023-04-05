from main import Backtester


import time
import math

# Start the timer
start_time = time.time()


# default_params = {
#     "param1": [],
#     "param2": [],
#     "param3": [],
#     # ... add other parameters here
# }





default_parms = {
    'mac': 1,
    'main_or_all': 'all',
    'filter_by_dates_on': 1,
    'start_date': '2021-10-01', # YYYY-MM-DD Maintickerdatabase starts 21-04-11 DownloadAll '2021-10-01'
    'end_date': '2023-4-02',
    # Scanner Settings
    # Insample out of sample settings
    "insample_per_on": 1,
    "split_per": 0.6,
    "return_start": 1,  # True
    # Random insample out of sample testing
    "random_insample_on": 0,  # Turn on randon insample
    "random_insample_start": 1,  # 1 for start 0 for end
    "random_insample_per": 0.25,
 
    #Scanner
    'volume_min': -999999,
    'pm_vol_set': 0, # main
    'yclose_to_open_percent_filter': 25,# # only working filter for All file 

    # System settings
    "longshort": "short",  # 'long' or 'short'
    "take_second_trade" : False,
    
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
    "max_locate_per_price": 0.02,
    "max_risk": 999999,  # set low to prevent compounding
    
    "open_slippage": 0.01,
    "close_slippage": 0.01,

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
    "locate_fee": 0.01,  # per share
    "trip_comm": 2,  # round trip commission
    
    # Stop loss percent from trade price
    "close_stop_on": 1,
    "close_stop": 0.1,  # percent percent away from open pricee/ .001 is to small dont get even r

    # Pre-market high stop
    "pre_market_h_stop_on": 0,
    #Trailing stop
    "pre_market_h_stop_on": 0,
    "trail_stop_on": 0,
    "min_reward_then_let_it_run": 0,
    
    "reward": 4,# times the close_stop - 1 R for trailstop
    "trail_stop_per": 0,#.03,.06,.1 if this is greater than close_stop it affects R

    # Both Main and All
    "sharesfloat_on": 0,
    "sharesfloat_min": -999999999,
    "sharesfloat_max": 9999999999,
    "market_cap_on": 0,
    "market_cap_min": -999,
    "market_cap_max": 9999999999999999,

    "price_between_on": 1,
    "min_between_price": 2.5,
    "max_between_price": 20,
    
    "buytime_on": 0,
    "buy_time": "09:30:00",
    
    "buylocatecondition_on": 0,
    "buy_locate_time":"09:25:00", 
    "last_close_per_locate":.50,
    
    "selltime_on": 1,
    "sell_time": "15:58:00",
    
    "buy_between_time_on": 1,
    "buy_after": "09:29:00",
    "buy_before": "09:30:00",
    

    
    "volume_sum_cal_on": 0,
    "vol_sum_greaterthan": 1000000,
    "pm_volume_sum_cal_on": 0,
    "pm_volume_sum_greaterthat": 1000000,
    "pm_gap_on": 0,
    "pmg_greater": 0.4,
    "per_change_first_tick_on": 0,
    "precent_greater": 0.3,
    
    "per_change_open_on": 0,
    "per_change_open_on_2": 0,
    "open_greater": 0.05,
    
    "vwap_above_on": 0,
    "vwap_below_on": 0,
    
    "last_close_change_on": 1,
    "last_close_change_on_2": 0,
    "last_close_per": [round(0.05 + i*0.05, 2) for i in range(math.ceil((0.50-0.05)/0.05))],
    
    "percent_from_pmh_on": 0,
    "per_pmh_val": 0.3,
    "day_greater_than_pm_on": 0,
    "pm_greater_than_day_on": 0,
    "st_close_lessthan_on": 0,# Long
    "st_close_greaterthan_on": 0, # short
    "st_close_greaterthan_on_2": 0, # short 2
    
    "close_stop_on_2": 0,
    "close_stop_2": 0.04,
    "min_reward_then_let_it_run_2": 0,
    "buy_between_time_on_2": 0,
    "buy_after_2": "09:32:00",
    "buy_before_2": "10:00:00",
    
    
    }
    


# define ranges of values for each parameter
close_stop_range = [i / 100 for i in range(1, 21, 2)] 
last_close_per_range  = [round(0.05 + i*0.05, 2) for i in range(math.ceil((0.50-0.05)/0.05))]



results = []  # list to store parameter values and finish_bal for each iteration

# loop over each combination of parameter values

for close_stop in close_stop_range:
    print(close_stop)
    for last_close_per in last_close_per_range:
        print(last_close_per)
        params = {
            "close_stop": close_stop,
            "last_close_per": last_close_per,
            # ... add other parameters here
        }
        params.update(default_params)  # update params with default parameters
        print(params)
        bt = Backtester(params)
        finish_bal = bt.backtester(params)
        results.append(params.copy())  # add a copy of the dictionary to the results
        results[-1]["finish_bal"] = finish_bal  # add the finish_bal to the latest dictionary in results

# print results
for result in results:
    print(result)


d = {
    'ANIMAL': ['CAT', 'DOG', 'FISH', 'HEDGEHOG'],
    'FRUIT': ['APPLE', 'BANANA', 'ORANGE', 'STRAWBERRY'],
    'COLOR': ['RED', 'GREEN', 'BLUE', 'YELLOW']
}

for key, value in default_parms.items():
    print(f"{key}:")
    if isinstance(value, list):
        for item in value:
            print(f"\t{item}")
    else:
        print(f"\t{value}")