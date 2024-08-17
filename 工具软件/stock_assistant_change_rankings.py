import os

import pandas as pd
import pymysql
from pandas import Series
import numpy as np
import datetime
import sys

from sqlalchemy import create_engine, text

sys.path.append('D:/不要删除牛爸爸的程序/') # 绝对路径
from __utils import messagebox, kline

def change_rankings(start_date='20230522', end_date='20240522'):
    print(f'change_rankings par：start_date={start_date}, end_date={end_date}')
    sql_query_flatten_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_flatten.csv'
    df_all = pd.read_csv(sql_query_flatten_file_name, skiprows= 0*200, nrows=10000, index_col=0)
    # df_all = pd.read_csv(sql_query_flatten_file_name, skiprows=0 * 200, nrows=100)

    # df_all.set_index('trade_date', inplace=True)
    # pd.options.display.max_rows = None
    # # print('未按日期排序前的N个股票报价：\n', df_all)
    # df_all.sort_index(inplace=True)
    #
    # df_all.to_csv('D:/不要删除牛爸爸的程序/量价策略/数据挖掘/sql_query_flatten_tmp.csv')
    # print(df_all)
    df_all = df_all.loc[start_date:end_date, ]
    print(f'日期介于【{start_date},{end_date}】，查询到的表格为：\n', df_all)
    df_last = df_all.tail(1)
    print('查询到的表格的最后一行为：\n', df_last)
    df_max = pd.DataFrame(df_all.max())
    df_max = df_max.T
    print('查询到的表格的max统计结果为：\n', df_max)
    df_min = pd.DataFrame(df_all.min())
    df_min = df_min.T
    print('查询到的表格的min统计结果为：\n', df_min)

    df_max_min = pd.concat([df_max, df_min, df_last])

    df_max_min.index = Series(['max', 'min', df_last.index[0]])
    # df_max_min = df_max_min.dropna(axis='columns')
    print('查询到的表格的max and min：\n', df_max_min)

    # df_div = np.array(df_max_min.loc['max':'max',:]) / np.array(df_max_min.loc['min':'min',:])
    #
    # print('查询到的表格的max and min single line：\n', df_max_min.loc['max':'max', :], '\n', df_max_min.loc['min':'min',:])
    # print(f'df_div=:\n{df_div}')

    for cur_column in df_max_min.columns:
        # print(f'processing: cur_column={cur_column}')
        cur_column_last_price = df_max_min.loc[df_last.index[0], cur_column]
        # print(cur_column_last_price)
        cur_column_max_price = df_max_min.loc['max', cur_column]
        # print(f'cur_column_max_price={cur_column_max_price}')
        cur_column_min_price = df_max_min.loc['min', cur_column]
        # if np.isnan(cur_column_max_price) or np.isnan(cur_column_last_price):
        #     print(cur_column, 'has nan')
        #     continue
        # print(f'cur_column_min_price={cur_column_min_price}')
        chg_from_max = (cur_column_last_price - cur_column_max_price) / cur_column_max_price
        # print(f'chg_from_max={chg_from_max}')
        df_max_min.loc['chg_from_max', cur_column] = chg_from_max

    print('result : \n', df_max_min)
    df_max_min.sort_values(by='chg_from_max', axis=1, ascending=True, inplace=True)
    pd.options.display.max_rows = None
    print('change_rankings top 100 results : \n', df_max_min.T.head(100))

    return df_max_min.T

def update_basic_data():
    pymysql.install_as_MySQLdb()
    try:
        sql_query_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_all.csv'
        sql_query_flatten_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_flatten.csv'

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

        if not os.path.exists(sql_query_file_name):
            print('开始查询数据库：select ts_code, trade_date, close from daily')
            # sql_text = text(f'''select ts_code, trade_date, close from daily where ts_code like \'000______\' and trade_date like \'2023____\' limit 10000000''')
            sql_text = text(f'''select ts_code, trade_date, close from daily''')
            result = conn.execute(sql_text)
            all_data = result.fetchall()
            df_daily = pd.DataFrame(list(all_data))
            df_daily = df_daily[['ts_code', 'trade_date', 'close']]
            df_daily.to_csv(sql_query_file_name)
        else:
            df_daily = pd.read_csv(sql_query_file_name, index_col=0)
        print('从数据库中查询到的表格为：\n', df_daily)

        df_all = pd.DataFrame(None, columns=['trade_date'])
        if not os.path.exists(sql_query_flatten_file_name):
            print('开始拍平数据库查询结果')
            for ts_code in all_data__ts_codes:
                tmp_df = df_daily[df_daily['ts_code'] == ts_code[0]]
                # 新股还是别分析趋势了
                if len(tmp_df) < 200:
                    continue
                tmp_df = tmp_df[['trade_date', 'close']]
                tmp_df.rename(columns={'close': str(ts_code[0])}, inplace=True)
                df_all = pd.merge(df_all, tmp_df, on='trade_date', how='outer')
                print('\t processing: ', ts_code)

            df_all.set_index('trade_date', inplace=True)
            # print('未按日期排序前的N个股票报价：\n', df_all)
            df_all.sort_index(inplace=True)

            df_all.to_csv(sql_query_flatten_file_name)
        else:
            df_all = pd.read_csv(sql_query_flatten_file_name, index_col=0)

        print('拍平后的表格为：\n', df_all)

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # 删除sql_query_all.csv和sql_query_flatten.csv,可以触发数据更新。
    update_basic_data()
    start_date = str((datetime.datetime.now().date() - datetime.timedelta(365)).strftime("%Y%m%d"))
    end_date = str(datetime.datetime.now().date().strftime("%Y%m%d"))
    df_change_rankings = change_rankings(start_date, end_date)

    list_change_rankings = list(df_change_rankings.head(5).index)
    print(f'most change stocks between {start_date} and {end_date} ：', list_change_rankings)

    # kline.show_k_lines(list_change_rankings)
    kline.show_k_lines(list_change_rankings, start_date, end_date)

