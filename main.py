# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings

import tushare as ts



def get_total_flow_value():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import time
    from selenium.webdriver.common.by import By



    # 启动chromedriver
    chromedriver_path = "D:\Program Files (x86)\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 指定ChromeDriver的路径
    service = Service(chromedriver_path)
    service.start()




    # 建立会话
    options = Options()
    options.binary_location = "D:\Program Files (x86)\chrome-win64\chrome-win64\chrome.exe"  # 指定Chrome浏览器的路径
    driver = webdriver.Remote(service.service_url, options=options)



    driver.get('https://www.sse.com.cn/')
    time.sleep(3)

    # print(driver.page_source)  #https://cuiqingcai.com/2599.html

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print('++++++++++++++https://www.sse.com.cn/ page source +++++++++++++++++++')
    print(soup.prettify())
    print('--------------https://www.sse.com.cn/ page source --------------')


    # 定位<script>标签
    script_tag = soup.find_all('script')

    for script_content in script_tag:
        print('========')
        print(script_content.string)

    # 提取变量内容
    script_content = script_tag[0].string

    # 输出结果
    print('++++++++++++++https://www.sse.com.cn/ page source script +++++++++++++++++++')
    print(script_content)
    print('--------------https://www.sse.com.cn/ page source script --------------')


    result_shanghai = driver.execute_script('return home_sjtj.negotiable_value')

    print('result 上证总流通市值 = ', result_shanghai)




    driver.get('https://www.szse.cn/index/index.html')
    time.sleep(3)


    # print(driver.page_source)  #https://cuiqingcai.com/2599.html

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print('++++++++++++++https://www.szse.cn/index/index.html page source +++++++++++++++++++')
    print(soup.prettify())
    print('--------------https://www.szse.cn/index/index.html page source --------------')


    # element = driver.find_element(by=By.CLASS_NAME, value="hqicon hqicon- hqicon2")
    # element = driver.find_element(by=By.CLASS_NAME, value="hqicon hqicon- hqicon2")

    element = driver.find_element(by=By.CSS_SELECTOR, value="div[class='tab-pane fade in active']")
    print('++++++++++++++https://www.szse.cn/index/index.html div class = tab-pane fade in active element： +++++++++++++++++++')
    print(element)
    print(element.text)
    print('--------------https://www.szse.cn/index/index.html div class = tab-pane fade in active element --------------')

    # element1 = element.find_element(by=By.CSS_SELECTOR, value=".div[class='val']")
    element1 = element.find_elements(by=By.XPATH, value=".//div[@class='val']")

    print('++++++++++++++https://www.szse.cn/index/index.html div class = val second element： +++++++++++++++++++')
    print(element1[1])
    print('result 深证总流通市值 = ', element1[1].text)
    result_shenzhen = element1[1].text
    print('--------------https://www.szse.cn/index/index.html div class = val second element： ------------------')

    driver.quit()

    if float(result_shanghai) < 10000 or float(result_shenzhen) < 10000:
        print('get_total_flow_value return: 0')
        return 0
    else:
        print('get_total_flow_value return: ', float(result_shanghai) + float(result_shenzhen))
        return float(result_shanghai) + float(result_shenzhen)


def check_bafeite_index():
    total_flow_value = get_total_flow_value()
    current_GDP = 1210000

    if total_flow_value > current_GDP:
        print('！！！！！！！！！！中国巴菲特指标已经高于100%，极度风险，请清仓！！！！！！！！！！')

    if total_flow_value < current_GDP * 0.47:
        print('！！！！！！！！！！中国巴菲特指标已经低于47%，再去看看平均市盈率'
              '以及破净股个数、价值股下跌幅度，接近满仓吧！！！！！！！！！！')

    if total_flow_value < current_GDP * 0.37:
        print('！！！！！！！！！！中国巴菲特指标已经低于37%，卖房加仓吧！！！！！！！！！！')

    print('check_bafeite_index: 当前中国巴菲特指标是 ', total_flow_value / current_GDP)


def get_stock_data_from_tushare():
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # from bs4 import BeautifulSoup
    # import requests
    #
    # url = 'http://finance.sina.com.cn/stock/'
    #
    # response = requests.get(url)
    #
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # print(soup.prettify())

    import requests
    from bs4 import BeautifulSoup



    # # stock_code = 'sz002682'
    # # url = f'http://finance.sina.com.cn/realstock/company/{stock_code}/nc.shtml'
    #
    # url = f'https://www.sse.com.cn/'
    # # url = f'https://www.szse.cn/market/stock/indicator/index.html'
    #
    #
    # response = requests.get(url)
    #
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # print(soup.prettify())
    #
    #
    # print('+=========================')
    #
    # trs=soup.find_all('tbody')
    # for tr in trs:
    #     print(tr)
    #
    #
    # print('-=========================')




    # 如何用Python爬数据
    # https: // zhuanlan.zhihu.com / p / 34206711?utm_source = com.tencent.tim

    # from requests_html import HTMLSession
    #
    # session = HTMLSession()
    # url = 'https://www.sse.com.cn/'
    # # url = 'https://www.jianshu.com/p/85f4624485b9'
    #
    # r = session.get(url)
    # print(r.html.text)
    #
    # sel = 'body > div.sse_home_row.gray_bg.wow.fadeIn > div > div > div.col-md-5 > div > div.tab_main > div.tab_content.js_marketData > ul > li:nth-child(1) > span.tab_data'
    # # sel = '#__next > div._21bLU4._3kbg6I > div > div._gp-ck > section:nth-child(1) > article > h1:nth-child(127)'
    #
    #
    # results = r.html.find(sel)
    #
    # print('=========++++++===========')
    # print(results)
    # print(results[0].text)
    # print('====================')






    # import webbrowser
    #
    # url = 'www.baidu.com'
    #
    # # 设置使用Chrome浏览器
    # # webbrowser.register('chrome', None,
    # #                     webbrowser.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
    #
    # webbrowser.register('chrome', None,
    #                     webbrowser.BackgroundBrowser("C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"))
    # webbrowser.get('chrome').open(url)

    # import webbrowser
    # import requests
    #
    # # kw = input('百度一下：')
    # url = 'https://data.eastmoney.com/gzfx/'
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0', }
    # response = requests.get(url=url, headers=headers)
    # fileName = 'a.html'
    # with open(fileName, 'w', encoding='utf-8') as fp:
    #     fp.write(response.text)
    # webbrowser.open(fileName)

    # check_bafeite_index()
    get_stock_data_from_tushare()










    # ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')
    # pro = ts.pro_api()
    #
    # # 示例
    # # df = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')
    # # print(df)
    #
    # #获取某一天的总市值
    #
    # df = pro.daily(trade_date='20180810')
    # print(df)
    # print('=================================')
    # df = pro.daily(trade_date='20231027')
    # print(df)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def get_stock_data_from_tushare():

    return


