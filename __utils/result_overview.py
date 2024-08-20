# https://www.runoob.com/python/python-gui-tkinter.html
# !/usr/bin/python
# -*- coding: UTF-8 -*-
from time import sleep
# Python3.x 导入方法
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from __utils import messagebox

__all__ = ["collect_result", "show_result"]

labels = []
values = []

web_info = [("深圳房地产交易数据", "https://zjj.sz.gov.cn/xxgk/ztzl/pubdata/"),
            ("appStore数据", "https://app.diandian.com/app/13uouqg2qvqr7b1/ios?market=1&country=75&id=6466232155"),
            ("深圳市房地产信息平台", "https://zjj.sz.gov.cn:8004/")]

def collect_result(label='标签1', value=("", "", "")):
    labels.append(label)
    values.append(value)
    messagebox.logger.warning(value)

def show_result_bak():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表

    tree = Treeview(root, columns=("A", "B", "C"))

    tree.heading("#0", text="指标名称")
    tree.heading("#1", text="买入信号")  # "#1"也可换成"A"
    tree.heading("#2", text="无所谓")
    tree.heading("#3", text="卖出信号")

    # tree.column('A', width=600)  # 设置列宽
    # tree.column('B', width=300)  # 设置列宽
    # tree.column('C', width=600)  # 设置列宽

    for i in range(len(labels)):
        tree.insert("", "end", text=labels[i], values=values[i])

    # # Create a Style
    # style = ttk.Style()
    # style.configure("CustomTreeview", rowheight=60)
    # # Apply Style to Treeview
    # tree.config(style="CustomTreeview")

    tree.pack()

    # root.geometry("500x500+500+100")
    root.mainloop()  # 进入消息循环


def show_result():

    replace_string = """
        <table style="white-space: pre-line;">
        <tr>
            <th>指标名称</th>
            <th>买入信号</th>
            <th>无所谓</th>
            <th>卖出信号</th>
        </tr>
    """


    for i in range(len(labels)):
        replace_string += f"""
        <tr>
            <td>{labels[i]}</td>
            <td>{values[i][0]}</td>
            <td>{values[i][1]}</td>
            <td>{values[i][2]}</td>
        </tr>
        """

    replace_string += "</table>"

    replace_string_more_data = """
        <a> 先行指标 </a>
        <table style="white-space: pre-line;">
        <tr>
            <th>指标名称</th>
        </tr>
    """

    for i in range(len(web_info)):
        replace_string_more_data += f"""
        <tr>
            <td><a href="{web_info[i][1]}">{web_info[i][0]}</a></td>
        </tr>
        """
    replace_string_more_data += "</table>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang = "en">

    <head>
    <meta charset = "UTF-8">
    <title> Title </title>
    </head>
    
    <style>
    table {{
        border-right: 1px solid #000000;
        border-bottom: 1px solid #000000;
        text-align: left;
    }}
    
    table th {{
        border-left: 1px solid #000000;
        border-top: 1px solid #000000;
    }}
    
    table td {{
        border-left: 1px solid #000000;
        border-top: 1px solid #000000;
    }}
    </style>

    <body>
    <div>
    <h1> 择时信号看板 </h1>
    </div>
    
    {replace_string}
    
    {replace_string_more_data}
    
    </body>

    </html>
    """

    print(html_content)
    # 将HTML内容保存到文件
    with open("D:/不要删除牛爸爸的程序/__utils/result_overview.html", "w", encoding='utf-8') as f:
        f.write(html_content)

    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    options = Options()

    caps = {
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
    }
    # 将caps添加到options中
    for key, value in caps.items():
        options.set_capability(key, value)
    # options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # options.add_argument('--window-size=1,1')  # 指定浏览器分辨率
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    options.add_argument('--start-maximized')
    # options.add_argument('--no-startup-window')
    # options.add_argument('--window-position=2900,2024')
    options.binary_location = "D:\Program Files (x86)\chrome-win64\chrome-win64\chrome.exe"  # 指定Chrome浏览器的路径
    # 启动chromedriver
    chromedriver_path = "D:\Program Files (x86)\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 指定ChromeDriver的路径
    service = Service(chromedriver_path)
    service.start()
    browser = webdriver.Chrome(service=service, options=options)  # 启动浏览器
    # browser.set_window_size(1000, 700)
    browser.get("D:/不要删除牛爸爸的程序/__utils/result_overview.html")
    sleep(1000)

if __name__ == '__main__':
    collect_result(label="1", value=("A1", "This is a very long piece of text that needs to be wrapped in the TreeView widget\r\n in order to be completely visible.", "C1"))
    collect_result(label="2", value=("A2", "B2", "C2"))
    show_result()