import mysql.connector # pip install mysql-connector-python
import csv

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
CREATE TABLE IF NOT EXISTS snp (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mosaicID VARCHAR(255) NOT NULL,
    areaType VARCHAR(255) NOT NULL,
    SNPSite INT NOT NULL,
    SNPType VARCHAR(255) NOT NULL,
    IsoSeqEvidence VARCHAR(255) NOT NULL,
    RNASeqEvidence VARCHAR(255) NOT NULL,
    haplotypeSNP LONGTEXT NOT NULL,
    color VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 为mosaicID列创建索引以加快查询速度
cursor.execute("ALTER TABLE snp ADD INDEX idx_mosaicID (mosaicID);")

# data = [
#     ['GT42G000001', 'SNP',17,'A/C','10045/5210','5921/1705','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000001', 'SNP',32,'C/G','8346/3244','2133/4543','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#003666'],
#     ['GT42G000001', 'SNP',45,'G/T','10045/5210','5921/1705','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000001', 'SNP',56,'T/A','8346/3244','2133/4543','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#003666'],
#     ['GT42G000001', 'SNP',675,'A/C/G','10045/3410','7521/1705','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000001', 'SNP',175,'A/G/C','34045/5210','5921/1755','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000001', 'SNP',325,'C/G/G','8346/3444','2133/7543','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#003666'],
#     ['GT42G000001', 'SNP',455,'G/G/T','10045/3410','7521/1705','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000001', 'SNP',565,'T/A/G','8346/3244','7533/4543','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#003666'],
#     ['GT42G000001', 'SNP',675,'A/G/C','34045/5210','5921/1755','GT42G000001.SO.1:C; GT42G000001.SS.1:A', '#050f2c'],
#     ['GT42G000002', 'SNP',17,'A/C','10045/5210','5921/1705','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#050f2c'],
#     ['GT42G000002', 'SNP',32,'C/G','8346/3244','2133/4543','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#003666'],
#     ['GT42G000002', 'SNP',45,'G/T','10045/5210','5921/1705','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#050f2c'],
#     ['GT42G000002', 'SNP',56,'T/A','8346/3244','2133/4543','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#003666'],
#     ['GT42G000002', 'SNP',675,'A/C/G','10045/3410','7521/1705','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#050f2c'],
#     ['GT42G000002', 'SNP',175,'A/G/C','34045/5210','5921/1755','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#050f2c'],
#     ['GT42G000002', 'SNP',325,'C/G/G','8346/3444','2133/7543','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#003666'],
#     ['GT42G000002', 'SNP',455,'G/G/T','10045/3410','7521/1705','GT42G000002.SO.1:C; GT42G000002.SS.1:A', '#050f2c'],
# ]

# # 插入数据
# for line in data:
#     if len(line) == 8:
#         mosaicID, areaType, SNPSite, SNPType, IsoSeqEvidence, RNASeqEvidence, haplotypeSNP, color = line
#         data_to_insert = (mosaicID, areaType, SNPSite, SNPType, IsoSeqEvidence, RNASeqEvidence, haplotypeSNP, color)
#         # 推荐使用%s占位符来构建参数化的SQL语句, 参数化查询不仅可以提高性能，还可以防止SQL注入攻击
#         insert_sql = "INSERT INTO snp (mosaicID, areaType, SNPSite, SNPType, IsoSeqEvidence, RNASeqEvidence, haplotypeSNP, color) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
#         cursor.execute(insert_sql, data_to_insert)

# 读取数据文件并插入数据
data_file = './table_for_mysql/snp_table.tsv'
# data_file = './testData/snp/snp_table.tsv'
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行
    for line in reader:
        if len(line) == 8:
            data_to_insert = tuple(line)
            insert_sql = "INSERT INTO snp (mosaicID, areaType, SNPSite, SNPType, IsoSeqEvidence, RNASeqEvidence, haplotypeSNP, color) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_sql, data_to_insert)

# 提交更改并关闭连接
cnx.commit()
cursor.close()
cnx.close()