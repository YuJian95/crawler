import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# 抓取天气数据
def crawling_weather_data(url):
    print("抓取地址：" + url)
    # 获取网页源代码
    html = requests.get(url)
    # 设置编码，防止中文乱码
    html = html.content.decode('gbk')
    # 数据提取，进行解析，这里使用自带的解析库
    soup = BeautifulSoup(html, 'html.parser')
    tr_list = soup.find_all('tr')  # 提取其中的tr标签

    dates, conditions, temperature, wind = [], [], [], []
    # c从1开始，只要数据不要列名
    for text in tr_list[1:]:
        # 删除字符串前后空白内容
        sub_data = text.text.split()
        # 将日期加载到列表中
        dates.append(sub_data[0])
        # 根据 html 内容获取对应的 文字内容。
        # 索引 1-3 实际上取得是字符串的2,3内容，取不到第4个，join可以把字符串整合一块
        conditions.append(''.join(sub_data[1:3]))
        temperature.append(''.join(sub_data[3:6]))
        wind.append(''.join(sub_data[6:10]))

    # 创建表格，对其追加数据
    weather = pd.DataFrame()
    weather['日期'] = dates
    weather['天气状况'] = conditions
    weather['气温'] = temperature
    weather['风力风向'] = wind
    return weather


# 抓取一年的天气数据
def get_year_weather_data(year, city):
    print("开始抓取：" + year + "年，开始时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    weather_data_of_month = []
    # 循环获取 1 ~ 12 月的数据
    for month in range(1, 13):
        if month >= 10:
            weather_data_of_month.append(
                crawling_weather_data(
                    'http://www.tianqihoubao.com/lishi/' + city + '/month/' + year + '{}.html'.format(month)))
        # 当月份为 1 ~ 9 时，链接中补充 0 前缀，例如 01 代表一月
        else:
            weather_data_of_month.append(
                crawling_weather_data(
                    'http://www.tianqihoubao.com/lishi/' + city + '/month/' + year + '0{}.html'.format(month)))

    print("抓取完成，结束时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 拼接 12 个月的天气数据
    return pd.concat(weather_data_of_month).reset_index(drop=True)
