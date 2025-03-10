import os
import json
from datetime import datetime


def load_json_data(base_dir):
    """读取所有JSON文件并转换为统一格式"""
    all_data = []

    # 遍历目录下的所有.json文件
    for filename in os.listdir(base_dir):
        if not filename.endswith('.json'):
            continue

        brand = os.path.splitext(filename)[0]  # 获取品牌名称
        file_path = os.path.join(base_dir, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 验证JSON数据有效性
                if data.get('success') and data.get('code') == 200:
                    for item in data['result']:
                        # 字段映射和类型转换
                        record = {
                            'brand': brand,
                            'moneyday': datetime.strptime(item['moneyDay'], '%Y-%m-%d').date(),
                            'money': float(item['money']),
                            'source_file': filename  # 可选字段
                        }
                        all_data.append(record)
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")

    return all_data


def simulate_database_query(data):
    """模拟数据库查询逻辑：按日期排序"""
    sorted_data = sorted(data, key=lambda x: x['moneyday'])
    return sorted_data


def export_to_csv(output_path, data):
    """将数据导出为CSV文件（与数据库查询结果格式一致）"""
    import csv

    with open(output_path, 'w', newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)

        # 写入表头
        writer.writerow(['brand', 'moneyday', 'money'])

        # 写入数据
        for row in data:
            writer.writerow([
                row['brand'],
                row['moneyday'].strftime('%Y-%m-%d'),
                f"{row['money']:.2f}"
            ])


def main():
    # 输入参数配置
    input_dir = './3years'  # JSON文件目录
    output_file = 'query_result.csv'  # 输出文件

    # 执行数据处理流程
    raw_data = load_json_data(input_dir)
    sorted_data = simulate_database_query(raw_data)

    # 导出结果
    export_to_csv(output_file, sorted_data)
    print(f"成功生成 {output_file}，包含 {len(sorted_data)} 条记录")


if __name__ == "__main__":
    main()