import akshare as ak
import tkinter as tk
from __utils import messagebox
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def remove_unit(money):  # 去除单位部分，转化为元
    if money[-2:] == "万亿":
        money = float(money.replace("万亿", "")) * 1000000000000
    elif money[-1] == "亿":
        money = float(money.replace("亿", "")) * 100000000
    elif money[-1] == "万":
        money = float(money.replace("万", "")) * 10000
    else:
        money = float(money)
    return money


def get_unit(money):  # 将元转为为亿元或万元或万亿元
    if abs(money) > 1000000000000:
        scale = 1e-12
        result = f"{money * scale:,.2f}万亿元"
    elif abs(money) > 10000000:
        scale = 1e-8
        result = f"{money * scale:,.2f}亿元"
    else:
        scale = 1e-4
        result = f"{money * scale:,.2f}万元"
    return result


def str2percentage(percentage_string):
    return float(percentage_string.strip('%'))  # 将字符串形式的涨跌幅转变为小数形式


def generate_summary(name, period_desc, revenue, revenue_change, profit, profit_change, pre_profit):
    if revenue_change > 0:
        revenue_desc = f"同比上升{revenue_change:.2f}%"
    elif revenue_change < 0:
        revenue_desc = f"同比下降{abs(revenue_change):.2f}%"
    else:
        revenue_desc = "同比持平"

    if profit >= 0 and pre_profit >= 0:
        if profit > pre_profit:
            profit_decs = f"同比上升{profit_change:.2f}%"
        elif profit < pre_profit:
            profit_decs = f"同比下降{abs(profit_change):.2f}%"
        else:
            profit_decs = "同比持平"
    elif profit > 0 > pre_profit:
        profit_decs = "扭亏为盈"
    elif profit < 0 < pre_profit:
        profit_decs = "转盈为亏"
    else:  # 连年亏损
        if abs(profit) > abs(pre_profit):
            profit_decs = "亏损扩大"
        elif abs(profit) < abs(pre_profit):
            profit_decs = "亏损减少"
        else:
            profit_decs = "同比持平"
    # 转化为亿元、万元的单位
    revenue = get_unit(revenue)
    profit = get_unit(profit)

    summary = f"【{name}】{period_desc}实现营业总收入{revenue}，{revenue_desc}；" \
              f"归母净利润{profit}，{profit_decs}。"
    return summary


date_mapping_1 = {
    "03-31": "季度报告：",
    "06-30": "半年度报告：",
    "09-30": "季度报告：",
    "12-31": "年度报告："
}
date_mapping_2 = {
    "03-31": "Q1",
    "06-30": "H1",
    "09-30": "前三季度",
    "12-31": "年"
}


def get_summary():
    # period = period_entry.get()
    # code_list = code_list_entry.get().split(',')

    period = '2023-03-31'
    code_list = ['000001']

    try:
        results = []  # 输出结果

        title = date_mapping_1.get(period[5:], "未知")  # 摘要标题
        if title == "未知":
            messagebox.showerror("报告期错误")
            return  # 结束函数的运行
        quarter = date_mapping_2.get(period[5:], "未知")  # 季度描述

        # 获取去年同期的报告期字符串
        year = period[:4]  # 获取前四个字符
        int_year = int(year) - 1  # 将前四个字符转换为数字并减去1
        last_year = str(int_year).zfill(4)  # 将得到的数字转换为字符串，补齐至四位
        yoy_period = period.replace(year, last_year, 1)  # 替换字符串的前四个字符，得到去年同期的报告期

        period_desc = f"{title}公司{year}{quarter}"

        # 对每个输入的code取数据
        for code in code_list:
            # 检查code能否匹配公司
            try:
                company = ak.stock_individual_info_em(symbol=code)
                name = company.iloc[5][1]
            except KeyError:
                results.append(f"{code}：无法匹配\n")
                continue
            # 从同花顺获取关键财务指标
            try:
                data = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
                data = data.set_index(data.columns[0])
                print(data)
            except KeyError:
                results.append(f"{code}：{name}获取财报数据失败\n")
                continue
            # 判断是否存在数据
            try:
                revenue = remove_unit(data.loc[period, "营业总收入"])
                revenue_change = str2percentage(data.loc[period, "营业总收入同比增长率"])
                profit = remove_unit(data.loc[period, "净利润"])
                profit_change = str2percentage(data.loc[period, "净利润同比增长率"])
                # 获取去年归母净利润数据
                pre_profit = remove_unit(data.loc[yoy_period, "净利润"])
            except KeyError:
                results.append(f"{code}：{name}报告未更新\n")
                continue

            # 调用函数获取财报摘要，并保存在输出列表中
            summary = generate_summary(name, period_desc, revenue, revenue_change, profit, profit_change, pre_profit)
            results.append(f"{summary}\n")
            print(results)
        # result_text.config(state='normal')  # 将输出区域状态更改为可编辑
        # result_text.delete('1.0', tk.END)  # 清空区域
        # result_text.insert(tk.END, "\n".join(results))  # 将输出列表中的内容以换行符分隔，添加到输出区域中
        # result_text.config(state='disabled')  # 将输出区域状态更改为不可编辑
    except Exception as e:
        messagebox.showerror("Error", f"获取摘要时出错：{str(e)}")

