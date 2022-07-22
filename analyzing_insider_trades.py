import settings

import pandas as pd
import yfinance as yf
import numpy as np

import os
import glob

import time
from datetime import datetime

from win10toast import ToastNotifier



def analyzing():
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

    os.chdir(settings.directory)

    today = datetime.today().strftime('%Y%m%d')
    new_name = 'insider_buy_' + str(today) + '.xls'
    # new_name2 = 'insider_sell_' + str(today) + '.xls'
    input1 = os.path.join('input', new_name)
    # input2 = os.path.join('input', new_name2)


    df_insider_buy = pd.read_csv(input1, sep='\t')
    # df_insider_sell = pd.read_csv(input2, sep='\t')
    # df_insider_buy=df_insider_buy.drop(df_insider_buy.columns[-3:1], axis=1)
    df_insider_buy = df_insider_buy.iloc[:, :-3]
    # df_insider_sell = df_insider_sell.iloc[:, :-3]

    # df_insider_sell=df_insider_sell.drop(df_insider_sell.columns[-1], axis=1)
    df_insider_buy["DATE"] = pd.to_datetime(df_insider_buy["DATE"])
    # df_insider_sell["DATE"] = pd.to_datetime(df_insider_sell["DATE"])

    #accessing to the database/not really but you know
    insider =  'insiders.csv'
    insiders = pd.read_csv(insider)
    insiders = insiders[
        (insiders['high_diff'] > 0.03) & (insiders['RANK'] > 1) & (insiders['MKT VALUE'] > 10000)]

    df_insider_buy2 = df_insider_buy[df_insider_buy['FILER NAME'].isin(list(insiders.INSIDER))]
    tickerStrings = df_insider_buy2.TICKER.unique()
    df_list = list()
    for ticker in tickerStrings:
        data = yf.download(ticker, group_by="Ticker", period="1mo", interval="1d")
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

    # combine all dataframes into a single dataframe
    if not len(df_list)== 0:
        df = pd.concat(df_list)
        df.reset_index(inplace=True)
        df_insider_buy2['next_day_high_price'] = df_insider_buy2.apply(get_next_value, axis=1)
        df_insider_buy2['next_2day_high_price'] = df_insider_buy2.apply(get_next2_value, axis=1)
        df_insider_buy2['next_3day_high_price'] = df_insider_buy2.apply(get_next3_value, axis=1)
        df_insider_buy2['high_avg'] = df_insider_buy2[
            ['next_day_high_price', 'next_2day_high_price', 'next_3day_high_price']].mean(axis=1)
        df_insider_buy2['high_diff'] = (df_insider_buy2['high_avg'] - df_insider_buy2['TRANS. PRICE']) / df_insider_buy2[
            'high_avg']

        df_insider_buy2['next_day_low_price'] = df_insider_buy2.apply(get_next_low_value, axis=1)
        df_insider_buy2['next_2day_low_price'] = df_insider_buy2.apply(get_next2_low_value, axis=1)
        df_insider_buy2['next_3day_low_price'] = df_insider_buy2.apply(get_next3_low_value, axis=1)
        df_insider_buy2['low_avg'] = df_insider_buy2[
            ['next_day_low_price', 'next_2day_low_price', 'next_3day_low_price']].mean(axis=1)

        df_insider_buy2['low_diff'] = (df_insider_buy2['low_avg'] - df_insider_buy2['TRANS. PRICE']) / df_insider_buy2[
            'low_avg']

        #output analysis
            #buy
        if not df_insider_buy2.empty:
            output_name= 'analyzed_insider_buy_' + str(today) + '.csv'
            output = os.path.join('output', output_name)
            df_insider_buy2.to_csv(output)
            toast = ToastNotifier()
            toast.show_toast(
                output_name,
                "File is ready.",
                duration=600,
                # icon_path="icon.ico",
                threaded=True,
            )
            #sell

    # print(settings.directory)
    # sell = df_insider_sell[(df_insider_sell['TICKER'].isin(settings.my_stocks))|(df_insider_sell['TICKER'].isin(df_insider_buy2['TICKER']))]
    # if not sell.empty:
    #     output_sell= 'analyzed_insider_sell_' + str(today) + '.csv'
    #     output = os.path.join('output', output_sell)
    #     sell.to_csv(output)
    #     toast = ToastNotifier()
    #     toast.show_toast(
    #         output_name,
    #         "File is ready.",
    #         duration=600,
    #         # icon_path="icon.ico",
    #         threaded=True,
    #     )

    #move files to backup
    output_name2 = 'insider_buy_' + str(today) + '.csv'
    # output_name3 = 'insider_sell_' + str(today) + '.csv'
    output2 = os.path.join('input/backup', output_name2)
    # output3 = os.path.join('input/backup', output_name3)
    df_insider_buy.to_csv(output2)
    # df_insider_sell.to_csv(output3)

    #remove files
    os.remove(input1)
    # os.remove(input2)

        # os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

# os.path.join('subdirectory', 'analyzed_insider_buy_' + str(today) + '.csv')
# os.chdir(settings.directory)
#
# test1 = pd.DataFrame()
# output = os.path.join('output', 'test.csv')
# test1.to_csv(output)
