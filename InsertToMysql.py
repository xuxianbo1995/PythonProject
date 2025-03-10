import os
import json
import pymysql

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "zjzyscb",
    "charset": "utf8mb4"
}


# 遍历文件夹处理JSON文件
def process_files(folder_path):
    # 连接数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 遍历文件夹
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(folder_path, filename)
                    brand = os.path.splitext(filename)[0]  # 去除扩展名

                    # 读取JSON文件
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        # 验证数据结构
                        if not isinstance(data.get("result"), list):
                            print(f"文件 {filename} 格式异常，跳过处理")
                            continue

                        # 准备插入数据
                        sql = """INSERT INTO xyhq (
                            brand, moneyDay, money, 
                            bili, type, guidePrice, tradePrice
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                        batch_data = []
                        for item in data["result"]:
                            batch_data.append((
                                brand,
                                item.get("moneyDay"),
                                float(item.get("money")) if item.get("money") else None,
                                float(item.get("bili")) if item.get("bili") else None,
                                item.get("type"),
                                float(item.get("guidePrice")) if item.get("guidePrice") else None,
                                float(item.get("tradePrice")) if item.get("tradePrice") else None
                            ))

                        # 批量插入
                        cursor.executemany(sql, batch_data)
                        print(f"已插入 {len(batch_data)} 条记录（品牌：{brand}）")

        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"发生错误：{str(e)}")
    finally:
        connection.close()


if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = "./3years"  # 如果脚本在工程根目录，使用这个路径

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在")
    elif not os.path.isdir(folder_path):
        print(f"错误：{folder_path} 不是目录")
    else:
        process_files(folder_path)