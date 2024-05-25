# import networkx as nx
# import pandas as pd
# import math
# import time

# # Sony + More4 + Mapbox
# # 000000, 7c8285, bfbdb0, b1b134, bbd634, dbe3b6, b2c8bd, 165b65, 697d99, 96b8db, 00a4e8, a4dbdb, fdd666, dc9018, e31a22, df8f2d, b24f3f, b51f29, f58268, f4979c, 949483, f47b7b, 9f1f5c, ef9020, 00af3e, 85b7e2, 29245c, ffd616, e5352b, e990ab, 0081b4, 96cbb3, 91be3e, 39a6dd, eb0973, dde2e0, 333c41, 3bb2d0, 3887be, 8a8acb, 56b881, 50667f, 41afa5, f9886c, e55e5e, ed6498, fbb03b, 142736, 28353d, 222b30.
# # 
# colors = ['#b1b134', '#bbd634', '#b2c8bd', '#96b8db', '#a4dbdb', '#fdd666', '#dc9018', '#f58268', '#f4979c', '#f47b7b', '#ef9020', '#00af3e', '#85b7e2','#ffd616', '#e5352b', '#e990ab', '#96cbb3', '#91be3e', '#39a6dd', '#3bb2d0', '#8a8acb', '#56b881', '#41afa5', '#f9886c', '#e55e5e', '#ed6498', '#fbb03b']

# # 创建空图
# G = nx.DiGraph()  # 使用有向图以正确计算入度和出度

# # 从文件读取数据
# # data_path = './testData/network/test_orthologous.grnboost2.txt'
# # data_path = './network/orthologous.grnboost2.txt'
# # data_path = './network/xenologous.grnboost2.txt'
# data_path = './network/gene.grnboost2.txt'


# start_time = time.time()  # 开始计时
# # 从模拟数据添加边到图中
# with open(data_path, 'r') as file:
#     data = file.read()
#     for line in data.split('\n'):
#         if not line:
#             continue
#         node1, node2, weight = line.strip().split('\t')
#         weight = float(weight)
#         if weight >= 1:
#             G.add_edge(node1, node2, weight=weight)
# end_time = time.time()  # 结束计时
# print(f"Reading file Time cost: {end_time - start_time:.4f}s")

# # start_time = time.time()  # 开始计时
# # # 计算弹簧布局
# # pos = nx.spring_layout(G)  # 生成布局的位置信息
# # # pos = nx.spectral_layout(G)  # 生成布局的位置信息
# # end_time = time.time()  # 结束计时
# # print(f"Spring layout Time cost: {end_time - start_time:.4f}s")


# # 创建nodes和edges的DataFrame
# node_list = []
# edge_list = []

# cnt = 0
# start_time = time.time()  # 开始计时
# # 节点信息
# for node in G.nodes:
#     in_degree = G.in_degree(node)
#     out_degree = G.out_degree(node)
#     total_degree = in_degree + out_degree
#     # symbol_size = 10
#     symbol_size = math.log(in_degree + out_degree + 1) # 取自然对数作为节点大小，加1防止log(0)和log(1)的问题
#     # symbol_size = in_degree + out_degree  # 直接取入度和出度之和作为节点大小
#     adjacency_set = set()  # 使用集合来存储邻接点，自动处理重复
#     for neighbor in nx.all_neighbors(G, node):
#         adjacency_set.add(neighbor)
#     adjacency = ', '.join(adjacency_set)
#     color_index = len(node_list) % len(colors)  # 循环使用颜色列表
#     color = colors[color_index]
    
#     node_list.append({
#         'name': node,
#         # 'x': pos[node][0],
#         # 'y': pos[node][1],
#         'symbolSize': round(symbol_size, 4),
#         'color': color,
#         'totalDegree': total_degree,
#         'inDegree': in_degree,
#         'outDegree': out_degree,
#         'adjacency': adjacency
#     })

#     cnt += 1
#     if cnt % 10000 == 0:
#         print(f"{cnt} nodes processed. Time elapsed: {time.time() - start_time:.2f} seconds.")

