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
def zhuizhang_analizer(start_index):
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

        sql_text = text(f''' select * from daily where ts_code=\'{all_data__ts_codes[0][0]}\' ''')
        print(sql_text)

        # has_reach_last_point = False
        analyze_single_stock = False  # 分析单个股票的情况
        save_analyze_result = False  # 将分析结果保存到“追涨分析”文件里

        current_index = 0

        df_trade_history = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date',
                                                       'sell_price', 'ts_code', 'buy_date_change'])
        df_trade_total = pd.DataFrame(None, columns=['total_profit_change', 'total_profit', 'ts_code', 'trace_count',
                                                     'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])
        for ts_code in all_data__ts_codes:

            MIN_CHANGE = 5
            MAX_CHANGE = 9

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
            sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' limit 10000''')
            result = conn.execute(sql_text)

            print('========== select * from daily result:==========')
            all_data = result.fetchall()
            print(all_data)

            all_data_format = np.array(all_data)

            print('length of result:', len(all_data))

            if len(all_data) < 3 : # 跳过新股，不然会index out of range
                continue

            # print(all_data[1])
            #
            # print(all_data[1][2])

            print(all_data_format)

            # print(all_data_format[1])
            # print(all_data_format[1][1])


            print('--------end of ', sql_text)

            print('========== dataframe :==========')

            # dataframe的用法：https: // blog.csdn.net / Parzival_ / article / details / 114240650

            df_daily = pd.DataFrame(list(all_data))
            print(df_daily)
            print(df_daily.columns)

            print("===iter elments in df_daily:===")
            i = 0
            # curIndex = 0
            total_profit = 0
            total_profit_change = 0

            detail_filename = '追涨分析'+str(start_index[0])+'_detail.csv'
            total_filename = f'追涨分析{start_index[0]}_total.csv'




            for row_index, row_value in df_daily.iterrows():
                # if( row_value[8] < -9.5 ):
                if (row_value['pct_chg'] > MIN_CHANGE and row_value['pct_chg'] < MAX_CHANGE):
                    i = i + 1
                    print("+" * 5, f''' this is {i}td elements.''')
                    print(f'''    trade_date is {row_value['trade_date']}''')
                    print(f'''    row_index is {row_index} ; row_value is:\n{row_value} ''')
                    if row_index < len(df_daily) - 2 :
                        print(f''' the next daily is:\n{df_daily.iloc[row_index+1]}''')
                        print(f'''   buy:{row_value['close']} sell:{df_daily.iloc[row_index+1]['open']}  ''')
                        print(f'''   profit: {df_daily.iloc[row_index + 1]['open'] - row_value['close']}''')
                        total_profit += df_daily.iloc[row_index + 1]['open'] - row_value['close']
                        total_profit_change += ((df_daily.iloc[row_index + 1]['open'] - row_value['close']) * 100/ row_value['close'])

                        # s = pd.Series({'profit' : df_daily.iloc[row_index + 1]['open'] - row_value['close'], \
                        #                         'buy_date' : row_value['trade_date'], \
                        #                         'buy_price' : row_value['close'],\
                        #                         'sell_date' : df_daily.iloc[row_index+1]['trade_date'], \
                        #                         'sell_price' : df_daily.iloc[row_index+1]['open'], \
                        #                         'ts_code' : ts_code[0], \
                        #                         'buy_date_change' : row_value[8]})
                        # print(s)
                        # df_trade_history._append(s,ignore_index = True)
                        df_trade_history = df_trade_history._append({'profit_change': ((df_daily.iloc[row_index + 1]['open'] - row_value['close']) * 100/ row_value['close']), \
                                                'profit' : df_daily.iloc[row_index + 1]['open'] - row_value['close'], \
                                                'buy_date' : row_value['trade_date'], \
                                                'buy_price' : row_value['close'],\
                                                'sell_date' : df_daily.iloc[row_index+1]['trade_date'], \
                                                'sell_price' : df_daily.iloc[row_index+1]['open'], \
                                                'ts_code' : ts_code[0], \
                                                'buy_date_change' : row_value['pct_chg']}, ignore_index = True)

                    print("-" * 5, f''' end of this is {i}td elements.\n''')
                #     print(f'curIndex = {curIndex}')
                #     print(f'''curIndex = {curIndex} , the element is: {df_daily[curIndex]['trade_date']}''')
                # curIndex += 1


            print('-----end iter elements in df_daily')
            df_trade_total = df_trade_total._append(
                {'total_profit_change': total_profit_change, \
                 'total_profit': total_profit, \
                 'ts_code': ts_code[0], \
                 'begin_date': df_daily.iloc[0]['trade_date'], \
                 'end_date': df_daily.iloc[-1]['trade_date'], \
                 'MIN_CHANGE': MIN_CHANGE, \
                 'MAX_CHANGE': MAX_CHANGE}, ignore_index=True)

            print(df_trade_history)
            print(f'''total_profit is {total_profit} total_profit_change is {total_profit_change}  with ts_code={ts_code} [MIN_CHANGE, MAX_CHANGE] = [{MIN_CHANGE}, {MAX_CHANGE}] \n''')

            if save_analyze_result:
                with open(f'追涨分析', 'a+') as my_file:
                    my_file.write(f'''total_profit is {total_profit}  with ts_code={ts_code} [MIN_CHANGE, MAX_CHANGE] = [{MIN_CHANGE}, {MAX_CHANGE}] \n''')
                    # my_file.seek(0)
                    # print(my_file.read())
                    my_file.close()

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

        df_trade_history.to_csv(detail_filename, index=False)
        df_trade_total.to_csv(total_filename, index=False)

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()
def merge_files():

    detail_merge_filename = '追涨分析_detail_5_9.xlsx'
    total_merge_filename = '追涨分析_total_5_9.xlsx'

    df_merge = df_ori = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date', \
                                                    'sell_price', 'ts_code', 'buy_date_change', 'is_total'])
    df_total_merge = df_total_ori = pd.DataFrame(None, columns=['total_profit_change', 'total_profit', 'ts_code',
                                                                'trace_count',
                                                                'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])

    for i in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, 3000), (3000, 3500), (3500, 4000), \
              (4000, 4500), (4500, 5000), (5000, 6000)):



        detail_filename = '追涨分析' + str(i[0]) + '_detail.xlsx'
        total_filename = f'追涨分析{i[0]}_total.xlsx'

        print(f'''begein process{detail_filename} and {total_filename}''')

        try:
            df_ori = pd.read_excel(detail_filename)
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
        df_merge = df_merge._append(df_ori, ignore_index=True)

        try:
            df_total_ori = pd.read_excel(total_filename)
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
        df_total_merge = df_total_merge._append(df_total_ori, ignore_index=True)

    print(f'''begin save file''')
    try:
        df_merge.to_csv(detail_merge_filename)
        df_total_merge.to_csv(total_merge_filename)
    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

pymysql.install_as_MySQLdb()


# merge_files()
# sys.exit()

# for i in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, 3000), (3000, 3500), (3500, 4000), \
#           (4000, 4500), (4500, 5000), (5000, 6000)):
#     zhuizhang_analizer1 = threading.Thread(target = zhuizhang_analizer, args=(i, ))
#     zhuizhang_analizer1.start()

zhuizhang_analizer((0, 10000))


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
