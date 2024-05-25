import pandas as pd
import csv

mosaicID = []
xenologousID = []
geneID = []
transcriptID = []

# 从haplotype文件中提取mosaicID和geneID
haplotype_data_file = './table_for_mysql/haplotype_table.tsv'
with open(haplotype_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行
    for line in reader:
        mosaicID.append(line[0])
        geneID.append(line[1])

# 从xenologous文件中提取xenologousID
xenologous_data_file = './table_for_mysql/xenologous_tpm_table.tsv'
with open(xenologous_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行
    for line in reader:
        xenologousID.append(line[1])


# 从transcript文件中提取transcriptID
transcript_data_file = './table_for_mysql/transcript_table.tsv'
with open(transcript_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t') # 使用制表符分隔
    next(reader)  # 跳过标题行
    for line in reader:
        transcriptID.append(line[2])

def remove_duplicates(sorted_list):
    seen = set()
    unique_list = []
    for item in sorted_list:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list



# 对mosaicID和transcriptID进行去重
unique_mosaicID = remove_duplicates(mosaicID)
unique_transcriptID = remove_duplicates(transcriptID)

# 存储最终结果
genomeID = []

for id in unique_mosaicID:
    genomeID.append([id, 'mosaic']) # GT42G000001 mosaic
    genomeID.append([f'{id}.0.0', 'mosaic']) # GT42G000001.0.0 mosaic

for id in xenologousID:
    genomeID.append([id, 'xenologous']) # GT42G000001.SO xenologous

for id in geneID:
    # 如果geneID以'.0.0'结尾，则跳过
    if id.endswith('.0.0'):
        continue
    genomeID.append([id, 'gene']) # GT42G000001.SO.1 gene
    genomeID.append([f'{id}.0', 'gene']) # GT42G000001.SO.1.0 gene

for id in unique_transcriptID:
    # 如果transcriptID以'.0'结尾，则跳过
    if id.endswith('.0'):
        continue
    genomeID.append([id, 'transcript']) # GT42G000001.SO.1.1 transcript



# 保存数据到文件
df = pd.DataFrame(genomeID, columns=['genomeID', 'type'])
df.to_csv('./table_for_mysql/genomeID_table.tsv', sep='\t', index=False)

