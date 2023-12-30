import sys

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import numpy as np
import pandas as pd
import mplfinance as mpl
import pysnooper



df_zhuizhang_total = pd.read_csv('./追涨分析/追涨分析5_9_total.csv')
df_zhuizhang_total['profit_trade_count_percent'] = np.nan
df_zhuizhang_total['total_trade_count'] = np.nan
df_zhuizhang_total['profit_trade_count'] = np.nan

detail_filename = './追涨分析/追涨分析_detail_5_9.xlsx'



# detail_filename = './追涨分析/追涨分析_total_5_9.xlsx'

# try:
#     df_ori = pd.read_excel(detail_filename)
# except Exception as e:
#     print("\033[0;31;40m", e, "\033[0m")
#
# detail_filename = './追涨分析/追涨分析_detail_5_9.csv'
# df_ori.to_csv(detail_filename, index=False)


detail_filename = './追涨分析/追涨分析5_9_detail.csv'
df_ori = pd.read_csv(detail_filename, nrows=500000)

grouped_df = df_ori.groupby('ts_code')

df_statics = pd.DataFrame(None, columns=['profit_trace_count_percent',
                                         'ts_code',
                                         'total_trade_count',
                                         'profit_trade_count'])

for name, group in grouped_df:
    print(name)
    # print(group)
    total_trade_count = len(group)
    # print(f'------------profit----------')
    profit_group=group[(group['profit_change']>0)]
    # print(profit_group)

    profit_trade_count = len(profit_group)
    profit_trade_count_percent = profit_trade_count * 100.0 / total_trade_count
    # print(profit_trace_count_percent)

    df_statics = df_statics._append({'profit_trace_count_percent' : profit_trade_count_percent, \
                                         'ts_code' : name, \
                                         'total_trade_count' : total_trade_count, \
                                         'profit_trade_count' : profit_trade_count}, ignore_index=True)

    df_zhuizhang_total.loc[df_zhuizhang_total['ts_code']==name, 'profit_trade_count_percent'] = profit_trade_count_percent
    df_zhuizhang_total.loc[df_zhuizhang_total['ts_code']==name, 'total_trade_count'] = total_trade_count
    df_zhuizhang_total.loc[df_zhuizhang_total['ts_code']==name, 'profit_trade_count'] = profit_trade_count

print(df_statics)
df_statics.to_csv('./追涨分析/追涨分析5_9_profit_count.csv', index=False)

print(df_zhuizhang_total)

df_zhuizhang_total.to_csv('./追涨分析/追涨分析5_9_total_with_profit_count.csv', index=False)






print(df_zhuizhang_total)



sys.exit()


# print(df_ori)