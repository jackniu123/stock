import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql

from __utils import messagebox


# 无法成交判断：
# 1，volume过低
# 2，涨停无法买入，跌停无法卖出

class Portforlio:
    s_stock_code = ""
    s_current_shares = 0

    def __init__(self, stock_code, current_shares):
        self.s_stock_code = stock_code
        self.s_current_shares = current_shares


class TradeHistory:
    s_stock_code = ""
    s_share_change = 0
    s_price = 0
    s_trade_time = 0
    s_buy_or_sell = False

    def __init__(self, stock_code, shares_change, price, trade_time, buy_or_sell):
        self.s_stock_code = stock_code
        self.s_share_change = shares_change
        self.s_price = price
        self.s_trade_time = trade_time
        self.s_buy_or_sell = buy_or_sell

    def dump(self):
        print(f"""stock_code:{self.s_stock_code}, shares_change:{self.s_share_change}, price:{self.s_price}, trade_time:{self.s_trade_time}, buy_or_sell:{self.s_buy_or_sell}""")

class TradeCore:

    g_is_trade_inited = False
    g_cur_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_begin_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_end_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_df_daily = pd.DataFrame()
    g_df_close = pd.DataFrame()
    g_df_vol = pd.DataFrame()
    g_trade_func = None
    g_filter_func = None
    g_stock_codes = ['000001.SZ']

    def init_trade(self, init_func, trade_func, begin_day, end_day, cash=1000000):
        if not self.g_is_trade_inited:
            self.g_trade_func = trade_func
            self.g_begin_day = datetime.datetime(year=int(begin_day[0:4]), month=int(begin_day[4:6]), day=int(begin_day[6:8])).date()
            self.g_end_day = datetime.datetime(year=int(end_day[0:4]), month=int(end_day[4:6]), day=int(end_day[6:8])).date()
            self.g_cur_day = self.g_begin_day
            init_func(self)
            self.init_df_daily()
            self.g_is_trade_inited = True

    def init_df_daily(self):
        # 更高性能的做法
        # if True:
        #     field_name = 'close'
        #     sql_query_flatten_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_flatten_' + field_name + '.csv'
        #     self.g_df_close = pd.read_csv(sql_query_flatten_file_name, index_col=0)
        #
        #     field_name = 'vol'
        #     sql_query_flatten_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_flatten_' + field_name + '.csv'
        #     self.g_df_vol = pd.read_csv(sql_query_flatten_file_name, index_col=0)
        #     return

        pymysql.install_as_MySQLdb()
        try:
            # 创建数据库连接
            engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
            conn = engine.connect()
            # sql_text = text(
            #     f'''select ts_code, trade_date, open, close, high from daily where trade_date=\'{self.g_cur_day.strftime("%Y%m%d")}\' and ts_code=\'{stock_list}\' ''')
            # sql_text = text(f'''select * from daily''')
            # stock_list = ','.join(self.g_stock_codes)
            stock_list = ','.join("'{0}'".format(x) for x in self.g_stock_codes)
            sql_text = text(f'''select * from daily where ts_code in ({stock_list}) ''')

            import time
            start_time = time.time()
            print(f'开始查询数据库：:{sql_text}')
            result = conn.execute(sql_text)
            all_data = result.fetchall()
            end_time = time.time()
            print('从数据库中读取股票的所有数据的耗时 {:.2f}秒'.format(end_time - start_time))

            self.g_df_daily = pd.DataFrame(list(all_data))
            # g_df_daily = self.g_df_daily[['ts_code', 'trade_date', 'close']]
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
            import traceback
            messagebox.showerror('出错了', f'{traceback.format_exc()}')
        finally:
            conn.commit()
            conn.close()

        print('从数据库中查询到的表格为：\n', self.g_df_daily)
        return

    def trade_by_daily(self):

        while self.g_cur_day < self.g_end_day:
            # print(f'===begin processing: {self.g_cur_day} {self.g_cur_day.strftime("%Y%m%d")}===')
            # 跳过非交易日
            if len(self.g_df_daily[self.g_df_daily['trade_date']==self.g_cur_day.strftime("%Y%m%d")]) < 1:
                self.g_cur_day = self.g_cur_day + datetime.timedelta(1)
                continue
            # else:
            #     print(self.g_df_daily)
            self.g_trade_func(self, self.g_df_daily[self.g_df_daily['trade_date']<=self.g_cur_day.strftime("%Y%m%d")])
            # print(f'===end processing: {self.g_cur_day} ===')
            self.g_cur_day = self.g_cur_day + datetime.timedelta(1)

        return

    g_portforlio = []
    g_trade_history = []

    def get_sharehold(self, stock_code):
        for cur_portforlio in self.g_portforlio:
            if cur_portforlio.s_stock_code == stock_code:
                return cur_portforlio.s_current_shares
        return 0

    def buy(self, stock_code, price, shares):
        # print(f'TradeCore---buy par: stock_code = {stock_code}, price = {price}, shares = {shares}, cur_day = {self.g_cur_day}')
        has_add = False
        for cur_portforlio in self.g_portforlio:
            if cur_portforlio.s_stock_code == stock_code:
                cur_portforlio.s_current_shares += shares
                has_add = True

        if not has_add:
            sharehold = Portforlio(stock_code, shares)
            self.g_portforlio.append(sharehold)

        trade_history = TradeHistory(stock_code, shares, price, self.g_cur_day, "buy")
        self.g_trade_history.append(trade_history)

        return

    def sell(self, stock_code, price, shares=-1):
        # print(f'TradeCore---sell par: stock_code = {stock_code}, price = {price}, cur_day = {self.g_cur_day}')
        for cur_portforlio in self.g_portforlio:
            if cur_portforlio.s_stock_code == stock_code:
                # 代表清仓处理
                if shares == -1:
                    cur_portforlio.s_current_shares = 0
                else:
                    cur_portforlio.s_current_shares -= shares

        trade_history = TradeHistory(stock_code, shares, price, self.g_cur_day, "sell")
        self.g_trade_history.append(trade_history)

        return

    def trade_by_tick(self):
        return

    def show_result(self):
        # 策略收益曲线
        # 下单历史
        for cur_trade_history in self.g_trade_history:
            cur_trade_history.dump()
        return

