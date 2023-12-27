from pytdx.hq import *
from pytdx.exhq import *


# https://zhuanlan.zhihu.com/p/135349115
# https://rainx.gitbooks.io/pytdx
# https://zhuanlan.zhihu.com/p/458889137


api_hq = TdxHq_API()
api_hq = api_hq.connect('119.147.212.81', 7709)

# 返回普通list
data = api_hq.get_security_bars(9, 0, '000001', 0, 10)
print('list:======\n',data)
# 返回DataFrame
data = api_hq.to_df(api_hq.get_security_bars(9, 0, '000001', 0, 800))
print('dataframe:======\n',data)

