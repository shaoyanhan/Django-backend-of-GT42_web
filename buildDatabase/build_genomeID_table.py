import mysql.connector # pip install mysql-connector-python
import csv
import time

# 数据库连接配置
config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'raise_on_warnings': True
}

# 连接到MySQL
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# # 创建数据库
# create_db_sql = "CREATE DATABASE IF NOT EXISTS testdb;"
# cursor.execute(create_db_sql)

# 选择数据库
cnx.database = 'testdb'

# 创建数据表
create_table_sql = """
CREATE TABLE IF NOT EXISTS gt42_genome_id (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    genomeID VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 为genomeID列创建索引以加快查询速度
cursor.execute("ALTER TABLE gt42_genome_id ADD INDEX idx_genomeID (genomeID);")

# data = [
#     ["GT42G000001","mosaic"],
#     ["GT42G000002","mosaic"],
#     ["GT42G000003","mosaic"],
#     ["GT42G000004","mosaic"],
#     ["GT42G000005","mosaic"],
#     ["GT42G000001.0.0", "mosaic"],
#     ["GT42G000001.SO.1", "gene"],
#     ["GT42G000001.SO.2", "gene"],
#     ["GT42G000001.SO.3", "gene"],
#     ["GT42G000002.0.0", "mosaic"],
#     ["GT42G000002.SO.1", "gene"],
#     ["GT42G000002.SO.2", "gene"],
#     ["GT42G000002.SO.3", "gene"],
#     ["GT42G000002.SO.4", "gene"],
#     ["GT42G000002.SO.5", "gene"],
#     ["GT42G000002.SO.6", "gene"],
#     ["GT42G000002.SO.7", "gene"],
#     ["GT42G000001.SO.1.0", "gene"],
#     ["GT42G000001.SO.1.1", "transcript"],
#     ["GT42G000001.SO.1.2", "transcript"],
#     ["GT42G000001.SO.1.3", "transcript"],
#     ["GT42G000001.SO.1.4", "transcript"],
#     ["GT42G000001.SO.1.5", "transcript"],
#     ["GT42G000001.SO.2.0", "gene"],
#     ["GT42G000001.SO.2.1", "transcript"],
#     ["GT42G000001.SO.2.2", "transcript"],
#     ["GT42G000001.SO.2.3", "transcript"],
#     ["GT42G000001.SO.3.0", "gene"],
#     ["GT42G000001.SO.3.1", "transcript"],
#     ["GT42G000001.SO.3.2", "transcript"],
#     ["GT42G000001.SO.3.3", "transcript"]
# ]

# # 插入数据
# for line in data:
#     if len(line) == 2:
#         genomeID, type = line
#         data_to_insert = (genomeID, type)
#         # 推荐使用%s占位符来构建参数化的SQL语句, 参数化查询不仅可以提高性能，还可以防止SQL注入攻击
#         insert_sql = "INSERT INTO gt42_genome_id (genomeID, type) VALUES (%s, %s);"
#         cursor.execute(insert_sql, data_to_insert)

# # 读取数据文件并插入数据
# data_file = './table_for_mysql/genomeID_table.tsv'
# with open(data_file, newline='', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
#     next(reader)  # 跳过标题行

#     cnt = 0
#     start_time = time.time()  # 开始计时

#     for line in reader:
#         if len(line) == 2:
#             data_to_insert = tuple(line)
#             insert_sql = "INSERT INTO gt42_genome_id (genomeID, type) VALUES (%s, %s);"
#             cursor.execute(insert_sql, data_to_insert)
        
#             cnt += 1
#             if cnt % 10000 == 0:
#                 print(f"{cnt} records inserted. Time elapsed: {time.time() - start_time:.2f} seconds.")


# # 提交更改并关闭连接
# cnx.commit()
# cursor.close()
# cnx.close()

# 读取数据文件并插入数据
data_file = './table_for_mysql/genomeID_table.tsv'
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    batch_size = 2000  # 您可以根据需要调整批量大小
    batch_data = []

    cnt = 0
    start_time = time.time()  # 开始计时

    for line in reader:
        if len(line) == 2:
            batch_data.append(line)
            if len(batch_data) >= batch_size:
                cursor.executemany("INSERT INTO gt42_genome_id (genomeID, type) VALUES (%s, %s);", batch_data)
                batch_data = []  # 清空批处理列表
            
            cnt += 1
            if cnt % 10000 == 0: # 约62万行，每一万行耗时约2s
                print(f"{cnt} records inserted. Time elapsed: {time.time() - start_time:.2f} seconds.")

    # 插入剩余的数据
    if batch_data:
        cursor.executemany("INSERT INTO gt42_genome_id (genomeID, type) VALUES (%s, %s);", batch_data)

    # 提交更改
    cnx.commit()
    print(f"All records inserted. Total time: {time.time() - start_time:.2f} seconds.")

cursor.close()
cnx.close()