# packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import qis as qis
from enum import Enum

np.random.seed(0)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from bbg_fetch import fetch_field_timeseries_per_tickers, fetch_fundamentals

tickers = ["CAT US Equity", "IBM US Equity",
           "HD US Equity", "JPM US Equity",
           "NESN SW Equity", "AZN LN Equity", "OR FP Equity",
           "SPY US Equity", "TLT US Equity", "USO US Equity", "GLD US Equity",
           "91282CMM Govt", "BA 5.805 05/01/50 Corp", "BAC 5.015 07/22/33 Corp"]

start_position = 10*np.floor(np.random.randint(100, high=1000, size=len(tickers), dtype=int)/10)

prices = fetch_field_timeseries_per_tickers(tickers=tickers,
                                            start_date=pd.Timestamp('30Sep2025'),
                                            end_date=pd.Timestamp.now())
print(prices)

df = fetch_fundamentals(tickers=tickers, fields=['name', 'crncy', 'security_des', 'ult_parent_ticker_exchange',
                                                 'security_typ', 'gics_sector_name'])

df['Price0'] = prices.iloc[0, :]
df['Price1'] = prices.iloc[-1, :]
df['Return'] = df['Price1'] / df['Price0'] - 1.0
df['Position0'] = start_position
df['Position1'] = start_position
df['ExchangeRateUSD'] = 1.0
df['CurrentValueUSD'] = start_position * df['Price1'] * df['ExchangeRateUSD']

print(df)
df.to_clipboard()

