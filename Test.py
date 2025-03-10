# import pandas as pd
# import json
#
# # 从 JSON 文件中读取数据
# with open('30days/czz.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# with open('30days/hl.json', 'r', encoding='utf-8') as file1:
#     data1 = json.load(file1)
#
# # 提取 result 部分
# result_data = data['result']
#
# result_data1 = data1['result']
#
# # 将 JSON 数据转换为 DataFrame
# df = pd.DataFrame(result_data)
# df1 = pd.DataFrame(result_data1)
#
# # 将 DataFrame 写入 Excel 文件
# df.to_excel('czz30days.xlsx', index=False)
# df.to_excel('hl30days.xlsx', index=False)
#
# print("Excel 文件已生成：czz30days.xlsx")

import os
import pandas as pd
import json

# 定义文件夹路径
folder_path = '30days'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件是否为 JSON 文件
    if filename.endswith('.json'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)

        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取 result 部分
        result_data = data.get('result', [])

        # 将 JSON 数据转换为 DataFrame
        df = pd.DataFrame(result_data)

        # 生成对应的 Excel 文件名
        excel_filename = filename.replace('.json', '.xlsx')
        excel_filepath = os.path.join(folder_path, excel_filename)

        # 将 DataFrame 写入 Excel 文件
        df.to_excel(excel_filepath, index=False)

        print(f"Excel 文件已生成：{excel_filepath}")