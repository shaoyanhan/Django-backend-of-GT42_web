import pandas as pd
import time

# skip_list_filename = "./skipMosaicID.txt"
# varients_final_filename = "./testData/snp/test_variants.final.txt"
# iso_evidences_filename = "./testData/snp/test_iso_vars.final.txt"
# rna_evidences_filename = "./testData/snp/test_rna_vars.final.txt"
# haplotype_varients_filename = "./testData/snp/test_haplotypes.final.txt"

skip_list_filename = "./skipMosaicID.txt"
varients_final_filename = "./mosaic/variants.final.txt"
iso_evidences_filename = "./mosaic/iso_vars.final.txt"
rna_evidences_filename = "./mosaic/rna_vars.final.txt"
haplotype_varients_filename = "./mosaic/haplotypes.final.txt"

# Load data from files
skip_mosaic_id_df = pd.read_csv(skip_list_filename, names=['mosaicID'], header=None)
variants_final_df = pd.read_csv(varients_final_filename, sep='\t', names=['mosaicID', 'SNPSite', 'SNPType'], header=None, usecols=[0, 1, 2], skipinitialspace=True)
iso_vars_final_df = pd.read_csv(iso_evidences_filename, sep='\t', names=['mosaicID', 'SNPSite', 'SNPType', 'IsoSeqEvidence'], header=None)
rna_vars_final_df = pd.read_csv(rna_evidences_filename, sep='\t', names=['mosaicID', 'SNPSite', 'SNPType', 'RNASeqEvidence'], header=None)
haplotypes_final_df = pd.read_csv(haplotype_varients_filename, sep='\t', names=['mosaicID', 'areaType', 'haplotype'], header=None)
print("Data loaded successfully.\n")

# 使用 apply 和 lambda 结合iso_vars_final_df 和 rna_vars_final_df 的 SNPType 与 SeqEvidence 两列
iso_vars_final_df['IsoSeqEvidence'] = iso_vars_final_df.apply(lambda row: f"{row['SNPType']} : {row['IsoSeqEvidence']}", axis=1)
rna_vars_final_df['RNASeqEvidence'] = rna_vars_final_df.apply(lambda row: f"{row['SNPType']} : {row['RNASeqEvidence']}", axis=1)

# 添加临时列以用于对 haplotypes_final_df 排序
haplotypes_final_df['areaPrefix'] = haplotypes_final_df['areaType'].str.extract(r'([A-Za-z]+)\.')[0] # SO.1 -> SO
haplotypes_final_df['areaNumber'] = haplotypes_final_df['areaType'].str.extract(r'\.(\d+)')[0].astype(int) # SO.1 -> 1

# 按照 mosaicID, areaPrefix 和 areaNumber 排序
sorted_haplotypes_df = haplotypes_final_df.sort_values(by=['mosaicID', 'areaPrefix', 'areaNumber'])

# 删除用于排序的临时列
sorted_haplotypes_df = sorted_haplotypes_df.drop(['areaPrefix', 'areaNumber'], axis=1)
print("Haplotypes sorted successfully.\n")


# 根据skip_list过滤mosaicID，reset_index 函数使用了参数 drop=True 来重置索引
filtered_variants_df = variants_final_df[~variants_final_df['mosaicID'].isin(skip_mosaic_id_df['mosaicID'])].reset_index(drop=True)
final_df = filtered_variants_df.copy()
final_df.insert(1, 'areaType', 'SNP')
print("Variants filtered successfully.\n")



# Add evidence columns with default values
final_df['IsoSeqEvidence'] = 'none'
final_df['RNASeqEvidence'] = 'none'
final_df['haplotypeSNP'] = 'none'
final_df['color'] = '#000000'  # default color


# Merge for IsoSeqEvidence
final_df = pd.merge(final_df, iso_vars_final_df[['mosaicID', 'SNPSite', 'IsoSeqEvidence']], 
                    on=['mosaicID', 'SNPSite'], 
                    how='left', 
                    suffixes=('', '_iso'))

# Merge for RNASeqEvidence
final_df = pd.merge(final_df, rna_vars_final_df[['mosaicID', 'SNPSite', 'RNASeqEvidence']], 
                    on=['mosaicID', 'SNPSite'], 
                    how='left', 
                    suffixes=('', '_rna'))

