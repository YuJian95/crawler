from cn.yujian95.crawler.weather.weather import get_year_weather_data
import pandas as pd

# 抓取城市
city = 'guangzhou'
# 抓取年份开始
start_year = 2011
# 抓取年份结束
end_year = 2013

print("------------开始执行程序------------")
weather_data_of_year = []
# 设定抓取的年份范围
for year in range(start_year, end_year):
    weather_data_of_year.append(get_year_weather_data(str(year), city))
# 数据拼接，重新生成索引
result = pd.concat(weather_data_of_year).reset_index(drop=True)
# 数据储存为csv格式，去除索引，解码以防止乱码
result.to_csv(str(start_year) + '_to_' + city + '_data.csv', index=False, encoding='utf-8')
file_name = 'Weather data for ' + city + ' in ' + str(start_year) + ' and ' + str(end_year) + '.csv'
result.to_csv(file_name, index=False, encoding='utf-8')
print("------------结束执行程序------------")
