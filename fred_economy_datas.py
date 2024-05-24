# https://fredaccount.stlouisfed.org/login/secure/#
import os.path

# https://zhuanlan.zhihu.com/p/464169438


from fredapi import Fred
import requests
import numpy as np
import pandas as pd
import datetime as dt


def fetch_releases(api_key):
    """
    取得 FRED 大分类信息
    Args:
        api_key (str): 秘钥
    """
    # print('fetch_releases: before send request')
    r = requests.get('https://api.stlouisfed.org/fred/releases?api_key=' + api_key + '&file_type=json', verify=True)
    # print('fetch_releases: after send request:', r)
    full_releases = r.json()['releases']
    full_releases = pd.DataFrame.from_dict(full_releases)
    full_releases = full_releases.set_index('id')
    # full_releases.to_csv("full_releases.csv")
    return full_releases

# import pysnooper
# @pysnooper.snoop()
def fetch_release_id_data(release_id):
    """
    按照分类ID获取数据

    Args:
        release_id (int): 大分类ID

    Returns:
        dataframe: 数据
    """
    econ_data = pd.DataFrame(index=pd.date_range(start='1950-01-01', end=dt.datetime.today(), freq='MS'))
    series_df = fred.search_by_release(release_id, limit=3, order_by='popularity', sort_order='desc')
    for topic_label in series_df.index:
        econ_data[series_df.loc[topic_label].title] = fred.get_series(topic_label, observation_start='1950-01-01',
                                                                      observation_end=dt.datetime.today())
    return econ_data


m2_file_name = "m2.csv"


def update_m2():
    global m2_file_name
    if os.path.exists(m2_file_name):
        import time
        # m2.csv文件上次更新不到一天的间隔，继续用吧，不用更新
        if time.time() - os.path.getmtime(m2_file_name) < 24 * 60 * 60:
            return
        # print(f'creation time of {m2_file_name}:{time.ctime(os.path.getctime(m2_file_name))}')
        # print(f'last modification time of {m2_file_name}:{time.ctime(os.path.getmtime(m2_file_name))}')
        # print(f'current time: {time.ctime(time.time())}')
        # print('elapsed time:', time.time() - os.path.getmtime(m2_file_name))

    api_key = '98e80f259dcaebd91fae32adce6430d4'

    # print('Fred: before')
    fred = Fred(api_key)
    # print('Fred: after')

    full_releases = fetch_releases(api_key)

    print(full_releases)

    # keywords = ["producer price", "consumer price", "fomc", "manufacturing", "employment"]

    keywords = ["m2"]

    for search_keywords in keywords:
        print('\n\nprocess:', search_keywords)
        search_result = full_releases.name[full_releases.name.apply(lambda x: search_keywords in x.lower())]
        econ_data = pd.DataFrame(index=pd.date_range(start='1950-01-01', end=dt.datetime.today(), freq='MS'))

        for release_id in search_result.index:
            print("scraping release_id: ", release_id)
            econ_data = pd.concat([econ_data, fetch_release_id_data(release_id)], axis=1)
        print('econ_data:\n', econ_data)
        econ_data.to_csv(f"{search_keywords}.csv")

        # import matplotlib.pyplot as plt
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # econ_data.plot(figsize=(20, 12))
        # plt.show()
        # plt.close()

# if __name__ == '__main__':
#     update_m2()

#
# # https://zhuanlan.zhihu.com/p/341254102
# # https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
# # https://blog.csdn.net/weixin_38544360/article/details/94022670
# import numpy as np
# import pandas as pd
# import pandas_datareader.data as web
# import math
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import pymysql
# import datetime
#
#
# # 连接数据库
# def connect():
#     conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='mysql123', db='stock', charset='utf8')
#     return conn
#
#
# # 关闭数据库连接
# def close(conn):
#     conn.close()
#
#
# # 查询数据库
# def select(sql):
#     conn = connect()
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     # print("cursor.excute:",cursor.rowcount)
#     # rs = cursor.fetchone()
#     rs = cursor.fetchall()
#     close(conn)
#     return rs
#
#
# # 查询最近一天
# def getLastTransDate():
#     statement = 'select max(date) from t_gold '
#     rs = select(statement)
#     if rs[0][0] is None:
#         startDate = '1960-01-01'
#     else:
#         startDate = rs[0][0].strftime('%Y-%m-%d')
#     return startDate
#
#
# def main():
#     startDate = getLastTransDate()
#     # https://fred.stlouisfed.org/series/IQ12260
#     df = web.DataReader(name='IQ12260', data_source='fred', start=startDate)
#     print(df.info())
#     print(df)
#     # df.to_csv(r'./test.csv',encoding='gbk')
#     # df.plot()
#     # plt.show()
#
#     connect = create_engine('mysql+pymysql://root:mysql123@127.0.0.1:3306/stock?charset=utf8')
#
#     df.to_sql('t_gold', con=connect, if_exists='append', index=True)
#
#
# if __name__ == '__main__':
#     # main()
#
# '''
# CREATE TABLE `t_gold` (
#   `DATE` datetime DEFAULT NULL,
#   `GOLDAMGBD228NLBM` double DEFAULT NULL,
#   KEY `ix_t_gold_DATE` (`DATE`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
# '''



