import datetime
from __utils import messagebox

import akshare as ak
from stock_assistant_price_alert import dic_target_price_a
import traceback


def stock_assistant_add_main():
    messagebox.logger.warning('===begin.')

    for key, value in dic_target_price_a.items():
        try:
            print(value[1], "增发日历:")
            stock_add_stock_df = ak.stock_add_stock(symbol=key)

            for index, row in stock_add_stock_df.iterrows():
                print(index, ":", row['公告日期'])
                if (row['公告日期'] - datetime.datetime.now().date()).days >= 0:
                    print("!!! 这支股票要增发，妈的。")
                    messagebox.showerror('警告', f"{{{value[1]}}} 增发日期是 {{{row['公告日期']}}}")
        except TypeError as te:
            te_msg = f'{traceback.format_exc()}'
            if '无增发' in te_msg:
                print('found TypeError: \n', f'{traceback.format_exc()}')
            else:
                messagebox.showerror('出错了', te_msg)
        except:
            messagebox.showerror('出错了', f'{traceback.format_exc()}')

    messagebox.logger.warning('===finished.')


if __name__ == '__main__':
    stock_assistant_add_main()
    messagebox.dump()