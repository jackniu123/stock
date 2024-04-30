import akshare as ak
from tkinter import messagebox
import datetime
import re
import matplotlib.pyplot as plt
import matplotlib # https://www.runoob.com/matplotlib/seaborn-tutorial.html
import numpy
import requests
import pandas as pd
import numpy as np
# import akshare as ak

'''
不同的声音 https://zhuanlan.zhihu.com/p/189426241
巴菲特在《福布斯》杂志上的这篇超长文章的核心是解释为什么美国国民生产总值GNP在1964年到1981年上涨了2.7倍，但同期道琼斯指数只涨了1点，而美国GNP在1981年到1988年只上涨了0.8倍，但同期道琼斯指数却上涨了9.5倍。
值得一提的是，现在各国GNP和GDP的差距很小，各国主要公布GDP，所以用GDP取代GNP是普遍的做法。
大家想一想，中国GDP过去十年高增长，但是A股上证指数过去十年基本没涨，是不是有点类似。将来中国GDP增速肯定会放缓，但是A股也有比较大的可能迎来较大的涨幅，过去我曾经多次解释过背后可能的原因。

在投资上，没有单一指标是完美的，不要过多依赖听上去似乎最简单的估值指标，要重点关注利率走势和其他基本面指标
未来充满不确定性，你仍然可以有所为有所不为。降低高估值国家和个股的配置比率，增加低估值国家和个股的配置比率，把业绩评估的目光放长远，是很不错的选择。

相关支持：
美国参加的战争：https://www.zhihu.com/question/67203048
美国国债占GDP比例的历史数据：https://xueqiu.com/8458090377/262611597
原油价格历史走势：https://zhuanlan.zhihu.com/p/150056672
1970年代，美国的国债利息占GDP的规模一直在1.2%左右，参加的战争主要是1970年入侵柬埔寨，1965-1973越南战争，同期道琼斯指数几乎没有上涨。
1980年代开始，该比例急速飙升到3.0%左右，发起了两场中东的战争和两场美洲的巴拿马运河战争，苏联于1989年解体，同期道琼斯指数上涨9.5倍。
70年代的油价相对于80年代高很多。

'''

import pandas as pd
import requests

def check_buffet_index():
    stock_buffett_index_lg_df = ak.stock_buffett_index_lg()
    print(stock_buffett_index_lg_df.tail(20))

    current_buffet_index = stock_buffett_index_lg_df.iloc[-1]['总市值'] / stock_buffett_index_lg_df.iloc[-1]['GDP']
    print(f'current buffet index is {{{current_buffet_index}}}')

    if current_buffet_index < 0.6 or stock_buffett_index_lg_df.iloc[-1]['近十年分位数'] < 0.15:
        messagebox.showinfo('提示',
                            f'当前巴菲特指数超级便宜：{{{current_buffet_index}}} \n {{{stock_buffett_index_lg_df.iloc[-1]}}}')

    if current_buffet_index > 1 or stock_buffett_index_lg_df.iloc[-1]['近十年分位数'] > 0.9:
        messagebox.showerror('警告',
                             f'！！！你在玩火，巴菲特指数已经高达：{{{current_buffet_index}}} \n {{{stock_buffett_index_lg_df.iloc[-1]}}}')

    # print(stock_buffett_index_lg_df)


def check_ipo():
    b_has_ipo = False
    last_ipo = '不存在科技'

    response = requests.get('https://data.eastmoney.com/xg/xg/calendar.html')

    # print(response.text)

    i = 0
    for item in response.text.splitlines():
        i += 1

        if 'calendardata' in item:
            print(i, ":", item)
            print('========================================================')
            j = 0
            for line in re.split('SECURITY_NAME_ABBR', item):
                j += 1
                if '申购' in line:
                    print(j, ":", line)
                    last_ipo = line
                    for days in range(0, 30):
                        if 'TRADE_DATE":"' + str(datetime.datetime.now().date() + datetime.timedelta(days)) in line:
                            print('/n ============================================')
                            print(line)
                            # messagebox.showinfo('提示', str(datetime.datetime.now().date()+datetime.timedelta(days)) + line)
                            b_has_ipo = True

    if not b_has_ipo:
        messagebox.showinfo('提示', f'没有IPO了，最近的IPO情况是：{{{last_ipo}}}')

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
import matplotlib.ticker as mticker

