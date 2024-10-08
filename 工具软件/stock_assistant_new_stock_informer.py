# -*- coding = utf-8 -*-
import datetime
import re
import requests

from 工具软件.stock_assistant_good_chance_gold_price_alert import check_gold_price
from __utils import messagebox


def stock_assistant_new_stock_informer_main():
    messagebox.logger.warning('===begin.')

    response = requests.get('https://data.eastmoney.com/xg/xg/calendar.html')

    try:
        i = 0
        for item in response.text.splitlines():
            i += 1

            if 'calendardata' in item:
                print( i, ":" , item )
                print('========================================================')
                j = 0
                for line in re.split('{', item):
                    j += 1
                    if '申购' in line:
                        print(j, ":", line)
                        for days in range(0, 30):
                            if 'TRADE_DATE":"'+str(datetime.datetime.now().date()+datetime.timedelta(days)) in line:
                                line = "{" + line
                                line = line[:-1]
                                print('即将发生的申购：',line)

                                dic = eval(line)

                                if days <= 1:
                                    messagebox.showwarning('警告', '申购日期：' + dic['TRADE_DATE']
                                                           + '\n !!!!!!!!!!!!!!!!今天申购!!!!!!!!!!!!!!!!!!!!!!!!!!'
                                                           + '\n当前时间：' + str(datetime.datetime.now().date())
                                                           + '\n股票名称：' + dic['SECURITY_NAME_ABBR'])
                                else:
                                    messagebox.showinfo('提示', '申购日期：' + dic['TRADE_DATE']
                                                        + ' 当前时间：' + str(datetime.datetime.now().date())
                                                        + ' 股票名称：' + dic['SECURITY_NAME_ABBR'])

    except Exception as e:
        messagebox.showerror('出错了', e)

    from stock_assistant_good_chance import check_MA20_percent, check_buffet_index, check_ipo, check_below_net_asset, \
        check_high_low_statictics_legu, check_high_low_turnover_statictics_legu
    from requests import utils

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    utils.default_user_agent = lambda: DEFAULT_USER_AGENT

    check_MA20_percent()
    check_buffet_index()
    check_ipo()
    check_below_net_asset()
    check_high_low_statictics_legu()
    check_high_low_turnover_statictics_legu()
    check_gold_price()

    messagebox.logger.warning('===finished.')


if __name__ == '__main__':
    stock_assistant_new_stock_informer_main()