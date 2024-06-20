import datetime

import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text, VARCHAR
import akshare as ak
from sqlalchemy.orm import Session


# 执行一条sql语句
def execute_sql(sql='show databases'):
    print('executing... : ', sql)
    engine = create_engine("mysql+pymysql://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
    conn = engine.connect()
    sql_text = text(sql)
    conn.execute(sql_text)
    conn.commit()
    conn.close()


def execute_sql_with_return(sql='show databases'):
    print('executing... : ', sql)
    engine = create_engine("mysql+pymysql://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
    conn = engine.connect()
    sql_text = text(sql)
    result = conn.execute(sql_text).fetchall()
    conn.commit()
    conn.close()
    return result


# 增加数据库的主键
def add_primary_key(table_name='us_daily'):
    execute_sql(f'''alter table {table_name} add constraint pk_stock_daily primary key(date, symbol)''')

# # 删除数据库的主键
def delete_primary_key(table_name='us_daily'):
    execute_sql(f'''alter table {table_name} drop primary key''')


# # 查询数据库中的情况
def check_table_status(table_name='us_daily'):
    print(f'table {table_name} status is: \n', execute_sql_with_return(f'''show table status like \'{table_name}\' '''))


# **********************************数据清洗************************************
''' 参考这里的数据清洗： https://www.heywhale.com/mw/project/5f098536192ac2002c87c5aa
# 2. 查看数据情况

## 1）数据总体情况
print(f'样本量共有 {df.shape[0]} 个')

## 2) 判断是否有重复项
df.duplicated().sum()

## 3) 判断是否有缺失值
df.isnull().sum()

## 4) 查看数据类型
df.dtypes

## 4) 唯一标签值
print(df['朝向'].unique())
print(df['楼层'].unique())
print(df['装修'].unique())
print(df['产权性质'].unique())
print(df['住宅类别'].unique())
print(df['建筑结构'].unique())
print(df['建筑类别'].unique())
print(df['区域'].unique())
print(df['建筑年代'].unique())

初步探索性结果：

去重、缺失值处理
建筑面积、年代、单价需要进行转换（取掉单位）
楼层、区域需要进行数据整合
'''

# 删除重复行, 并将结果存到一个临时表格里。稍后需要执行：
# drop table us_daily;
# rename table tmp_us_daily to us_daily;
def delete_repeat_rows(table_name='us_daily'):
    tmp_table_name = 'tmp_' + table_name
    check_table_status(tmp_table_name)
    execute_sql(f'''insert into {tmp_table_name} select distinct * from {table_name}''')
    print('after delete repeating rows:\n')
    check_table_status(tmp_table_name)


# 删除成交量为0的行，没有意义：
def delete_0_volume_rows(table_name='us_daily'):
    execute_sql(f'''delete from {table_name} where volume < 1''')

# 删除仙股，没法交易：


if __name__ == "__main__":

    # delete_repeat_rows()
    # add_primary_key()
    delete_0_volume_rows()
    exit(0)

    us_daily_file_name = './us_daily/us_daily.csv'
    engine = create_engine("mysql+pymysql://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
    conn = engine.connect()

    need_create_clean_table = False
    if need_create_clean_table:
        df_all = pd.read_csv(us_daily_file_name, nrows=2)
        # df_all['date'] = df_all['date'].astype(datetime.date)
        print(df_all)
        df_all.set_index('date', inplace=True)
        print('data read from csv:\n', df_all)

        try:
            # sql_text = text(f'''drop table us_daily''')
            # conn.execute(sql_text)
            # print(df_all.index.get_level_values('date').str.len().max())
            df_all.to_sql(name='us_daily', con=engine, if_exists='replace',
                          dtype={'date':VARCHAR(df_all.index.get_level_values('date').str.len().max()), 'symbol':VARCHAR(20)})
            sql_text = text(f'''alter table us_daily add constraint pk_stock_daily primary key(date, symbol)''')
            conn.execute(sql_text)

        except Exception as e:
            print(e)

        print('describe us_daily:\n' + str(conn.execute(text(f'''describe us_daily''')).fetchall()))
        # print('describe daily:' + str(conn.execute(text(f'''describe daily''')).fetchall()))

        sql_text = text(f'''truncate table us_daily''')
        conn.execute(sql_text)

        sql_text = text(f''' select * from us_daily''')
        result = conn.execute(sql_text)
        df_us_daily = pd.DataFrame(result.fetchall())
        print('data after truncate table: \n', df_us_daily)

    df_all = pd.read_csv(us_daily_file_name)
    df_all.set_index('date', inplace=True)
    print('all data read from csv:\n', df_all)

    i = 0
    df_len = len(df_all)
    step_len = 100000
    while i < int(df_len/step_len) + 1:
        if i < 268:
            i = i + 1
            continue
        begin_index = i * step_len
        end_index = (i + 1) * step_len
        if end_index > df_len:
            end_index = df_len
        df_insert = df_all[begin_index:end_index]
        print(f'insert step_len is {step_len} current steps is {i} total steps is {int(df_len/step_len)}')
        print(df_insert)

        # 创建Session
        session = Session(bind=conn)
        # 使用cursor.fast_executemany加速批量插入操作
        cursor = session.connection().connection.cursor()
        cursor.fast_executemany = True
        df_insert.to_sql(name='us_daily', con=engine, if_exists='append', method='multi', chunksize=step_len,
                  dtype={'date': VARCHAR(df_all.index.get_level_values('date').str.len().max()), 'symbol': VARCHAR(20)})
        session.close()

        i = i + 1

    print('after insert table')
    sql_db=pd.read_sql('us_daily', con=engine)
    print('content of table:\n', sql_db)

    print('describe us_daily:' + str(conn.execute(text(f'''describe us_daily''')).fetchall()))

    conn.commit()
    conn.close()

    exit(0)