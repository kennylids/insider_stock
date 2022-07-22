import settings

import pandas as pd
import yfinance as yf
import numpy as np

import os
import glob

import time
from datetime import datetime

def consolidate(dir):
    def get_next_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['High']

        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=1)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next2_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['High']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['High']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=2)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next3_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        elif x['DATE'].dayofweek == 2:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['Low']

        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=1)))
                            ]['Low']
        return next((v for v in values), np.nan)

    def get_next2_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['Low']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['Low']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=2)))
                            ]['Low']
        return next((v for v in values), np.nan)

    def get_next3_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        elif x['DATE'].dayofweek == 2:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['Low']
        return next((v for v in values), np.nan)

    # os.chdir(settings.directory)
    # print(settings.directory)
    os.chdir(dir + "\\input")

    csv_files = glob.glob(os.path.join('input', "*"))
    print(csv_files[-1])

    #og insider master list
    master = pd.read_csv('insiders.csv')
    master = master.iloc[:, 1:]




    df_insider = pd.read_csv(csv_files[-1], sep='\t')
    df_insider = df_insider.drop(df_insider.columns[-1], axis=1)
    df_insider["DATE"] = pd.to_datetime(df_insider["DATE"])

    tickerStrings = df_insider.TICKER.unique()
    df_list = list()
    for ticker in tickerStrings:
        data = yf.download(ticker, group_by="Ticker", period="1mo", interval="1d")
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

    # combine all dataframes into a single dataframe
    df = pd.concat(df_list)
    df.reset_index(inplace=True)

    # df.loc[lastday]
    df_insider['next_day_high_price'] = df_insider.apply(get_next_value, axis=1)
    df_insider['next_2day_high_price'] = df_insider.apply(get_next2_value, axis=1)
    df_insider['next_3day_high_price'] = df_insider.apply(get_next3_value, axis=1)
    df_insider['high_avg'] = df_insider[['next_day_high_price', 'next_2day_high_price', 'next_3day_high_price']].mean(
        axis=1)
    df_insider['high_diff'] = (df_insider['high_avg'] - df_insider['TRANS. PRICE']) / df_insider['high_avg']

    df_insider['next_day_low_price'] = df_insider.apply(get_next_low_value, axis=1)
    df_insider['next_2day_low_price'] = df_insider.apply(get_next2_low_value, axis=1)
    df_insider['next_3day_low_price'] = df_insider.apply(get_next3_low_value, axis=1)
    df_insider['low_avg'] = df_insider[['next_day_low_price', 'next_2day_low_price', 'next_3day_low_price']].mean(
        axis=1)
    df_insider['low_diff'] = (df_insider['low_avg'] - df_insider['TRANS. PRICE']) / df_insider['low_avg']

    result = pd.concat([df_insider,master])
    result.to_csv('insiders.csv')

    today = datetime.today().strftime('%Y%m%d')
    backup_name= 'weekly_insider_' + str(today) + '.csv'
    backup = os.path.join('input\\backup', backup_name)
    os.rename(csv_files[-1], backup)


def consolidate_daily(dir):
    def get_next_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['High']

        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=1)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next2_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['High']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['High']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=2)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next3_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        elif x['DATE'].dayofweek == 2:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['High']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['High']
        return next((v for v in values), np.nan)

    def get_next_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['Low']

        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=1)))
                            ]['Low']
        return next((v for v in values), np.nan)

    def get_next2_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['Low']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=4)))
                            ]['Low']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=2)))
                            ]['Low']
        return next((v for v in values), np.nan)

    def get_next3_low_value(x):
        # The day of the week with Monday=0, Sunday=6.
        if x['DATE'].dayofweek == 4:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        elif x['DATE'].dayofweek == 3:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        elif x['DATE'].dayofweek == 2:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=5)))
                            ]['Low']
        else:
            values = df.loc[(df['ticker'] == x['TICKER']) &
                            (df['Date'] == (x['DATE'] + pd.Timedelta(days=3)))
                            ]['Low']
        return next((v for v in values), np.nan)

    # os.chdir(settings.directory)
    os.chdir(dir + "\\input")

    df_insider_buy = pd.read_csv('insiders.csv')

    df_insider_buy["DATE"] = pd.to_datetime(df_insider_buy["DATE"])
    df_insider_buy = df_insider_buy.iloc[:, 1:]

    today = pd.datetime.today().date()
    tickerStrings = df_insider_buy[
        df_insider_buy['DATE'].dt.date >= (today - pd.Timedelta(7, unit='d'))].TICKER.unique()

    df_list = list()
    for ticker in tickerStrings:
        data = yf.download(ticker, group_by="Ticker", period="1mo", interval="1d")
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

    df = pd.concat(df_list)
    df.reset_index(inplace=True)

    mask = (df_insider_buy['DATE'].dt.date >= (today - pd.Timedelta(7, unit='d')))
    df_insider_buy_masked = df_insider_buy[mask]

    # z['c'] = 0
    df_insider_buy.loc[mask, 'next_day_high_price'] = df_insider_buy_masked.apply(get_next_value, axis=1)
    df_insider_buy.loc[mask, 'next_2day_high_price'] = df_insider_buy_masked.apply(get_next2_value, axis=1)
    df_insider_buy.loc[mask, 'next_3day_high_price'] = df_insider_buy_masked.apply(get_next3_value, axis=1)
    df_insider_buy.loc[mask, 'high_avg'] = df_insider_buy[
        ['next_day_high_price', 'next_2day_high_price', 'next_3day_high_price']].mean(axis=1)
    df_insider_buy.loc[mask, 'high_diff'] = (df_insider_buy['high_avg'] - df_insider_buy['TRANS. PRICE']) / \
                                            df_insider_buy['high_avg']

    df_insider_buy.loc[mask, 'next_day_low_price'] = df_insider_buy_masked.apply(get_next_low_value, axis=1)
    df_insider_buy.loc[mask, 'next_2day_low_price'] = df_insider_buy_masked.apply(get_next2_low_value, axis=1)
    df_insider_buy.loc[mask, 'next_3day_low_price'] = df_insider_buy_masked.apply(get_next3_low_value, axis=1)
    df_insider_buy.loc[mask, 'low_avg'] = df_insider_buy[
        ['next_day_low_price', 'next_2day_low_price', 'next_3day_low_price']].mean(axis=1)
    df_insider_buy.loc[mask, 'low_diff'] = (df_insider_buy['low_avg'] - df_insider_buy['TRANS. PRICE']) / \
                                           df_insider_buy['low_avg']
    df_insider_buy.to_csv('insiders.csv')

