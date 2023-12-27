# APIKEY:    Y23833JK7VUY3GUH
# https://www.alphavantage.co/support/#api-key
# https://www.alphavantage.co/documentation/

import pysnooper



from alpha_vantage.timeseries import TimeSeries



@pysnooper.snoop()
def get_daily():
    # dictionary version
    ts = TimeSeries(key='Y23833JK7VUY3GUH')
    data, meta_data = ts.get_intraday('OXY')
    print(data)


    #  dataframe version
    ts = TimeSeries(key='Y23833JK7VUY3GUH', output_format='pandas', indexing_type='date')
    data, meta_data = ts.get_intraday('OXY')
    print(data)


    #  dataframe version
    ts = TimeSeries(key='Y23833JK7VUY3GUH', output_format='pandas', indexing_type='date')
    # 分钟级数据
    data, meta_data = ts.get_intraday('OXY', interval='1min', outputsize='full')
    print(data)



if __name__ == '__main__':
    get_daily()