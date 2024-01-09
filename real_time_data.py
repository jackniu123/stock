import tushare as ts
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
import os
import math

# https://zhuanlan.zhihu.com/p/674945970
# import yfinance as yf
#
# # CREATE A TICKER INSTANCE PASSING TESLA AS THE TARGET COMPANY
# tsla = yf.Ticker('TSLA')
#
# # print all attributes of Ticker
# print(dir(tsla))
#
# # CALL THE MULTIPLE FUNCTIONS AVAILABLE AND STORE THEM IN VARIABLES.
# actions = tsla.get_actions()
# balance = tsla.get_balance_sheet()
# cf = tsla.get_cashflow()
# info = tsla.get_info()
# inst_holders = tsla.get_institutional_holders()
# news = tsla.get_news()
#
# # PRINT THE RESULTS
# print(actions)
# print('*'*20)
# print(balance)
# print('*'*20)
# print(cf)
# print('*'*20)
# print(info)
# print('*'*20)
# print(inst_holders)
# print('*'*20)
# print(news)
# print('*'*20)
#
#
#

# 语音播报的用法：https://blog.csdn.net/mfsdmlove/article/details/124500805
import pyttsx3
import datetime
import time



# while True:
#     current_time = datetime.datetime.now()
#     hour = current_time.hour
#     minute = current_time.minute
#
#
#     engine = pyttsx3.init()
#     # engine.setProperty('volume', 1)
#
#     pyttsx3.speak('牛东升真牛B！')
#     pyttsx3.speak(f'current time: {hour}:{minute}')
#
#     if (hour != 14) or (minute < 55):
#         time.sleep(5)
#         continue
#     else:
#         break



# https://blog.csdn.net/lly1122334/article/details/115739576
import schedule

import time
import schedule


# def job():
#     print('working...')


# schedule.every(5).seconds.do(job)  # 每10分钟
# schedule.every(10).minutes.do(job)  # 每10分钟
# schedule.every().hour.do(job)  # 每小时
# schedule.every().day.at('20:07').do(job)  # 每天10:30
# schedule.every().monday.do(job)  # 每周一
# schedule.every().wednesday.at('13:15').do(job)  # 每周三13:15
# schedule.every().minute.at(':17').do(job)  # 每分钟的17秒

# while True:
#     schedule.run_pending()
#     time.sleep(1)




# https://blog.csdn.net/u012940698/article/details/135054433
# 实时股票行情接口列表：https://www.llldbz.cn/article/96549.html



COUNT_PER_REQUEST = 870

def stock_getter(df, in_query_str):
    print('=' * 100)
    # sina数据
    df = df.append(ts.realtime_quote(ts_code=in_query_str))







#设置你的token，登录tushare在个人用户中心里拷贝
ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')

#sina数据
df = ts.realtime_quote(ts_code='600000.SH,000001.SZ,000001.SH')

print(f'sina============\n{df}')

#东财数据
df = ts.realtime_quote(ts_code='600000.SH', src='dc')

print(f'dongcai============\n{df}')

pymysql.install_as_MySQLdb()

try:
    # 创建数据库连接
    engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
    conn = engine.connect()

    result = conn.execute(text('describe daily'))
    print('========== describe daily result:==========')
    print(result.fetchall())
    print('-------------------')

    result = conn.execute(text('select distinct ts_code from daily where trade_date=\'20231101\''))
    print('========== select distinct ts_code from daily limit 10000:==========')
    all_data__ts_codes = result.fetchall()
    print(all_data__ts_codes, '\n the above data length is:' , len(all_data__ts_codes))
    print('--------- end of select distinct ts_code from daily limit 10000:==========')

    cur_index = 0
    total_count = 0
    query_str = ''
    df = []

    threads = []

    for ts_code in all_data__ts_codes:

        if len(query_str) < 1:
            query_str = ts_code[0]
        else:
            query_str = query_str + ',' + ts_code[0]

        if cur_index < COUNT_PER_REQUEST - 1 and total_count < len(all_data__ts_codes) - 1:
            cur_index += 1
            total_count += 1
            continue
        else:
            threads.append(threading.Thread(target=stock_getter, args=(df, query_str)))

            # stock_getter(df, query_str)

            cur_index = 0
            total_count += 1
            query_str = ''

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=30)

    if len(df) != math.ceil(5500/COUNT_PER_REQUEST):
        print("\033[0;31;40m", 'we have lost connection!', "\033[0m")
    else:
        print('len of df:',math.ceil(5500 / COUNT_PER_REQUEST))

    pd.set_option('display.width', 1000)  # 设置字符显示宽度
    # pd.set_option('display.max_rows', None)  # 设置显示最大行
    pd.set_option('display.max_columns', 20)  # 设置显示最大行

    print(f'outer df:============', len(df), type(df), ":\n", df)

    print(f'outer df[0]:============', len(df[0]), type(df[0]), ":\n", df[0])
    print(df[0].columns)

except Exception as e:
    print("\033[0;31;40m", e, "\033[0m")

finally:
    conn.commit()
    conn.close()