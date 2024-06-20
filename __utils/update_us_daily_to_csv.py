# 里面有数据挖掘的预测方法：https://blog.csdn.net/wuShiJingZuo/article/details/135614467#:~:text=1%20import%20%C2%A0akshare%C2%A0as%C2%A0ak%202%20%23%C2%A0%E8%8E%B7%E5%8F%96%E8%82%A1%E7%A5%A8%E6%97%A5%E7%BA%BF%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE%203%20stock_data%C2%A0%3D%C2%A0ak.stock_zh_a_daily%28symbol%3D%20%22sz000001%22,%5D%C2%A0%3D%C2%A0stock_data%5B%20%22close%22%20%5D.pct_change%28%29%206%20print%20%28stock_data%5B%20%22return%22%20%5D.describe%28%29%29
# 买入下跌幅度大于95分位的股票，第二天卖出的盈利率有多少？
import akshare as ak
import pandas as pd
import os
from __utils import messagebox


def create_sub_csv():
    us_daily_file_name = './us_daily/us_daily.csv'
    df_all = pd.read_csv(us_daily_file_name)
    df_all.set_index('date', inplace=True)
    df_all_tmp = df_all.head(100000)
    us_daily_sub_file_name = './us_daily/us_daily_sub.csv'
    df_all_tmp.to_csv(us_daily_sub_file_name, header=True, index=True, mode='a')

# 核对某个股票在csv中的数据是否重复
def check_unique_us_daily(s_symbol = 'SWKH'):
    # pd.options.display.max_rows = None
    us_daily_file_name = './us_daily/us_daily.csv'
    df_all = pd.read_csv(us_daily_file_name)
    df_all.set_index('date', inplace=True)
    df_all_tmp = df_all[df_all['symbol'] == s_symbol]
    print('df_all_tmp:\n', df_all_tmp)
    dup_row = df_all_tmp.duplicated(keep=False)
    print('dup_row:\n', dup_row)
    df_all_tmp = df_all_tmp.drop_duplicates(keep='first')
    print('after drop duplicates:\n', df_all_tmp)

# 数据集去重
def drop_duplicates_us_daily():
    # pd.options.display.max_rows = None
    us_daily_file_name = './us_daily/us_daily.csv'
    df_all = pd.read_csv(us_daily_file_name)
    df_all.set_index('date', inplace=True)
    print('before drop duplicates:\n', df_all)
    df_all.drop_duplicates(keep='first', inplace=True)
    print('after drop duplicates:\n', df_all)
    us_daily_file_name_tmp = './us_daily/tmp_us_daily.csv'
    df_all.to_csv(us_daily_file_name_tmp, header=True, index=True, mode='a')


# 从网络上获取某个股票的日线历史
def get_us_daily_single_stock_from_web(s_symbol = 'SWKH'):
    stock_us_daily_df = ak.stock_us_daily(symbol=s_symbol, adjust="")
    stock_us_daily_df['symbol'] = s_symbol
    print(stock_us_daily_df)
    return stock_us_daily_df

