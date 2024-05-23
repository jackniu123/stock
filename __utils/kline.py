__all__ = ["show_k_lines", "get_name_by_code"]

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import os, datetime


def show_k_lines(stock_codes=['000001.SZ', '000002.SZ'], start_date=None, end_date=None):
    if len(stock_codes) < 1:
        print(f"!!!show_k_lines: wrong par: stock_codes={stock_codes}")
        return
    if start_date is None:
        start_date = '20050101'
    if end_date is None:
        end_date = str(datetime.datetime.now().date().strftime("%Y%m%d"))
    if not (len(start_date) == 8 and len(end_date) == 8):
        print(f"!!!show_k_lines: wrong par: start_date={start_date} end_date={end_date}")

    pymysql.install_as_MySQLdb()

    try:
        df_all = pd.DataFrame()
        df_daily = pd.DataFrame()
        engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
        conn = engine.connect()
        for stock_code in stock_codes:

            if len(stock_code) < 6:
                print(f'!!!! error: stock_code is invalid: {stock_code}')
                continue
            else:
                stock_code = stock_code[0:6]


            sql_text = text(
                f'''select ts_code, trade_date, close from daily where ts_code like \'{stock_code}___\' 
                and trade_date between \'{start_date}\' and \'{end_date}\' ''')

            print(f'===processing {stock_code}:{sql_text}')

            result = conn.execute(sql_text)
            all_data = result.fetchall()
            df_daily = pd.DataFrame(list(all_data))
            # print(df_daily)
            if len(df_daily) == 0:
                continue
            df_daily = df_daily[['trade_date', 'close']]
            df_daily.rename(columns={'close': str(stock_code) + ':' + get_name_by_code(str(stock_code))}, inplace=True)

            if len(df_all) == 0:
                df_all = df_daily
            else:
                df_all = pd.merge(df_all, df_daily, on='trade_date', how='outer')

        if len(df_all) == 0:
            return

        df_all.set_index('trade_date', inplace=True)
        pd.options.display.max_rows = None
        # print('未按日期排序前的N个股票报价：\n', df_all)
        df_all.sort_index(inplace=True)
        df_all.ffill(axis=0, inplace=True)
        # print('按日期排序后的N个股票报价：\n', df_all)

        """
        rows_null = df_all.isnull().sum(axis=1)
        for index_in_item, value in rows_null.items():
            # print(index_in_item, ':', value)
            if value > len(stock_codes) - 2:
                df_all.drop(index_in_item, inplace=True)
        # print('===============================')
        # print(df_all)
        df_all.ffill(axis=0, inplace=True)
        corr = df_all.corr(method='pearson', min_periods=1)
        print(corr)
        """

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        df_all.plot(figsize=(20, 12))
        plt.show()
        plt.close()

    except Exception as e:
        print("\033[0;31;40m", e, "\033[0m")

    finally:
        conn.commit()
        conn.close()


df_code_name = pd.DataFrame()


def get_name_by_code(stock_code:str):
    stock_name = ''

    if len(stock_code) < 6:
        print(f'!!!! error: stock_code is ivalid: {stock_code}')
        return stock_name
    else:
        stock_code = stock_code[0:6]

    # print(stock_code)

    code_name_file_name = 'D:/不要删除牛爸爸的程序/__utils/code_name.csv'

    global df_code_name
    if len(df_code_name) == 0:
        if not os.path.exists(code_name_file_name):
            import akshare as ak
            df_code_name = ak.stock_info_a_code_name()
            df_code_name.to_csv(code_name_file_name)
        else:
            df_code_name = pd.read_csv(code_name_file_name, index_col=0)
    # print(df_code_name)
    # print(df_code_name[df_code_name['code'] == int(stock_code)])
    find_df = df_code_name[df_code_name['code'] == int(stock_code)]
    if len(find_df) > 0:
        stock_name = find_df.iloc[0]['name']
    return stock_name