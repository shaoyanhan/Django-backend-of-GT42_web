import itertools

def read_skip_list(filename):
    """
    从文件中读取要跳过的mosaicID，并返回一个集合。
    """
    with open(filename, 'r') as file:
        return {line.strip() for line in file}

def filter_dictionaries(mosaic_dict, gene_dict, skip_list):
    """
    删除skip_list中指定的mosaicID对应的条目。
    """
    # 过滤mosaic_dict
    filtered_mosaic_dict = {key: value for key, value in mosaic_dict.items() if key not in skip_list}
    
    # 过滤gene_dict
    filtered_gene_dict = {key: value for key, value in gene_dict.items() if key.split('.')[0] not in skip_list}
    
    return filtered_mosaic_dict, filtered_gene_dict


def parse_fasta(filename):
    """
    读取一个fasta文件并返回一个字典。
    键是序列的ID，值是对应的序列字符串。
    """
    fasta_dict = {}
    with open(filename, 'r') as file:
        sequence_id = None
        sequence = []
        for line in file:
            line = line.strip()  # 去除行尾的换行符
            if line.startswith('>'):  # 如果是描述行
                if sequence_id is not None:
                    # 保存上一个序列
                    fasta_dict[sequence_id] = ''.join(sequence)
                sequence_id = line[1:]  # 去除开头的>并保存序列ID
                sequence = []  # 重置序列列表
            else:
                sequence.append(line)
        if sequence_id is not None:
            # 保存最后一个序列
            fasta_dict[sequence_id] = ''.join(sequence)
    return fasta_dict

def sort_and_group(table_data):
    # 按mosaicID和geneID排序，确保mosaic排在其对应的gene序列之前
    table_data.sort(key=lambda x: (x['mosaicID'], x['geneID']))

    # 分组并排序gene序列
    sorted_data = []
    for mosaic_id, group in itertools.groupby(table_data, key=lambda x: x['mosaicID']):
        mosaic_and_genes = list(group)
        # 对mosaic的gene序列按亚型和尾号进行排序
        genes_only = [item for item in mosaic_and_genes if item['areaType'] != 'mosaic']
        genes_only.sort(key=lambda x: (x['geneID'].split('.')[1], int(x['geneID'].split('.')[2])))
        
        # 重新分配areaType
        haplotype_number = 1
        for gene in genes_only:
            gene['areaType'] = f"haplotype{haplotype_number}"
            haplotype_number += 1

        # 将排序后的gene序列添加回mosaic序列之后
        mosaic_entry = next(item for item in mosaic_and_genes if item['areaType'] == 'mosaic')
        sorted_data.append(mosaic_entry)
        sorted_data.extend(genes_only)

    return sorted_data


def generate_table(mosaic_filename, gene_filename):
    # 解析两个fasta文件
    mosaic_dict = parse_fasta(mosaic_filename)
    gene_dict = parse_fasta(gene_filename)

    # 读取要跳过的mosaicID
    skip_list = read_skip_list("skipMosaicID.txt")

    # 过滤mosaic_dict和gene_dict
    mosaic_dict, gene_dict = filter_dictionaries(mosaic_dict, gene_dict, skip_list)

    # 准备数据容器
    table_data = []

    # 处理mosaic序列
    for mosaic_id in mosaic_dict:
        # 生成.mosaic序列
        table_data.append({
            'mosaicID': f"{mosaic_id}",
            'geneID': f"{mosaic_id}.0.0",
            'areaType': 'mosaic',
            'length': len(mosaic_dict[mosaic_id]),
            'nucleotideSequence': mosaic_dict[mosaic_id]
        })

    # 处理gene序列，使用累积数量的方式命名haplotype
    haplotype_count = {}
    for gene_id in gene_dict:
        mosaic_id = gene_id.split('.')[0]  # 分离基本mosaicID
        haplotype_count[mosaic_id] = haplotype_count.get(mosaic_id, 0) + 1
        table_data.append({
            'mosaicID': f"{mosaic_id}",
            'geneID': gene_id,
            'areaType': f"haplotype{haplotype_count[mosaic_id]}",
            'length': len(gene_dict[gene_id]),
            'nucleotideSequence': gene_dict[gene_id]
        })

    # 对数据进行排序和分组
    table_data = sort_and_group(table_data)

    # 保存数据到文件
    with open('./table_for_mysql/haplotype_table.tsv', 'w') as file:
        file.write("mosaicID\tgeneID\tareaType\tlength\tnucleotideSequence\n")
        for row in table_data:
            file.write(f"{row['mosaicID']}\t{row['geneID']}\t{row['areaType']}\t{row['length']}\t{row['nucleotideSequence']}\n")
    # for row in table_data:
    #     print(f"{row['mosaicID']}\t{row['geneID']}\t{row['areaType']}\t{row['length']}\t{row['nucleotideSequence']}")

def main():
    mosaic_filename = "./mosaic/mosaic.cogent.final.fasta"
    gene_filename = "./cogent/cogent.final.fasta"
    # mosaic_filename = "./testData/test.mosaic.cogent.final.fasta"
    # gene_filename = "./testData/test.cogent.final.fasta"
    generate_table(mosaic_filename, gene_filename)

if __name__ == '__main__':
    main()