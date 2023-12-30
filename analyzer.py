from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import numpy as np
import pandas as pd
import mplfinance as mpl
import pysnooper

detail_filename = './追涨分析/追涨分析_detail_5_9.xlsx'



# detail_filename = './追涨分析/追涨分析_total_5_9.xlsx'

# try:
#     df_ori = pd.read_excel(detail_filename)
# except Exception as e:
#     print("\033[0;31;40m", e, "\033[0m")
#
# detail_filename = './追涨分析/追涨分析_detail_5_9.csv'
# df_ori.to_csv(detail_filename, index=False)


detail_filename = './追涨分析/追涨分析_detail_5_9.csv'
df_ori = pd.read_csv(detail_filename)

print(df_ori)