def check_MA20_percent():
    pymysql.install_as_MySQLdb()
    pd.options.display.max_columns = None
    try:
        # 创建数据库连接
        engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
        conn = engine.connect()

        result = conn.execute(text('describe daily'))
        print('========== describe daily result: ==========')
        print(result.fetchall())
        print('----------- end of describe daily --------')

        result = conn.execute(text(f'''select distinct ts_code from daily where ts_code like \'______.SH\' '''))
        print('========== select distinct ts_code from daily limit 10000: ==========')
        all_data__ts_codes = result.fetchall()
        print("数据库daily中的所有上海市场股票代码：", all_data__ts_codes)
        print('--------- end of select distinct ts_code from daily limit 10000:==========')

        # sql_text = text(f''' select * from daily where trade_date like \'202301__\' limit 100000000''')
        # result = conn.execute(sql_text)
        # # print(f'========== begin {{{sql_text}}}:==========')
        # all_data = result.fetchall()
        # print(all_data)
        # print("all_data len = ", len(all_data))


        analyze_single_stock = False

        df_all = pd.DataFrame(None, columns=['ts_code', 'trade_date', 'close', 'MA20'])

        for ts_code in all_data__ts_codes:
            if analyze_single_stock :
                if not (ts_code[0] == '688536.SH') \
                        and not (ts_code[0] == '600757.SH')\
                        and not (ts_code[0] == '600758.SH'):
                    continue

            print("+"*10, f'''begin calc MA20 of : {ts_code[0]}''', "+"*10)
            sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' and trade_date like \'2024____\' limit 10000''')
            result = conn.execute(sql_text)
            # print(f'========== begin {{{sql_text}}}:==========')
            all_data = result.fetchall()
            # print(f'all_data = {all_data}')
            # print(f'---------- end of {{{sql_text}}} ----------')

            if len(all_data) < 60 : # 跳过新股，没啥参考意义，且容易index out of bounds
                continue

            df_daily = pd.DataFrame(list(all_data))

            # df_daily = df_daily.close
            df_daily = df_daily.loc[:,['ts_code', 'trade_date', 'close']]
            # print(df_daily)
            df_daily['MA20'] = df_daily.close.rolling(20).mean()
            df_daily['L_MA20'] = df_daily['MA20'] < df_daily['close']
            # print(df_daily.MA20)
            # print(df_daily)
            df_all = pd.concat([df_all, df_daily], ignore_index=True)
            # del df_daily['close']
            # for row_index, row_value in df_daily.iterrows():
            #     print(f'\n {row_index} : {row_value}')

        print(df_all)

        df_all_grouped = df_all.groupby('trade_date')

        date_array = []
        percent_array = []

        for name, group in df_all_grouped:
            # print(name, group)
            # df_specific_date = df_all[df_all['trade_date'] == name]
            # print(f""" {name} : close less than MA20 count: {len(df_specific_date[df_specific_date['L_MA20'] == True])}""")
            date_array = numpy.append(date_array, [name])
            percent_array = numpy.append(percent_array, [len(group[group['L_MA20'] == True]) * 100 / len(group)])

            # result_list.append((name, len(df_specific_date[df_specific_date['L_MA20'] == True]) * 100 / len(df_specific_date)))
        print(date_array)
        print(percent_array)
        print(date_array[-1])
        print(percent_array[-1])

        if percent_array[-1] > 80:
            messagebox.showwarning('警告', f"""{date_array[-1]} 超过20日均线的个股比例超过了80%：{percent_array[-1]}""")
        elif percent_array[-1] < 10:
            messagebox.showwarning('警告', f"""{date_array[-1]} 超过20日均线的个股比例低于了10%：{percent_array[-1]}""")
        else:
            return

        fig, ax = plt.subplots(1, 1)
        ax.plot(date_array, percent_array)

        tick_spacing = len(date_array) / 100  # x軸密集度
        ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
        plt.xticks(rotation=90)
        plt.rcParams['figure.figsize'] = [40, 10]

        plt.show()

    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def check_below_net_asset():
    stock_a_below_net_asset_statistics_df = ak.stock_a_below_net_asset_statistics()
    print(stock_a_below_net_asset_statistics_df.iloc[-1])

    if stock_a_below_net_asset_statistics_df.iloc[-1]['below_net_asset_ratio'] > 0.1:
        messagebox.showwarning('警告', f'破净股占比达到新高，底部区域呈现：\n {stock_a_below_net_asset_statistics_df.iloc[-1]}')

    if stock_a_below_net_asset_statistics_df.iloc[-1]['below_net_asset_ratio'] < 0.07:
        messagebox.showwarning('警告', f'破净股占比达到新低，头部区域呈现：\n {stock_a_below_net_asset_statistics_df.iloc[-1]}')


    # print()

def check_turnover_percent():
    # https: // legulegu.com / stockdata / market - turn - over - ratio - statistics
    return
# https://legulegu.com/stockdata/bottom-research-nav
# https://legulegu.com/stockdata/ma-statistics   https://zhuanlan.zhihu.com/p/63603249  https://zhuanlan.zhihu.com/p/637665421
# 20日均线占比统计，极端值几乎与股市的高低点完全同步。
if __name__ == '__main__':

    from requests import utils

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    utils.default_user_agent = lambda: DEFAULT_USER_AGENT

    # check_buffet_index()
    # check_ipo()
    # check_MA20_percent()
    # check_turnover_percent()
    check_below_net_asset()
