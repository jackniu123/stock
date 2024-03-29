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

"""
# 实验日期：2024年3月25日
# 实验方法：在成交量连续N日位于最近M月的地量时，买入；在成交量放大到月成交量的X倍时，卖出；止损设置为下跌Y%；
#          其中各个参数的设定，先取绝对值，后基于个股最近一年的特征做参数优化。
#
#
# 实验结果：
    1,无止损情况下，1500+股票亏损，4000股票盈利。
    2,需要验证实验结果在不同年份是否有差异。
"""

def volume_analizer(start_index, CONTINUE_LOW_VOLUME_DAY_COUNT, DAY_COUNT_OF_INSPECTION, TIMES_OF_BUY, TIMES_OF_SELL):
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

        # has_reach_last_point = False
        analyze_single_stock = False  # 分析单个股票的情况
        analyze_recent_year = True

        current_index = 0

        df_trade_history = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date',
                                                       'sell_price', 'ts_code', 'buy_date_change'])
        df_trade_total = pd.DataFrame(None, columns=['total_profit_change', 'win_percent', 'total_profit', 'ts_code',
                                                     'trade_count', 'profit_trade_count',
                                                     'begin_date', 'end_date'])

        detail_filename = f'量价分析_{CONTINUE_LOW_VOLUME_DAY_COUNT}_{DAY_COUNT_OF_INSPECTION}_{TIMES_OF_BUY}_{TIMES_OF_SELL}_detail.csv'
        total_filename = f'量价分析_{CONTINUE_LOW_VOLUME_DAY_COUNT}_{DAY_COUNT_OF_INSPECTION}_{TIMES_OF_BUY}_{TIMES_OF_SELL}_total.csv'


        #挨个分析股票
        for ts_code in all_data__ts_codes:

            # if not has_reach_last_point :
            #     if ts_code[0] == '603107.SH' :
            #         has_reach_last_point = True
            #         continue
            #     continue

            # 分析前多少个股票，该参数有助于在验证程序时，减小计算量
            if (current_index < start_index[0] or current_index >= start_index[1]):
                current_index += 1
                continue
            current_index += 1

            # 分析单个股票，用于验证程序时减小计算量
            if analyze_single_stock:
                if not (ts_code[0] == '688536.SH'):
                    continue

            print("+"*10, f'''begin analyze: {ts_code[0]}''', "+"*10)

            sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' limit 10000''')
            if analyze_recent_year:
                sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' and trade_date like \'2023____\' limit 10000''')

            # begin_time = time.perf_counter()
            result = conn.execute(sql_text)
            # print(time.perf_counter()-begin_time)



            # print('========== select * from daily result:==========')
            all_data = result.fetchall()

            # print(len(all_data))
            # print(all_data)

            # print(time.perf_counter() - begin_time)
            # print(all_data)
            # sys.exit()

            # all_data_format = np.array(all_data)

            # print('length of result:', len(all_data))

            if len(all_data) < 500: # 跳过交易日不够500的新股，不然会index out of range
                continue

            # print(all_data[1])
            #
            # print(all_data[1][2])

            # print(all_data_format)

            # print(all_data_format[1])
            # print(all_data_format[1][1])


            # print('--------end of ', sql_text)

            # print('========== dataframe :==========')

            # dataframe的用法：https: // blog.csdn.net / Parzival_ / article / details / 114240650

            df_daily = pd.DataFrame(list(all_data))
            # print(df_daily)
            # print(df_daily.columns)

            # print("===iter elments in df_daily:===")
            trade_count = 0
            profit_count = 0
            # curIndex = 0
            total_profit = 0
            total_profit_change = 0
            has_buy = False
            buy_index = -1
            sell_index = -1

            kline_index = 0

            sum_of_volume = 0

            for row_index, row_value in df_daily.iterrows():

                sum_of_volume += row_value['vol']
                if row_index >= DAY_COUNT_OF_INSPECTION:
                    sum_of_volume -= df_daily.iloc[row_index - DAY_COUNT_OF_INSPECTION]['vol']


                # if B_CONF_CLOSE_EQUAL_HIGH:
                #     if row_value['close'] != row_value['high']:
                #         continue

                #一开始是观察阶段，不需要交易。
                if row_index < DAY_COUNT_OF_INSPECTION or row_index < CONTINUE_LOW_VOLUME_DAY_COUNT:
                    continue

                #计算最近DAY_COUNT_OF_INSPECTION天的成交量平均值

                if not has_buy:
                    if df_daily.iloc[row_index]['vol'] < sum_of_volume/DAY_COUNT_OF_INSPECTION / TIMES_OF_BUY:
                        if row_value['pct_chg'] < 9:
                            buy_index = row_index
                            print('trade history---buy record++++++:\n', row_value)
                            has_buy = True
                        else:
                            print('trade history---buy record failed because too much pct_chg:\n', row_value)
                else:
                    if row_index == len(df_daily) - 1:
                        sell_index = row_index
                        has_buy = False
                    else:
                        if df_daily.iloc[row_index]['vol'] > sum_of_volume/DAY_COUNT_OF_INSPECTION * TIMES_OF_SELL:
                            if row_value['pct_chg'] > -9:
                                sell_index = row_index
                                has_buy = False
                            else:
                                print('trade history---sell record failed because too much pct_chg:\n', row_value)

                        # TODO：止损

                #记录买卖情况：
                if sell_index != -1:
                    tmp_sell_index = sell_index
                    sell_index = -1
                    trade_count = trade_count + 1
                    # print(f''' the next daily is:\n{df_daily.iloc[row_index+1]}''')
                    # print(f'''   buy:{row_value['close']} sell:{df_daily.iloc[row_index+1]['open']}  ''')
                    profit = df_daily.iloc[tmp_sell_index]['close'] - df_daily.iloc[buy_index]['close']
                    # print(f'''   profit: {profit}''')
                    total_profit += profit
                    if profit > 0:
                        profit_count += 1
                    total_profit_change += (profit * 100 / df_daily.iloc[buy_index]['close'])

                    # s = pd.Series({'profit' : df_daily.iloc[row_index + 1]['open'] - row_value['close'], \
                    #                         'buy_date' : row_value['trade_date'], \
                    #                         'buy_price' : row_value['close'],\
                    #                         'sell_date' : df_daily.iloc[row_index+1]['trade_date'], \
                    #                         'sell_price' : df_daily.iloc[row_index+1]['open'], \
                    #                         'ts_code' : ts_code[0], \
                    #                         'buy_date_change' : row_value[8]})
                    # print(s)
                    # df_trade_history._append(s,ignore_index = True)
                    if len(df_trade_history) > 5000:
                        df_trade_history.to_csv(detail_filename, mode='a',
                                                header=True if not os.path.exists(detail_filename) else False,
                                                index=False)
                        df_trade_history = df_trade_history.drop(index=df_trade_history.index)


                    print('trade history---sell record------:\n', row_value)

                    df_trade_history = df_trade_history._append({'profit_change': profit * 100 / df_daily.iloc[buy_index]['close'], \
                                                                 'profit': profit, \
                                                                 'buy_date': df_daily.iloc[buy_index]['trade_date'], \
                                                                 'buy_price': df_daily.iloc[buy_index]['close'], \
                                                                 'sell_date': df_daily.iloc[row_index]['trade_date'], \
                                                                 'sell_price': df_daily.iloc[row_index]['close'], \
                                                                 'ts_code': ts_code[0]},
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
                 'CONTINUE_LOW_VOLUME_DAY_COUNT': CONTINUE_LOW_VOLUME_DAY_COUNT, \
                 'DAY_COUNT_OF_INSPECTION': DAY_COUNT_OF_INSPECTION, \
                 'TIMES_OF_BUY': TIMES_OF_BUY, \
                 'TIMES_OF_SELL': TIMES_OF_SELL}, ignore_index=True)

            # print(df_trade_history)
            print(f'''total_profit is {total_profit} total_profit_change is {total_profit_change}  with ts_code={ts_code} [TIMES_OF_BUY, TIMES_OF_SELL] = [{TIMES_OF_BUY}, {TIMES_OF_SELL}] \n''')
            #
            #     # if( row_value[8] < -9.5 ):
            #     if (row_value['pct_chg'] > MIN_CHANGE and row_value['pct_chg'] < MAX_CHANGE):
            #         if ((MAX_CHANGE == -9) or (MIN_CHANGE == 9)):
            #             if (row_value['open'] == row_value['close']): # 剔除了开盘就涨停的情况，TODO:判断不够精确
            #                 print(f'''{row_value['trade_date']}  cannot buy, maybe zhangting because open == close''')
            #                 continue
            #             if (row_value['vol'] * row_value['close'] < 1000000): #判断成交量太低的情况，这种情况没有交易意义
            #                 print(f'成交量太低了，无法买入 row_value = {row_value}')
            #                 continue
            #             # 需要判断尾盘是涨停价的情况，此种情况在收盘的最后几分钟无法成交。我们引入了未来函数，
            #             # 我们是在盘中买入了收盘时涨停的股票，如果在盘中就买入，那么应该会面临打开涨停的亏损。
            #
            #             if MAX_CHANGE >= 9:
            #                 if math.isclose(row_value['close'], float(cal_zhangting(row_value['pre_close']))):
            #                     print(f'''下面的交易是完成不了的，涨停了：今收：{row_value['close']} 昨收：{row_value['pre_close']}''')
            #                     continue
            #
            #                 if row_value['close'] > float(cal_zhangting(row_value['pre_close'])):
            #                     print("\033[0;31;40m", f'''收盘价大于涨停价，什么鬼：{cal_zhangting(row_value['pre_close'])} < {row_value['close']}''', \
            #                           "\033[0m")
            #                     print(row_value)
            #                     if (row_value['pct_chg'] > 10):
            #                         continue
            #                         sys.exit()
            #                     continue
            #             # if ( row_value['close'] == row_value[] ):
            #             #     continue
            #
            #
            #
            #

            print("-" * 10, f'''end of analyze: {ts_code[0]}''', "-" * 10, "\n\n")

        df_trade_history.to_csv(detail_filename, mode='a', header=True if not os.path.exists(detail_filename) else False, index=False)
        df_trade_total.to_csv(total_filename, mode='a', header=True if not os.path.exists(total_filename) else False, index=False)

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    pymysql.install_as_MySQLdb()

    # 实验方法：在成交量连续N日位于最近M天的地量时，买入；在成交量放大到月成交量的X倍且盈利时，卖出；止损设置为下跌10%；
    #          其中各个参数的设定，先取绝对值，后基于个股最近一年的特征做参数优化。

    CONTINUE_LOW_VOLUME_DAY_COUNT = 1
    DAY_COUNT_OF_INSPECTION = 30
    TIMES_OF_BUY = 3
    TIMES_OF_SELL = 3

    volume_analizer((0,10000), CONTINUE_LOW_VOLUME_DAY_COUNT, DAY_COUNT_OF_INSPECTION, TIMES_OF_BUY, TIMES_OF_SELL)

    print("program is exiting.")
    exit(0)
    print("can not reach!!!!!!!!")






