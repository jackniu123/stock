#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import time
import numpy as np

'''
https://zhuanlan.zhihu.com/p/242239006
这个模块有一个函数timeit.timeit（stmt = pass，setup = pass，timer = <default timer>，number = 1000000）这个函数有四个参数：

stmt：要测量其执行时间的代码段。
setup：执行stmt之前要运行的代码。通常，它用于导入一些模块或声明一些必要的变量。通过示例将更加清楚。
timer：这是默认的timeit.Timer对象。它有一个合理的默认值，因此我们不必做太多事情。
number：指定将执行stmt的次数。
'''

import timeit
def study_timeit():
    # 此代码在stmt之前仅执行一次。
    setup_code ="from math import sqrt"
    # 此代码将按照参数 'number'  的指定执行
    stmt_code ="sum(sqrt(x) for x in range(1, 10000))"
    iterations = 1000
    time_spend = timeit.timeit(stmt=stmt_code, setup=setup_code, number=iterations)
    print(f"单次执行{stmt_code}的时间为 {time_spend/iterations}")

    time_spend = timeit.repeat(stmt=stmt_code, setup=setup_code, number=iterations, repeat=5)
    print(f"每轮实验的时间为 {time_spend}")

    return

'''
ndarray的菜鸟教程（含抽取元素等）
https://www.runoob.com/numpy/numpy-sort-search.html

ndarray筛选满足条件的行：
https://geek-docs.com/numpy/numpy-ask-answer/459_numpy_filtering_lines_in_a_numpy_array_according_to_values_in_a_range.html
https://deepinout.com/numpy/numpy-questions/459_numpy_filtering_lines_in_a_numpy_array_according_to_values_in_a_range.html

ndarray的基本用法
https://blog.csdn.net/wd9ljs18/article/details/104630606

如何读取csv到ndarray
https://www.delftstack.com/zh/howto/numpy/read-csv-to-numpy-array/

如何给ndarray插入列标题
https://deepinout.com/numpy/numpy-questions/7_numpy_adding_rowcolumn_headers_to_numpy_arrays.html
'''

import numpy as np
import pandas as pd
import time
def study_ndarray():
#     setup_code = '''import numpy as np
# rows = 1000 * 10000
# lines = 15'''
#     setup_code = '''import numpy as np;rows = 1000 * 10000;lines = 15; ndarray_ins = np.random.random((rows, lines))'''
#     stmt_code = "ndarray_ins = ndarray_ins[:-2]"
#     time_spend = timeit.timeit(stmt=stmt_code, setup=setup_code, number=1)
#     print(f"单次执行:\n    {setup_code}\n    {stmt_code}\n的时间为{time_spend}秒")

    start_time = time.time()
    field_name = 'close_vol'
    sql_query_file_name = 'D:/不要删除牛爸爸的程序/__utils/sql_query_all_' + field_name + '.csv'
    df_daily = pd.read_csv(sql_query_file_name, index_col=0, nrows=100000, dtype={'trade_date': str})
    print(f"dataframe df_daily content of {sql_query_file_name} {time.time() - start_time}秒  : \n{df_daily}")
    print(f"df_daily.dtypes={{{df_daily.dtypes}}}")


    # 测量df转ndarray后的切片耗时，结论是该耗时与df自己直接切片的耗时比是2：3
    def calc_slice_ndarray():
        start_time = time.time()

        # data_np = df_daily.to_numpy()
        # data_np = np.array(df_daily)
        data_np = df_daily.values
        # data_np = df_daily.as_matrix()  has been deprecated.

        print(f"ndarray 属性和方法：", data_np.__dir__())
        print(f"data_np.dtype={{{data_np.dtype}}}")
        print(f"data_np.data={{{data_np.data}}}")

        dtypes = [("ts_code", str), ("trade_date", str), ("close", float), ("vol", float)]

        # 插入列标题
        # data_np = np.insert(data_np, 0, df_daily.columns.values, axis=0)
        # data_np = np.insert(data_np, 0, ["Index"], axis=1)

        # w = df_daily.dtypes.reshape(4, 1)
        # X = np.vstack((w.T, df_daily.data))
        # print(X)

        print(f"从df_daily 转化为data_np is {time.time() - start_time}秒: \n{data_np}")
        print(data_np.dtype.names)

        start_time = time.time()
        found_index = 0
        for i in range(len(data_np)):
            if data_np[i][1] > '20240302':
                # print(data_np[i][1])
                found_index = i
                break
        print(data_np[found_index:])
        print(f"从data_np[{len(data_np)}] 切片的耗时is {time.time() - start_time}秒")

    # calc_slice_ndarray()

    def calc_ndarray_and_series_index_speed():

        # ndarray比series的访问速度快4-15倍，也就是只需要给series的下标访问加一个values就能提速好多倍。
        start_time = time.time()
        len_of_df_daily_vol = len(df_daily['vol'])
        mean_of_it = 0
        for i in range(len_of_df_daily_vol):
            mean_of_it = df_daily['vol'][0:i].sum()
        print(f'''sum of vol : {mean_of_it}, time spend is {time.time()-start_time}''')

        start_time = time.time()
        len_of_df_daily_vol = len(df_daily['vol'])
        mean_of_it = 0
        for i in range(len_of_df_daily_vol):
            mean_of_it = df_daily['vol'].values[0:i].sum()
        print(f'''sum of vol by nadarray : {mean_of_it}, time spend is {time.time() - start_time}''')

        return


    calc_ndarray_and_series_index_speed()



    # start_time = time.time()
    # dtypes = [("ts_code", str), ("trade_date", str), ("close", float), ("vol", float)]
    # data_np_with_columns = np.rec.array(data_np, dtype=dtypes)
    # print(data_np_with_columns[found_index:])
    # print(f"从data_np_with_columns[{len(data_np_with_columns)}] 切片的耗时is {time.time() - start_time}秒")

    return

def study_performance_for_data_frame_and_nparray():
    return

if __name__ == "__main__":
    # study_timeit()
    # study_performance_for_data_frame_and_nparray()
    study_ndarray()
