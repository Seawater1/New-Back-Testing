#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:11:22 2023

@author: briansheehan
"""

import pandas as pd 
###########################################################################################################
###########################KPIs#############################################################################

def abs_return(date_stats):
    df = pd.DataFrame(date_stats).T
    df["ret"] = 1+df.mean(axis=1)
    cum_ret = (df["ret"].cumprod() - 1)[-1]
    return  cum_ret

def win_rate(date_stats):
    win_count = 0
    lose_count = 0
    for i in date_stats:
        for ret in date_stats[i]:
            if date_stats[i][ret] > 0:
                win_count+=1
            elif date_stats[i][ret] < 0:
                lose_count+=1
    return (win_count/(win_count+lose_count))*100

def mean_ret_winner(date_stats):
    win_ret = []
    for i in date_stats:
        for ret in date_stats[i]:
            if date_stats[i][ret] > 0:
                win_ret.append(date_stats[i][ret])                
    return sum(win_ret)/len(win_ret)

def mean_ret_loser(date_stats):
    los_ret = []
    for i in date_stats:
        for ret in date_stats[i]:
            if date_stats[i][ret] < 0:
                los_ret.append(date_stats[i][ret])                
    return sum(los_ret)/len(los_ret)
