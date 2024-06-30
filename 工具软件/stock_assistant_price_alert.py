from __utils import messagebox

# 超过目标价位进行告警
# 涨跌幅过大进行告警

dic_target_price_a = {
    '001979': (15, '招商蛇口'),
    '300059': (20, '东方财富'),
    '000006': (5, '深振业'),
    '000069': (5.2, '华侨城'),
    '002918': (16, '蒙娜丽莎'),
    '601828': (5.2, '美凯龙'),
    '601933': (3.3, '永辉超市'),
    '600837': (16.66, '海通证券'),
    '002739': (25, '万达电影'),
    '000538': (75, '云南白药'),
    '601111': (9.13, '中国国航'),
    '600153': (8.9, '建发股份')
}

dic_target_price_us = {'AAL': (19, '美国航空'),
                       'BILI': (18, '哔哩哔哩'),
                       'SE': (100, 'Sea'),
                       'ORGN': (2, 'Origin Materials')
                       }

dic_target_price_hk = {
    '01024': (100, '快手'),
    '02007': (2, '碧桂园'),
    '09868': (90, '小鹏汽车'),
    '02777': (2.03, '富力地产'),
    '02202': (13, '万科企业')
}


def check_price():
    # for key, value in dic_target_price_us.items():
    #     print(value[1], f'目标价格={value[0]}', ':')
    #     data, meta_data = ts.get_intraday(key)
    #     print(data)
    # exit(0)

    import akshare as ak

    for key, value in dic_target_price_a.items():
        print(value[1], f'目标价格={value[0]}', ':')
        df = ak.stock_zh_a_hist(symbol=key, adjust="qfq")
        # print(df)
        # print(df.columns)
        current_price = df.iloc[-1]['收盘']
        last_price = df.iloc[-2]['收盘']
        # print(current_price, last_price)

        if len(df) < 1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  没有获取到数据 !!!!!!!!!!!!!!!!!!!!')
            continue

        # 跳过未开盘的情况
        if float(current_price) < 0.1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  获取到的当前价格小于0.1 !!!!!!!!!!!!!!!!!!!!')
            continue

        if float(current_price) > value[0]:
            print(f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')

        if float(current_price) > float(last_price) * 1.09 or \
                float(current_price) * 1.09 < float(last_price):
            print(f'!!!!!!!!!!!  {value[1]} too much turbulence !!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!! {value[1]} too much turbulence '
                                        f'\n change={current_price/last_price} '
                                        f'\n current_price={current_price}'
                                        f'\n last_price={last_price}!!!!!!!!!!!!!!!!!!!!')

    for key, value in dic_target_price_us.items():
        print(value[1], f'目标价格={value[0]}', ':')
        df = ak.stock_us_daily(symbol=key, adjust="qfq")
        # print(df)
        # print(df.columns)
        current_price = df.iloc[-1]['close']
        last_price = df.iloc[-2]['close']
        # print(current_price, last_price)

        if len(df) < 1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  没有获取到数据 !!!!!!!!!!!!!!!!!!!!')
            continue

        # 跳过未开盘的情况
        if float(current_price) < 0.1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  获取到的当前价格小于0.1 !!!!!!!!!!!!!!!!!!!!')
            continue

        if float(current_price) > value[0]:
            print(f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')

        if float(current_price) > float(last_price) * 1.09 or \
                float(current_price) * 1.09 < float(last_price):
            print(f'!!!!!!!!!!!  {value[1]} too much turbulence !!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!! {value[1]} too much turbulence '
                                        f'\n change={current_price/last_price} '
                                        f'\n current_price={current_price}'
                                        f'\n last_price={last_price}!!!!!!!!!!!!!!!!!!!!')

    for key, value in dic_target_price_hk.items():
        print(value[1], f'目标价格={value[0]}', ':')
        df = ak.stock_hk_daily(symbol=key, adjust="qfq")
        # print(df)
        # print(df.columns)
        current_price = df.iloc[-1]['close']
        last_price = df.iloc[-2]['close']
        # print(current_price, last_price)

        if len(df) < 1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  没有获取到数据 !!!!!!!!!!!!!!!!!!!!')
            continue

        # 跳过未开盘的情况
        if float(current_price) < 0.1:
            messagebox.showerror('出错', f'!!!!!!!!!!!  获取到的当前价格小于0.1 !!!!!!!!!!!!!!!!!!!!')
            continue

        if float(current_price) > value[0]:
            print(f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')

        if float(current_price) > float(last_price) * 1.09 or \
                float(current_price) * 1.09 < float(last_price):
            print(f'!!!!!!!!!!!  {value[1]} too much turbulence !!!!!!!!!!!!!!!!!!!!')
            messagebox.showinfo('提示', f'!!!!!!!!!!! {value[1]} too much turbulence '
                                        f'\n change={current_price/last_price} '
                                        f'\n current_price={current_price}'
                                        f'\n last_price={last_price}!!!!!!!!!!!!!!!!!!!!')

#
# def check_a_price():
#     dic_target_price_a = {
#         '001979.SZ': (15, '招商蛇口'),
#         '300059.SZ': (10, '东方财富'),
#         '000006.SZ': (5, '深振业'),
#         '000069.SZ': (5.2, '华侨城'),
#         '002918.SZ': (16, '蒙娜丽莎'),
#         '601828.SH': (5.2, '美凯龙'),
#         '601933.SH': (3.3, '永辉超市'),
#         '600837.SH': (16.66, '海通证券'),
#         '002739.SZ': (25, '万达电影'),
#         '000538.SZ': (75, '云南白药'),
#         '601111.SH': (9.13, '中国国航')
#     }
#     # 设置你的token，登录tushare在个人用户中心里拷贝
#     ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')
#
#     """
#     #sina数据
#     df = ts.realtime_quote(ts_code='600000.SH,000001.SZ,000001.SH')
#     print(f'==============sina============\n{df}\n ==============sina end============\n')
#
#     #东财数据
#     df = ts.realtime_quote(ts_code='600000.SH', src='dc')
#     print(f'==============dongcai============\n{df}\n ==============dongcai end============\n')
#     """
#
#     # 到价提醒
#     print(f'++++++++++++++++++++++++ 到价提醒 A股 begin ++++++++++++++++++++++++\n')
#
#     for key, value in dic_target_price_a.items():
#         print(value[1], f'目标价格={value[0]}', ':')
#         df = ts.realtime_quote(ts_code=key)
#         # print(df)
#         # print(df.columns)
#         # print(df.iloc[0]['PRICE'])
#
#         current_price = df.iloc[0]['PRICE']
#         last_price = df.iloc[0]['PRE_CLOSE']
#
#         # 跳过未开盘的情况
#         if float(current_price) < 0.1:
#             continue
#
#         if float(current_price) > value[0]:
#             print(f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
#             messagebox.showinfo('提示', f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
#
#         if float(current_price) > float(last_price) * 1.09 or \
#                 float(current_price) * 1.09 < float(last_price):
#             print(f'!!!!!!!!!!!  {value[1]} too much turbulence !!!!!!!!!!!!!!!!!!!!')
#             messagebox.showinfo('提示', f'!!!!!!!!!!! {value[1]} too much turbulence change={current_price/last_price} current_price={current_price} last_price={last_price}!!!!!!!!!!!!!!!!!!!!')
#
#     print(f'---------------------到价提醒 A股 end----------------------------------\n')
#


def stock_assistant_price_alert_main():
    messagebox.logger.warning('===begin.')
    check_price()
    messagebox.logger.warning('===finished.')
    # check_a_price()


if __name__ == '__main__':
    stock_assistant_price_alert_main()
