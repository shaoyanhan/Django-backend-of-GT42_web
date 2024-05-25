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
CREATE TABLE IF NOT EXISTS haplotype (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mosaicID VARCHAR(255) NOT NULL,
    geneID VARCHAR(255) NOT NULL,
    areaType VARCHAR(255) NOT NULL,
    length INT NOT NULL,
    nucleotideSequence LONGTEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 为mosaicID列创建索引以加快查询速度
cursor.execute("ALTER TABLE haplotype ADD INDEX idx_mosaicID (mosaicID);")


# data = [
#     ["GT42G000001","GT42G000001.0.0","mosaic",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.1","haplotype1",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.2","haplotype2",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.3","haplotype3",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.4","haplotype4",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.5","haplotype5",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.6","haplotype6",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.7","haplotype7",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.8","haplotype8",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.9","haplotype9",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.10","haplotype10",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.11","haplotype11",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.12","haplotype12",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.13","haplotype13",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.14","haplotype14",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.15","haplotype15",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.16","haplotype16",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.17","haplotype17",5420,"ATCGATCG"],
#     ["GT42G000001","GT42G000001.SO.18","haplotype18",5420,"ATCGATCG"]
# ]

# # 插入数据
# for line in data:
#     if len(line) == 5:
#         mosaicID, geneID, areaType, length, nucleotideSequence = line
#         data_to_insert = (mosaicID, geneID, areaType, length, nucleotideSequence)
#         # 推荐使用%s占位符来构建参数化的SQL语句, 参数化查询不仅可以提高性能，还可以防止SQL注入攻击
#         insert_sql = "INSERT INTO haplotype (mosaicID, geneID, areaType, length, nucleotideSequence) VALUES (%s, %s, %s, %s, %s);"
#         cursor.execute(insert_sql, data_to_insert)

# 读取数据文件并插入数据
data_file = './table_for_mysql/haplotype_table.tsv'
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    cnt = 0
    start_time = time.time()  # 开始计时

    for line in reader:
        if len(line) == 5:
            data_to_insert = tuple(line)
            insert_sql = "INSERT INTO haplotype (mosaicID, geneID, areaType, length, nucleotideSequence) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(insert_sql, data_to_insert)

            cnt += 1
            if cnt % 10000 == 0: # 每插入一万行大约耗时50s，haplotype文件约15万行，
                print(f"{cnt} records inserted. Time elapsed: {time.time() - start_time:.2f} seconds.")

# 提交更改并关闭连接
cnx.commit()
cursor.close()
cnx.close()