# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:26:27 2023

@author: brian
Slippage is the difference between the expected price of a trade and the actual executed price. 
The amount of slippage depends on various factors, such as the trading volume, liquidity, and market volatility. 
Therefore, you need to decide on a slippage model that best reflects the behavior of the markets you are trading. 
Some commonly used slippage models include fixed slippage, percentage-based slippage, and market impact slippage.

Trade Execution: The way your backtester executes trades can also affect the amount of slippage. 
For example, if you assume that trades are executed at the close of the bar, you may experience more slippage than if you assume that trades are executed at the open of the bar. 
Therefore, you need to decide on a trade execution model that best reflects the way trades are executed in the real world.

"""

slippage = 0.01  # 1% slippage
class SlippageCalculator:
    def calculate_open_slippage(self, direction, open_price, open_slippage):
        """
        Calculates the entry price with slippage based on the given direction and slippage.

        Args:
        - direction (str): Either 'long' or 'short' to indicate the trade direction.
        - open_price (float): The entry price for the trade.
        - open_slippage (float): The slippage for the entry price as a decimal.

        Returns:
        The entry price with slippage.
        """

        # Calculate entry price with slippage
        open_price_slippage = open_price * (1 + open_slippage) if direction == 'long' else open_price * (1 - open_slippage)
        
        return open_price_slippage


    def calculate_close_slippage(self, direction, close_price, close_slippage):
        """
        Calculates the exit price with slippage based on the given direction and slippage.

        Args:
        - direction (str): Either 'long' or 'short' to indicate the trade direction.
        - close_price (float): The exit price for the trade.
        - close_slippage (float): The slippage for the exit price as a decimal.

        Returns:
        The exit price with slippage.
        """

        # Calculate exit price with slippage
        close_price_slippage = close_price * (1 - close_slippage) if direction == 'long' else close_price * (1 + close_slippage)
        
        return close_price_slippage



"""
In this example, slippage is the percentage-based slippage rate. 
The entry_price_slippage and exit_price_slippage are the adjusted entry and exit prices, respectively, with slippage factored in. 
Finally, the pnl is calculated based on the adjusted entry and exit prices with slippage.

You would need to implement this logic in your backtesting framework to adjust your simulated trades' prices and 
evaluate the impact of slippage on your backtest results
"""
