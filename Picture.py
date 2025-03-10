import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 从 JSON 文件中读取数据
with open('useTheNewQueryList.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取 result 部分
result_data = data['result']

# 准备横坐标（日期）和纵坐标（money）数据
dates = []
money_values = []

for item in result_data:
    # 将 moneyDay 转换为 datetime 对象
    date = datetime.strptime(item['moneyDay'], '%Y-%m-%d')
    dates.append(date)
    # 将 money 转换为浮点数
    money_values.append(float(item['money']))

# 创建折线图
plt.figure(figsize=(10, 6))  # 设置图表大小
plt.plot(dates, money_values, marker='o', linestyle='-', color='b', label='Money')

# 设置横坐标为日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 日期格式
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # 每天一个刻度
plt.gcf().autofmt_xdate()  # 自动旋转日期标签

# 设置标题和坐标轴标签
plt.title('Money Trend Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Money', fontsize=12)

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)

# 显示图表
plt.show()