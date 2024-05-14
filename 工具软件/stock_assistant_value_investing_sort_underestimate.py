# 影响估值的几个因素，查询并排序：市净率、市盈率、市销率、市场空间、行业周期、货币流动性、政策导向、外部局势、上下游价格、营业收入增长率、毛利率
# 市净率
# https://zhuanlan.zhihu.com/p/407705325


import akshare as ak
import pandas as pd

# pd.options.display.max_columns = None
# pd.set_option('display.width', 200)
#
# stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol="000001")
# print(stock_a_indicator_lg_df)

import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.style as mplstyle
mplstyle.use('fast')

stock_market_pe_lg_df = ak.stock_market_pe_lg(symbol="上证")
print(stock_market_pe_lg_df)

stock_market_pe_lg_df = stock_market_pe_lg_df[:100]
print(stock_market_pe_lg_df)


stock_market_pe_lg_df.set_index(['日期'], inplace=True)
fig, ax = plt.subplots(1, 1)


tick_spacing = len(stock_market_pe_lg_df) / 10  # x軸密集度

ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
# plt.xticks(rotation=90)
plt.rcParams['figure.figsize'] = [100, 10]

print(tick_spacing)
ax.plot(stock_market_pe_lg_df.index, stock_market_pe_lg_df['指数'])
# stock_market_pe_lg_df.plot(ax=ax)

plt.show()

