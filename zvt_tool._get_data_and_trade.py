# https://zhuanlan.zhihu.com/p/583384302
# https://gitee.com/ppiao/zvt

from zvt.domain import *
Stock.record_data(provider="em")
df = Stock.query_data(provider="em", index='code')
print(df)