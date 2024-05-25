import pandas as pd

# csvFile = './testData/tpm/test.orthologous.tpm.filter.log2.csv'
# skipMosaicIDFile = './skipMosaicID.txt'
# sortHeaderFile = './sortHeader.txt'
# outputFile = './testData/tpm/mosaic_tpm_table.tsv'

csvFile = './tpm/orthologous.tpm.filter.log2.csv'
skipMosaicIDFile = './skipMosaicID.txt'
sortHeaderFile = './sortHeader.txt'
outputFile = './table_for_mysql/mosaic_tpm_table.tsv'

# 1. 读取CSV文件
df = pd.read_csv(csvFile) 

# 替换标题行中的'-'为'_'，以便在MySQL中创建数据表，当然也可以直接使用任意查看器的替换功能
df.columns = df.columns.str.replace('-', '_')

# 2. 读取skip.txt文件并过滤ID
with open(skipMosaicIDFile, 'r') as file:
    skip_ids = file.read().splitlines()
df = df[~df['mosaicID'].isin(skip_ids)]

# 按照 'mosaicID'排序
sorted_df = df.sort_values(by=['mosaicID'])

# 3. 保留四位小数
sorted_df = sorted_df.round(4)



# 4. 读取sortHeader.txt文件并重排列
with open(sortHeaderFile, 'r') as file:
    new_order = file.read().splitlines()
new_order.insert(0, 'mosaicID')
sorted_df = sorted_df[new_order]

# 5. 输出最终的表格到新的CSV文件
sorted_df.to_csv(outputFile,sep='\t', index=False)