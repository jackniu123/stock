import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import numpy as np
import pandas as pd
import mplfinance as mpl



pymysql.install_as_MySQLdb()

# 创建数据库连接
engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)

try:
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

    for ts_code in all_data__ts_codes:
        print("+"*10, f'''begin analyze: {ts_code[0]}''', "+"*10)
        sql_text = text(f''' select * from daily where ts_code=\'{ts_code[0]}\' limit 10000''')
        result = conn.execute(sql_text)

        print('========== select * from daily result:==========')
        all_data = result.fetchall()
        print(all_data)

        all_data_format = np.array(all_data)

        print('length of result:', len(all_data))

        print(all_data[1])

        print(all_data[1][2])

        print(all_data_format)

        print(all_data_format[1])
        print(all_data_format[1][1])


        print('-------------------')

        print('========== dataframe :==========')

        # dataframe的用法：https: // blog.csdn.net / Parzival_ / article / details / 114240650

        df_daily = pd.DataFrame(list(all_data))
        print(df_daily)
        print(df_daily.columns)

        print("===iter elments in df_daily:===")
        i = 0
        # curIndex = 0
        total_profit = 0
        for row_index, row_value in df_daily.iterrows():
            # if( row_value[8] < -9.5 ):
            if (row_value[8] > 5 and row_value[8] < 9):
                i = i + 1
                print("+" * 5, f''' this is {i}td elements.''')
                print(f'''    trade_date is {row_value['trade_date']}''')
                print(f'''    row_index is {row_index} ; row_value is:\n{row_value} ''')
                if row_index < len(df_daily) - 2 :
                    print(f''' the next daily is:\n{df_daily.iloc[row_index+1]}''')
                    print(f'''   buy:{row_value['close']} sell:{df_daily.iloc[row_index+1]['open']}  ''')
                    print(f'''   profit: {df_daily.iloc[row_index + 1]['open'] - row_value['close']}''')
                    total_profit += df_daily.iloc[row_index + 1]['open'] - row_value['close']
                print("-" * 5, f''' end of this is {i}td elements.\n''')
            #     print(f'curIndex = {curIndex}')
            #     print(f'''curIndex = {curIndex} , the element is: {df_daily[curIndex]['trade_date']}''')
            # curIndex += 1
        print('-----end iter elements in df_daily')
        print(f'''total_profit is {total_profit}\n''')

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

        print('-------------------')

        print("-" * 10, f'''end of analyze: {ts_code[0]}''', "-" * 10, "\n\n")







except Exception as e:
    print("\033[0;31;40m", e, "\033[0m")

conn.commit()
conn.close()


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
