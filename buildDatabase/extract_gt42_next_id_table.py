import pandas as pd
import csv

mosaicID = []

# 从haplotype文件中提取mosaicID和geneID
haplotype_data_file = './table_for_mysql/haplotype_table.tsv'
with open(haplotype_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行
    for line in reader:
        mosaicID.append(line[0])


def remove_duplicates(sorted_list):
    seen = set()
    unique_list = []
    for item in sorted_list:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list

# 对mosaicID进行去重
unique_mosaicID = remove_duplicates(mosaicID)


# 存储最终结果
genomeID = []

for id in unique_mosaicID:
    genomeID.append([id, 'mosaic']) # GT42G000001 mosaic


# 保存数据到文件
df = pd.DataFrame(genomeID, columns=['nextID', 'type'])
df.to_csv('./table_for_mysql/gt42_next_id_table.tsv', sep='\t', index=False)

