# https://www.runoob.com/python/python-gui-tkinter.html
# !/usr/bin/python
# -*- coding: UTF-8 -*-



# Python3.x 导入方法
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from __utils import messagebox

__all__ = ["collect_result", "show_result"]

labels = []
values = []

def collect_result(label='标签1', value=("", "", "")):
    labels.append(label)
    values.append(value)
    messagebox.logger.warning(value)

def show_result():
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


if __name__ == '__main__':
    collect_result(label="1", value=("A1", "This is a very long piece of text that needs to be wrapped in the TreeView widget in order to be completely visible.", "C1"))
    collect_result(label="2", value=("A2", "B2", "C2"))
    show_result()