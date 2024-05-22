
import pandas as pd
from pandas import Series
import numpy as np


def change_rankings(start_date='20230522', end_date='20240522'):
    sql_query_flatten_file_name = 'D:/不要删除牛爸爸的程序/量价策略/数据挖掘/sql_query_flatten.csv'
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
    print('result : \n', df_max_min)


    return df_all.loc[start_date:end_date, ]

if __name__ == '__main__':
    change_rankings()