#
# def trade_strategy_MA20(trade_core_ins=None, cur_day=None, cur_df_daily=None):
#     stock_code = '000001.SZ'
#     cur_df_daily = cur_df_daily[cur_df_daily['ts_code'] == stock_code]
#     trade_core_ins.buy(stock_code, cur_df_daily['open'][0], cur_day)
#     trade_core_ins.sell(stock_code, cur_df_daily['close'][0], cur_day)
#     print(f'trade_strategy_MA20: cur_day = {cur_day}: stock_daily of {stock_code} is:\n ' ,  cur_df_daily)
#
#     return

def init_trade_strategy_low_volume(trade_core_ins=None):
    # trade_core_ins.g_stock_codes = ["000001.SZ", "000020.SZ"]
    trade_core_ins.g_stock_codes = ["000020.SZ"]

    trade_core_ins.g_sum_of_compare_volume = 0
    trade_core_ins.g_cur_count_of_compare_volume = 0
    trade_core_ins.g_sum_of_low_volume = 0
    trade_core_ins.g_cur_count_of_low_volume_days = 0

    trade_core_ins.const_count_of_compare_volume = 200
    trade_core_ins.const_count_of_low_volume_days = 20
    trade_core_ins.const_times_of_buy = 1
    trade_core_ins.const_times_of_sell = 2

def handle_data_trade_strategy_low_volume(trade_core_ins=None, cur_df_daily=None):
    for stock_code in trade_core_ins.g_stock_codes:
        # print(cur_df_daily)
        df_daily = cur_df_daily[cur_df_daily['ts_code'] == stock_code]
        if len(df_daily) < trade_core_ins.const_count_of_compare_volume:
            continue

        compare_volume = df_daily['vol'][-trade_core_ins.const_count_of_compare_volume:].mean()
        current_max_volume = df_daily['vol'][-trade_core_ins.const_count_of_low_volume_days:].max()

        if trade_core_ins.get_sharehold(stock_code) == 0 \
                and current_max_volume < compare_volume * trade_core_ins.const_times_of_buy:
            trade_core_ins.buy(stock_code, df_daily['close'].tail(1).values[0], 1000)
        if trade_core_ins.get_sharehold(stock_code) > 0 \
                and current_max_volume > compare_volume * trade_core_ins.const_times_of_sell:
            trade_core_ins.sell(stock_code, df_daily['close'].tail(1).values[0])

    # print(f'end of handle_data_trade_strategy_low_volume')

    return


if __name__ == '__main__':
    trade_core = TradeCore()
    trade_core.init_trade(init_func=init_trade_strategy_low_volume, trade_func=handle_data_trade_strategy_low_volume, begin_day='20050104', end_day='20240820', cash=1000000)
    trade_core.trade_by_daily()
    trade_core.show_result()