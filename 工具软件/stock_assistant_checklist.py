"""
    买入股票时候的检查功能，检查列表如下：
    1, 宏观环境（科技革命的进展情况、国家经济发展所处阶段、国际局势、各国通胀（原油走势）、各国就业、各国货币政策、各国财政政策）
    2，行业环境（发展阶段和空间、周期）
    3，个股质地
    4，技术面（走势、消息）
    5，仓位控制

"""
import datetime


def show_jpg_jiejin():
    import akshare as ak
    import matplotlib.pyplot as plt


    plt.figure(figsize=(200, 50))

    # 股票代码
    stock_name = '601138'

    # 获取股票解禁数据
    ak.stock_restricted_release_summary_em()
    # "stock_restricted_release_queue_sina"  # 限售解禁-新浪
    # "stock_restricted_release_summary_em"  # 东方财富网-数据中心-特色数据-限售股解禁
    # "stock_restricted_release_detail_em"  # 东方财富网-数据中心-限售股解禁-解禁详情一览
    # "stock_restricted_release_queue_em"  # 东方财富网-数据中心-个股限售解禁-解禁批次
    # "stock_restricted_release_stockholder_em"  # 东方财富网-数据中心-个股限售解禁-解禁股东

    stock_restricted_shares_df = ak.stock_restricted_release_queue_em(symbol=stock_name)
    print(stock_restricted_shares_df)
    # print(stock_restricted_shares_df.values[:, 1])

    # 获取20190101至20220331的股价数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_name, period="daily", start_date="20190101",
                                            end_date='20220331', adjust="")

    date = []
    price = []
    color = []
    for i in range(0, stock_zh_a_hist_df.shape[0]):
        date.append(stock_zh_a_hist_df.values[i][0])
        price.append(stock_zh_a_hist_df.values[i][2])
        # print(stock_zh_a_hist_df.values[i][0])
        if stock_zh_a_hist_df.values[i][0] in stock_restricted_shares_df.values[:, 1]:
            color.append('r')
            plt.text(stock_zh_a_hist_df.values[i][0], stock_zh_a_hist_df.values[i][2], stock_zh_a_hist_df.values[i][0])
        else:
            color.append('b')

    plt.plot(date, price, 'b')
    plt.scatter(date, price, c=color)
    plt.savefig("./res.jpg")


def check_jiejin(stock_code, stock_name):
    print("\n\n", stock_name, " 解禁日历======================:")
    jiejin_df = ak.stock_restricted_release_queue_em(symbol=stock_code)
    # print(ak.stock_restricted_release_queue_em(symbol=key))

    for key, value in jiejin_df.iterrows():
        # print(key)
        if value['解禁时间'] > datetime.datetime.now().date():
            print(value)
            messagebox.showwarning('警告', stock_name + '有即将发生的限售解禁：\n' + value.to_string())

def check_debt(stock_code, stock_name):

    return


def check_shixiaolv(stock_code, stock_name):
    return


import akshare as ak
import pandas as pd
import sys
sys.path.append('D:/不要删除牛爸爸的程序/') # 绝对路径
from __utils import messagebox

pd.options.display.max_columns = None

if __name__ == '__main__':
    stock_code = '001979'
    stock_name = '招商蛇口'
    check_hongguan()
    check_jiejin(stock_code, stock_name)
    check_debt(stock_code, stock_name)
