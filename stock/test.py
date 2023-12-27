import sys


for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i}={j*i}",end=" ")
    print("\n")

result_count = str(datetime.datetime.now()) + '瑞幸在一线城市开店数量是:' + str(1023) + '\r'
with open(f'瑞星咖啡开店结果', 'a+') as my_file:
    my_file.write(result_count)
    my_file.seek(0)
    print(my_file.read())
    my_file.close()



sys.exit()