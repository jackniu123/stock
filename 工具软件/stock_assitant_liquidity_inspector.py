import datetime
import json
import os.path
import time
from __utils import messagebox
from __utils import result_overview
# 市场京流动性：https://sc.macromicro.me/charts/81331/mei-guo-shi-chang-jing-liu-dong-xing-yu-sp500

def find_data(main_url='https://sc.macromicro.me/charts/81331/mei-guo-shi-chang-jing-liu-dong-xing-yu-sp500',
              match_url=None, match_content=None) -> str:
    # -*- coding: utf-8 -*-
    # @Time   : 2022-08-27 11:59
    # @Name   : selenium_cdp.py

    import json
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
    # options.add_argument('--start-minimized')
    # options.add_argument('--no-startup-window')
    options.add_argument('--window-position=2900,2024')
    options.binary_location = "D:\Program Files (x86)\chrome-win64\chrome-win64\chrome.exe"  # 指定Chrome浏览器的路径
    # 启动chromedriver
    chromedriver_path = "D:\Program Files (x86)\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 指定ChromeDriver的路径
    service = Service(chromedriver_path)
    service.start()
    browser = webdriver.Chrome(service=service, options=options)  # 启动浏览器
    # browser.set_window_size(100, 50)
    browser.minimize_window()
    browser.get(main_url)  # 访问该url

    # time.sleep(10)

    def filter_type(_type: str):
        types = [
            'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',
            'image/jpeg', 'image/x-icon', 'application/octet-stream'
        ]

        if _type not in types:
            return True
        return False

    i = 0
    while True:
        performance_log = browser.get_log('performance')  # 获取名称为 performance 的日志
        if len(performance_log) < 10:
            print('no data received!')
            i = i + 1

        if i > 5:
            messagebox.logger.warning('!!!no data received.')
            break

        for packet in performance_log:
            message = json.loads(packet.get('message')).get('message')  # 获取message的数据
            if message.get('method') != 'Network.responseReceived':  # 如果method 不是 responseReceived 类型就不往下执行
                continue
            packet_type = message.get('params').get('response').get('mimeType')  # 获取该请求返回的type
            if not filter_type(_type=packet_type):  # 过滤type
                continue
            requestId = message.get('params').get('requestId')  # 唯一的请求标识符。相当于该请求的身份证
            url = message.get('params').get('response').get('url')  # 获取 该请求  url
            try:
                resp = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})  # selenium调用 cdp
                print(f'type: {packet_type} url: {url}')
                try:
                    print(f'response: {resp}')
                except Exception as e:
                    print("!!!\033[0;31;40m", e, "\033[0m")
                if match_url and match_content:
                    if match_url in url and match_content in resp:
                        return resp['body']
                if match_url and match_url in url:
                    return resp['body']
                if match_content and match_content in resp:
                    return resp['body']
            except WebDriverException:  # 忽略异常
                pass
        time.sleep(10)
        print(100*'=')


    return ''


