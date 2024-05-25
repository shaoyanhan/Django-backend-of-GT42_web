import pandas as pd
import csv
import time

def remove_duplicates(sorted_list):
    seen = set()
    unique_list = []
    for item in sorted_list:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list

mosaic_tpm_table_path = './table_for_mysql/mosaic_tpm_table.tsv'
transcript_tpm_table_path = './table_for_mysql/transcript_tpm_table.tsv'

mosaic_id_table = pd.read_csv(mosaic_tpm_table_path, sep='\t', usecols=['mosaicID'])
all_id_table = pd.read_csv(transcript_tpm_table_path, sep='\t', usecols=['mosaicID', 'xenologousID', 'geneID', 'transcriptID'])

# 用于存储最终结果的字典列表，格式：[{'GT42G0001': 'GT42G0001;GT420001.SO,GT42G0001.SS,...;GT420001.SO.1,...;GT420001.SO.1.1,...'}, ...]
result_dict_list = []

cnt = 0
start_time = time.time()
# 借助mosaic_id_table，从all_id_table中提取出所有的同一mosaicID的所有行，然后再进行提取这个mosaicID对应的所有homologousID的操作
for mosaic_id in mosaic_id_table['mosaicID']:

    filtered_table = all_id_table[all_id_table['mosaicID'] == mosaic_id]

    # 对xenologousID、geneID进行去重，由于是transcript的表格，transcriptID不需要去重
    unduplicated_xenologousID_list = remove_duplicates(filtered_table['xenologousID'].tolist())
    unduplicated_geneID_list = remove_duplicates(filtered_table['geneID'].tolist())
    unduplicated_transcriptID_list = filtered_table['transcriptID'].tolist()

    # 将去重后的xenologousID、geneID、transcriptID拼接成一个字符串，作为这个mosaicID所下属的所有ID的集合
    id_sequence = mosaic_id + ';' + ','.join(unduplicated_xenologousID_list) + ';' + ','.join(unduplicated_geneID_list) + ';' + ','.join(unduplicated_transcriptID_list)
    
    # 按照 ID：id_sequence 的格式存入结果字典列表，这样任何一个ID都可以通过这个字典列表找到其附属的mosaicID所对应的id_sequence
    result_dict_list.append({mosaic_id: id_sequence})
    for xenologous_id in unduplicated_xenologousID_list:
        result_dict_list.append({xenologous_id: id_sequence})
    for gene_id in unduplicated_geneID_list:
        result_dict_list.append({gene_id: id_sequence})
    for transcript_id in unduplicated_transcriptID_list:
        result_dict_list.append({transcript_id: id_sequence})

    cnt += 1
    if cnt % 1000 == 0:
        print('已处理{}个mosaicID，耗时{}s'.format(cnt, time.time()-start_time)) # 每1000个mosaicID约12s

# 将结果写入文件
with open('./table_for_mysql/homologous_id_table.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['genomeID', 'homologousIDSet'])
    for result_dict in result_dict_list:
        for key in result_dict.keys():
            writer.writerow([key, result_dict[key]])

