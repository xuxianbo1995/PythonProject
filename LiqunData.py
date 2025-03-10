# app.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pymysql
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "zjzyscb",
    "charset": "utf8mb4"
}


def safe_convert_date(date_str):
    """安全转换日期字符串（处理格式异常）"""
    try:
        # 假设日期格式为 YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        return None  # 或返回默认日期


def safe_convert_float(value_str):
    """安全转换浮点数（处理非数字字符）"""
    try:
        return float(value_str)
    except:
        return None


def get_price_data():
    """获取并清洗数据"""
    try:
        conn = pymysql.connect(**db_config)
        with conn.cursor() as cursor:
            sql = """
                SELECT brand, moneyday, money 
                FROM xyhq
                ORDER BY STR_TO_DATE(moneyday, '%Y-%m-%d') ASC  # 数据库层按日期排序
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            # 数据清洗
            clean_data = []
            for row in results:
                brand, moneyday_str, money_str = row
                # 转换日期
                date = safe_convert_date(moneyday_str)
                if not date:
                    continue  # 跳过无效日期
                # 转换价格
                price = safe_convert_float(money_str)
                if price is None:
                    continue  # 跳过无效价格

                clean_data.append({
                    "brand": brand,
                    "date": date,
                    "price": price
                })
            return clean_data
    except Exception as e:
        print("数据库错误:", str(e))
        return []
    finally:
        if conn:
            conn.close()


@app.route('/api/price-data')
def price_data():
    data = get_price_data()
    return jsonify({"data": data})

@app.route('/')
def index():
    return send_from_directory('static', 'LiqunData.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)