# Rename and clean up if necessary
final_df['IsoSeqEvidence'] = final_df['IsoSeqEvidence_iso'].combine_first(final_df['IsoSeqEvidence'])
final_df['RNASeqEvidence'] = final_df['RNASeqEvidence_rna'].combine_first(final_df['RNASeqEvidence'])

# Drop the temporary columns
final_df.drop(columns=['IsoSeqEvidence_iso', 'RNASeqEvidence_rna'], inplace=True)

# # Fill IsoSeqEvidence and RNASeqEvidence
# cnt = 0
# start_time = time.time()  # 开始计时
# for idx, row in final_df.iterrows():
#     isoseq_evidence = iso_vars_final_df[(iso_vars_final_df['mosaicID'] == row['mosaicID']) & 
#                                         (iso_vars_final_df['SNPSite'] == row['SNPSite'])]['IsoSeqEvidence']
#     rnaseq_evidence = rna_vars_final_df[(rna_vars_final_df['mosaicID'] == row['mosaicID']) & 
#                                         (rna_vars_final_df['SNPSite'] == row['SNPSite'])]['RNASeqEvidence']
#     if not isoseq_evidence.empty:
#         final_df.at[idx, 'IsoSeqEvidence'] = isoseq_evidence.iloc[0]
#     if not rnaseq_evidence.empty:
#         final_df.at[idx, 'RNASeqEvidence'] = rnaseq_evidence.iloc[0]
#     cnt += 1
#     if cnt % 1000 == 0:
#         end_time = time.time()  # 结束计时
#         elapsed_time = end_time - start_time  # 计算总耗时
#         print(f"{cnt} rows fill IsoSeqEvidence and RNASeqEvidence processed.")
#         print(f"Elapsed time: {elapsed_time:.2f} seconds.\n")
#         start_time = time.time()
# print("IsoSeqEvidence and RNASeqEvidence filled successfully.\n")

# Fill haplotypeSNP and handling '?' cases
cnt = 0
start_time = time.time()  # 开始计时

for idx, row in final_df.iterrows():
    current_mosaicID = row['mosaicID']
    former_mosaicID = final_df.at[idx - 1, 'mosaicID'] if idx > 0 else None
    if current_mosaicID != former_mosaicID:
        sequence_idx = 0
        haplotypes = sorted_haplotypes_df[sorted_haplotypes_df['mosaicID'] == current_mosaicID]
    haplotype_snps = []
    
    for _, h_row in haplotypes.iterrows():
        snp_base = h_row['haplotype'][sequence_idx]  # adjust index for 0-based in Python
        if snp_base == '?':
            snp_base = 'no exon evidence'
        haplotype_snps.append(f"{h_row['mosaicID']}.{h_row['areaType']}:{snp_base}")
        
    if haplotype_snps:
        final_df.at[idx, 'haplotypeSNP'] = '; '.join(haplotype_snps)
    sequence_idx += 1
    cnt += 1

    if cnt % 10000 == 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{cnt} rows fill haplotypeSNP processed.")
        print(f"Elapsed time: {elapsed_time:.2f} seconds.\n")
        start_time = time.time()
print("haplotypeSNP filled successfully.\n")

# Map colors to SNP types: 050f2c, 003666, 00aeff, 3369e7, 8e43e7, b84592, ff4f81, ff6c5f, ffc168, 2dde98, 1cc7d0
color_mapping = {
    'A/C': '#050f2c', 'C/G': '#003666', 'A/G': '#00aeff', 'C/G/T': '#3369e7', 'G/T': '#8e43e7',
    'C/T': '#b84592', 'A/T': '#ff4f81', 'A/C/T': '#ff6c5f', 'A/G/T': '#ffc168', 'A/C/G': '#2dde98', 'A/C/G/T': '#1cc7d0'
}
print("Color mapping created successfully.\n")

# Apply color mapping
final_df['color'] = final_df['SNPType'].map(color_mapping)
print("Colors mapped successfully.\n")

# Save the final table
final_df.to_csv('./table_for_mysql/snp_table.tsv', sep='\t', index=False)
print("Final table saved successfully.\n")