import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql

from __utils import messagebox


# 无法成交判断：
# 1，volume过低
# 2，涨停无法买入，跌停无法卖出


class TradeCore:
    def buy(self, stock_code, price, cur_day=None):
        print(f'TradeCore---buy par: stock_code = {stock_code}, price = {price}, cur_day = {cur_day}')
        return

    def sell(self, stock_code, price, cur_day=None):
        print(f'TradeCore---sell par: stock_code = {stock_code}, price = {price}, cur_day = {cur_day}')
        return

    g_is_trade_inited = False
    g_cur_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_begin_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_end_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_cur_df_daily = pd.DataFrame()

    def init_trade(self, begin_day, end_day):
        if not self.g_is_trade_inited:
            self.g_begin_day = datetime.datetime(year=int(begin_day[0:4]), month=int(begin_day[4:6]), day=int(begin_day[6:8])).date()
            self.g_end_day = datetime.datetime(year=int(end_day[0:4]), month=int(end_day[4:6]), day=int(end_day[6:8])).date()
            self.g_cur_day = self.g_begin_day

    def get_cur_df_daily(self):
        pymysql.install_as_MySQLdb()
        try:
            # 创建数据库连接
            engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
            conn = engine.connect()
            sql_text = text(f'''select ts_code, trade_date, open, close, high from daily where trade_date=\'{self.g_cur_day.strftime("%Y%m%d")}\' limit 10000000''')
            print(f'开始查询数据库：:{sql_text}')
            result = conn.execute(sql_text)
            all_data = result.fetchall()
            self.g_cur_df_daily = pd.DataFrame(list(all_data))
            # g_df_daily = self.g_cur_df_daily[['ts_code', 'trade_date', 'close']]
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
            import traceback
            messagebox.showerror('出错了', f'{traceback.format_exc()}')
        finally:
            conn.commit()
            conn.close()

        print('从数据库中查询到的表格为：\n', self.g_cur_df_daily)
        return


    def trade_by_daily(self, trade_func, begin_day, end_day):
        self.init_trade(begin_day, end_day)
        while self.g_cur_day < self.g_end_day:
            print(f'===begin processing: {self.g_cur_day} ===')
            self.get_cur_df_daily()
            if len(self.g_cur_df_daily) < 1:
                self.g_cur_day = self.g_cur_day + datetime.timedelta(1)
                continue
            # else:
            #     print(self.g_cur_df_daily)
            trade_func(self, self.g_cur_day.strftime("%Y%m%d"), self.g_cur_df_daily)
            print(f'===end processing: {self.g_cur_day} ===')
            self.g_cur_day = self.g_cur_day + datetime.timedelta(1)

        return

    def trade_by_tick(self):
        return

    def show_result(self):
        return


def trade_strategy_MA20(trade_core_ins=None, cur_day=None, cur_df_daily=None):
    stock_code = '000001.SZ'
    cur_df_daily = cur_df_daily[cur_df_daily['ts_code'] == stock_code]
    trade_core_ins.buy(stock_code, cur_df_daily['open'][0], cur_day)
    trade_core_ins.sell(stock_code, cur_df_daily['close'][0], cur_day)
    print(f'trade_strategy_MA20: cur_day = {cur_day}: stock_daily of {stock_code} is:\n ' ,  cur_df_daily)

    return


if __name__ == '__main__':
    trade_core = TradeCore()
    trade_core.trade_by_daily(trade_func=trade_strategy_MA20, begin_day='20230104', end_day='20230110')
    trade_core.show_result()