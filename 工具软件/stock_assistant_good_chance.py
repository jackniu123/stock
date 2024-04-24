import akshare as ak
from tkinter import messagebox
import datetime
import re
import requests

'''
不同的声音 https://zhuanlan.zhihu.com/p/189426241
巴菲特在《福布斯》杂志上的这篇超长文章的核心是解释为什么美国国民生产总值GNP在1964年到1981年上涨了2.7倍，但同期道琼斯指数只涨了1点，而美国GNP在1981年到1988年只上涨了0.8倍，但同期道琼斯指数却上涨了9.5倍。
值得一提的是，现在各国GNP和GDP的差距很小，各国主要公布GDP，所以用GDP取代GNP是普遍的做法。
大家想一想，中国GDP过去十年高增长，但是A股上证指数过去十年基本没涨，是不是有点类似。将来中国GDP增速肯定会放缓，但是A股也有比较大的可能迎来较大的涨幅，过去我曾经多次解释过背后可能的原因。

在投资上，没有单一指标是完美的，不要过多依赖听上去似乎最简单的估值指标，要重点关注利率走势和其他基本面指标
未来充满不确定性，你仍然可以有所为有所不为。降低高估值国家和个股的配置比率，增加低估值国家和个股的配置比率，把业绩评估的目光放长远，是很不错的选择。

相关支持：
美国参加的战争：https://www.zhihu.com/question/67203048
美国国债占GDP比例的历史数据：https://xueqiu.com/8458090377/262611597
原油价格历史走势：https://zhuanlan.zhihu.com/p/150056672
1970年代，美国的国债利息占GDP的规模一直在1.2%左右，参加的战争主要是1970年入侵柬埔寨，1965-1973越南战争，同期道琼斯指数几乎没有上涨。
1980年代开始，该比例急速飙升到3.0%左右，发起了两场中东的战争和两场美洲的巴拿马运河战争，苏联于1989年解体，同期道琼斯指数上涨9.5倍。
70年代的油价相对于80年代高很多。

'''


def check_buffet_index():
    stock_buffett_index_lg_df = ak.stock_buffett_index_lg()
    print(stock_buffett_index_lg_df.tail(20))

    current_buffet_index = stock_buffett_index_lg_df.iloc[-1]['总市值'] / stock_buffett_index_lg_df.iloc[-1]['GDP']
    print(f'current buffet index is {{{current_buffet_index}}}')

    if current_buffet_index < 0.6 or stock_buffett_index_lg_df.iloc[-1]['近十年分位数'] < 0.15:
        messagebox.showinfo('提示',
                            f'当前巴菲特指数超级便宜：{{{current_buffet_index}}} \n {{{stock_buffett_index_lg_df.iloc[-1]}}}')

    if current_buffet_index > 1 or stock_buffett_index_lg_df.iloc[-1]['近十年分位数'] > 0.9:
        messagebox.showerror('警告',
                             f'！！！你在玩火，巴菲特指数已经高达：{{{current_buffet_index}}} \n {{{stock_buffett_index_lg_df.iloc[-1]}}}')


def check_ipo():
    b_has_ipo = False
    last_ipo = '不存在科技'

    response = requests.get('https://data.eastmoney.com/xg/xg/calendar.html')

    # print(response.text)

    i = 0
    for item in response.text.splitlines():
        i += 1

        if 'calendardata' in item:
            print(i, ":", item)
            print('========================================================')
            j = 0
            for line in re.split('SECURITY_NAME_ABBR', item):
                j += 1
                if '申购' in line:
                    print(j, ":", line)
                    last_ipo = line
                    for days in range(0, 30):
                        if 'TRADE_DATE":"' + str(datetime.datetime.now().date() + datetime.timedelta(days)) in line:
                            print('/n ============================================')
                            print(line)
                            # messagebox.showinfo('提示', str(datetime.datetime.now().date()+datetime.timedelta(days)) + line)
                            b_has_ipo = True

    if not b_has_ipo:
        messagebox.showinfo('提示', f'没有IPO了，最近的IPO情况是：{{{last_ipo}}}')


if __name__ == '__main__':
    check_buffet_index()
    check_ipo()
