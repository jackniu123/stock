# https://blog.csdn.net/xiaomingxiansen/article/details/78686067
# https://blog.csdn.net/CSDN_fzs/article/details/118018817
import os.path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts
import sys
sys.path.append('D:/不要删除牛爸爸的程序/') # 绝对路径
from __utils import messagebox
from __utils.kline import show_k_lines, get_name_by_code

def sample():
    s_qjd = '002186.SZ'
    s_gm = '600597.SH'
    sdate = '20160101'
    edate = '20161231'
    # df_qjd = ts.get_h_data(s_qjd, start=sdate, end=edate).sort_index(axis=0, ascending=True)
    # df_gm = ts.get_h_data(s_gm, start=sdate, end=edate).sort_index(axis=0, ascending=True)

    ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')
    pro = ts.pro_api()

    df_qjd = pro.daily(ts_code=s_qjd, start_date=sdate, end_date=edate)
    df_gm = pro.daily(ts_code=s_gm, start_date=sdate, end_date=edate)

    df_qjd = df_qjd.sort_values(by="trade_date", ascending=True)
    df_gm = df_gm.sort_values(by="trade_date", ascending=True)

    print('全聚德的股价历史：')
    print(df_qjd[['trade_date', 'close']])
    print('光明乳业的股价历史：')
    print(df_gm[['trade_date', 'close']])

    # df = pd.concat([df_qjd.close, df_gm.close, df_qjd.trade_date], axis=1, keys=['qjd_close', 'gm_close', 'trade_date'], ignore_index=True)
    df = pd.merge(df_qjd, df_gm, on='trade_date', how='outer')


    print('合并后的空值的行和列：\n', df[df.isnull().T.any()])

    df.ffill(axis=0, inplace=True)
    df.to_csv('qjd_gm.csv')
    df = df[['trade_date', 'close_x', 'close_y']]
    print('合并后的DF：\n', df)

    corr = df.corr(method='pearson', min_periods=1)

    print('pearson 相关矩阵：\n', corr)

    df.plot(figsize=(20, 12))
    plt.savefig('qjd_gm.jpg')
    plt.close()

    df['qjd_one'] = df.close_x / float(df.close_x[0]) * 100
    df['gm_one'] = df.close_y / float(df.close_y[0]) * 100
    df.qjd_one.plot(figsize=(20, 12))
    df.gm_one.plot(figsize=(20, 12))
    plt.savefig('qjd_gm_one.jpg')


from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql


def correlation_analizer():
    pymysql.install_as_MySQLdb()
    try:
        sql_query_file_name = 'sql_query_all.csv'
        sql_query_flatten_file_name = 'sql_query_flatten.csv'
        corr_file_name = 'correlation_analysis.csv'

        # sql_query_file_name = 'tmp_sql_query_all.csv'
        # sql_query_flatten_file_name = 'tmp_sql_query_flatten.csv'
        # corr_file_name = 'tmp_correlation_analysis.csv'

        df_daily = pd.DataFrame()

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
            sql_text = text(f'''select ts_code, trade_date, close from daily where ts_code like \'000______\' and trade_date like \'2023____\' limit 10000000''')
            # sql_text = text(f'''select ts_code, trade_date, close from daily''')
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

        del df_all['trade_date']
        print('拍平后的表格空值行为：\n', df_all[df_all.isnull().T.any()])
        df_all.ffill(axis=0, inplace=True)
        print('拍平后的表格填充后为：\n', df_all[df_all.isnull().T.any()])

        print('开始计算相关性矩阵')
        corr = df_all.corr(method='pearson', min_periods=1)
        print('pearson 相关矩阵：\n', corr)
        corr.to_csv(corr_file_name)

        if len(df_all) < 20:
            print('开始生成股价曲线图')
            df_all.plot(figsize=(20, 12))
            plt.savefig('corelation_analysis.jpg')
            plt.close()

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()
def sort_correlation():
    if os.path.exists('correlation_analysis.csv'):
        corr = pd.read_csv('correlation_analysis.csv', nrows=20000, index_col=0)
        corr.replace(1, 0, inplace=True)
        print('got correlation data:\n', corr)
        print(corr.idxmin())
        print(corr.min())

        # corrid = pd.merge(pd.DataFrame(corr.idxmax()), pd.DataFrame(corr.max()), how='outer')

        corrid = corr.idxmin()
        for row, value in corrid.items():
            # print(row)
            # print('value:', value)
            # print(row)
            code_name = get_name_by_code(row)

            if len(code_name) > 0:
                corrid.rename(index={row:code_name}, inplace=True)
                corrid.replace(row, code_name, inplace=True)
        print(corrid)

def get_max_min_by_code(stock_code:str, topN = 3):
    if len(stock_code) < 6:
        print(f'!!!! error: stock_code is ivalid: {stock_code}')
        return
    else:
        stock_code = stock_code[0:6]

    if os.path.exists('correlation_analysis.csv'):
        corr = pd.read_csv('correlation_analysis.csv', nrows=7000, index_col=0)
        corr.replace(1, 0, inplace=True)

        max_min_list = []
        for row, value in corr.items():
            if row.startswith(stock_code):
                value_sorted = value.sort_values(ascending=False)
                print(value_sorted)
                max_min_list.append(row)
                for i in range(topN):
                    max_min_list.insert(i, value_sorted.index[i])
                    max_min_list.append(value_sorted.index[-topN+i])
                break
        print(max_min_list)
    return max_min_list


if __name__ == '__main__':
    pd.options.display.max_columns = 10
    pd.set_option('display.width', 200)
    print('correlation_analysis')

    # correlation_analizer()
    # sort_correlation()

    topN = 10
    max_min_list = get_max_min_by_code('000001', topN)
    for max_min_list_item in max_min_list:
        print(f'{max_min_list_item} :', get_name_by_code(max_min_list_item))
    show_k_lines(max_min_list)
    # show_k_lines(max_min_list[0:topN+1])
    # show_k_lines(max_min_list[topN:topN+1])


    # codes_list = ['000001.SZ', '000002.SH', '000003.SH', '000004.SH']
    # show_k_lines(codes_list)

    messagebox.dump()

