import datetime

import sys
import threading

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import numpy as np
import pandas as pd
import mplfinance as mpl
import pysnooper

# @pysnooper.snoop()
def show_Kline(stock_code):
    try:
        # 创建数据库连接
        engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
        conn = engine.connect()

        result = conn.execute(text('describe daily'))
        print('========== describe daily result:==========')
        print(result.fetchall())
        print('-------------------')

        result = conn.execute(text('select distinct ts_code from daily limit 10000'))
        print('========== select distinct ts_code from daily limit 10000:==========')
        all_data__ts_codes = result.fetchall()
        print(all_data__ts_codes)
        print('--------- end of select distinct ts_code from daily limit 10000:==========')

        sql_text = text(f''' select * from daily where ts_code=\'{stock_code}\' limit 10000''')
        result = conn.execute(sql_text)
        all_data = result.fetchall()
        print(all_data)

        if len(all_data) < 3 : # 跳过新股，不然会index out of range
            print("\033[0;31;40m", f'''this stock {stock_code} is too new''', "\033[0m")
            return

        df_daily = pd.DataFrame(list(all_data))
        print(f'''df_daily:{df_daily}''')
        print(f'''df_daily.columns:{df_daily.columns}''')


        del df_daily['amount']
        del df_daily['pct_chg']
        del df_daily['_change']
        del df_daily['pre_close']
        del df_daily['ts_code']

        df_daily.index = pd.DatetimeIndex(df_daily['trade_date'])
        del df_daily['trade_date']

        print(f'''df_daily.columns after del:{df_daily.columns}''')
        print(f'''df_daily.index:{df_daily.index}''')

        df_daily.columns = ['open', 'high', 'low', 'close', 'volume']
        mpl.plot(df_daily, type='line', mav=(3, 6, 9), volume=True, axtitle=stock_code)
        # mpl.plot(df_daily, type='candle',mav=(3,6,9), volume=True)

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()


pymysql.install_as_MySQLdb()
stock_code = '000001.SZ'
show_Kline(stock_code)

stock_code = '000002.SZ'
show_Kline(stock_code)