def main_from_web():
    # 创建主窗口
    root = tk.Tk()
    root.title("日报-财务报告摘要akshare")

    # 添加标签和输入框
    period_label = tk.Label(root, text="请输入报告期（如2023-06-30）")
    period_label.pack()

    period_entry = tk.Entry(root)
    period_entry.pack()

    code_list_label = tk.Label(root, text="请输入公司code（多个则以英文逗号分隔）")
    code_list_label.pack()

    code_list_entry = tk.Entry(root, width=100)
    code_list_entry.pack()

    # 添加按钮
    run_button = tk.Button(root, text="运行", command=get_summary)
    run_button.pack()

    # 添加结果显示区域
    result_text = tk.Text(root, height=30, width=120, state='disabled')
    result_text.pack()

    # 启动 GUI 循环
    root.mainloop()


def show_finance_by_code_list(code_list=[]):

    for code in code_list:
        # 检查code能否匹配公司
        try:
            company = ak.stock_individual_info_em(symbol=code)
            name = company.iloc[5][1]
        except KeyError:
            messagebox.showerror(f"{code}：无法匹配\n")
            continue
        # 从同花顺获取关键财务指标
        try:
            data = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
            data = data.set_index(data.columns[0])
            print(data.columns)
            print(data)
            data_c = data.copy()

            b_is_asset_liability_ratio = False
            b_is_operating_income = False
            b_is_net_profit = True
            if b_is_asset_liability_ratio:
                # data = data[['净利润', '营业总收入', '资产负债率']]
                # data = data[['资产负债率', '营业总收入']]
                data = data[['资产负债率']]
                data['资产负债率'] = data['资产负债率'].apply(lambda x: '00' if 'False' == str(x) else x)
                data['资产负债率'] = data['资产负债率'].map(lambda x: str(x)[0:-1])
                data.bfill(inplace=True)
                # print(data)
                # data = data.head(1)
                data['资产负债率'] = data['资产负债率'].astype(float)
                for i in range(len(data)):
                    if data.iloc[i]['资产负债率'] < 0.1 and i > 0:
                        data.iloc[i]['资产负债率'] = data.iloc[i - 1]['资产负债率']
            elif b_is_operating_income:
                data = data[['营业总收入']]
                data['营业总收入'] = data['营业总收入'].apply(lambda x: remove_unit(x) if not 'False' == str(x) else 0)
                # data['资产负债率'] = data['资产负债率'].map(lambda x: str(x)[0:-1])
                data.bfill(inplace=True)
                # data = data.head(1)
                data['营业总收入'] = data['营业总收入'].astype(float)
            elif b_is_net_profit:
                data = data[['净利润']]
                data['净利润'] = data['净利润'].apply(lambda x: remove_unit(x) if not 'False' == str(x) else 0)
                # data['资产负债率'] = data['资产负债率'].map(lambda x: str(x)[0:-1])
                data.bfill(inplace=True)
                # data = data.head(1)
                data['净利润'] = data['净利润'].astype(float)

            print(data)
            data.sort_index(ascending=True, inplace=True)
            data.plot()
            plt.rcParams["font.sans-serif"] = ["SimHei"]
            plt.title(code)
            plt.show()
            plt.close()
        except KeyError:
            messagebox.showerror(f"{code}：{name}获取财报数据失败\n")
            continue


if __name__ == '__main__':
    # main_from_web()
    show_finance_by_code_list(['000001', '000002'])
    messagebox.dump()
