import re
from itertools import groupby

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

def parse_gff(gff_path):
    """
    读取一个gff文件并返回一个字典列表和一个字典。
    将所有exon行保存到字典列表中，将所有transcript行保存到字典中。
    """
    transcript_entries = {} # {transcript_id: [start, end], ...}
    exon_entries = [] # [{mosaic_id, gene_id, transcript_id, start, end}, ...]
    with open(gff_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                parts = line.split('\t')
                # 提取第2, 3, 4, 5, 9列
                feature_type = parts[2]  # 区分transcript和exon
                start = int(parts[3])
                end = int(parts[4])
                attributes = parts[8]
                # 从attributes中提取geneID和transcriptID
                gene_id_match = re.search(r'gene_id ""([^"]+)""', attributes) # 适应包含连续双引号的格式
                transcript_id_match = re.search(r'transcript_id ""([^"]+)""', attributes)
                if gene_id_match and transcript_id_match:
                    gene_id = gene_id_match.group(1)
                    transcript_id = transcript_id_match.group(1)
                    # 从gene_id或transcript_id中获取mosaicID
                    mosaic_id = gene_id.split('.')[0]
                    entry = {
                        # 'feature_type': feature_type,
                        'mosaic_id': mosaic_id,
                        'gene_id': gene_id,
                        'transcript_id': transcript_id,
                        'start': start,
                        'end': end,
                    }
                    # entries.append(entry)
                    if feature_type == 'transcript': # 存储transcript的start和end
                        transcript_entries[transcript_id] = [start, end]
                    else:
                        exon_entries.append(entry) # 存储exon的行
   
    return transcript_entries, exon_entries

# 读取skipMosaicID.txt文件，返回一个集合
def load_skip_list(skip_path):
    with open(skip_path, 'r') as file:
        return {line.strip() for line in file}

# 按照skip_mosaic_ids中的mosaic_id对entries进行过滤
def filter_entries(entries, skip_mosaic_ids):
    return [entry for entry in entries if entry['mosaic_id'] not in skip_mosaic_ids]

# 生成最终的数据表
def generate_rows(filtered_exon_entries, transcript_entries, cogent_final_fasta, transcriptome_final_fasta, transcriptome_final_pep):
    # 首先对 entries 按照transcriptID 进行排序，排序规则是：首先利用'.'将transcript_id拆分成四部分，
    # 例如：GT42G000001、SO、1、1，然后依次按照四部分进行排序，注意数字部分需要转换成整数进行排序，否则会出现1, 10, 2这种排序错误
    filtered_exon_entries.sort(key=lambda x: (x['transcript_id'].split('.')[0], x['transcript_id'].split('.')[1], int(x['transcript_id'].split('.')[2]), int(x['transcript_id'].split('.')[3])))
    
    # 根据gene_id进行分组，groupby函数返回一个迭代器，每次迭代返回一个元组，元组的第一个元素是分组的键，第二个元素是分组后的数据
    grouped_exon_entries = groupby(filtered_exon_entries, key=lambda x: x['gene_id'])

    rows = [] # 用于存储最终的数据表
    for gene_id, group in grouped_exon_entries: # 遍历分组后的数据
        group = list(group) # 将这一组gene_id对应的group转换为列表
        # 每一组group的第一行都添加一行haplotype行
        if gene_id in cogent_final_fasta:
            rows.append({
                'mosaicID': gene_id.split('.')[0],
                'geneID': gene_id,
                'transcriptID': f"{gene_id}.0",
                'transcriptIndex': 'haplotype',
                'areaType': 'haplotype',
                'start': 1,
                'end': len(cogent_final_fasta[gene_id]),
                'length': len(cogent_final_fasta[gene_id]),
                'transcriptRange': f"1 - {len(cogent_final_fasta[gene_id])}",
                'transcriptLength': len(cogent_final_fasta[gene_id]),
                'nucleotideSequence': cogent_final_fasta[gene_id],
                'proteinSequence': 'none'
            })

        current_transcript_id = ''
        former_transcript_id = None
        transcript_index = 0
        last_exon_end = 0
        current_exon_start = 0
        # 遍历group中的每一行，生成intron和exon行
        for i, exon in enumerate(group):
            current_transcript_id = exon['transcript_id']

            # 如果当前行的transcript_id和上一行的transcript_id不同，说明已经进入下一个transcript，transcript_index加1，并生成exon行
            if current_transcript_id != former_transcript_id: 
                transcript_index += 1
                areaType = 'exon'
            # 如果当前行的transcript_id和上一行的transcript_id相同，说明当前的可变剪接尚未结束，需要在当前exon和上一个exon之间生成intron行，然后再生成exon行
            else:
                # 生成intron行
                areaType = 'intron'
                current_exon_start = exon['start']
                start = last_exon_end + 1
                end = current_exon_start - 1

                rows.append({
                    'mosaicID': exon['mosaic_id'],
                    'geneID': exon['gene_id'],
                    'transcriptID': exon['transcript_id'],
                    'transcriptIndex': f"transcript{transcript_index}",
                    'areaType': areaType,
                    'start': start,
                    'end':end,
                    'length': end - start + 1,
                    'transcriptRange': f"{transcript_entries[current_transcript_id][0]} - {transcript_entries[current_transcript_id][1]}", # 包含intron区域
                    'transcriptLength': len(transcriptome_final_fasta[current_transcript_id]), # 只有exon区域的长度总和
                    'nucleotideSequence': transcriptome_final_fasta[current_transcript_id],  # 只有exon区域
                    # 先检查在transcriptome_final_pep字典中是否存在current_transcript_id，然后再填充具体蛋白序列
                    'proteinSequence': transcriptome_final_pep.get(current_transcript_id, 'none')
                })

            # 生成exon行
            areaType = 'exon'
            start = exon['start']
            end = exon['end']

            rows.append({
                'mosaicID': exon['mosaic_id'],
                'geneID': exon['gene_id'],
                'transcriptID': exon['transcript_id'],
                'transcriptIndex': f"transcript{transcript_index}",
                'areaType': areaType,
                'start': start,
                'end':end,
                'length': end - start + 1,
                'transcriptRange': f"{transcript_entries[current_transcript_id][0]} - {transcript_entries[current_transcript_id][1]}",
                'transcriptLength': len(transcriptome_final_fasta[current_transcript_id]),
                'nucleotideSequence': transcriptome_final_fasta[current_transcript_id],  # 填充具体序列
                # 先检查在transcriptome_final_pep字典中是否存在current_transcript_id，然后再填充具体蛋白序列
                'proteinSequence': transcriptome_final_pep.get(current_transcript_id, 'none')
            })

            last_exon_end = end
            former_transcript_id = current_transcript_id

    return rows


def main():
    skip_mosaic_ids_filename = "./skipMosaicID.txt"
    # cogent_final_fasta_filename = "./testData/transcript/test.cogent.final.fasta"
    # transcriptome_final_fasta_filename = "./testData/transcript/test.transcriptome.final.fasta"
    # transcriptome_final_pep_filename = "./testData/transcript/test.transcriptome.final.pep"
    # transcriptome_collapsed_final_gff_filename = "./testData/transcript/test.transcriptome.collapsed.final.gff"
    cogent_final_fasta_filename = "./cogent/cogent.final.fasta"
    transcriptome_final_fasta_filename = "./transcriptome/transcriptome.final.fasta"
    transcriptome_final_pep_filename = "./transcriptome/transcriptome.final.pep"
    transcriptome_collapsed_final_gff_filename = "./transcriptome/transcriptome.collapsed.final.gff"

    cogent_final_fasta = parse_fasta(cogent_final_fasta_filename)
    transcriptome_final_fasta = parse_fasta(transcriptome_final_fasta_filename)
    transcriptome_final_pep = parse_fasta(transcriptome_final_pep_filename)
    transcript_entries, exon_entries  = parse_gff(transcriptome_collapsed_final_gff_filename)

    skip_mosaic_ids = load_skip_list(skip_mosaic_ids_filename)
    filtered_exon_entries = filter_entries(exon_entries, skip_mosaic_ids)

    all_rows = generate_rows(filtered_exon_entries, transcript_entries, cogent_final_fasta, transcriptome_final_fasta, transcriptome_final_pep)

    # 保存数据到文件
    with open ('./table_for_mysql/transcript_table.tsv', 'w') as file:
        file.write("mosaicID\tgeneID\ttranscriptID\ttranscriptIndex\tareaType\tstart\tend\tlength\ttranscriptRange\ttranscriptLength\tnucleotideSequence\tproteinSequence\n")
        for row in all_rows:
            file.write(f"{row['mosaicID']}\t{row['geneID']}\t{row['transcriptID']}\t{row['transcriptIndex']}\t{row['areaType']}\t{row['start']}\t{row['end']}\t{row['length']}\t{row['transcriptRange']}\t{row['transcriptLength']}\t{row['nucleotideSequence']}\t{row['proteinSequence']}\n")


if __name__ == '__main__':
    main()