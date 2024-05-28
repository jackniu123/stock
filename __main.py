# 开机启动程序的总入口文件
import sys
import time
import threading
from __utils import messagebox
sys.path.append('D:/不要删除牛爸爸的程序') # 绝对路径
sys.path.append('D:/不要删除牛爸爸的程序/工具软件') # 绝对路径

if __name__ == '__main__':
    messagebox.logger.warning('=================begin...=================')

    if True:
        from tushare_get_data import tushare_get_data_main
        tushare_get_data_main()
        from 工具软件.stock_assistant_new_stock_informer import stock_assistant_new_stock_informer_main
        stock_assistant_new_stock_informer_main()
        from 工具软件.stock_assistant_price_alert import stock_assistant_price_alert_main
        stock_assistant_price_alert_main()
        from 工具软件.stock_assistant_add import stock_assistant_add_main
        stock_assistant_add_main()

    else: # akshare多线程不安全，导致错误多发，还是串行执行吧
        from tushare_get_data import tushare_get_data_main, tushare_get_data_is_finished
        threading.Thread(target=tushare_get_data_main).start()

        while True:
            if tushare_get_data_is_finished():
                break
            else:
                time.sleep(1)

        from 工具软件.stock_assistant_new_stock_informer import stock_assistant_new_stock_informer_main
        t1 = threading.Thread(target=stock_assistant_new_stock_informer_main)
        from 工具软件.stock_assistant_price_alert import stock_assistant_price_alert_main
        t2 = threading.Thread(target=stock_assistant_price_alert_main)
        from 工具软件.stock_assistant_add import stock_assistant_add_main
        t3 = threading.Thread(target=stock_assistant_add_main)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

    from __utils import messagebox
    messagebox.dump()
    messagebox.logger.warning('=================finished========================')