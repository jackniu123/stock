import datetime
import os
import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
import pymysql

from __utils import messagebox, kline
import inspect
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from line_profiler import LineProfiler

# 全局开关
# g_debug_mode = True
g_debug_mode = False
g_single_stock_debug = False
g_debug_from_last_100_days = False

g_cur_abs_path = ""


# 无法成交判断：
# 1，volume过低
# 2，涨停无法买入，跌停无法卖出

class Portforlio:
    s_stock_code = ""
    s_current_shares = 0
    s_average_cost = 0

    def __init__(self, stock_code, current_shares, average_cost):
        self.s_stock_code = stock_code
        self.s_current_shares = current_shares
        self.s_average_cost = average_cost


class TradeHistory:
    s_stock_code = ""
    s_share_change = 0
    s_price = 0
    s_trade_time = 0
    s_buy_or_sell = False
    s_profit = 0
    s_profit_change = 0
    # 这是为了计算最终成绩，对最后的残留持仓做清空操作
    s_last_clear = False

    def __init__(self, stock_code, shares_change, price, trade_time, buy_or_sell, last_clear=False):
        self.s_stock_code = stock_code
        self.s_share_change = shares_change
        self.s_price = price
        self.s_trade_time = trade_time
        self.s_buy_or_sell = buy_or_sell
        self.s_last_clear = last_clear

    def dump(self):
        result_string = f"""stock_code:{self.s_stock_code}, shares_change:{self.s_share_change}, price:{self.s_price}, trade_time:{self.s_trade_time}, buy_or_sell:{self.s_buy_or_sell}"""
        if self.s_last_clear:
            result_string += f""" [this is last clear]"""
        if self.s_buy_or_sell == 'sell':
            result_string += f"""\n             ===profit:{int(self.s_profit)}, profit_change:{self.s_profit_change * 100:.2f}% ==="""
        print(result_string)

    def get_df(self):
        tmp_df = pd.DataFrame({'stock_code': self.s_stock_code,
                               'share_change': self.s_share_change,
                               'price': self.s_price,
                               'trade_time': self.s_trade_time,
                               'buy_or_sell': self.s_buy_or_sell,
                               's_last_clear': self.s_last_clear}, index=[0])
        return tmp_df


