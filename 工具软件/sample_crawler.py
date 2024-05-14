# https://blog.csdn.net/weixin_42430074/article/details/95067429
# https://www.cnblogs.com/cyywork/p/16996224.html

import requests

import xlwt  # 进行excel操作

import xlrd

import numpy as np

from sklearn import datasets, linear_model

from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error, r2_score

from sklearn.model_selection import cross_val_score

import sklearn.linear_model

import sklearn.datasets

import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score

import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error

url = 'http://27.push2.eastmoney.com/api/qt/clist/get'

datalist = []
#
# for i in range(1, 100):
#
#     data = {
#
#         'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
#
#         'pz': 1000,  # 每页条数
#
#         'pn': i,  # 页码
#
#         'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
#
#     }
#
#     response = requests.get(url, data)
#
#     response_json = response.json()
#
#     print(i, response_json)
#
#     # 返回数据为空时停止循环
#
#     if response_json['data'] is None:
#         break
#
#     for j, k in response_json['data']['diff'].items():
#         datas = []
#
#         code = k['f12']  # 代码
#
#         name = k['f14']  # 名称
#
#         price = k['f2']  # 股价
#
#         pe = k['f9']  # 动态市盈率
#
#         pb = k['f23']  # 市净率
#
#         total_value = k['f20']  # 总市值
#
#         currency_value = k['f21']  # 流通市值
#
#         price = round(price / 100, 2)  # 价格转换为正确值（保留2位小数）
#
#         pe = round(pe / 100, 2)  # 市盈率转换为正确值（保留2位小数）
#
#         pb = round(pb / 100, 2)  # 市净率转换为正确值（保留2位小数）
#
#         total_value = round(total_value / 100000000, 2)  # 总市值转换为亿元（保留2位小数）
#
#         currency_value = round(currency_value / 100000000, 2)  # 流通市值转换为亿元（保留2位小数）
#
#         print('代码: %s, 名称: %s, 现价: %s, 动态市盈率: %s, 市净率: %s, 总市值: %s亿, 流通市值: %s' % (
#             code, name, price, pe, pb, total_value, currency_value))
#
#         datas.append(code)
#
#         datas.append(name)
#
#         datas.append(price)
#
#         datas.append(pe)
#
#         datas.append(pb)
#
#         datas.append(total_value)
#
#         datas.append(currency_value)
#
#         datalist.append(datas)
#
# print("save......")
#
# book = xlwt.Workbook(encoding='utf-8', style_compression=0)
#
# sheet = book.add_sheet('stockers', cell_overwrite_ok=True)
#
# col = ('代码', "名称", "现价", "动态市盈率", "市净率", "总市值", "流通市值")
#
# for i in range(0, 7):
#     sheet.write(0, i, col[i])
#
# for i in range(0, len(datalist)):
#
#     print("第%d条" % i)
#
#     data = datalist[i]
#
#     for j in range(0, 7):
#         sheet.write(i + 1, j, data[j])
#
# book.save(".\\stockers.xls")

###数据清洗

import pandas as pd

excel = pd.read_excel("stockers.xls")  # 打开excel文件

# 1、是否存在空值

print(f''' excel has total lines: {len(excel)} , null value lines: {pd.isnull(excel.values).sum()}''')

excel = excel.dropna()

######

####数据可视化

import matplotlib.pyplot as plt

import numpy as np

sort_df = excel.sort_values(by="市净率", ascending=[True])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

sort_df = sort_df[sort_df['总市值'] > 1]

index = sort_df['名称'][:10]

values = sort_df['市净率'][:10]

pd.options.display.max_columns = None
pd.options.display.max_rows = None

print(sort_df)


plt.bar(index, values.values, color="red")

