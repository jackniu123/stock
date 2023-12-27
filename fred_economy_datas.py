# https://fredaccount.stlouisfed.org/login/secure/#

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
    print('fetch_releases: before send request')
    r = requests.get('https://api.stlouisfed.org/fred/releases?api_key=' + api_key + '&file_type=json', verify=True)
    print('fetch_releases: after send request:', r)
    full_releases = r.json()['releases']
    full_releases = pd.DataFrame.from_dict(full_releases)
    full_releases = full_releases.set_index('id')
    # full_releases.to_csv("full_releases.csv")
    return full_releases

import pysnooper
@pysnooper.snoop()
def fetch_release_id_data(release_id):
    """
    按照分类ID获取数据

    Args:
        release_id (int): 大分类ID

    Returns:
        dataframe: 数据
    """
    econ_data = pd.DataFrame(index=pd.date_range(start='2000-01-01', end=dt.datetime.today(), freq='MS'))
    series_df = fred.search_by_release(release_id, limit=3, order_by='popularity', sort_order='desc')
    for topic_label in series_df.index:
        econ_data[series_df.loc[topic_label].title] = fred.get_series(topic_label, observation_start='2000-01-01',
                                                                      observation_end=dt.datetime.today())
    return econ_data


api_key = '98e80f259dcaebd91fae32adce6430d4'

print('Fred: before')
fred = Fred(api_key)
print('Fred: after')

full_releases = fetch_releases(api_key)

print(full_releases)

keywords = ["producer price", "consumer price", "fomc", "manufacturing", "employment"]

for search_keywords in keywords:
    print('process:', search_keywords)
    search_result = full_releases.name[full_releases.name.apply(lambda x: search_keywords in x.lower())]
    econ_data = pd.DataFrame(index=pd.date_range(start='2000-01-01', end=dt.datetime.today(), freq='MS'))

    for release_id in search_result.index:
        print("scraping release_id: ", release_id)
        econ_data = pd.concat([econ_data, fetch_release_id_data(release_id)], axis=1)
    print('econ_data:', econ_data)
    econ_data.to_csv(f"{search_keywords}.csv")




