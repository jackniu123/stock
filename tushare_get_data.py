import datetime

import tushare as ts
import pymysql
import numpy as np


def dataFrame_To_List(df):
    dataset = np.array(df)
    datalist = dataset.tolist()
    return datalist


class tushareMethod:
    pro = None

    def set_Token(self):
        ts.set_token('4125c08f0909642ddd3d663a94cf9e8768021ad98780a0254125766c')
        self.pro = ts.pro_api()

    def get_Trade_cal(self, start, end):  # 调用trade_cal接口，设置起始日期和终止日期
        df = self.pro.query('trade_cal', start_date=start, end_date=end, fields='cal_date,is_open,pretrade_date')
        return df


class mysqlMethod:
    db = None
    cursor = None

    def connect_To_Mysql(self, user_, password_, db_="stock"):
        # 打开数据库连接
        self.db = pymysql.connect(host='localhost', port=3306, user=user_, passwd=password_, db=db_, charset='utf8mb4')
        self.cursor = self.db.cursor()

    def insert_Datas(self, table, keys_list, values_list):
        suc_count = 0
        err_count = 0
        sql = "INSERT INTO {} ({}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table, keys_list)
        # sql = "INSERT INTO {} ({}) VALUES (%s)".format(table, keys_list)
        for i in values_list:
            try:
                self.cursor.execute(sql, i)
                self.db.commit()
                suc_count += 1

            except Exception as e:
                print(i)
                print("Error:{}".format(e))
                self.db.rollback()
                err_count += 1
        print("Finnish! Successed:{}, Failed:{}".format(suc_count, err_count))

    def disconnect_to_Mysql(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    # 公众号：二七阿尔量化
    import exchange_calendars as xcals

    xshg = xcals.get_calendar("XSHG")
    xshg_range = xshg.schedule.loc[str(datetime.datetime.now().date() - datetime.timedelta(7)):str(datetime.datetime.now().date() - datetime.timedelta(1))]
    # xshg_range = xshg.schedule.loc["2024-04-26":"2024-04-27"]
    jiaoyiri_list = xshg_range.index.strftime("%Y%m%d").tolist()
    print(jiaoyiri_list)




    # 实例化对象
    Obj_tushare = tushareMethod()
    Obj_mysql = mysqlMethod()

    # 设置Token
    Obj_tushare.set_Token()

    # # 从tushare获取交易日数据
    # df1 = Obj_tushare.get_Trade_cal("20160101", "20180101")
    #
    # # 转换为list
    # data = dataFrame_To_List(df1)



    pro = ts.pro_api()

    # 连接数据库
    Obj_mysql.connect_To_Mysql("root", "mysql123")

    for jiaoyiri in jiaoyiri_list:
        # 获取某一天全市场的日线行情
        df = pro.daily(trade_date=jiaoyiri)
        print(df)

        # 转换为list
        data = dataFrame_To_List(df)
        Obj_mysql.insert_Datas("daily", "ts_code,trade_date,open,high,low,close,pre_close,_change,pct_chg,vol,amount", data)

    # 断开数据库连接
    Obj_mysql.disconnect_to_Mysql()