class TradeCore:
    g_is_trade_inited = False
    g_trade_calendar = []
    g_cur_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_begin_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_end_day = datetime.datetime(year=2005, month=1, day=1).date()
    g_df_daily = pd.DataFrame()
    g_cur_df_daily = pd.DataFrame()
    g_df_close = pd.DataFrame()
    g_df_vol = pd.DataFrame()
    g_trade_func = None
    g_filter_func = None
    g_stock_codes = ['000001.SZ']
    g_path = ""
    g_root_path = __file__.replace('.', '_')

    def init_trade(self, init_func, trade_func, begin_day, end_day, cash=1000000):
        if not self.g_is_trade_inited:
            print(f"""{"="*10}trade_core init_trade: init_trade:{init_func.__name__}, trade_func:{trade_func.__name__}, begin_day:{begin_day}, end_day:{end_day}{"="*10}""")
            self.g_trade_func = trade_func
            self.g_begin_day = datetime.datetime(year=int(begin_day[0:4]), month=int(begin_day[4:6]),
                                                 day=int(begin_day[6:8])).date()
            self.g_end_day = datetime.datetime(year=int(end_day[0:4]), month=int(end_day[4:6]),
                                               day=int(end_day[6:8])).date()
            self.g_cur_day = self.g_begin_day
            init_func(self)

            # 记录下来所有参数
            self.g_path = __file__.replace('.', '_') + "\\" + trade_func.__name__ + "\\" + str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            os.makedirs(self.g_path)
            with open(self.g_path + "\\" + 'config.conf', 'a+') as f:
                attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))
                for attribute in attributes:
                    f.write(str(attribute) + "\r\n")
                f.close()

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
            engine = create_engine("mysql+mysqldb://root:mysql123@127.0.0.1:3306/stock", max_overflow=5)
            conn = engine.connect()
            sql_text = ""

            # 初始化交易日历
            sql_text = text(f'''select distinct trade_date from daily ''')
            result = conn.execute(sql_text).fetchall()
            self.g_trade_calendar = []
            for element in result:
                self.g_trade_calendar.append(element[0])
            print(self.g_trade_calendar)

            # 初始化g_df_daily
            if self.g_stock_codes == "all" or len(self.g_stock_codes) == 0:
                sql_text = text(f'''select distinct ts_code from daily ''')
                result = conn.execute(sql_text).fetchall()
                self.g_stock_codes = []
                for element in result:
                    self.g_stock_codes.append(element[0])
                print(self.g_stock_codes)
                sql_text = text(f'''select ts_code, trade_date, open, close, high, vol from daily where trade_date between \'{self.g_begin_day.strftime("%Y%m%d")}\' and \'{self.g_end_day.strftime("%Y%m%d")}\' ''')
            else:
                stock_list = ','.join("'{0}'".format(x) for x in self.g_stock_codes)
                sql_text = text(f'''select * from daily where ts_code in ({stock_list}) and trade_date between \'{self.g_begin_day.strftime("%Y%m%d")}\' and \'{self.g_end_day.strftime("%Y%m%d")}\' ''')

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
        print(f'''{'='*10}trade_by_daily begin{'='*10}''')
        start_time = time.time()
        last_print_time = time.time()

        while self.g_cur_day < self.g_end_day:
            # print(f'===begin processing: {self.g_cur_day} {self.g_cur_day.strftime("%Y%m%d")}===')
            if g_debug_from_last_100_days and self.g_cur_day < self.g_end_day - datetime.timedelta(100):
                self.g_cur_day = self.g_cur_day + datetime.timedelta(1)
                continue

            self.g_cur_day = self.g_cur_day + datetime.timedelta(1)
            # 跳过非交易日
            if self.g_cur_day.strftime("%Y%m%d") not in self.g_trade_calendar:
                continue

            self.g_cur_df_daily = self.g_df_daily[
                    self.g_df_daily['trade_date'] <= self.g_cur_day.strftime("%Y%m%d")]

            if True:
                lp = LineProfiler(self.g_trade_func)
                last_perf_time = time.time()
                lp.runcall(self.g_trade_func, self, self.g_cur_df_daily)
                # 5秒的总执行时间是7小时
                if time.time() - last_perf_time > 5:
                    lp.print_stats()
            else:
                self.g_trade_func(self, self.g_cur_df_daily)

            if time.time() - last_print_time > 100:
                print(f'=== progress: {(self.g_cur_day-self.g_begin_day)/(self.g_end_day-self.g_begin_day) * 100:.2f}% --- end processing: {self.g_cur_day}, days processed: {(self.g_cur_day-self.g_begin_day).days}天, time passed:{time.time() - start_time:.2f} 秒   ===')
                last_print_time = time.time()

        end_time = time.time()
        print('trade_by_daily执行完的耗时 {:.2f}秒'.format(end_time - start_time))

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
                cur_portforlio.s_average_cost = ((cur_portforlio.s_average_cost * cur_portforlio.s_current_shares) + (
                        price * shares)) / (cur_portforlio.s_current_shares + shares)
                cur_portforlio.s_current_shares += shares
                has_add = True

        if not has_add:
            sharehold = Portforlio(stock_code, shares, price)
            self.g_portforlio.append(sharehold)

        trade_history = TradeHistory(stock_code, shares, price, self.g_cur_day, "buy")
        self.g_trade_history.append(trade_history)

        return

    def sell(self, stock_code, price, shares=-1, last_clear=False, sell_date=None):
        # print(f'TradeCore---sell par: stock_code = {stock_code}, price = {price}, cur_day = {self.g_cur_day}')

        if shares == -1:
            self.g_portforlio = list(filter(lambda cur_portforlio: not cur_portforlio.s_stock_code == stock_code, self.g_portforlio))
        else:
            for cur_portforlio in self.g_portforlio:
                if cur_portforlio.s_stock_code == stock_code:
                    cur_portforlio.s_current_shares -= shares

        trade_history = TradeHistory(stock_code, shares, price, self.g_cur_day if sell_date is None else sell_date, "sell", last_clear)
        self.g_trade_history.append(trade_history)

        return

    def trade_by_tick(self):
        return

    def generate_result(self):
        print(f'''{'=' * 10}generate_result begin{'=' * 10}''')
        # 清空持仓
        for portforlio in self.g_portforlio:
            if portforlio.s_current_shares > 0:
                # current_price = self.g_df_daily.loc[
                #     (self.g_df_daily['trade_date'] <= self.g_cur_day.strftime("%Y%m%d")) & (
                #             self.g_df_daily['ts_code'] == portforlio.s_stock_code)]['close'].tail(1).values[0]
                cur_stock_df = self.g_cur_df_daily[self.g_cur_df_daily['ts_code'] == portforlio.s_stock_code]
                sell_price = cur_stock_df['close'].tail(1).values[0]
                sell_date = cur_stock_df['trade_date'].tail(1).values[0]
                # print(self.g_df_daily.loc[(self.g_df_daily['trade_date']<=self.g_cur_day.strftime("%Y%m%d")) & (self.g_df_daily['ts_code']==portforlio.s_stock_code)][['ts_code', 'trade_date', 'close']])
                self.sell(portforlio.s_stock_code, sell_price, -1, last_clear=True, sell_date=sell_date)

        # 下单历史
        # 计算卖出时的每笔盈利和盈利率, 进而计算总盈利、胜率、最大回撤等
        with_header = True

        df_trade_history_to_file = pd.DataFrame()
        df_trade_statics_to_file = pd.DataFrame()

        for stock_code, df_cur_stock in self.g_cur_df_daily.groupby('ts_code'):
        # for stock_code in self.g_stock_codes:
            if stock_code == self.g_stock_codes[0] or stock_code == self.g_stock_codes[-1]:
                print(f'''==================================={stock_code}==================================''')

            last_buy = None
            total_profit = 0
            total_profit_change = 1
            max_loss = 0
            win_count = 0
            loss_count = 0
            win_percent = 0
            for cur_trade_history in self.g_trade_history:
                if cur_trade_history.s_stock_code == stock_code:
                    if cur_trade_history.s_buy_or_sell == 'buy':
                        last_buy = cur_trade_history
                    if cur_trade_history.s_buy_or_sell == 'sell':
                        # TODO: 如果并非每次都清仓，那么需要计算平均持仓成本
                        if cur_trade_history.s_share_change == -1:
                            cur_trade_history.s_profit = (
                                                                 cur_trade_history.s_price - last_buy.s_price) * last_buy.s_share_change
                            total_profit += cur_trade_history.s_profit
                            cur_trade_history.s_profit_change = cur_trade_history.s_profit / (
                                    last_buy.s_price * last_buy.s_share_change)
                            total_profit_change *= 1 + cur_trade_history.s_profit_change
                            if cur_trade_history.s_profit_change > 0:
                                win_count += 1
                            else:
                                loss_count += 1
                            max_loss = max_loss if max_loss < cur_trade_history.s_profit_change else cur_trade_history.s_profit_change
            win_percent = 0.5 if win_count + loss_count == 0 else win_count / (win_count + loss_count)

            df_trade_history = pd.DataFrame()
            for cur_trade_history in self.g_trade_history:
                if cur_trade_history.s_stock_code == stock_code:
                    cur_trade_history.dump()
                    df_trade_history = pd.concat([df_trade_history, cur_trade_history.get_df()], ignore_index=True)
                    # print(df_trade_history)

            detail_filename = self.g_path + "\\" + "trade_history.csv"
            # df_trade_history.to_csv(detail_filename, mode='a', header=with_header, index=False)
            df_trade_history_to_file = pd.concat([df_trade_history_to_file, df_trade_history], ignore_index=True)

            # 继而计算相对收益
            # df_cur_stock = self.g_df_daily.loc[(self.g_df_daily['trade_date'] <= self.g_cur_day.strftime("%Y%m%d"))
            #                                    & (self.g_df_daily['ts_code'] == stock_code)]
            # print(df_cur_stock[['ts_code', 'trade_date', 'close']])
            if len(df_trade_history) >= 2:
                begin_price = df_cur_stock['close'].values[0]
                end_price = df_cur_stock['close'].values[-1]
                benchmark_profit_change = (end_price - begin_price) / begin_price * 100
                relative_profit_change = (total_profit_change - 1) * 100 - benchmark_profit_change
            else:
                benchmark_profit_change = 0
                relative_profit_change = 0

            if stock_code == self.g_stock_codes[0] or stock_code == self.g_stock_codes[-1]:
                print(
                    "=" * 10 + f'''total_profit_change:{(total_profit_change - 1) * 100:.2f}%, win_percent:{(win_percent * 100):.2f}%, max_loss:{max_loss * 100:.2f}%, trade_count:{win_count + loss_count}, total_profit:{int(total_profit)}, benchmark_profit_change is {benchmark_profit_change:.2f}% relative_profit_change is {relative_profit_change:.2f}% ''' + '=' * 10)
            statics_filename = self.g_path + "\\" + "statics.csv"
            df_trade_statics = pd.DataFrame(
                {'ts_code': stock_code,
                 'total_profit_change': (total_profit_change - 1) * 100,
                 'win_percent': (win_percent * 100),
                 'max_loss': max_loss * 100,
                 'trade_count': win_count + loss_count,
                 'total_profit': int(total_profit),
                 'benchmark_profit_change': benchmark_profit_change * 100,
                 'relative_profit_change': relative_profit_change * 100}, index=[0])
            # df_trade_statics.to_csv(statics_filename, mode='a', header=with_header, index=False)
            df_trade_statics_to_file = pd.concat([df_trade_statics_to_file, df_trade_statics], ignore_index=True)
            # with_header = False
            if stock_code == self.g_stock_codes[0] or stock_code == self.g_stock_codes[-1]:
                print(f'''*******************************{stock_code}*******************************''')

        df_trade_history_to_file.to_csv(detail_filename, mode='a', header=True, index=False)
        df_trade_statics_to_file.to_csv(statics_filename, mode='a', header=True, index=False)
        return

    def show_result(self, trade_func=None):
        print(f'''{'=' * 10}show_result begin{'=' * 10}''')
        result_path = self.g_root_path + "\\" + trade_func.__name__

        top = tk.Tk()
        top.geometry("1700x1000")
        lbl = tk.Label(top, text=trade_func.__name__ + "的分析结果...")
        listbox = tk.Listbox(top, width=900)

        # create treeview
        treeview_statics = ttk.Treeview(top, show="headings", columns=(
            "ts_code", "total_profit_change", "win_percent", "max_loss", "trade_count", "total_profit"))

        # set column headings
        treeview_statics.heading("#0", text="ID")
        treeview_statics.heading("ts_code", text="ts_code")
        treeview_statics.heading("total_profit_change", text="total_profit_change")
        treeview_statics.heading("win_percent", text="win_percent")
        treeview_statics.heading("max_loss", text="max_loss")
        treeview_statics.heading("trade_count", text="trade_count")
        treeview_statics.heading("total_profit", text="total_profit")

        trv_trade_history = ttk.Treeview(top, show="headings", columns=(
            "ts_code", "share_change", "price", "trade_time", "buy_or_sell", "s_last_clear"))

        # set column headings
        trv_trade_history.heading("#0", text="ID")
        trv_trade_history.heading("ts_code", text="ts_code")
        trv_trade_history.heading("share_change", text="share_change")
        trv_trade_history.heading("price", text="price")
        trv_trade_history.heading("trade_time", text="trade_time")
        trv_trade_history.heading("buy_or_sell", text="buy_or_sell")
        trv_trade_history.heading("s_last_clear", text="s_last_clear")

        def show_selected_item(event):
            selected_item = listbox.get(listbox.curselection())
            # messagebox.showinfo("Selected Item", selected_item)
            global g_cur_abs_path
            g_cur_abs_path = selected_item
            print(selected_item + "\\" + "statics.csv  content:")
            statics_data = pd.read_csv(selected_item + "\\" + "statics.csv")
            print(statics_data)
            items = treeview_statics.get_children()
            for item_trv in items:
                treeview_statics.delete(item_trv)
            for key, data in statics_data.iterrows():
                print(data)
                treeview_statics.insert("", tk.END, values=list(data))

        last_folder_path = []
        for dir_name in os.listdir(result_path):
            dir_path = os.path.join(result_path, dir_name)
            if os.path.isfile(dir_path):
                print("file:", dir_path)
            else:
                print("folder", dir_path)
                last_folder_path.insert(0, dir_path)
        for item in last_folder_path:
            listbox.insert(tk.END, item)
        listbox.bind("<Double-Button-1>", show_selected_item)
        listbox.bind("<ButtonRelease-1>", show_selected_item)

        # https://blog.csdn.net/sinat_27382047/article/details/80161637
        def treeview_statics_show_selected_item(event):
            global g_cur_abs_path
            for selected_item_id in treeview_statics.selection():
                print("treeview_statics_show_selected_item selected_item:", treeview_statics.item(selected_item_id))
                stock_code = treeview_statics.item(selected_item_id)['values'][0]
                df_trade_history = pd.read_csv(g_cur_abs_path + "\\" + "trade_history.csv")
                # print(df_trade_history)

                items = trv_trade_history.get_children()
                for item_trv in items:
                    trv_trade_history.delete(item_trv)
                for key, data in df_trade_history.iterrows():
                    if data['stock_code'] == stock_code:
                        trv_trade_history.insert("", tk.END, values=list(data))

                if True:
                    begin_day = None
                    end_day = None
                    # g_cur_abs_path = "D:\\不要删除牛爸爸的程序\\__utils\\tradecore_py\\handle_data_trade_strategy_low_volume\\20240825_114911\\"
                    for line in open(g_cur_abs_path + "\\" + "config.conf", 'r'):
                        if line.find("g_begin_day") > 0 and line.find(", datetime") > 0:
                            print('content:', line)
                            start_index = line.find('20')
                            line = line[start_index:-3]
                            spllit_strings = line.split(",")
                            print(spllit_strings)
                            year = spllit_strings[0]
                            month = spllit_strings[1]
                            day = spllit_strings[2]
                            print(year, month, day)
                            begin_day = datetime.datetime(year=int(year), month=int(month), day=int(day)).strftime(
                                "%Y%m%d")
                            print(begin_day)
                        elif line.find("g_end_day") > 0 and line.find(", datetime") > 0:
                            print('content:', line)
                            start_index = line.find('20')
                            line = line[start_index:-3]
                            spllit_strings = line.split(",")
                            print(spllit_strings)
                            year = spllit_strings[0]
                            month = spllit_strings[1]
                            day = spllit_strings[2]
                            print(year, month, day)
                            end_day = datetime.datetime(year=int(year), month=int(month), day=int(day)).strftime(
                                "%Y%m%d")
                            print(end_day)

                    df_trade_history = df_trade_history[df_trade_history['stock_code'] == stock_code]
                    print(df_trade_history)

                    print("will show kline:")
                    print(stock_code)
                    print(begin_day)
                    print(end_day)
                    # 显示分析图
                    daily_by_code = kline.get_daily_by_code(stock_code=stock_code, start_date=begin_day, end_date=end_day)
                    print(daily_by_code)
                    daily_will_show = daily_by_code.copy()
                    daily_will_show['buy_price'] = np.nan
                    daily_will_show['sell_price'] = np.nan
                    for key, cur_trade_history in df_trade_history.iterrows():
                        print("cur_trade_history:", cur_trade_history)
                        if cur_trade_history.buy_or_sell == "buy":
                            daily_will_show.loc[daily_will_show['trade_date'] == str(cur_trade_history.trade_time.replace("-", "")), [
                                "buy_price"]] = cur_trade_history.price
                        if cur_trade_history.buy_or_sell == "sell":
                            daily_will_show.loc[daily_will_show['trade_date'] == str(cur_trade_history.trade_time.replace("-", "")), [
                                'sell_price']] = cur_trade_history.price

                    print(daily_will_show)
                    kline.show_trade_history(daily_will_show)

        treeview_statics.bind("<Double-Button-1>", treeview_statics_show_selected_item)

        lbl.pack()
        listbox.pack()
        # display treeview
        treeview_statics.pack()
        trv_trade_history.pack()

        top.mainloop()

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
    trade_core_ins.g_stock_codes = ["000001.SZ", "000020.SZ"] if g_debug_mode else "all"
    trade_core_ins.g_stock_codes = ["000020.SZ"] if g_single_stock_debug else trade_core_ins.g_stock_codes

    trade_core_ins.g_sum_of_compare_volume = 0
    trade_core_ins.g_cur_count_of_compare_volume = 0
    trade_core_ins.g_sum_of_low_volume = 0
    trade_core_ins.g_cur_count_of_low_volume_days = 0

    trade_core_ins.const_count_of_compare_volume = 200
    trade_core_ins.const_count_of_low_volume_days = 20
    trade_core_ins.const_times_of_buy = 1
    trade_core_ins.const_times_of_sell = 2