B_CONF_CLOSE_EQUAL_HIGH = FALSE


#涨停密集的交易日，是否追涨策略更容易成功？分析方法：累计每日的追涨策略盈利比，看与交易次数是否正相关
def detail_analyzer_mijizhangting():
    detail_filename = '追涨分析_9_11_after_2023_detail.csv'
    df_result = pd.DataFrame(None, columns=['buy_date', 'buy_count', 'total_profit_change', 'avg_profit'])

    try:
        df_detail = pd.read_csv(detail_filename)
    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    # print(df_detail)
    print(df_detail.groupby('buy_date').size())
    print(df_detail.groupby('buy_date').count())

    for date_gr, gr in df_detail.groupby('buy_date'):
        # print(gr, f'type={type(gr)}', f'len={len(gr)}')

        total_profit_change = 0
        for row_index, row_value in gr.iterrows():
            total_profit_change += row_value['profit_change']

        df_result = df_result._append({'buy_date': date_gr, \
                                        'buy_count': len(gr),\
                                        'total_profit_change': total_profit_change, \
                                        'avg_profit': total_profit_change/len(gr)}, \
                                        ignore_index = True)

    df_result = df_result.sort_values('avg_profit', ascending=False)

    df_result_profit = df_result[df_result['avg_profit'] > 0.5]

    pd.set_option('display.width', 1000)  # 设置字符显示宽度
    pd.set_option('display.max_rows', None)  # 设置显示最大行
    pd.set_option('display.max_columns', 200)  # 设置显示最大行

    print(df_result)

    print(f'len(df_result_profit) = {len(df_result_profit)} df_result_profit =: \n {df_result_profit}')


from decimal import Decimal
import math
def cal_zhangting(pre_close):

    if pre_close == 0:
        return 0


    pre_close = float(pre_close) * 1.1
    print(pre_close)

    if isinstance(pre_close, float):
        pre_close = str(pre_close)

    limit = Decimal(pre_close).quantize(Decimal("0.00"), rounding="ROUND_HALF_UP")
    print(limit)

    #
    # limit = pre_close + pre_close * 0.1
    # limit = '%.2f' % limit
    #
    # print(f'''limit = {limit}''')

    return limit

