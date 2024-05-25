import matplotlib.pyplot as plt
import akshare as ak
import pandas as pd

from __utils import messagebox


def get_m2_and_gold_price_df():
    spot_hist_sge_df = ak.spot_hist_sge(symbol='Au99.99')
    # print(spot_hist_sge_df)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    spot_hist_sge_df.set_index('date', inplace=True)

    for i_index in range(len(spot_hist_sge_df)):
        # print(pd.to_datetime(spot_hist_sge_df.index[i_index]))
        # print(pd.to_datetime(spot_hist_sge_df.index[i_index]).strftime('%Y年%m月份'))
        spot_hist_sge_df.loc[spot_hist_sge_df.index[i_index], '月份'] = pd.to_datetime(spot_hist_sge_df.index[i_index]).strftime('%Y年%m月份')
        spot_hist_sge_df.loc[spot_hist_sge_df.index[i_index], 'gold_change'] = \
            spot_hist_sge_df.loc[spot_hist_sge_df.index[i_index], 'close']/spot_hist_sge_df.loc[spot_hist_sge_df.index[0], 'close']
    spot_hist_sge_df.set_index('月份', inplace=True)

    # print(spot_hist_sge_df)
    spot_hist_sge_df = spot_hist_sge_df.reset_index().drop_duplicates(subset=['月份'], keep='last').set_index('月份')
    print(spot_hist_sge_df)

    macro_china_money_supply_df = ak.macro_china_money_supply()
    macro_china_money_supply_df.set_index('月份', inplace=True)
    macro_china_money_supply_df.sort_values('月份', ascending=True, inplace=True)

    # m2 数据比 gold 数据历史数据多很多个月份
    macro_china_money_supply_df = macro_china_money_supply_df[macro_china_money_supply_df.index
                                                              >= spot_hist_sge_df.index[0]]
    print(macro_china_money_supply_df)
    df_all = pd.merge(macro_china_money_supply_df, spot_hist_sge_df, on='月份', how='outer')

    # print(df_all)

    for i_index in range(len(df_all)):
        df_all.loc[df_all.index[i_index], 'm2_change'] = \
            df_all.loc[df_all.index[i_index], '货币和准货币(M2)-数量(亿元)'] / df_all.loc[df_all.index[0], '货币和准货币(M2)-数量(亿元)']
        df_all.loc[df_all.index[i_index], 'gold_m2_ratio'] = \
            df_all.loc[df_all.index[i_index], 'gold_change'] / df_all.loc[df_all.index[i_index], 'm2_change']

    df_all = df_all[['m2_change', 'gold_change', 'gold_m2_ratio']]
    # df_all = df_all[['m2_change', 'gold_change']]
    pd.options.display.max_rows = None
    print(df_all)
    # print(df_all.sort_values(by='gold_m2_ratio'))

    return df_all

def check_gold_price():
    df_all = get_m2_and_gold_price_df()

    last_m2_change = 0
    import numpy as np
    # 最后一个月的数据没有及时更新
    if np.isnan(df_all.loc[df_all.index[-1], 'm2_change']):
        last_m2_change = df_all.loc[df_all.index[-2], 'm2_change']
    else:
        last_m2_change = df_all.loc[df_all.index[-1], 'm2_change']

    message_info = ''
    latest_gold_change = df_all.loc[df_all.index[-1], 'gold_change']

    print(f'金价指数={latest_gold_change}, m2指数={last_m2_change}')
    #
    if latest_gold_change / last_m2_change > df_all['gold_m2_ratio'].quantile(0.95):
        message_info = '金价涨幅除以M2涨幅高于95分位了，卖出黄金呗！' + f'\n 金价指数：{latest_gold_change} m2指数：{last_m2_change}'
    elif latest_gold_change / last_m2_change < df_all['gold_m2_ratio'].quantile(0.05):
        message_info = '金价涨幅除以M2涨幅低于0.05分位了，抄底黄金呗！' + f'\n 金价指数：{latest_gold_change} m2指数：{last_m2_change}'

    if len(message_info) > 0:
        messagebox.showwarning('警告', message_info)
        df_all = df_all[['m2_change', 'gold_change']]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        df_all.plot(figsize=(20, 12))
        plt.show()
        plt.close()


if __name__ == '__main__':
    check_gold_price()
