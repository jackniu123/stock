import datetime
import sys
sys.path.append('D:/不要删除牛爸爸的程序/') # 绝对路径
from __utils import messagebox

import akshare as ak
from stock_assistant_price_alert import dic_target_price_a

def stock_assistant_add_main():
    for key, value in dic_target_price_a.items():
        try:
            print(value[1], "增发日历:")
            stock_add_stock_df = ak.stock_add_stock(symbol=key)

            for index, row in stock_add_stock_df.iterrows():
                print(index, ":", row['公告日期'])
                if (row['公告日期'] - datetime.datetime.now().date()).days >= 0:
                    print("!!! 这支股票要增发，妈的。")
                    messagebox.showerror('警告', f"{{{value[1]}}} 增发日期是 {{{row['公告日期']}}}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    stock_assistant_add_main()