plt.title("市净率排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

exit()


# 获取现价排名最高的前10名股票

sort_df = excel.sort_values(by="现价", ascending=[False])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

index = sort_df['名称'][:7]

values = sort_df['现价'][:7]

plt.bar(index, values.values)

plt.title("现价排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

# 获取动态市盈率排名最高的前10名股票

sort_df = excel.sort_values(by="动态市盈率", ascending=[False])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

index = sort_df['名称'][:7]

values = sort_df['动态市盈率'][:7]

plt.bar(index, values.values, color="green")

plt.title("动态市盈率排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

sort_df = excel.sort_values(by="市净率", ascending=[False])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

index = sort_df['名称'][:7]

values = sort_df['市净率'][:7]

plt.bar(index, values.values, color="red")

plt.title("市净率排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

sort_df = excel.sort_values(by="总市值", ascending=[False])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

index = sort_df['名称'][:7]

values = sort_df['总市值'][:7]

plt.bar(index, values.values, color="pink")

plt.title("总市值排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

sort_df = excel.sort_values(by="流通市值", ascending=[False])

plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False

index = sort_df['名称'][:7]

values = sort_df['流通市值'][:7]

plt.bar(index, values.values, color="brown")

plt.title("流通市值排名")

# 设置x轴标签名

plt.xlabel("股票名称")

# 设置y轴标签名

plt.ylabel("现价")

# 显示

plt.show()

# 250

n = 250

area = 20 * np.arange(1, n + 1)

# 5. 设置点的边界线宽度 【可选参数】

widths = np.arange(n)  # 0-9的数字

x = excel["现价"]

y = excel["市净率"]

plt.scatter(x, y, s=area, linewidths=widths, alpha=0.5, marker='o')

# 7. 设置轴标签：xlabel、ylabel

# 设置X轴标签

plt.xlabel('X坐标')

# 设置Y轴标签

plt.ylabel('Y坐标')

# 8. 设置图标题：title

plt.title('test绘图函数')

# 9. 设置轴的上下限显示值：xlim、ylim

# 设置横轴的上下限值

plt.xlim(-100, 100)

# 设置纵轴的上下限值

plt.ylim(-100, 100)

# 10. 设置轴的刻度值：xticks、yticks

# 设置横轴精准刻度

plt.xticks(np.arange(np.min(x) - 0.2, np.max(x) + 0.2, step=0.3))

# 设置纵轴精准刻度

plt.yticks(np.arange(np.min(y) - 0.2, np.max(y) + 0.2, step=0.3))

# 也可按照xlim和ylim来设置

# 设置横轴精准刻度

plt.xticks(np.arange(-10, 10, step=0.5))

# 设置纵轴精准刻度

plt.yticks(np.arange(-10, 10, step=0.5))

#

plt.scatter(x, y)

# 7. 设置轴标签：xlabel、ylabel


########计算相关系数


import numpy as np

pc = np.corrcoef(x, y)

x = excel["现价"]

y = excel["市净率"]

print(pc)

import pandas as pd

from numpy import mean


# 相关系数计算公式

def R_Square(x, y):
    p1 = x2 = y2 = 0.0

    # 计算平均值

    x_ = mean(x)

    y_ = mean(y)

    # 循环读取每个值，计算对应值的累和

    for i in range(len(x)):
        p1 += (x[i] - x_) * (y[i] - y_)

        x2 += (x[i] - x_) ** 2

        y2 += (y[i] - y_) ** 2

    # print(p1,x2,y2)

    # 计算相关系数

    r = p1 / ((x2 ** 0.5) * (y2 ** 0.5))

    return r


# 读取数据

df = pd.read_csv("data.csv", encoding='utf-8')

x = df['x'].tolist()

y = df['y'].tolist()

# 调用并输出相关系数

print(R_Square(x, y))

######

x = np.array(x)

x = x.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# 创建一个线性模型对象

regr = linear_model.LinearRegression()

print('交叉检验的R^2: ', np.mean(cross_val_score(regr, x, y, cv=3)))

# 用训练集训练模型fit(x,y,sample_weight=None)sample_weight为数组形状

regr.fit(X_train, y_train)

#

# 用测试集做一个预测

y_pred = regr.predict(X_test)

# 估计系数a

print("估计系数a: ", regr.coef_)

# 模型截距b

print("模型截距b: ", regr.intercept_)

# 均方误差即E(y_test-y_pred)^2

print("均方误差: ", mean_squared_error(y_test, y_pred))

# 决定系数r^2,越接近1越好

print("决定系数R^2: ", r2_score(y_test, y_pred))

# 对比不同的划分系数

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)

# 创建一个线性模型对象

regr = linear_model.LinearRegression()

print('交叉检验的R^2: ', np.mean(cross_val_score(regr, x, y, cv=3)))

# 用训练集训练模型fit(x,y,sample_weight=None)sample_weight为数组形状

regr.fit(X_train, y_train)

#

# 用测试集做一个预测

y_pred = regr.predict(X_test)

# 估计系数a

print("估计系数a: ", regr.coef_)

# 模型截距b

print("模型截距b: ", regr.intercept_)

# 均方误差即E(y_test-y_pred)^2

print("均方误差: ", mean_squared_error(y_test, y_pred))

# 决定系数r^2,越接近1越好

print("决定系数R^2: ", r2_score(y_test, y_pred))

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# 创建一个线性模型对象

regr = linear_model.LinearRegression()

print('交叉检验的R^2: ', np.mean(cross_val_score(regr, x, y, cv=3)))

# 用训练集训练模型fit(x,y,sample_weight=None)sample_weight为数组形状

regr.fit(X_train, y_train)

#

# 用测试集做一个预测

y_pred = regr.predict(X_test)

# 估计系数a

print("估计系数a: ", regr.coef_)

# 模型截距b

print("模型截距b: ", regr.intercept_)

# 均方误差即E(y_test-y_pred)^2

print("均方误差: ", mean_squared_error(y_test, y_pred))

# 决定系数r^2,越接近1越好

print("决定系数R^2: ", r2_score(y_test, y_pred))
