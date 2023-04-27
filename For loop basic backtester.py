from main import Backtester


import time
import itertools
import pandas as pd
from datetime import datetime


# Start the timer
start_time = time.time()


default_parms = {
    'mac': [0],
    'main_or_all': ['all'],
    'filter_by_dates_on': [1],
    'start_date': ['2023-04-23'], # YYYY-MM-DD Maintickerdatabase starts 2021-04-11 DownloadAll '2021-10-01'
    'end_date': ['2023-04-26'],
    
    # Scanner Settings 
    'volume_min': [-999999],
    'pm_vol_set': [-999999],  # main
    # filter by one or all 
    'yclose_to_open_percent': [30],
    'Gap_per': [999999],
    'Pre_market_Gap': [999999],
    'Change_from_Open': [999999],
    'Change_per': [999999],
    
    # Insample out of sample settings
    "insample_per_on": [0],
    "split_per": [0.05],
    "return_start": [1],  # True
    # Random insample out of sample testing
    "random_insample_on": [0],  # Turn on randon insample
    "random_insample_start": [1],  # 1 for start 0 for end
    "random_insample_per": [0.25],

    # System settings
    "longshort": ["short"],  # 'long' or 'short'
    # Plots
    "plot": [1],  # 1 to plot on
    "plot_trades_only": [1],
    "save_winners_df": [0],
    # Starting balance
    "full_balance": [0],
    "imaginary_account": [10000],
    # Percent of account to risk
    "risk_acc": [0.01],  # 0.01
    "max_risk": [100],  # set low to prevent compounding#???
    # Locate fees
    "locate_fee": [0.01],  # set locate fee %default
    "locate_cost_per_on": [1],
    "max_locate_per_price": [0.01],  # variable depending on share price % if above on
    # Slippage
    "open_slippage": [0.01],
    "close_slippage": [0.01],
    # Indicator Settings
    # Super T setting
    "lookback": [10],
    "multiplier": [3],
    # ATR settings
    "lenth": [14],
    "lessthan": [0.11],
    "shift": [3],
    # Acquisition filter
    "drop_acquistions_on": [1],
    "aq_value": [1.05],
    # Testing Settings
    # Commissions
    "trip_comm": [2],  # round trip commission
    # Stop loss percent from trade price
    "close_stop_on": [1],
    "close_stop": [.1],  # percent percent away from open pricee/ .001 is to small dont get even
    
    "vwap_stop_on":[1],
    "dip_below_per":[.1],
    "vwap_stop_per":[.1],
    
    # Pre-market high stop
    "pre_market_h_stop_on": [0],
    # Trailing stop
    "trail_stop_on": [0],
    "min_reward_then_let_it_run": [0],
    "reward": [4],  # times the close_stop - 1 R for trailstop
    "trail_stop_per": [.03],  #.03,.06,.1 if this is greater than close_stop it affects R
    
    
    
    "sharesfloat_on": [0],
    "sharesfloat_min": [1000000],
    "sharesfloat_max": [9999999999],
    "market_cap_on": [0],
    "market_cap_min": [3000000],
    "market_cap_max": [9999999999999999],
    # for both strategys
    "price_between_on": [1],
    "min_between_price": [2.5],
    "max_between_price": [20],

    "buytime_on": [0],
    "buy_time": ["09:30:00"],

    "buylocatecondition_on": [0],
    "buy_locate_time": ["09:25:00"],
    "last_close_per_locate": [.50],

    "selltime_on": [1],
    "sell_time": ['15:30:00'],

    "buy_between_time_on": [1],
    "buy_after": ["09:29:00"],
    "buy_before": ["09:45:00"],

    "volume_sum_cal_on": [0],
    "vol_sum_greaterthan": [1000000],
    "pm_volume_sum_cal_on": [0],
    "pm_volume_sum_greaterthat": [1000000],
    "pm_gap_on": [0],
    "pmg_greater": [0.4],
    "per_change_first_tick_on": [0],
    "precent_greater": [0.3],

    "per_change_open_on": [0],
    "per_change_open_on_2": [0],
    "open_greater": [0.05],

    "vwap_above_on": [0],
    "vwap_below_on": [0],
    
    "vwap_push_on": [0],
    "open_greater_vwap_push": [.5],

    "last_close_change_on": [1],

    "last_close_per": [.5],

    "percent_from_pmh_on": [0],
    "per_pmh_val": [0.3],

    "day_greater_than_pm_on": [0],
    "pm_greater_than_day_on": [0],
    "st_close_lessthan_on": [0],  # Long
    "st_close_greaterthan_on": [0],  # short


    # System 2--------------------------------
    "take_second_trade": [False],

    "last_close_change_on_2": [0],
    "last_close_per_2": [.4],

    "percent_from_pmh_on_2": [0],
    "per_pmh_val_2": [0.02],

    "close_stop_on_2": [0],
    "close_stop_2": [.1],
    "min_reward_then_let_it_run_2": [0],
    "buy_between_time_on_2": [0],
    "buy_after_2": ["09:32:00"],
    "buy_before_2": ["11:00:00"],

    "st_close_greaterthan_on_2": [0],  # short 2
    }
# close_stop_range = [i / 100 for i in range(1, 21, 2)]
# last_close_per_range  = [round(0.05 + i*0.05, 2) for i in range(math.ceil((0.50-0.05)/0.05))]
# [i / 100 for i in range(1, 21, 2)] #generates a sequence of numbers starting from 1 and incrementing by 2 until it reaches 21 (exclusive).


def dict_combinations(default_parms):
    # Get the keys and values for the dictionary
    keys = list(default_parms.keys())
    values = list(default_parms.values())
    # Use itertools.product to get all possible combinations of the values
    combinations = itertools.product(*values)
    # Loop through the combinations and print them out (or do whatever you need with them)

    df = pd.DataFrame()
    for combination in combinations:
        # print(combination)


# # define ranges of values for each parameter
        my_dict = {}
        for i, value in enumerate(combination):
            my_dict[keys[i]] = value
        bt = Backtester(my_dict)
        ohlc_intraday, results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal,date_stats,date_stats_2 = bt.backtester(my_dict)
        my_dict['finish_bal'] = finish_bal
        df = pd.concat([df, pd.DataFrame(my_dict, index=[0])], ignore_index=True)

        print('--------------finishing bal',finish_bal,'-------------------')
    return df,my_dict,ohlc_intraday, results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal,date_stats,date_stats_2


df,my_dict,ohlc_intraday, results_store, num_of_trades, total_win, win_per, gross_profit,total_locate_fee,total_comm,finish_bal,date_stats,date_stats_2 = dict_combinations(default_parms)

mac = my_dict['mac']
print('mac', mac)

# Get todays date
today_dt = datetime.now()
today = today_dt.strftime("%Y-%m-%d")
time_now = today_dt.strftime("_%H-%M")
results_name = today + time_now +  '_for_loop_backtest_results.csv' #
if mac == 1:
    df.to_csv("/Users/briansheehan/Documents/mac_quant/Backtesting/Backtest_results/%s"% results_name, index=False)
if mac == 0:
    df.to_csv(r"C:/Users/brian/OneDrive/Documents/Quant/2_System_Trading/Backtesting/Backtest_results\%s"% results_name, index=False)
    print('got here')
