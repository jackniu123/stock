"""
一、 行情告警
 检测是否已经开市
 拉取最新行情信息
 基于规则告警：
    1， 达到特定价位告警
    2， 达到特定成交量告警
    3， 涨跌速率告警

二、 数据、要闻速览

三、 数据告警
    1, 底部识别：巴菲特指标偏下部区间

四、 重要新闻告警

"""

from selenium import webdriver
import time


"""
快速浏览关键资讯、数据等内容，通过异常数据实现盈利。
"""

driver = webdriver.Edge()
driver.maximize_window()
driver.get('about:blank')


js="window.open('{}','_blank');"
# 深圳住建局房地产销售数据
driver.execute_script(js.format('https://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面
# driver.find_element_by_id('userid').send_keys('user2')
# driver.find_element_by_id('pwd').send_keys('pass2')
# driver.find_element_by_id('Submit').click() #点击按钮

# 巴菲特指标---中美一张图（图线相互背离达到很大值的时候，往往是中美间流动性会逆转流向的时候）
driver.execute_script(js.format('https://legulegu.com/stockdata/marketcap-gdp'))
driver.execute_script(js.format('https://sc.macromicro.me/charts/12177/zhong-guo-gu-shi-GDP-mei-guo-gu-shi-GDP'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# # 巴菲特指标---美股
# driver.execute_script(js.format('https://sc.macromicro.me/charts/105/us-market-cap-gdp'))
# # driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面
#
# # 巴菲特指标---中国
# driver.execute_script(js.format('https://legulegu.com/stockdata/marketcap-gdp'))
# # driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# VIX恐慌指数(没有大的恐慌，不要买入，没有大的乐观，不要离开)
driver.execute_script(js.format('https://cn.investing.com/indices/volatility-s-p-500'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# 世界主要股指
driver.execute_script(js.format('https://cn.investing.com/indices/major-indices'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# 底部研究
driver.execute_script(js.format('https://legulegu.com/stockdata/bottom-research-nav'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# 大宗商品价格、农产品价格

# 房地产价格
driver.execute_script(js.format('https://data.house.163.com/bj/housing/trend/district/todayflat/180/week/allDistrict/1.html?districtname=%E5%85%A8%E5%B8%82#stoppoint'))


# 流动性
# 流动性---中国央行资产负债表
driver.execute_script(js.format('https://zh.tradingeconomics.com/china/central-bank-balance-sheet'))

# 流动性---美债收益率
driver.execute_script(js.format('https://cn.investing.com/rates-bonds/u.s.-10-year-bond-yield'))
# driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面

# 流动性---比特币走势
# 流动性---LPR
# 流动性---中美CPI
# 流动性---全球M2
# ● 新增信贷 2022年12月到2023年4月，连续多个月新增信贷同比大增，带来上证一段涨幅：https://data.eastmoney.com/cjsj/xzxd.html

# ● 中国准备金率：https://data.eastmoney.com/cjsj/ckzbj.html
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/ckzbj.html'))
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/xzxd.html'))
# ● 中国货币供应量：https://data.eastmoney.com/cjsj/hbgyl.html
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/hbgyl.html'))
# 美国利率
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/foreign_0_22.html'))
# ● LPR：https://data.eastmoney.com/cjsj/globalRateLPR.html
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/globalRateLPR.html'))
# ● 隔夜利率：https://data.eastmoney.com/shibor/shibor/001,CNY,001.html
driver.execute_script(js.format('https://data.eastmoney.com/shibor/shibor/001,CNY,001.html'))
# 	○ 有时候财政政策也会导致隔夜利率下降：https://wallstreetcn.com/articles/3666632
driver.execute_script(js.format('https://wallstreetcn.com/articles/3666632'))
# 	○
# ● 中国CPI数据：https://data.eastmoney.com/cjsj/cpi.html
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/cpi.html'))
# 	○ 猪肉价格比较关键，预测当月CPI，可以提前看猪肉价格当月按日的细分走势：
# https://bj.zhue.com.cn/zoushi.php
driver.execute_script(js.format('https://bj.zhue.com.cn/zoushi.php'))
# 	○ 世界粮食价格指数：https://www.fao.org/worldfoodsituation/foodpricesindex/zh/
driver.execute_script(js.format('https://www.fao.org/worldfoodsituation/foodpricesindex/zh/'))

#
# 流动性---汇率 人民币相对一揽子货币：https://www.chinamoney.com.cn/english/
driver.execute_script(js.format('https://www.chinamoney.com.cn/english/'))

# 中国进出口贸易数据
driver.execute_script(js.format('http://data.mofcom.gov.cn/hwmy/imexmonth.shtml'))


# 经济活力---发电量
# 经济活力---PMI（PMI在08年11月份，制造业降低到38.8；在20年2月份35.7，非制造业29.6；22年制造业降低到47，非制造业41.6。这些点位都是股市的阶段性低点。）
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/pmi.html'))
# 经济活力---美国失业率
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/foreign_0_4.html'))
# 经济活力---美国通胀率
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/foreign_0_11.html'))
# 经济活力---海运价格
driver.execute_script(js.format('https://sc.macromicro.me/charts/947/commodity-ccfi-scfi'))

# 行业研报---QuestionMobile
driver.execute_script(js.format('https://www.questmobile.com.cn/research/reports'))



# 财经日历
driver.execute_script(js.format('https://wallstreetcn.com/calendar'))
driver.execute_script(js.format('https://cn.investing.com/earnings-calendar/'))


# 情绪指标---全国股票交易金额曲线（2015年相对于往年有尖尖的顶部，20年7月和21年8月，此时是市场疯狂的时候）
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/gpjytj.html'))
# 情绪指标---新增投资者（新增投资者的下跌，领先于股市下跌，两条曲线最终会收敛到一处，收敛的地方往往是变盘的时间点）
driver.execute_script(js.format('https://data.eastmoney.com/cjsj/gpkhsj.html'))


# 国策
driver.execute_script(js.format('https://www.gov.cn/'))




# 国际形势
driver.execute_script(js.format('https://wallstreetcn.com/'))
driver.execute_script(js.format('https://www.ndrc.gov.cn/'))
#

# driver.execute_script(js.format('https://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html'))
# # driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面
#
#
# driver.execute_script(js.format('https://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html'))
# # driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面
#
#
# driver.execute_script(js.format('https://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html'))
# # driver.switch_to.window(driver.window_handles[-1]) #切换到最新页面


time.sleep(5000)
driver.quit()

