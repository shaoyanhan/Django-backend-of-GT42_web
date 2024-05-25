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

# 创建数据表，标题为：mosaicID  xenologousID  geneID	Ca1_1	Ca1_2	Ca1_3	Ca2_1	Ca2_2	Ca2_3	Ca3_1	Ca3_2	Ca3_3	Ro1_1	Ro1_2	Ro1_3	Ro2_1	Ro2_2	Ro2_3	Le1_1	Le1_2	Le1_3	LS1_1	LS1_2	LS1_3	Bu1_1	Bu1_2	Bu1_3	In1_1	In1_2	In1_3	NR1_1	NR1_2	NR1_3	AM_1	AM_2	AM_3	Bu2_1	Bu2_2	Bu2_3	Sp_1	Sp_2	Sp_3	Br_1	Br_2	Br_3	St_1	St_2	St_3	Pi_1	Pi_2	Pi_3	Gl_2	Gl_3	LS2_2	LS2_3	In2_1	In2_3	No2_1	No2_2	No2_3	Bu3_1	Bu3_3	Le2_1	Le2_2	Le2_3
create_table_sql = """
CREATE TABLE IF NOT EXISTS gene_tpm (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mosaicID VARCHAR(255) NOT NULL,
    xenologousID VARCHAR(255) NOT NULL,
    geneID VARCHAR(255) NOT NULL,
    Ca1_1 DECIMAL(10, 4) NOT NULL,
    Ca1_2 DECIMAL(10, 4) NOT NULL,
    Ca1_3 DECIMAL(10, 4) NOT NULL,
    Ca2_1 DECIMAL(10, 4) NOT NULL,
    Ca2_2 DECIMAL(10, 4) NOT NULL,
    Ca2_3 DECIMAL(10, 4) NOT NULL,
    Ca3_1 DECIMAL(10, 4) NOT NULL,
    Ca3_2 DECIMAL(10, 4) NOT NULL,
    Ca3_3 DECIMAL(10, 4) NOT NULL,
    Ro1_1 DECIMAL(10, 4) NOT NULL,
    Ro1_2 DECIMAL(10, 4) NOT NULL,
    Ro1_3 DECIMAL(10, 4) NOT NULL,
    Ro2_1 DECIMAL(10, 4) NOT NULL,
    Ro2_2 DECIMAL(10, 4) NOT NULL,
    Ro2_3 DECIMAL(10, 4) NOT NULL,
    Le1_1 DECIMAL(10, 4) NOT NULL,
    Le1_2 DECIMAL(10, 4) NOT NULL,
    Le1_3 DECIMAL(10, 4) NOT NULL,
    LS1_1 DECIMAL(10, 4) NOT NULL,
    LS1_2 DECIMAL(10, 4) NOT NULL,
    LS1_3 DECIMAL(10, 4) NOT NULL,
    Bu1_1 DECIMAL(10, 4) NOT NULL,
    Bu1_2 DECIMAL(10, 4) NOT NULL,
    Bu1_3 DECIMAL(10, 4) NOT NULL,
    In1_1 DECIMAL(10, 4) NOT NULL,
    In1_2 DECIMAL(10, 4) NOT NULL,
    In1_3 DECIMAL(10, 4) NOT NULL,
    NR1_1 DECIMAL(10, 4) NOT NULL,
    NR1_2 DECIMAL(10, 4) NOT NULL,
    NR1_3 DECIMAL(10, 4) NOT NULL,
    AM_1 DECIMAL(10, 4) NOT NULL,
    AM_2 DECIMAL(10, 4) NOT NULL,
    AM_3 DECIMAL(10, 4) NOT NULL,
    Bu2_1 DECIMAL(10, 4) NOT NULL,
    Bu2_2 DECIMAL(10, 4) NOT NULL,
    Bu2_3 DECIMAL(10, 4) NOT NULL,
    Sp_1 DECIMAL(10, 4) NOT NULL,
    Sp_2 DECIMAL(10, 4) NOT NULL,
    Sp_3 DECIMAL(10, 4) NOT NULL,
    Br_1 DECIMAL(10, 4) NOT NULL,
    Br_2 DECIMAL(10, 4) NOT NULL,
    Br_3 DECIMAL(10, 4) NOT NULL,
    St_1 DECIMAL(10, 4) NOT NULL,
    St_2 DECIMAL(10, 4) NOT NULL,
    St_3 DECIMAL(10, 4) NOT NULL,
    Pi_1 DECIMAL(10, 4) NOT NULL,
    Pi_2 DECIMAL(10, 4) NOT NULL,
    Pi_3 DECIMAL(10, 4) NOT NULL,
    Gl_2 DECIMAL(10, 4) NOT NULL,
    Gl_3 DECIMAL(10, 4) NOT NULL,
    LS2_2 DECIMAL(10, 4) NOT NULL,
    LS2_3 DECIMAL(10, 4) NOT NULL,
    In2_1 DECIMAL(10, 4) NOT NULL,
    In2_3 DECIMAL(10, 4) NOT NULL,
    No2_1 DECIMAL(10, 4) NOT NULL,
    No2_2 DECIMAL(10, 4) NOT NULL,
    No2_3 DECIMAL(10, 4) NOT NULL,
    Bu3_1 DECIMAL(10, 4) NOT NULL,
    Bu3_3 DECIMAL(10, 4) NOT NULL,
    Le2_1 DECIMAL(10, 4) NOT NULL,
    Le2_2 DECIMAL(10, 4) NOT NULL,
    Le2_3 DECIMAL(10, 4) NOT NULL
   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)

# 为mosaicID列创建索引以加快查询速度
cursor.execute("ALTER TABLE gene_tpm ADD INDEX idx_mosaicID (mosaicID);")
cursor.execute("ALTER TABLE gene_tpm ADD INDEX idx_xenologousID (xenologousID);")
cursor.execute("ALTER TABLE gene_tpm ADD INDEX idx_geneID (geneID);")

# 读取数据文件并插入数据
# data_file = './testData/tpm/gene_tpm_table.tsv'
data_file = './table_for_mysql/gene_tpm_table.tsv'
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    cnt = 0
    start_time = time.time()  # 开始计时

    for line in reader:
        if len(line) == 65:
            data_to_insert = tuple(line)
            insert_sql = " INSERT INTO gene_tpm (mosaicID, xenologousID, geneID, Ca1_1, Ca1_2, Ca1_3, Ca2_1, Ca2_2, Ca2_3, Ca3_1, Ca3_2, Ca3_3, Ro1_1, Ro1_2, Ro1_3, Ro2_1, Ro2_2, Ro2_3, Le1_1, Le1_2, Le1_3, LS1_1, LS1_2, LS1_3, Bu1_1, Bu1_2, Bu1_3, In1_1, In1_2, In1_3, NR1_1, NR1_2, NR1_3, AM_1, AM_2, AM_3, Bu2_1, Bu2_2, Bu2_3, Sp_1, Sp_2, Sp_3, Br_1, Br_2, Br_3, St_1, St_2, St_3, Pi_1, Pi_2, Pi_3, Gl_2, Gl_3, LS2_2, LS2_3, In2_1, In2_3, No2_1, No2_2, No2_3, Bu3_1, Bu3_3, Le2_1, Le2_2, Le2_3) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_sql, data_to_insert)

            cnt += 1
            if cnt % 10000 == 0: # 每插入一万行大约耗时50s，mosaic_tpm文件约15万行，
                print(f"{cnt} records inserted. Time elapsed: {time.time() - start_time:.2f} seconds.")

# 提交更改并关闭连接
cnx.commit()
cursor.close()
cnx.close()