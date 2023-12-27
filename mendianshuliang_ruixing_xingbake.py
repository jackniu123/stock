# xsMHwSFdpNsgiYmAB6jyppT01jha3te
# https://lbs.qq.com/dev/console/application/mine
# https://pythondict.com/category/python-data-analyze/
import datetime
import hashlib

import requests
import time
import pysnooper
import json


class LocationSearch(object):

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.key = 'Z6BBZ-63DW3-E5G3Y-O2Y73-LUIQO-P4F2Z'
        self.sk = 'xsMHwSFdpNsgiYmAB6jyppT01jha3te'
        self.url = (
            'https://apis.map.qq.com/ws/place/v1/search?'
            'boundary=region({},0)&key={}&keyword={}'
            '&page_index={}&page_size=20'
        )

    @pysnooper.snoop()
    def request_data(self, location: str, page: int):
        """
        请求接口数据
        Arguments:
            location {str} -- 地点
            page {int} -- 第几页

        Returns:
            {list} -- 该页该地点的数据
            {int} -- 该地点结果总数
        """
        # 拼接链接time
        url = self.url.format(location, self.key, self.keyword, page)
        # 获得数字签名，并将签名加到链接后面进行请求
        wait_sig = url.split('qq.com')[1] + str(self.sk)
        sig = hashlib.md5(wait_sig.encode('utf-8')).hexdigest()
        res = requests.get(url + '&sig=' + sig)
        print(url + '&sig=' + sig)
        print(res.json()['message'])
        # 获得数据返回
        pois = res.json()['data']
        # 避免请求上限
        time.sleep(0.2)
        return pois, res.json()['count']

    def get_single_location(self, location: str):
        """
        获得单个地点的数据

        Arguments:
            location {str} -- 地点

        Returns:
            {list} -- 该地点某关键词的所有数据
            {int} -- 该地点某关键词的所有数量
        """
        page = 1
        location_data = []
        pois, total = self.request_data(location, page)
        for poisition in pois:
            location_data.append(poisition)
        # 如果有多页
        while (total / 20) > page:
            pois, _ = self.request_data(location, page)
            for poisition in pois:
                location_data.append(poisition)
            page += 1
        print(f'{self.keyword} {location} 门店总数为：{total}')

        result_count = str(datetime.datetime.now()) + '瑞幸在 ' + location + ' 开店数量是:' + str(total) + '\r'
        with open(f'瑞星咖啡开店结果', 'a+') as my_file:
            my_file.write(result_count)
            my_file.seek(0)
            print(my_file.read())
            my_file.close()


        return location_data, total

    def get_cities_data(self, cities: str):
        """
        获得所有城市某关键词的数据

        Arguments:
            cities {list} -- 城市列表
        """
        result = []
        keyword_count = 0
        for city in cities:
            # 获得该城市的所有门店和总数
            data, count = self.get_single_location(city)
            keyword_count += count
            result.extend(data)
        print('===================get_cities_data======================')
        print(f'{self.keyword} 一线城市门店总数为：{keyword_count}')
        # 导出数据
        with open(f'{self.keyword}.json', 'w') as my_file:
            json.dump(result, my_file, ensure_ascii=False)


        result_count = str(datetime.datetime.now()) + '瑞幸在一线城市开店数量是:' + str(keyword_count) + '\r'
        with open(f'瑞星咖啡开店结果', 'a+') as my_file:
            my_file.write(result_count)
            my_file.seek(0)
            print(my_file.read())
            my_file.close()



if __name__ == '__main__':
    cities = ['北京', '上海', '广州', '深圳']

    loc = LocationSearch('瑞幸咖啡')
    loc.get_cities_data(cities)

    # loc = LocationSearch('星巴克咖啡')
    # loc.get_cities_data(cities)