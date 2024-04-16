# -*- coding = utf-8 -*-
import datetime
import re
import requests

from tkinter import messagebox

response = requests.get('https://data.eastmoney.com/xg/xg/calendar.html')

# print(response.text)

i = 0
for item in response.text.splitlines():
    i += 1

    if 'calendardata' in item:
        print( i, ":" , item )
        print('========================================================')
        j = 0
        for line in re.split('SECURITY_NAME_ABBR', item):
            j += 1
            if '申购' in line:
                print(j, ":", line)
                for days in range(0, 30):
                    if 'TRADE_DATE":"'+str(datetime.datetime.now().date()+datetime.timedelta(days)) in line:
                        print('/n ============================================')
                        print(line)
                        messagebox.showinfo('提示', str(datetime.datetime.now().date()+datetime.timedelta(days)) + line)