# 2、显示黄金价格趋势图，goldTrends.py
#
# 使用pandas
# 读取mysql数据库，使用matplotlib.pyplot
# 画价格曲线
#
# import numpy as np
# import pandas as pd
# import pandas_datareader.data as web
# import math
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import pymysql
# import datetime
#
#
# # 绘制图形
# def drawTrends(startDate):
#     connect = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/finance_db?charset=utf8')
#     sql = 'select * from t_gold where date>=\'' + startDate + '\''
#     # print(sql)
#
#     df = pd.read_sql_query(sql, connect)
#     # print(df.info())
#     df2 = df[['DATE', 'GOLDAMGBD228NLBM']]
#     df2['DATE'] = pd.to_datetime(df2['DATE'])
#     df2 = df2[['DATE', 'GOLDAMGBD228NLBM']]
#     df2 = df2.sort_values(['DATE'])
#     df2 = df2.set_index('DATE')
#     ax = df2.plot(kind='line', title="Gold Price Change")
#     ax.set_xlabel("Period", fontsize=12)
#     ax.set_ylabel("Price", fontsize=12)
#
#     plt.show()
#
#
# def main():
#     startDate = input('请输入起始日期【yyyy-mm-dd】：')
#     drawTrends(startDate)
#
#
# if __name__ == '__main__':
#     main()



#
# # https://blog.csdn.net/donglxd/article/details/136293289
#
# import requests
# from bs4 import BeautifulSoup as bs4
# from datetime import datetime, timezone
# import json
# import pandas as pd  # 引入pandas库
# import time
#
#
# def time_to_date(time):
#     timestamp = time / 1000 + 24 * 60 * 60
#     return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')
#
#
# def date_to_time(date):
#     date_format = '%Y-%m-%d'
#     date_obj = datetime.strptime(date, date_format)
#     timestamp_seconds = date_obj.timestamp()
#     timestamp_milliseconds = int(timestamp_seconds * 1000)
#     return timestamp_milliseconds
#
#
# # 修改printout函数来收集数据到DataFrame
# def printout(pagecount, pageSize, json_data, data_style, all_data):
#     count = 0
#     for index in range(pageSize - 1, -1, -1):
#         item = json_data["data"][data_style][index]
#         count += 1
#         date = time_to_date(item["time"])
#         price_style = {"JO_52683": "基础", "JO_52684": "零售", "JO_52685": "回收"}.get(data_style, "")
#         # 收集数据而不是打印
#         all_data.append({"日期": date, "金价类型": price_style, "金价": item['q1']})
#         print(f"第{pagecount}页_{count}:日期:{date}, {price_style}金价:{item['q1']}元")
#
#
# def getPageData(pageSize, pagecount, data_style, header, time, all_data):
#     res = requests.get(
#         "https://api.jijinhao.com/quoteCenter/historys.htm?codes=" + data_style + "&style=3&pageSize=" + str(
#             pageSize) + "&currentPage=" + str(pagecount) + "&_=" + str(time), headers=header)
#     quote_json_str = res.content.decode("utf-8")
#     quote_json = json.loads(quote_json_str[4:].replace("quote_json = ", ""))
#     printout(pagecount, pageSize, quote_json, data_style, all_data)
#
#
# header = {
#     'Host': 'api.jijinhao.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
#     'Referer': 'https://quote.cngold.org/gjs/swhj_zghj.html'
# }
#
#
# def main():
#     date_str = datetime.now().strftime('%Y-%m-%d')
#     time = date_to_time(date_str)
#     pageSize = 10
#     data_style = 'JO_52684'
#     all_data = []  # 初始化一个列表来收集所有数据
#     pageMax = 326  # 如数据更新,请增加这里的总页数.
#     for count in range(pageMax + 1):
#         getPageData(pageSize, count, data_style, header, time, all_data)
#
#     # 创建DataFrame
#     df = pd.DataFrame(all_data)
#
#     # 写入Excel文件
#     df.to_excel('gold_prices.xlsx', index=False, engine='openpyxl')
#     print("写入excel文档已完成!")
#
#
# if __name__ == "__main__":
#     main()


