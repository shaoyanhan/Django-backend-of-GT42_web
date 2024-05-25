import pandas as pd

# csvFile = './testData/tpm/test.gene.tpm.filter.log2.csv'
# skipMosaicIDFile = './skipMosaicID.txt'
# sortHeaderFile = './sortHeader.txt'
# outputFile = './testData/tpm/gene_tpm_table.tsv'

csvFile = './tpm/gene.tpm.filter.log2.csv'
skipMosaicIDFile = './skipMosaicID.txt'
sortHeaderFile = './sortHeader.txt'
outputFile = './table_for_mysql/gene_tpm_table.tsv'

# 读取CSV文件
df = pd.read_csv(csvFile)

# 替换标题行中的'-'为'_'，以便在MySQL中创建数据表，当然也可以直接使用任意查看器的替换功能
df.columns = df.columns.str.replace('-', '_')

# 添加两列
df['mosaicID'] = df['geneID'].astype(str).str.split('.').str[0] # 全分割取第一个 GT42G000001.SO.1 -> GT42G000001
df['xenologousID'] = df['geneID'].astype(str).str.rsplit('.', n=1).str[0] # 从右往左分割一次 GT42G000001.SO.1 -> GT42G000001.SO

# 读取skip.txt文件并过滤ID
with open(skipMosaicIDFile, 'r') as file:
    skip_ids = file.read().splitlines()
df = df[~df['mosaicID'].isin(skip_ids)]

# 添加临时列以用于对 df 排序
df['xenoPrefix'] = df['geneID'].astype(str).str.split('.').str[1] # GT42G000001.SO.1 -> SO
df['geneNumber'] = df['geneID'].str.split('.').str[2].astype(int) # GT42G000001.SO.1 -> 1

# 按照 'mosaicID', 'xenoPrefix', 'geneNumber'依次排序
sorted_df = df.sort_values(by=['mosaicID', 'xenoPrefix', 'geneNumber'])

# 删除用于排序的临时列
sorted_df = sorted_df.drop(['xenoPrefix', 'geneNumber'], axis=1)

# 保留四位小数
sorted_df = sorted_df.round(4)

# 4. 读取sortHeader.txt文件并重排列
with open(sortHeaderFile, 'r') as file:
    new_order = file.read().splitlines()
new_order = ['mosaicID', 'xenologousID', 'geneID'] + new_order
sorted_df = sorted_df[new_order]

# 5. 输出最终的表格到新的CSV文件
sorted_df.to_csv(outputFile,sep='\t', index=False)  # 输出文件名为'processed_file.csv'