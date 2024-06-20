# 里面有数据挖掘的预测方法：https://blog.csdn.net/wuShiJingZuo/article/details/135614467#:~:text=1%20import%20%C2%A0akshare%C2%A0as%C2%A0ak%202%20%23%C2%A0%E8%8E%B7%E5%8F%96%E8%82%A1%E7%A5%A8%E6%97%A5%E7%BA%BF%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE%203%20stock_data%C2%A0%3D%C2%A0ak.stock_zh_a_daily%28symbol%3D%20%22sz000001%22,%5D%C2%A0%3D%C2%A0stock_data%5B%20%22close%22%20%5D.pct_change%28%29%206%20print%20%28stock_data%5B%20%22return%22%20%5D.describe%28%29%29

import pandas as pd


# 买入开盘价下跌幅度大于一定比例的股票，当天尾盘卖出的盈利率有多少？或者当天上涨1%就卖出的盈利会有多少？
def buy_low_open_sell_when(by='close'):
    # us_daily_file_name = 'D:/不要删除牛爸爸的程序/__utils/us_daily/us_daily_sub.csv'
    us_daily_file_name = 'D:/不要删除牛爸爸的程序/__utils/us_daily/us_daily.csv'
    buy_low_open_sell_close_trade_history_file_name = './buy_low_open_sell_close_trade_history_improve.csv'
    if not by == 'close':
        buy_low_open_sell_close_trade_history_file_name = './buy_low_open_sell_1.01_trade_history_improve.csv'

    df_all = pd.read_csv(us_daily_file_name)
    df_all.set_index('date', inplace=True)

    df_trade_history = pd.DataFrame()

    symbol_pool = df_all['symbol'].drop_duplicates()
    for symbol, group in df_all.groupby('symbol'):
        df_single_stock = group
        # print(symbol + ' daily history:\n', df_single_stock)
        len_df_single_stock = len(df_single_stock)
        if len_df_single_stock < 100:
            continue
        for i in range(1, len_df_single_stock):
            if df_single_stock.iloc[i-1]['close'] > 0.0001 and df_single_stock.iloc[i]['volume'] > 1:
                change = (df_single_stock.iloc[i]['open'] - df_single_stock.iloc[i-1]['close']) / df_single_stock.iloc[i-1]['close']
                if change < -0.5 and df_single_stock.iloc[i]['open'] > 0.0001:
                    sell_price = df_single_stock.iloc[i]['close']
                    if not by == 'close':
                        if df_single_stock.iloc[i]['high'] > 1.01 * df_single_stock.iloc[i]['open']:
                            sell_price = 1.01 * df_single_stock.iloc[i]['open']
                    df_trade_history_item = df_single_stock.iloc[i].copy()
                    df_trade_history_item['last_close'] = df_single_stock.iloc[i-1]['close']
                    df_trade_history_item['profit'] = sell_price - df_single_stock.iloc[i]['open']
                    df_trade_history_item['change'] = df_trade_history_item['profit'] / df_single_stock.iloc[i]['open']
                    print(f'processing...{i}/{len_df_single_stock}, found {len(df_trade_history)}st chance : \n', df_trade_history_item)
                    df_trade_history = df_trade_history._append(df_trade_history_item)
    print(df_trade_history)
    df_trade_history.to_csv(buy_low_open_sell_close_trade_history_file_name, header=True, index=True, mode='a')


if __name__ == '__main__':
    buy_low_open_sell_when(by='1.01')
    buy_low_open_sell_when(by='close')