def check_liquidity_chance_and_risk():
    messagebox.logger.warning('===begin.')
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    # 128,678
    if not os.path.exists('found_data.txt') \
            or (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getctime('found_data.txt'))).days > 0:
        found_data = find_data(
            main_url='https://sc.macromicro.me/charts/81331/mei-guo-shi-chang-jing-liu-dong-xing-yu-sp500',
            match_url='https://sc.macromicro.me/charts/data/81331')

        if len(str(found_data)) > 10:

            print('before json.load:', found_data)
            found_data = json.loads(found_data)
            print('after json.load:', found_data)
            found_data = found_data['data']['c:81331']['series']
            print('after index:', found_data)

            if os.path.exists('found_data.txt'):
                os.remove('found_data.txt')
            with open('found_data.txt', 'w') as f:
                f.write(str(found_data))
                f.close()
        else:
            messagebox.logger.warning('!!!failed to update data because no data received.')
            return

    # with open('test.json', 'r') as f:
    with open('found_data.txt', 'r') as f:
        str_data = f.read()
        f.close()
        # print(str_data)
        data_list = eval(str_data)
        # print(100*"=")

        df_liquidity = pd.DataFrame(data_list[0], columns=['date', 'liquidity'])
        df_index = pd.DataFrame(data_list[1], columns=['date', 'stock_index'])

        df_liquidity.set_index('date', inplace=True)
        df_index.set_index('date', inplace=True)

        # print(df_liquidity)
        # print(df_index)
        # print('===================')
        # print(df_liquidity.dtypes)
        # print(df_index.dtypes)

        df_all = pd.merge(df_liquidity, df_index, on=['date'], how='outer')
        df_all.sort_index(inplace=True)
        df_all.ffill(inplace=True)
        df_all.bfill(inplace=True)
        df_all['stock_index'] = df_all['stock_index'].astype(float)

        print('last 10 days data: ', df_all['liquidity'].tail(10))
        # liquidity_delta = 0
        # i = -2
        # while liquidity_delta == 0:
        #     liquidity_delta = df_all['liquidity'][-1] - df_all['liquidity'][i]
        #     i = i - 1

        # print('\n\ncurrent liquidity:\n', df_all.iloc[-1],
        #       '\nlast liquidity:\n', df_all.iloc[i+1],
        #       '\nliquidity delta:', liquidity_delta)

        # df_all = (df_all - df_all.min()) / (df_all.max()-df_all.min())
        # df_all.plot()
        # plt.show()
        # plt.close()

        df_all_delta = df_all.diff(1) / df_all

        print(f'\n\ndf_all_delta.tail(50) = \n {df_all_delta.tail(50)}')

        last_liquidity_delta_scaled = 0
        last_liquidity_release_date = ''
        i = 1
        while last_liquidity_delta_scaled == 0:
            last_liquidity_delta_scaled = df_all_delta['liquidity'][-i]
            last_liquidity_release_date = df_all_delta.index[-i]
            i = i + 1
        print('last liquidity delta:', last_liquidity_delta_scaled)

        liquidity_delta_95 = df_all_delta['liquidity'].quantile(0.95)
        print('liquidity delta 95分位数：', liquidity_delta_95)
        liquidity_delta_05 = df_all_delta['liquidity'].quantile(0.05)
        print('liquidity delta 05分位数：', liquidity_delta_05)

        if last_liquidity_delta_scaled > liquidity_delta_95:
            # messagebox.showwarning('警告', f'流动性大幅提升，请关注买入机会！\n '
            #                                f'last_liquidity_delta_scaled = {last_liquidity_delta_scaled} \n '
            #                                f'0.95分位数是{liquidity_delta_95}\n '
            #                                f'最近的流动性数据发布日期是：{last_liquidity_release_date}')
            result_overview.collect_result(label='流动性变化', value=(f'流动性大幅提升！\n '
                                                                 f'流动性提升幅度 = {last_liquidity_delta_scaled} \n'
                                                                 f'0.95分位数是{liquidity_delta_95}\n '
                                                                 f'最近的流动性数据发布日期是：{last_liquidity_release_date}', "", ""))
        elif last_liquidity_delta_scaled < liquidity_delta_05:
            # messagebox.showwarning('警告', f'流动性大幅减少，请关注风险，及时卖出！\n '
            #                                f'last_liquidity_delta_scaled = {last_liquidity_delta_scaled} \n '
            #                                f'0.05分位数是{liquidity_delta_05}\n '
            #                                f'最近的流动性数据发布日期是：{last_liquidity_release_date}')
            result_overview.collect_result(label='流动性变化', value=("", "", f'流动性大幅下降\n '
                                                                 f'流动性降低幅度 = {last_liquidity_delta_scaled} \n'
                                                                 f'0.05分位数是{liquidity_delta_05}\n '
                                                                 f'最近的流动性数据发布日期是：{last_liquidity_release_date}'))
        else:
            result_overview.collect_result(label='流动性变化', value=("", f'流动性平稳\n '
                                                                 f'last_liquidity_delta_scaled = {last_liquidity_delta_scaled} \n'
                                                                 f'0.95分位数是{liquidity_delta_95}\n '
                                                                 f'最近的流动性数据发布日期是：{last_liquidity_release_date}', ""))
        messagebox.logger.warning('===end.')


if __name__ == "__main__":
    check_liquidity_chance_and_risk()