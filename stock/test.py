import sys


# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{j}*{i}={j*i}",end=" ")
#     print("\n")
#
# result_count = str(datetime.datetime.now()) + '瑞幸在一线城市开店数量是:' + str(1023) + '\r'
# with open(f'瑞星咖啡开店结果', 'a+') as my_file:
#     my_file.write(result_count)
#     my_file.seek(0)
#     print(my_file.read())
#     my_file.close()

# print('鸡数       兔数      腿数','\n')
# n = 0
# a = input('请输入头数')
# d = input('请输入足数')
# j = 0
# t = 0
# while True:
#     j += 1
#     t = int(a) - j
#     n = j * 2 + t * 4
#     if n == int(d) :
#         print(f'''鸡的只数是：{j}；兔的头数是{t}\n''')
#         break

import pandas as pd


def merge_files():

    for i in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000), (2000, 2500), (2500, 3000), (3000, 3500), (3500, 4000), \
              (4000, 4500), (4500, 5000), (5000, 6000)):

        df_merge = df_ori = pd.DataFrame(None, columns=['profit_change', 'profit', 'buy_date', 'buy_price', 'sell_date', \
                                             'sell_price', 'ts_code', 'buy_date_change', 'is_total'])

        detail_merge_filename = '追涨分析_detail.xlsx'
        total_merge_filename = '追涨分析_total.xlsx'

        detail_filename = '追涨分析' + str(i[0]) + '_detail.xlsx'
        total_filename = f'追涨分析{i[0]}_total.xlsx'


        try:
            df_ori = pd.read_excel(detail_filename)
            df_merge = pd.read_excel(detail_merge_filename)
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
        df_merge = df_merge._append(df_ori, ignore_index=True)
        df_merge.to_excel(detail_merge_filename, index=False)

        df_total_merge = df_total_ori = pd.DataFrame(None, columns=['total_profit_change', 'total_profit', 'ts_code', 'trace_count',
                                                   'begin_date', 'end_date', 'MIN_CHANGE', 'MAX_CHANGE'])
        try:
            df_total_ori = pd.read_excel(total_filename)
            df_total_merge = pd.read_excel(total_merge_filename)
        except Exception as e:
            print("\033[0;31;40m", e, "\033[0m")
        df_total_merge = df_total_merge._append(df_total_ori, ignore_index=True)
        df_total_merge.to_excel(total_merge_filename, index=False)

'''
sys.exit()
'''