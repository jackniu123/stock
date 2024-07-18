# coding=utf-8
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


# 参考：https://blog.csdn.net/Shepherdppz/article/details/117575286  https://www.cnblogs.com/shclbear/p/17231948.html

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

# 读取示例数据
data = pd.read_csv('kline_test_data.csv', index_col=0)
data.index = pd.to_datetime(data.index)

my_color = mpf.make_marketcolors(up='r',
                                 down='g',
                                 edge='inherit',
                                 wick='inherit',
                                 volume='inherit')
my_style = mpf.make_mpf_style(marketcolors=my_color,
                              figcolor='(0.82, 0.83, 0.85)',
                              gridcolor='(0.82, 0.83, 0.85)')
# 定义各种字体
title_font = {'fontname': 'SimHei',
                  'size': '24',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom',
                  'ha': 'center'}
large_red_font = {'fontname': 'SimHei',
                  'size': '24',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
large_green_font = {'fontname': 'SimHei',
                    'size': '24',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
small_red_font = {'fontname': 'SimHei',
                  'size': '12',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
small_green_font = {'fontname': 'SimHei',
                    'size': '12',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
normal_label_font = {'fontname': 'SimHei',
                     'size': '12',
                     'color': 'black',
                     'weight': 'normal',
                     'va': 'bottom',
                     'ha': 'right'}
normal_font = {'fontname': 'SimHei',
               'size': '12',
               'color': 'black',
               'weight': 'normal',
               'va': 'bottom',
               'ha': 'left'}


class InterCandle:
    def __init__(self, data, my_style):
        self.pressed = False
        self.xpress = None

        # 初始化交互式K线图对象，历史数据作为唯一的参数用于初始化对象
        self.data = data
        self.style = my_style
        # 设置初始化的K线图显示区间起点为0，即显示第0到第99个交易日的数据（前100个数据）
        self.idx_start = 0
        self.idx_range = 100
        # 设置ax1图表中显示的均线类型
        self.avg_type = 'ma'
        self.indicator = 'macd'

        # 初始化figure对象，在figure上建立三个Axes对象并分别设置好它们的位置和基本属性
        self.fig = mpf.figure(style=my_style, figsize=(12, 8), facecolor=(0.82, 0.83, 0.85))
        fig = self.fig
        self.ax1 = fig.add_axes([0.08, 0.25, 0.88, 0.60])
        self.ax2 = fig.add_axes([0.08, 0.15, 0.88, 0.10], sharex=self.ax1)
        self.ax2.set_ylabel('volume')
        self.ax3 = fig.add_axes([0.08, 0.05, 0.88, 0.10], sharex=self.ax1)
        self.ax3.set_ylabel('macd')
        # 初始化figure对象，在figure上预先放置文本并设置格式，文本内容根据需要显示的数据实时更新
        self.t1 = fig.text(0.50, 0.94, '513100.SH - 纳斯达克指数ETF基金', **title_font)
        self.t2 = fig.text(0.12, 0.90, '开/收: ', **normal_label_font)
        self.t3 = fig.text(0.14, 0.89, f'', **large_red_font)
        self.t4 = fig.text(0.14, 0.86, f'', **small_red_font)
        self.t5 = fig.text(0.22, 0.86, f'', **small_red_font)
        self.t6 = fig.text(0.12, 0.86, f'', **normal_label_font)
        self.t7 = fig.text(0.40, 0.90, '高: ', **normal_label_font)
        self.t8 = fig.text(0.40, 0.90, f'', **small_red_font)
        self.t9 = fig.text(0.40, 0.86, '低: ', **normal_label_font)
        self.t10 = fig.text(0.40, 0.86, f'', **small_green_font)
        self.t11 = fig.text(0.55, 0.90, '量(万手): ', **normal_label_font)
        self.t12 = fig.text(0.55, 0.90, f'', **normal_font)
        self.t13 = fig.text(0.55, 0.86, '额(亿元): ', **normal_label_font)
        self.t14 = fig.text(0.55, 0.86, f'', **normal_font)
        self.t15 = fig.text(0.70, 0.90, '涨停: ', **normal_label_font)
        self.t16 = fig.text(0.70, 0.90, f'', **small_red_font)
        self.t17 = fig.text(0.70, 0.86, '跌停: ', **normal_label_font)
        self.t18 = fig.text(0.70, 0.86, f'', **small_green_font)
        self.t19 = fig.text(0.85, 0.90, '均价: ', **normal_label_font)
        self.t20 = fig.text(0.85, 0.90, f'', **normal_font)
        self.t21 = fig.text(0.85, 0.86, '昨收: ', **normal_label_font)
        self.t22 = fig.text(0.85, 0.86, f'', **normal_font)

        fig.canvas.mpl_connect('button_press_event', self.on_press)
        fig.canvas.mpl_connect('button_release_event', self.on_release)
        fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        fig.canvas.mpl_connect('scroll_event', self.on_scroll)

    def refresh_plot(self, idx_start, idx_range):
        print('refresh_plot idx_start:' + str(idx_start) + ' idx_range:' + str(idx_range))
        """ 根据最新的参数，重新绘制整个图表
        """
        all_data = self.data
        plot_data = all_data.iloc[idx_start: idx_start + idx_range]

        ap = []
        # 添加K线图重叠均线，根据均线类型添加移动均线或布林带线
        if self.avg_type == 'ma':
            ap.append(mpf.make_addplot(plot_data[['MA5', 'MA10', 'MA20', 'MA60']], ax=self.ax1))
        elif self.avg_type == 'bb':
            ap.append(mpf.make_addplot(plot_data[['bb-u', 'bb-m', 'bb-l']], ax=self.ax1))
        # 添加指标，根据指标类型添加MACD或RSI或DEMA
        if self.indicator == 'macd':
            ap.append(mpf.make_addplot(plot_data[['macd-m', 'macd-s']], ylabel='macd', ax=self.ax3))
            bar_r = np.where(plot_data['macd-h'] > 0, plot_data['macd-h'], 0)
            bar_g = np.where(plot_data['macd-h'] <= 0, plot_data['macd-h'], 0)
            ap.append(mpf.make_addplot(bar_r, type='bar', color='red', ax=self.ax3))
            ap.append(mpf.make_addplot(bar_g, type='bar', color='green', ax=self.ax3))
        elif self.indicator == 'rsi':
            ap.append(mpf.make_addplot([75] * len(plot_data), color=(0.75, 0.6, 0.6), ax=self.ax3))
            ap.append(mpf.make_addplot([30] * len(plot_data), color=(0.6, 0.75, 0.6), ax=self.ax3))
            ap.append(mpf.make_addplot(plot_data['rsi'], ylabel='rsi', ax=self.ax3))
        else:  # indicator == 'dema'
            ap.append(mpf.make_addplot(plot_data['dema'], ylabel='dema', ax=self.ax3))

        print(plot_data)
        # 绘制图表
        mpf.plot(plot_data,
                 ax=self.ax1,
                 volume=self.ax2,
                 addplot=ap,
                 type='candle',
                 style=self.style,
                 datetime_format='%Y-%m',
                 xrotation=0)

        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        self.fig.canvas.draw()

    def refresh_texts(self, display_data):
        """ 更新K线图上的价格文本
        """
        # display_data是一个交易日内的所有数据，将这些数据分别填入figure对象上的文本中
        self.t3.set_text(f'{np.round(display_data["open"], 3)} / {np.round(display_data["close"], 3)}')
        self.t4.set_text(f'{np.round(display_data["change"], 3)}')
        self.t5.set_text(f'[{np.round(display_data["pct_change"], 3)}%]')
        self.t6.set_text(f'{display_data.name.date()}')
        self.t8.set_text(f'{np.round(display_data["high"], 3)}')
        self.t10.set_text(f'{np.round(display_data["low"], 3)}')
        self.t12.set_text(f'{np.round(display_data["volume"] / 10000, 3)}')
        self.t14.set_text(f'{display_data["value"]}')
        self.t16.set_text(f'{np.round(display_data["upper_lim"], 3)}')
        self.t18.set_text(f'{np.round(display_data["lower_lim"], 3)}')
        self.t20.set_text(f'{np.round(display_data["average"], 3)}')
        self.t22.set_text(f'{np.round(display_data["last_close"], 3)}')
        # 根据本交易日的价格变动值确定开盘价、收盘价的显示颜色
        if display_data['change'] > 0:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'red'
        elif display_data['change'] < 0:  # 如果今日变动额小于0，即今天价格低于昨天，今天价格显示为绿色
            close_number_color = 'green'
        else:
            close_number_color = 'black'
        self.t3.set_color(close_number_color)
        self.t4.set_color(close_number_color)
        self.t5.set_color(close_number_color)

    def on_press(self, event):
        print('on_press 1 event.xdata:' + str(event.xdata) + str(type(event.xdata)))
        # 不处理volume图
        if not (event.inaxes == self.ax1) and (not event.inaxes == self.ax3):
            return
        # 只处理左键
        if event.button != 1:
            return
        self.pressed = True
        self.xpress = event.xdata

        # 切换当前ma类型, 在ma、bb、none之间循环
        if event.inaxes == self.ax1 and event.dblclick == 1:
            if self.avg_type == 'ma':
                self.avg_type = 'bb'
            elif self.avg_type == 'bb':
                self.avg_type = 'none'
            else:
                self.avg_type = 'ma'
        # 切换当前indicator类型，在macd/dma/rsi/kdj之间循环
        if event.inaxes == self.ax3 and event.dblclick == 1:
            if self.indicator == 'macd':
                self.indicator = 'dma'
            elif self.indicator == 'dma':
                self.indicator = 'rsi'
            elif self.indicator == 'rsi':
                self.indicator = 'kdj'
            else:
                self.indicator = 'macd'

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refresh_plot(self.idx_start, self.idx_range)

    def on_release(self, event):
        self.pressed = False
        print('on_release xdata:' + str(event.xdata) + str(type(event.xdata)))
        print('on_release xpress:' + str(self.xpress) + str(type(self.xpress)))
        dx = int(event.xdata - self.xpress)
        self.idx_start -= dx
        if self.idx_start <= 0:
            self.idx_start = 0
        if self.idx_start >= len(self.data) - 100:
            self.idx_start = len(self.data) - 100

        # self.ax1.clear()
        # self.ax2.clear()
        # self.ax3.clear()
        # self.refresh_plot(self.idx_start, self.idx_range)

    def on_motion(self, event):
        if not self.pressed:
            return
        if not event.inaxes == self.ax1:
            return
        print('on_motion xdata:' + str(event.xdata) + str(type(event.xdata)))
        print('on_motion xpress:' + str(self.xpress) + str(type(self.xpress)))
        dx = int(event.xdata - self.xpress)
        new_start = self.idx_start - dx
        # 设定平移的左右界限，如果平移后超出界限，则不再平移
        if new_start <= 0:
            new_start = 0
        if new_start >= len(self.data) - 100:
            new_start = len(self.data) - 100
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        print('on_motion self.idx_start:' + str(self.idx_start) + str(type(self.idx_start)))
        print('on_motion new_start:' + str(new_start))

        self.refresh_texts(self.data.iloc[new_start])
        self.refresh_plot(new_start, self.idx_range)

    def on_scroll(self, event):
        # 仅当鼠标滚轮在axes1范围内滚动时起作用
        scale_factor = 1.0
        if event.inaxes != self.ax1:
            return
        if event.button == 'down':
            # 缩小20%显示范围
            scale_factor = 0.8
        if event.button == 'up':
            # 放大20%显示范围
            scale_factor = 1.2
        # 设置K线的显示范围大小
        self.idx_range = int(self.idx_range * scale_factor)
        # 限定可以显示的K线图的范围，最少不能少于30个交易日，最大不能超过当前位置与
        # K线数据总长度的差
        data_length = len(self.data)
        if self.idx_range >= data_length - self.idx_start:
            self.idx_range = data_length - self.idx_start
        if self.idx_range <= 30:
            self.idx_range = 30
            # 更新图表（注意因为多了一个参数idx_range，refresh_plot函数也有所改动）
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refresh_texts(self.data.iloc[self.idx_start])
        self.refresh_plot(self.idx_start, self.idx_range)

    # 键盘按下处理
    def on_key_press(self, event):
        data_length = len(self.data)
        if event.key == 'a':  # avg_type, 在ma,bb,none之间循环
            if self.avg_type == 'ma':
                self.avg_type = 'bb'
            elif self.avg_type == 'bb':
                self.avg_type = 'none'
            elif self.avg_type == 'none':
                self.avg_type = 'ma'
        elif event.key == 'up':  # 向上，看仔细1倍
            if self.idx_range > 30:
                self.idx_range = self.idx_range // 2
        elif event.key == 'down':  # 向下，看多1倍标的
            if self.idx_range <= data_length - self.idx_start:
                self.idx_range = self.idx_range * 2
        elif event.key == 'left':
            if self.idx_start > self.idx_range:
                self.idx_start = self.idx_start - self.idx_range // 2
        elif event.key == 'right':
            if self.idx_start < data_length - self.idx_range:
                self.idx_start = self.idx_start + self.idx_range // 2
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refresh_texts(self.data.iloc[self.idx_start])
        self.refresh_plot(self.idx_start, self.idx_range)


if __name__ == '__main__':
    candle = InterCandle(data, my_style)
    candle.idx_start = 150
    candle.idx_range = 100
    candle.refresh_texts(data.iloc[249])
    candle.refresh_plot(150, 100)
    plt.show()
    # input()