# cnt = 0
# start_time = time.time()  # 开始计时
# # 边信息
# for edge in G.edges(data=True):
#     source, target, data = edge
#     width = round(data['weight'], 4)
#     color = next(item['color'] for item in node_list if item['name'] == source)  # 和源节点相同的颜色
#     edge_list.append({
#         'source': source,
#         'target': target,
#         # 'width': 1,
#         'width': width,
#         'color': color
#     })

#     cnt += 1
#     if cnt % 10000 == 0:
#         print(f"{cnt} edges processed. Time elapsed: {time.time() - start_time:.2f} seconds.")

# # 转换为DataFrame
# nodes_df = pd.DataFrame(node_list)
# edges_df = pd.DataFrame(edge_list)

# # edges_df.to_csv('./testData/network/edges.tsv', index=False, sep='\t')
# # nodes_df.to_csv('./testData/network/nodes.tsv', index=False, sep='\t')
# # edges_df.to_csv('./table_for_mysql/mosaic_network_edges.tsv', index=False, sep='\t')
# # nodes_df.to_csv('./table_for_mysql/mosaic_network_nodes.tsv', index=False, sep='\t')
# # edges_df.to_csv('./table_for_mysql/xenologous_network_edges.tsv', index=False, sep='\t')
# # nodes_df.to_csv('./table_for_mysql/xenologous_network_nodes.tsv', index=False, sep='\t')
# edges_df.to_csv('./table_for_mysql/gene_network_edges.tsv', index=False, sep='\t')
# nodes_df.to_csv('./table_for_mysql/gene_network_nodes.tsv', index=False, sep='\t')


import pandas as pd
import json

# 读取节点和边的数据
# nodes_df = pd.read_csv('./testData/network/nodes.tsv', sep='\t')
# edges_df = pd.read_csv('./testData/network/edges.tsv', sep='\t')
# edges_df = pd.read_csv('./table_for_mysql/mosaic_network_edges.tsv', sep='\t')
# nodes_df = pd.read_csv('./table_for_mysql/mosaic_network_nodes.tsv', sep='\t')
# edges_df = pd.read_csv('./table_for_mysql/xenologous_network_edges.tsv', sep='\t')
# nodes_df = pd.read_csv('./table_for_mysql/xenologous_network_nodes.tsv', sep='\t')
edges_df = pd.read_csv('./table_for_mysql/gene_network_edges.tsv', sep='\t')
nodes_df = pd.read_csv('./table_for_mysql/gene_network_nodes.tsv', sep='\t')

# mosaic: symbolSize: 2.5, width: 2, nodes: Array(1474), edges: Array(44925)
# xenologous: symbolSize: 2.5, width: 2, nodes: Array(2475), edges: Array(67990)
# gene: symbolSize: 4.2, width: 3, nodes: Array(3461), edges: Array(34495)
# 转换节点数据
nodes = []
for _, row in nodes_df.iterrows():
    if row['symbolSize'] < 4.2:
        continue
    node = {
        'name': row['name'],
        # 'x': row['x'] * 10000,
        # 'y': row['y'] * 10000,
        'symbolSize': row['symbolSize'],
        'itemStyle': {
            'color': row['color']
        },
        'totalDegree': row['totalDegree'],
        'inDegree': row['inDegree'],
        'outDegree': row['outDegree'],
        # 'adjacency': row['adjacency'].split(', ')
    }
    nodes.append(node)

# 转换边数据
edges = []
for _, row in edges_df.iterrows():
    if row['width'] < 3:
        continue
    edge = {
        'source': row['source'],
        'target': row['target'],
        'lineStyle': {
            # 'width': row['width'],
            'color': row['color']
        },
        'weight': row['width'] # 'width' -> 'weight
    }
    edges.append(edge)

# 构建JSON对象
graph = {
    'nodes': nodes,
    'edges': edges
}

# 保存到文件
# with open('./testData/network/graph.json', 'w') as f:
#     json.dump(graph, f, indent=4)
# with open('./table_for_mysql/mosaic_network_graph.json', 'w') as f:
#     json.dump(graph, f, indent=4)
# with open('./table_for_mysql/xenologous_network_graph.json', 'w') as f:
#     json.dump(graph, f, indent=4)
with open('./table_for_mysql/gene_network_graph.json', 'w') as f:
    json.dump(graph, f, indent=4)

print("JSON文件已生成")
