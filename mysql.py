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

B_CONF_CLOSE_EQUAL_HIGH = True


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


# @pysnooper.snoop()
def zhuizhang_analizer(start_index, MIN_CHANGE, MAX_CHANGE):
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
        save_analyze_result = False  # 将分析结果保存到“追涨分析”文件里

        current_index = 0

        df_trade_history = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date',
                                                       'sell_price', 'ts_code', 'buy_date_change'])
        df_trade_total = pd.DataFrame(None, columns=['total_profit_change', 'win_percent', 'total_profit', 'ts_code',
                                                     'trade_count', 'profit_trade_count',
                                                     'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])

        # detail_filename = '追涨分析' + str(start_index[0]) + '_detail.csv'
        # total_filename = f'追涨分析{start_index[0]}_total.csv'
        detail_filename = f'追涨分析_{MIN_CHANGE}_{MAX_CHANGE}_highestprice{B_CONF_CLOSE_EQUAL_HIGH}_detail.csv'
        total_filename = f'追涨分析_{MIN_CHANGE}_{MAX_CHANGE}_highestprice{B_CONF_CLOSE_EQUAL_HIGH}_total.csv'

        for ts_code in all_data__ts_codes:

            # if not has_reach_last_point :
            #     if ts_code[0] == '603107.SH' :
            #         has_reach_last_point = True
            #         continue
            #     continue


            if (current_index < start_index[0] or current_index >= start_index[1]):
                current_index += 1
                continue
            current_index += 1

            if analyze_single_stock :
                if not (ts_code[0] == '688536.SH'):
                    continue

            print("+"*10, f'''begin analyze: {ts_code[0]}''', "+"*10)

            # sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' and trade_date like \'2023____\' limit 10000''')

            sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' limit 10000''')

            # sql_text = text(f''' select * from daily limit 16300000 ''')

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

            if len(all_data) < 3 : # 跳过新股，不然会index out of range
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

            for row_index, row_value in df_daily.iterrows():

                if B_CONF_CLOSE_EQUAL_HIGH:
                    if row_value['close'] != row_value['high']:
                        continue

                # if( row_value[8] < -9.5 ):
                if (row_value['pct_chg'] > MIN_CHANGE and row_value['pct_chg'] < MAX_CHANGE):
                    if ((MAX_CHANGE == -9) or (MIN_CHANGE == 9)):
                        if (row_value['open'] == row_value['close']): # 剔除了开盘就涨停的情况，TODO:判断不够精确
                            print(f'''{row_value['trade_date']}  cannot buy, maybe zhangting because open == close''')
                            continue
                        if (row_value['vol'] * row_value['close'] < 1000000): #判断成交量太低的情况，这种情况没有交易意义
                            print(f'成交量太低了，无法买入 row_value = {row_value}')
                            continue
                        # 需要判断尾盘是涨停价的情况，此种情况在收盘的最后几分钟无法成交。我们引入了未来函数，
                        # 我们是在盘中买入了收盘时涨停的股票，如果在盘中就买入，那么应该会面临打开涨停的亏损。

                        if MAX_CHANGE >= 9:
                            if math.isclose(row_value['close'], float(cal_zhangting(row_value['pre_close']))):
                                print(f'''下面的交易是完成不了的，涨停了：今收：{row_value['close']} 昨收：{row_value['pre_close']}''')
                                continue

                            if row_value['close'] > float(cal_zhangting(row_value['pre_close'])):
                                print("\033[0;31;40m", f'''收盘价大于涨停价，什么鬼：{cal_zhangting(row_value['pre_close'])} < {row_value['close']}''', \
                                      "\033[0m")
                                print(row_value)
                                if (row_value['pct_chg'] > 10):
                                    continue
                                    sys.exit()
                                continue
                        # if ( row_value['close'] == row_value[] ):
                        #     continue




                    # print("+" * 5, f''' this is {i}td elements.''')
                    # print(f'''    trade_date is {row_value['trade_date']}''')
                    # print(f'''    row_index is {row_index} ; row_value is:\n{row_value} ''')

                    if row_index < len(df_daily) - 2 :
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
                        if len(df_trade_history) > 5000:
                            df_trade_history.to_csv(detail_filename, mode='a', header=True if not os.path.exists(detail_filename) else False,
                                                    index=False)
                            df_trade_history = df_trade_history.drop(index=df_trade_history.index)

                        print('trade history:\n', row_value)

                        df_trade_history = df_trade_history._append({'profit_change': profit * 100/ row_value['close'], \
                                                'profit' : profit, \
                                                'buy_date' : row_value['trade_date'], \
                                                'buy_price' : row_value['close'],\
                                                'sell_date' : df_daily.iloc[row_index+1]['trade_date'], \
                                                'sell_price' : df_daily.iloc[row_index+1]['open'], \
                                                'ts_code' : ts_code[0], \
                                                'buy_date_change' : row_value['pct_chg']}, ignore_index = True)

                    # print("-" * 5, f''' end of this is {i}td elements.\n''')
                #     print(f'curIndex = {curIndex}')
                #     print(f'''curIndex = {curIndex} , the element is: {df_daily[curIndex]['trade_date']}''')
                # curIndex += 1


            # print('-----end iter elements in df_daily')
            df_trade_total = df_trade_total._append(
                {'total_profit_change': total_profit_change, \
                 'win_percent':  profit_count * 100 / trade_count if trade_count > 0 else 0, \
                 'total_profit': total_profit, \
                 'ts_code': ts_code[0], \
                 'trade_count': trade_count, \
                 'profit_trade_count': profit_count, \
                 'begin_date': df_daily.iloc[0]['trade_date'], \
                 'end_date': df_daily.iloc[-1]['trade_date'], \
                 'MIN_CHANGE': MIN_CHANGE, \
                 'MAX_CHANGE': MAX_CHANGE}, ignore_index=True)

            # print(df_trade_history)
            print(f'''total_profit is {total_profit} total_profit_change is {total_profit_change}  with ts_code={ts_code} [MIN_CHANGE, MAX_CHANGE] = [{MIN_CHANGE}, {MAX_CHANGE}] \n''')


            if False :
                del df_daily['amount']
                del df_daily['pct_chg']
                del df_daily['_change']
                del df_daily['pre_close']
                del df_daily['ts_code']

                df_daily.index = pd.DatetimeIndex(df_daily['trade_date'])
                del df_daily['trade_date']

                df_daily.columns=['open', 'high', 'low', 'close', 'volume']

                # print(df_daily.columns)
                # print(df_daily)

                mpl.plot(df_daily, type='line', mav=(3, 6, 9), volume=True, axtitle=ts_code[0])

                # mpl.plot(df_daily, type='candle',mav=(3,6,9), volume=True)

            # df_ori = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date', \
            #                                              'sell_price', 'ts_code', 'buy_date_change', 'is_total'])
            # try:
            #     df_ori = pd.read_csv(detail_filename)
            # except Exception as e:
            #     print("\033[0;31;40m", e, "\033[0m")
            # df_ori = df_ori._append(df_trade_history, ignore_index=True)
            # df_ori.to_csv(detail_filename, index=False)
            #
            # df_total_ori = pd.DataFrame(None, columns=['total_profit_change', 'total_profit', 'ts_code', 'trade_count',
            #                                            'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])
            # try:
            #     df_total_ori = pd.read_csv(total_filename)
            # except Exception as e:
            #     print("\033[0;31;40m", e, "\033[0m")
            # df_total_ori = df_total_ori._append(df_trade_total, ignore_index=True)
            # df_total_ori.to_csv(total_filename, index=False)

            print("-" * 10, f'''end of analyze: {ts_code[0]}''', "-" * 10, "\n\n")

        df_trade_history.to_csv(detail_filename, mode='a', header=True if not os.path.exists(detail_filename) else False, index=False)
        df_trade_total.to_csv(total_filename, mode='a', header=True if not os.path.exists(total_filename) else False, index=False)

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()


# def merge_files():
#
#     detail_merge_filename = '追涨分析_detail_5_9.xlsx'
#     total_merge_filename = '追涨分析_total_5_9.xlsx'
#
#     df_merge = df_ori = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date', \
#                                                     'sell_price', 'ts_code', 'buy_date_change', 'is_total'])
#     df_total_merge = df_total_ori = pd.DataFrame(None, columns=['total_profit_change', 'total_profit', 'ts_code',
#                                                                 'trace_count',
#                                                                 'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])
#
#     for i in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, 3000), (3000, 3500), (3500, 4000), \
#               (4000, 4500), (4500, 5000), (5000, 6000)):
#
#
#
#         detail_filename = '追涨分析' + str(i[0]) + '_detail.xlsx'
#         total_filename = f'追涨分析{i[0]}_total.xlsx'
#
#         print(f'''begein process{detail_filename} and {total_filename}''')
#
#         try:
#             df_ori = pd.read_excel(detail_filename)
#         except Exception as e:
#             print("\033[0;31;40m", e, "\033[0m")
#         df_merge = df_merge._append(df_ori, ignore_index=True)
#
#         try:
#             df_total_ori = pd.read_excel(total_filename)
#         except Exception as e:
#             print("\033[0;31;40m", e, "\033[0m")
#         df_total_merge = df_total_merge._append(df_total_ori, ignore_index=True)
#
#     print(f'''begin save file''')
#     try:
#         df_merge.to_csv(detail_merge_filename)
#         df_total_merge.to_csv(total_merge_filename)
#     except Exception as e:
#         print("\033[0;31;40m", e, "\033[0m")

pymysql.install_as_MySQLdb()


# merge_files()
# sys.exit()

# for i in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, 3000), (3000, 3500), (3500, 4000), \
#           (4000, 4500), (4500, 5000), (5000, 6000)):
#     zhuizhang_analizer1 = threading.Thread(target = zhuizhang_analizer, args=(i, ))
#     zhuizhang_analizer1.start()


# zhuizhang_analizer((0, 10000), 1, 2)
# zhuizhang_analizer((0, 10000), -2, -1)
# zhuizhang_analizer((0, 10000), -3, -2)
# zhuizhang_analizer((0, 10000), -4, -3)
# zhuizhang_analizer((0, 10000), -5, -4)
# zhuizhang_analizer((0, 10000), -6, -5)
# zhuizhang_analizer((0, 10000), -7, -6)
# zhuizhang_analizer((0, 10000), -8, -7)
# zhuizhang_analizer((0, 10000), -9, -8)
# sys.exit()
# zhuizhang_analizer((0, 10000), 9, 11)
# zhuizhang_analizer((0, 10000), 9, 11)
# zhuizhang_analizer((0, 10000), 3, 4)
zhuizhang_analizer((0, 10000), 2, 3)

# detail_analyzer_mijizhangting()



# # 将dataframe 添加到 tmp_formidinfo 如果表存在就添加，不存在创建并添加
# # pd.io.sql.to_sql(name='table_formidinfo', con=engine, schema='max_overflow', if_exists='append')
#
# # 执行sql语句
# try:
#     # 获取元数据
#     metadata = MetaData()
#     # 定义表
#     user = Table('user', metadata,
#                  Column('id', Integer, primary_key=True),
#                  Column('name', String(20)),
#                  )
#
#     color = Table('color', metadata,
#                   Column('id', Integer, primary_key=True),
#                   Column('name', String(20)),
#                   )
#
#     user.create(engine)
#     conn.execute(
#         text("INSERT INTO user(id, name) VALUES ('1', 'niuniu');")
#     )
# except Exception as e:
#     print("\033[0;31;40m", e, "\033[0m")


import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

# ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')
# engine_ts = create_engine('mysql://root:mysql123@127.0.0.1:3306/demos?charset=utf8&use_unicode=1')
#
# def read_data():
#     sql = """SELECT * FROM stock_basic LIMIT 20"""
#     df = pd.read_sql_query(sql, engine_ts)
#     return df
#
#
# def write_data(df):
#     res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)
#     print(res)
#
#
# def get_data():
#     pro = ts.pro_api()
#     df = pro.stock_basic()
#     print(df)
#     return df
#
#
# if __name__ == '__main__':
# #     df = read_data()
#     df = get_data()
#     write_data(df)
#     print(df)