g_df_volume = pd.DataFrame()
def handle_data_trade_strategy_low_volume(trade_core_ins=None, cur_df_daily=None):
    if not b_need_history_daily:
        print("===cur day:",  trade_core_ins.g_cur_day)
        for stock_code, df_daily in cur_df_daily:
            cur_vol = df_daily['vol']
            print(stock_code, ":vol ", cur_vol)
            # g_df_volume[stock_code] = pd.DataFrame({})
        return

    # 下面的代码依赖历史数据，也就是b_need_history_daily==True
    if (trade_core_ins.g_cur_day - trade_core_ins.g_begin_day).days < trade_core_ins.const_count_of_compare_volume * 7 / 5:
        return

    for stock_code, df_daily in cur_df_daily.groupby('ts_code'):
    # for stock_code in trade_core_ins.g_stock_codes:
        # print(cur_df_daily)
        # df_daily = cur_df_daily[cur_df_daily['ts_code'] == stock_code]
        if len(df_daily) < trade_core_ins.const_count_of_compare_volume:
            continue

        compare_volume = df_daily['vol'][-trade_core_ins.const_count_of_compare_volume:].mean()

        if trade_core_ins.get_sharehold(stock_code) == 0 \
                and df_daily['vol'][-trade_core_ins.const_count_of_low_volume_days:].max() < compare_volume * trade_core_ins.const_times_of_buy:
            trade_core_ins.buy(stock_code, df_daily['close'].tail(1).values[0], 1000)
        elif trade_core_ins.get_sharehold(stock_code) > 0 \
                and df_daily['vol'].values[-1] > compare_volume * trade_core_ins.const_times_of_sell:
            trade_core_ins.sell(stock_code, df_daily['close'].tail(1).values[0])
    # print(f'end of handle_data_trade_strategy_low_volume')

    return


if __name__ == '__main__':
    trade_core = TradeCore()
    end_day = '20061012' if g_debug_mode else '20240820'
    trade_core.init_trade(init_func=init_trade_strategy_low_volume, trade_func=handle_data_trade_strategy_low_volume,
                          begin_day='20050104', end_day=end_day, cash=1000000)

    if False:
        lp = LineProfiler(trade_core.trade_by_daily)
        last_perf_time = time.time()
        lp.runcall(trade_core.trade_by_daily)
        if time.time() - last_perf_time > 3:
            lp.print_stats()
    else:
        trade_core.trade_by_daily()
    # trade_core.trade_by_month()

    lp = LineProfiler(trade_core.generate_result)
    last_perf_time = time.time()
    lp.runcall(trade_core.generate_result)
    if time.time() - last_perf_time > 10:
        lp.print_stats()
    # trade_core.generate_result()
    trade_core.show_result(trade_func=handle_data_trade_strategy_low_volume)
