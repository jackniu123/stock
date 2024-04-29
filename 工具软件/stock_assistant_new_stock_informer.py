# -*- coding = utf-8 -*-
import datetime
import re
import requests

from tkinter import messagebox

response = requests.get('https://data.eastmoney.com/xg/xg/calendar.html')

# print(response.text)

if __name__ == '__main__':
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
                                                           + '\n当前时间：' + str(datetime.datetime.now().date())
                                                           + '\n股票名称：' + dic['SECURITY_NAME_ABBR'])
                                else:
                                    messagebox.showinfo('提示', '申购日期：' + dic['TRADE_DATE']
                                                        + ' 当前时间：' + str(datetime.datetime.now().date())
                                                        + ' 股票名称：' + dic['SECURITY_NAME_ABBR'])

    except Exception as e:
        messagebox.showerror('出错了', e)

    from stock_assistant_good_chance import check_MA20_percent
    check_MA20_percent()

