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

# 创建nodes数据表
create_table_sql = """
CREATE TABLE IF NOT EXISTS gt42_gene_network_nodes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    symbolSize DECIMAL(10, 4) NOT NULL,
    color VARCHAR(255) NOT NULL,
    totalDegree INT NOT NULL,
    inDegree INT NOT NULL,
    outDegree INT NOT NULL,
    adjacency LONGTEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)
# 为name列创建索引以加快查询速度
cursor.execute("ALTER TABLE gt42_gene_network_nodes ADD INDEX idx_name (name);")

# 创建edges数据表
create_table_sql = """
CREATE TABLE IF NOT EXISTS gt42_gene_network_edges (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    target VARCHAR(255) NOT NULL,
    width DECIMAL(10, 4) NOT NULL,
    color VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)
# 为source和target列创建索引以加快查询速度
cursor.execute("ALTER TABLE gt42_gene_network_edges ADD INDEX idx_source (source);")
cursor.execute("ALTER TABLE gt42_gene_network_edges ADD INDEX idx_target (target);")


# 读取数据文件并插入数据
nodes_data_file = './network/gene_network_nodes.tsv'
with open(nodes_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    cnt = 0
    start_time = time.time()  # 开始计时

    for row in reader:
        name, symbolSize, color, totalDegree, inDegree, outDegree, adjacency = row
        data_to_insert = (name, symbolSize, color, totalDegree, inDegree, outDegree, adjacency)
        insert_sql = "INSERT INTO gt42_gene_network_nodes (name, symbolSize, color, totalDegree, inDegree, outDegree, adjacency) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, data_to_insert)

        cnt += 1
        if cnt % 10000 == 0:
            print(f"{cnt} nodes processed. Time elapsed: {time.time() - start_time:.2f} seconds.")

edges_data_file = './network/gene_network_edges.tsv'
with open(edges_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行

    cnt = 0
    start_time = time.time()  # 开始计时

    for row in reader:
        source, target, width, color = row
        data_to_insert = (source, target, width, color)
        insert_sql = "INSERT INTO gt42_gene_network_edges (source, target, width, color) VALUES (%s, %s, %s, %s);"
        cursor.execute(insert_sql, data_to_insert)

        cnt += 1
        if cnt % 10000 == 0:
            print(f"{cnt} edges processed. Time elapsed: {time.time() - start_time:.2f} seconds.")

# 提交更改并关闭连接
cnx.commit()
cursor.close()
cnx.close()