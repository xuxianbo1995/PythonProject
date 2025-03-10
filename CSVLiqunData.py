import csv
from datetime import datetime

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from collections import defaultdict
import os

app = Flask(__name__)
CORS(app)


# 移除无用的数据库相关代码

@app.route('/api/price-data', methods=['GET'])
def get_price_data():
    data = []
    csv_path = 'query_result.csv'

    # 检查CSV文件是否存在
    if not os.path.isfile(csv_path):
        print(f"[ERROR] CSV文件不存在: {csv_path}")
        return jsonify([]), 500

    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for row in csvreader:
                brand = row['brand']
                moneyday_str = row['moneyday']
                money_str = row['money']

                # 处理日期
                try:
                    moneyday = datetime.strptime(moneyday_str, '%Y-%m-%d').date()
                except ValueError:
                    print(f"[WARNING] 无效日期格式({moneyday_str})")
                    continue

                # 处理价格
                try:
                    money = float(money_str)
                except ValueError:
                    print(f"[WARNING] 无效价格格式({money_str})")
                    continue

                data.append({
                    'brand': brand,
                    'date': moneyday.strftime('%Y-%m-%d'),  # 转换为 YYYY-MM-DD 格式
                    'price': money
                })
    except Exception as e:
        print(f"[ERROR] 数据处理错误: {str(e)}")
        return jsonify([]), 500

    return jsonify(data)

@app.route('/')
def index():
    return send_from_directory('static', 'LiqunData.html')


if __name__ == '__main__':
    # 使用应用上下文激活
    with app.app_context():
        # 可在此处预加载数据（可选）
        pass
    app.run(host='0.0.0.0', port=10000)