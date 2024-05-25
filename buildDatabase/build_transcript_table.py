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
CREATE TABLE IF NOT EXISTS transcript (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mosaicID VARCHAR(255) NOT NULL,
    geneID VARCHAR(255) NOT NULL,
    transcriptID VARCHAR(255) NOT NULL,
    transcriptIndex VARCHAR(255) NOT NULL,
    areaType VARCHAR(255) NOT NULL,
    start INT NOT NULL,
    end INT NOT NULL,
    length INT NOT NULL,
    transcriptRange VARCHAR(255) NOT NULL,
    transcriptLength INT NOT NULL,
    nucleotideSequence LONGTEXT NOT NULL,
    proteinSequence LONGTEXT NOT NULL
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 为geneID列创建索引以加快查询速度
cursor.execute("ALTER TABLE transcript ADD INDEX idx_geneID (geneID);")

# data = [
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.2', 'transcript2', 'intron', 20, 30, 10, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.2', 'transcript2', 'exon', 30, 50, 20, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.3', 'transcript3', 'exon', 50, 80, 30, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.3', 'transcript3', 'intron', 80, 90, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.3', 'transcript3', 'exon', 90, 100, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.4', 'transcript4', 'exon', 100, 110, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.4', 'transcript4', 'intron', 110, 120, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.4', 'transcript4', 'exon', 120, 130, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.1', 'GT42G000001.SO.1.5', 'transcript5', 'exon', 130, 140, 10, '130 - 140', 10, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
    
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.2', 'transcript2', 'intron', 20, 30, 10, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.2', 'transcript2', 'exon', 30, 50, 20, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.3', 'transcript3', 'exon', 50, 80, 30, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.3', 'transcript3', 'intron', 80, 90, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.2', 'GT42G000001.SO.2.3', 'transcript3', 'exon', 90, 100, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],

#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.2', 'transcript2', 'exon', 100, 110, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.2', 'transcript2', 'intron', 110, 120, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.2', 'transcript2', 'exon', 120, 130, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000001', 'GT42G000001.SO.3', 'GT42G000001.SO.3.3', 'transcript3', 'exon', 130, 140, 10, '130 - 140', 10, 'ATGCCGTAGGTCA', 'MAGNGAIV'],

#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.2', 'transcript2', 'intron', 20, 30, 10, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.2', 'transcript2', 'exon', 30, 50, 20, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.3', 'transcript3', 'exon', 50, 80, 30, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.3', 'transcript3', 'intron', 80, 90, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.3', 'transcript3', 'exon', 90, 100, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.4', 'transcript4', 'exon', 100, 110, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.4', 'transcript4', 'intron', 110, 120, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.4', 'transcript4', 'exon', 120, 130, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.1', 'GT42G000002.SO.1.5', 'transcript5', 'exon', 130, 140, 10, '130 - 140', 10, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
    
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.2', 'transcript2', 'intron', 20, 30, 10, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.2', 'transcript2', 'exon', 30, 50, 20, '20 - 50', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.3', 'transcript3', 'exon', 50, 80, 30, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.3', 'transcript3', 'intron', 80, 90, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.2', 'GT42G000002.SO.2.3', 'transcript3', 'exon', 90, 100, 10, '50 - 80', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],

#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.0', 'haplotype', 'haplotype', 1, 140, 140, '1 - 140', 140, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.1', 'transcript1', 'exon', 1, 20, 20, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.1', 'transcript1', 'intron', 20, 30, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.1', 'transcript1', 'exon', 30, 40, 10, '1 - 40', 40, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.2', 'transcript2', 'exon', 100, 110, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.2', 'transcript2', 'intron', 110, 120, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.2', 'transcript2', 'exon', 120, 130, 10, '100 - 130', 30, 'ATGCCGTAGGTCA', 'MAGNGAIV'],
#     ['GT42G000002', 'GT42G000002.SO.3', 'GT42G000002.SO.3.3', 'transcript3', 'exon', 130, 140, 10, '130 - 140', 10, 'ATGCCGTAGGTCA', 'MAGNGAIV']

# ]

# # 插入数据
# for line in data:
#     if len(line) == 12:
#         mosaicID, geneID, transcriptID, transcriptIndex, areaType, start, end, length, transcriptRange, transcriptLength, nucleotideSequence, proteinSequence = line
#         data_to_insert = (mosaicID, geneID, transcriptID, transcriptIndex, areaType, start, end, length, transcriptRange, transcriptLength, nucleotideSequence, proteinSequence)
#         # 推荐使用%s占位符来构建参数化的SQL语句, 参数化查询不仅可以提高性能，还可以防止SQL注入攻击
#         insert_sql = "INSERT INTO transcript (mosaicID, geneID, transcriptID, transcriptIndex, areaType, start, end, length, transcriptRange, transcriptLength, nucleotideSequence, proteinSequence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#         cursor.execute(insert_sql, data_to_insert)

# 读取数据文件并插入数据
data_file = './table_for_mysql/transcript_table.tsv'
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    cnt = 0
    start_time = time.time()  # 开始计时

    for line in reader:
        if len(line) == 12:
            data_to_insert = tuple(line)
            insert_sql = "INSERT INTO transcript (mosaicID, geneID, transcriptID, transcriptIndex, areaType, start, end, length, transcriptRange, transcriptLength, nucleotideSequence, proteinSequence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_sql, data_to_insert)

            cnt += 1
            if cnt % 10000 == 0: # 每插入一万行大约耗时70s，transcript文件约130万行，
                print(f"{cnt} records inserted. Time elapsed: {time.time() - start_time:.2f} seconds.")


# 提交更改并关闭连接
cnx.commit()
cursor.close()
cnx.close()