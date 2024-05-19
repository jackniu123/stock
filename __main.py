# 开机启动程序的总入口文件
import sys

sys.path.append('D:/不要删除牛爸爸的程序') # 绝对路径
sys.path.append('D:/不要删除牛爸爸的程序/工具软件') # 绝对路径

if __name__ == '__main__':
    from tushare_get_data import tushare_get_data_main
    tushare_get_data_main()
    from 工具软件.stock_assistant_new_stock_informer import stock_assistant_new_stock_informer_main
    stock_assistant_new_stock_informer_main()
    from 工具软件.stock_assistant_price_alert import stock_assistant_price_alert_main
    stock_assistant_price_alert_main()
    from 工具软件.stock_assistant_add import stock_assistant_add_main
    stock_assistant_add_main()
    from __utils import messagebox
    messagebox.dump()