def update_us_daily():

    # # 补获取数据失败的一些股票
    # s_symbol = 'SNLN'
    # us_daily_file_name = './us_daily/us_daily_20240616_fail.csv'
    # stock_us_daily_df = ak.stock_us_daily(symbol=s_symbol, adjust="")
    # stock_us_daily_df['symbol'] = s_symbol
    # if len(stock_us_daily_df) > 0:
    #     stock_us_daily_df.to_csv(us_daily_file_name, header=False if os.path.exists(us_daily_file_name) else True, index=False, mode='a')
    #     print('store and clear:\n', stock_us_daily_df)
    # else:
    #     print(stock_us_daily_df)
    # exit(0)

    # # 删除表格中间出现的表头
    # us_daily_file_name = './us_daily/us_daily_20240616.csv'
    # df_all = pd.read_csv(us_daily_file_name)
    # df_all.set_index('date', inplace=True)
    # print(df_all)
    # df_all.drop('date', axis=0, inplace=True)
    # us_daily_file_name = './us_daily/us_daily.csv'
    # df_all.to_csv(us_daily_file_name, header=True, index=True, mode='a')


    # 查看表格尾部内容
    # us_daily_file_name = './us_daily/us_daily.csv'
    # stock_us_daily_df = pd.read_csv(us_daily_file_name)
    # print(stock_us_daily_df.tail(10))

    us_daily_stock_name_list_file_name = './us_daily/us_stock_name_list.csv'
    us_daily_file_name = './us_daily/us_daily.csv'
    df_stock_name_list = pd.DataFrame()
    if not os.path.exists(us_daily_stock_name_list_file_name):
        df_stock_name_list = ak.get_us_stock_name()
        df_stock_name_list.to_csv(us_daily_stock_name_list_file_name, header=True, index=False)
    else:
        df_stock_name_list = pd.read_csv(us_daily_stock_name_list_file_name)
    print(df_stock_name_list)

    found_last_symbol = True
    # stock_us_daily_df_all = pd.DataFrame()

    # 2024-06-15 17:40:53,310 [WARNING] [update_us_daily_test.py:54] !!!exception occurred:PCSClist index out of range
    # 2024-06-15 18:06:08,674 [WARNING] [update_us_daily.py:51] !!!exception occurred:naninvalid syntax (<string>, line 1)
    # 2024-06-15 21:23:42,467 [WARNING] [update_us_daily.py:51] !!!exception occurred:GVUS('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
    # 2024-06-15 21:25:00,242 [WARNING] [update_us_daily.py:51] !!!exception occurred:GXCHTTPSConnectionPool(host='finance.sina.com.cn', port=443): Read timed out. (read timeout=None)
    # 2024-06-15 21:39:11,688 [WARNING] [update_us_daily.py:50] !!!exception occurred:HHGCRHTTPSConnectionPool(host='finance.sina.com.cn', port=443): Read timed out. (read timeout=None)

    is_csv_exist = False
    for s_symbol in df_stock_name_list['symbol']:

        # # 只处理特定的股票
        # if s_symbol == "GVUS" or s_symbol == "GXC" or s_symbol == "HHGCR":
        #     found_last_symbol = True
        # else:
        #     continue

        # 断点接续
        if not found_last_symbol:
            if s_symbol == "HHGCR":
                found_last_symbol = True

                # print(10 * '=' + f'{s_symbol}' + 10 * '=')
                # stock_us_daily_df = ak.stock_us_daily(symbol=s_symbol, adjust="")
                # stock_us_daily_df['symbol'] = s_symbol
                # print(stock_us_daily_df.tail(10))
                # break

            continue

        print(10*'=' + f'{s_symbol}' + 10*'=')
        try:
            stock_us_daily_df = ak.stock_us_daily(symbol=s_symbol, adjust="")
            stock_us_daily_df['symbol'] = s_symbol
            if len(stock_us_daily_df) > 0:
                stock_us_daily_df.to_csv(us_daily_file_name, header=False if is_csv_exist else True, index=False, mode='a')
                is_csv_exist = True
                print('store and clear:\n', stock_us_daily_df)
            else:
                print(stock_us_daily_df)
        except Exception as e:
            messagebox.logger.warning('!!!exception occurred:' + str(s_symbol) + str(e))

        # 备份一个能够批量写入的优化
        # try:
        #     stock_us_daily_df = ak.stock_us_daily(symbol=s_symbol, adjust="")
        #     stock_us_daily_df['symbol'] = s_symbol
        #     stock_us_daily_df_all = pd.concat([stock_us_daily_df_all, stock_us_daily_df], ignore_index=True)
        #     if len(stock_us_daily_df_all) > 0:
        #         stock_us_daily_df_all.to_csv(us_daily_file_name, header=True, index=False, mode='a')
        #         print('store and clear:\n', stock_us_daily_df_all)
        #         stock_us_daily_df_all = pd.DataFrame()
        #     else:
        #         print(stock_us_daily_df_all)
        # except Exception as e:
        #     messagebox.logger.warning('!!!exception occurred:' + str(s_symbol) + str(e))

    # stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="")
    # print(stock_us_daily_df)
    # df_stock_name = ak.get_us_stock_name()
    # print(df_stock_name)
    #

    
if __name__ == '__main__':
    # create_sub_csv()
    # drop_duplicates_us_daily()
    df = get_us_daily_single_stock_from_web('CETXW')
    df.to_csv('CETXW.csv')
    # check_unique_us_daily()
    exit(0)
    update_us_daily()

