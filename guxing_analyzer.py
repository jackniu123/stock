import datetime

import sys
import threading

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import numpy as np
import pandas as pd
import mplfinance as mpl
import pysnooper
import time

try:
    # 创建数据库连接
    engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
    conn = engine.connect()

    result = conn.execute(text('describe daily'))
    print('========== describe daily result:==========')
    print(result.fetchall())
    print('-------------------')

    result = conn.execute(text('select distinct ts_code from daily'))
    print('========== select distinct ts_code from daily limit 10000:==========')
    all_data__ts_codes = result.fetchall()
    print(all_data__ts_codes)
    print('--------- end of select distinct ts_code from daily limit 10000:==========')

    sql_text = text(f''' select * from daily where ts_code=\'{all_data__ts_codes[0][0]}\' ''')
    print(sql_text)

    current_index = 0

    df_trade_history = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date',
                                                   'sell_price', 'ts_code', 'buy_date_change'])
    df_trade_total = pd.DataFrame(None, columns=['total_profit_change', 'win_percent', 'total_profit', 'ts_code',
                                                 'trade_count', 'profit_trade_count',
                                                 'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])

    detail_filename = '追涨分析_个股_detail.csv'
    total_filename = f'追涨分析_个股_total.csv'

    for ts_code in all_data__ts_codes:
        sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' limit 10000''')

        # sql_text = text(f''' select * from daily limit 16300000 ''')

        # begin_time = time.perf_counter()
        result = conn.execute(sql_text)
        # print(time.perf_counter()-begin_time)


        # print('========== select * from daily result:==========')
        all_data = result.fetchall()

        if len(all_data) < 3:  # 跳过新股，不然会index out of range
            continue

        df_daily = pd.DataFrame(list(all_data))

        trade_count = 0
        profit_count = 0
        total_profit = 0
        total_profit_change = 0

        for row_index, row_value in df_daily.iterrows():
            # if( row_value[8] < -9.5 ):
            if (row_value['pct_chg'] > MIN_CHANGE and row_value['pct_chg'] < MAX_CHANGE):
                # print("+" * 5, f''' this is {i}td elements.''')
                # print(f'''    trade_date is {row_value['trade_date']}''')
                # print(f'''    row_index is {row_index} ; row_value is:\n{row_value} ''')
                if row_index < len(df_daily) - 2:
                    trade_count = trade_count + 1
                    # print(f''' the next daily is:\n{df_daily.iloc[row_index+1]}''')
                    # print(f'''   buy:{row_value['close']} sell:{df_daily.iloc[row_index+1]['open']}  ''')
                    profit = df_daily.iloc[row_index + 1]['open'] - row_value['close']
                    # print(f'''   profit: {profit}''')
                    total_profit += profit
                    if profit > 0:
                        profit_count += 1
                    total_profit_change += (profit * 100 / row_value['close'])

                    # s = pd.Series({'profit' : df_daily.iloc[row_index + 1]['open'] - row_value['close'], \
                    #                         'buy_date' : row_value['trade_date'], \
                    #                         'buy_price' : row_value['close'],\
                    #                         'sell_date' : df_daily.iloc[row_index+1]['trade_date'], \
                    #                         'sell_price' : df_daily.iloc[row_index+1]['open'], \
                    #                         'ts_code' : ts_code[0], \
                    #                         'buy_date_change' : row_value[8]})
                    # print(s)
                    # df_trade_history._append(s,ignore_index = True)



                    df_trade_history = df_trade_history._append({'profit_change': (
                                (df_daily.iloc[row_index + 1]['open'] - row_value['close']) * 100 / row_value['close']), \
                                                                 'profit': df_daily.iloc[row_index + 1]['open'] -
                                                                           row_value['close'], \
                                                                 'buy_date': row_value['trade_date'], \
                                                                 'buy_price': row_value['close'], \
                                                                 'sell_date': df_daily.iloc[row_index + 1][
                                                                     'trade_date'], \
                                                                 'sell_price': df_daily.iloc[row_index + 1]['open'], \
                                                                 'ts_code': ts_code[0], \
                                                                 'buy_date_change': row_value['pct_chg']},
                                                                ignore_index=True)

                # print("-" * 5, f''' end of this is {i}td elements.\n''')
            #     print(f'curIndex = {curIndex}')
            #     print(f'''curIndex = {curIndex} , the element is: {df_daily[curIndex]['trade_date']}''')
            # curIndex += 1

        # print('-----end iter elements in df_daily')
        df_trade_total = df_trade_total._append(
            {'total_profit_change': total_profit_change, \
             'win_percent': profit_count * 100 / trade_count if trade_count > 0 else 0, \
             'total_profit': total_profit, \
             'ts_code': ts_code[0], \
             'trade_count': trade_count, \
             'profit_trade_count': profit_count, \
             'begin_date': df_daily.iloc[0]['trade_date'], \
             'end_date': df_daily.iloc[-1]['trade_date'], \
             'MIN_CHANGE': MIN_CHANGE, \
             'MAX_CHANGE': MAX_CHANGE}, ignore_index=True)

        print(
            f'''total_profit is {total_profit} total_profit_change is {total_profit_change}  with ts_code={ts_code} [MIN_CHANGE, MAX_CHANGE] = [{MIN_CHANGE}, {MAX_CHANGE}] \n''')

        print("-" * 10, f'''end of analyze: {ts_code[0]}''', "-" * 10, "\n\n")

    WITH_HEADER = True
    if (os.path.exists(detail_filename)):
        WITH_HEADER = False
    else:
        WITH_HEADER = True
    df_trade_history.to_csv(detail_filename, mode='a', header=WITH_HEADER, index=False)

    if (os.path.exists(total_filename)):
        WITH_HEADER = False
    else:
        WITH_HEADER = True
    df_trade_total.to_csv(total_filename, mode='a', header=WITH_HEADER, index=False)

except Exception as e:
    print("\033[0;31;40m", e, "\033[0m")

finally:
    conn.commit()
    conn.close()