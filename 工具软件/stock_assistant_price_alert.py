import tushare as ts

# 超过目标价位进行告警
# 涨跌幅过大进行告警


from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='你的API Key')
data, meta_data = ts.get_intraday('OXY')
print(data)


exit(0)



if __name__ == '__main__':
    #设置你的token，登录tushare在个人用户中心里拷贝
    ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')

    """
    #sina数据
    df = ts.realtime_quote(ts_code='600000.SH,000001.SZ,000001.SH')

    print(f'==============sina============\n{df}\n ==============sina end============\n')
        #东财数据
    df = ts.realtime_quote(ts_code='600000.SH', src='dc')

    print(f'==============dongcai============\n{df}\n ==============dongcai end============\n')
    
    """

    # 查询当前股价
    print(f'++++++++++++++++++++++++ sina ++++++++++++++++++++++++\n')
    dic_target_price = {'001979.SZ': (15, '招商蛇口'),
                        '300059.SZ': (20, '东方财富'),
                        '000006.SZ': (5, '深振业'),
                        '000069.SZ': (5.2, '华侨城'),
                        '002918.SZ': (16, '蒙娜丽莎'),
                        '601828.SH': (5.2, '美凯龙')
                        }

    for key, value in dic_target_price.items():
        df = ts.realtime_quote(ts_code=key)
        # print(df)
        # print(df.columns)
        # print(df.iloc[0]['PRICE'])
        print(value[0], value[1])
        if float(df.iloc[0]['PRICE']) > value[0]:
            print(f'!!!!!!!!!!!  we can sell {value[1]}!!!!!!!!!!!!!!!!!!!!')
        if float(df.iloc[0]['PRICE']) > float(df.iloc[0]['PRE_CLOSE']) * 1.09 or \
                float(df.iloc[0]['PRICE']) * 1.09 < float(df.iloc[0]['PRE_CLOSE']):
            print(f'!!!!!!!!!!!  {value[1]} too much turbulence !!!!!!!!!!!!!!!!!!!!')
        print('            ============')



    print(f'-------------------------------------------------------\n')


