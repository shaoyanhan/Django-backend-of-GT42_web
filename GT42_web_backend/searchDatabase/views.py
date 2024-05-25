from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DatabaseError
import json
from django.db.models import Q # 用于构建复杂的查询表达式
from django.forms.models import model_to_dict
import logging

from .models import haplotype, snp, transcript, GT42GenomeID, mosaicTPM, xenologousTPM, geneTPM, transcriptTPM, GT42NextID, GT42MosaicNetworkNodes, GT42MosaicNetworkEdges, GT42XenologousNetworkNodes, GT42XenologousNetworkEdges, GT42GeneNetworkNodes, GT42GeneNetworkEdges, GT42HomologousID

# 定义类型到模型映射字典，这里不考虑多级映射，因为需要使用递归访问，会增加复杂度
mosaic_network_nodes_model_map = {
    'mosaic': GT42MosaicNetworkNodes,
    'xenologous': GT42XenologousNetworkNodes,
    'gene': GT42GeneNetworkNodes,
    # 添加更多基因组与模型的映射
}
mosaic_network_edges_model_map = {
    'mosaic': GT42MosaicNetworkEdges,
    'xenologous': GT42XenologousNetworkEdges,
    'gene': GT42GeneNetworkEdges,
    # 添加更多基因组与模型的映射
}

# 定义网络图JSON文件路径映射字典, 与manage.py同级目录下的文件路径
network_graph_json_path_map = {
    'mosaic': 'searchDatabase/dataFiles/mosaic_network_graph.json',
    'xenologous': 'searchDatabase/dataFiles/xenologous_network_graph.json',
    'gene': 'searchDatabase/dataFiles/gene_network_graph.json',
}



# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the searchDatabase index.")

# def getHaplotypeTable(request):
#     # 从GET参数中获取关键字 
#     # 请求api：http://127.0.0.1:8080/searchDatabase/getHaplotypeTable/?searchKeyword=GT42G000002
#     searchKeyword = request.GET.get('searchKeyword', '')  # 如果没有关键字，默认为空字符串
#     if not searchKeyword:
#         raise Http404("searchKeyword parameter is required")  # 如果没有提供关键字，返回404错误
#     tableData = haplotype.objects.filter(mosaicID=searchKeyword)  # 使用过滤器来筛选符合条件的记录 
#     # 通过一个列表推导式创建了一个字典列表serialized_data，
#     # 其中每个字典代表一个Haplotype实例的字段值。然后我们将这个列表传递给JsonResponse来生成JSON响应
#     serialized_data = [
#         {
#             # 'id': instance.id,
#             'mosaicID': instance.mosaicID,
#             'geneID': instance.geneID,
#             'geneType': instance.geneType,
#             'length': instance.length,
#             'nucleotideSequence': instance.nucleotideSequence,
#         }
#         for instance in tableData
#     ]
#     return JsonResponse(serialized_data, safe=False)  # 返回序列化的数据

# def getSNPTable(request):
#     # 从GET参数中获取关键字 
#     # 请求api：http://127.0.0.1:8080/searchDatabase/getSNPTable/?searchKeyword=GT42G000002
#     searchKeyword = request.GET.get('searchKeyword', '')  # 如果没有关键字，默认为空字符串
#     if not searchKeyword:
#         raise Http404("searchKeyword parameter is required")  # 如果没有提供关键字，返回404错误
#     tableData = snp.objects.filter(mosaicID=searchKeyword)  # 使用过滤器来筛选符合条件的记录 
#     # 通过一个列表推导式创建了一个字典列表serialized_data，
#     # 其中每个字典代表一个SNP实例的字段值。然后我们将这个列表传递给JsonResponse来生成JSON响应
#     serialized_data = [
#         {
#             # 'id': instance.id,
#             'mosaicID': instance.mosaicID,
#             'geneType': instance.geneType,
#             'SNPSite': instance.SNPSite,
#             'SNPType': instance.SNPType,
#             'IsoSeqEvidence': instance.IsoSeqEvidence,
#             'RNASeqEvidence': instance.RNASeqEvidence,
#             'haplotypeSNP': instance.haplotypeSNP,
#             'color': instance.color,
#         }
#         for instance in tableData
#     ]
#     return JsonResponse(serialized_data, safe=False)  # 返回序列化的数据

# def getTranscriptTable(request):
#     # 从GET参数中获取关键字 
#     # 请求api：http://127.0.0.1:8080/searchDatabase/getTranscriptTable/?searchKeyword=GT42G000001.SO.1
#     searchKeyword = request.GET.get('searchKeyword', '')  # 如果没有关键字，默认为空字符串
#     if not searchKeyword:
#         raise Http404("searchKeyword parameter is required")  # 如果没有提供关键字，返回404错误
#     tableData = transcript.objects.filter(geneID=searchKeyword)  # 使用过滤器来筛选符合条件的记录
#     # 通过一个列表推导式创建了一个字典列表serialized_data，
#     # 其中每个字典代表一个Transcript实例的字段值。然后我们将这个列表传递给JsonResponse来生成JSON响应
#     serialized_data = [
#         {
#             # 'id': instance.id,
#             'mosaicID': instance.mosaicID,
#             'geneID': instance.geneID,
#             'transcriptID': instance.transcriptID,
#             'transcriptIndex': instance.transcriptIndex,
#             'isExon': instance.isExon,
#             'start': instance.start,
#             'end': instance.end,
#             'length': instance.length,
#             'transcriptRange': instance.transcriptRange,
#             'transcriptLength': instance.transcriptLength,
#             'proteinSequence': instance.proteinSequence,
#             'nucleotideSequence': instance.nucleotideSequence,
#         }
#         for instance in tableData
#     ]
#     return JsonResponse(serialized_data, safe=False)  # 返回序列化的数据


# 获取原生数据表
def getTable(model, filterField, type, request):
    # 从GET参数中获取关键字 
    # 请求api：
        # http://127.0.0.1:8080/searchDatabase/getHaplotypeTable/?searchKeyword=GT42G000002
        # http://127.0.0.1:8080/searchDatabase/getSNPTable/?searchKeyword=GT42G000002
        # http://127.0.0.1:8080/searchDatabase/getTranscriptTable/?searchKeyword=GT42G000001.SO.1
    searchKeyword = request.GET.get('searchKeyword', '')  # 如果没有关键字，默认为空字符串
    if not searchKeyword:
        raise Http404("searchKeyword parameter is required!")  # 如果没有提供关键字，返回404错误
    
    filter_kwargs = {filterField: searchKeyword} # 创建了一个字典filter_kwargs，其键为filterField变量的值（即字段名），其值为searchKeyword。    
    tableData = model.objects.filter(**filter_kwargs) # 字典展开操作符，它将filter_kwargs字典的键值对展开为函数的参数。这意味着如果filter_kwargs为{'mosaicID': 'GT42G000001'}，则**filter_kwargs会被解释为mosaicID='GT42G000001'。
    if not tableData:
        raise Http404("No data found!")

    dataItems = list(tableData.values()) # 将查询集转换为字典列表
    response_data = {
        'type': type, # 前端根据这个字段来判断是哪种数据表
        'data': dataItems,
    }
    return JsonResponse(response_data, safe=False)  # 返回序列化的数据

def getHaplotypeTable(request):
    return getTable(haplotype, 'mosaicID', 'haplotype', request)

def getSNPTable(request):
    return getTable(snp, 'mosaicID', 'SNP', request)

def getTranscriptTable(request):
    return getTable(transcript, 'geneID', 'transcript', request)

def getMosaicTPMTable(request):
    return getTable(mosaicTPM, 'mosaicID', 'mosaicTPM', request)

def getXenologousTPMTable(request):
    return getTable(xenologousTPM, 'mosaicID', 'xenologousTPM', request)

def getGeneTPMTable(request):
    return getTable(geneTPM, 'mosaicID', 'geneTPM', request)

def getTranscriptTPMTable(request):
    return getTable(transcriptTPM, 'geneID', 'transcriptTPM', request)




def getTableByPage(model, filterField, paginationType, request, itemsPerPage=10):
        # 请求api：
        # http://127.0.0.1:8080/searchDatabase/getHaplotypeTableByPage/?searchKeyword=GT42G000001&page=1
        # http://127.0.0.1:8080/searchDatabase/getSNPTableByPage/?searchKeyword=GT42G000001&page=1
        # http://127.0.0.1:8080/searchDatabase/getTranscriptTableByPage/?searchKeyword=GT42G000001.SO.1&page=1

    searchKeyword = request.GET.get('searchKeyword', '') # 从GET参数中获取关键字 
    page = request.GET.get('page', 1) # 从GET参数中获取请求分页的页码

    if not searchKeyword: # 如果没有提供关键字，返回404错误
        raise Http404("searchKeyword parameter is required")

    filter_kwargs = {filterField: searchKeyword} # 创建了一个字典filter_kwargs，其键为filterField变量的值（即字段名），其值为searchKeyword。    
    tableData = model.objects.filter(**filter_kwargs) # 字典展开操作符，它将filter_kwargs字典的键值对展开为函数的参数。这意味着如果filter_kwargs为{'mosaicID': 'GT42G000001'}，则**filter_kwargs会被解释为mosaicID='GT42G000001'。

    print('tableData: ',tableData)

    recordsCount = tableData.count() # 记录总数

    paginator = Paginator(tableData, itemsPerPage)
    print('paginator: ', paginator) 
    numPages = paginator.num_pages # 总页数

    try:
        data = paginator.page(page)
    except PageNotAnInteger: # 如果页码不是一个整数，则展示第一页
        data = paginator.page(1)
    except EmptyPage: # 如果页码超出范围，则展示最后一页的结果
        data = paginator.page(numPages)

    if not data:
        raise Http404("No data found!")

    print('data: ',data)
    print('data.object_list: ', data.object_list)

    currentPage = data.number
    print(type(data.object_list))
    dataItems = list(data.object_list.values()) # 将查询集转换为字典列表

    print(dataItems)

    response_data = {
        'numPages': numPages,
        'currentPage': currentPage,
        'pageSize': itemsPerPage,
        'totalRecords': recordsCount,
        'searchKeyword': searchKeyword,
        'type': paginationType,
        'data': dataItems,
    }

    print('response_data: ', response_data)

    return JsonResponse(response_data, safe=False)

def getHaplotypeTableByPage(request):
    return getTableByPage(haplotype, 'mosaicID', 'haplotypePagination', request)

def getSNPTableByPage(request):
    return getTableByPage(snp, 'mosaicID', 'SNPPagination', request)

def getTranscriptTableByPage(request):
    return getTableByPage(transcript, 'geneID', 'transcriptPagination', request)

def getMosaicTPMTableByPage(request):
    return getTableByPage(mosaicTPM, 'mosaicID', 'mosaicTPMPagination', request, 5)

def getXenologousTPMTableByPage(request):
    return getTableByPage(xenologousTPM, 'mosaicID', 'xenologousTPMPagination', request, 5)

def getGeneTPMTableByPage(request):
    return getTableByPage(geneTPM, 'mosaicID', 'geneTPMPagination', request, 5)

def getTranscriptTPMTableByPage(request):
    return getTableByPage(transcriptTPM, 'geneID', 'transcriptTPMPagination', request, 10)




def validateGenomeID(request):
    # 请求api：http://127.0.0.1:8080/searchDatabase/validateGenomeID/?genomeID=GT42G000001
    query_id = request.GET.get('genomeID', '')
    if not query_id: # 如果没有提供关键字，返回400错误
        return JsonResponse({'status': 'error', 'message': 'Genome ID is required.'}, status=400)

    try: # 查询数据库
        obj = GT42GenomeID.objects.get(genomeID=query_id) # 如果找到，返回ID和ID的类型
        return JsonResponse({'status': 'success', 'id': obj.genomeID, 'type': obj.type})
    except GT42GenomeID.DoesNotExist: 
        message = 'Genome ID: ' + query_id + ' not found!' # 如果未找到，返回错误消息
        return JsonResponse({'status': 'error', 'message': message}, status=404)
    
    # 如果数据库查询出错，返回错误消息，异常将被捕获，并将其实例化对象赋值给变量e，出于安全考虑，
    # 通常不推荐将详细的内部错误信息直接暴露给最终用户。在生产环境中，更倾向于记录这些详细信息到日志文件中，并给用户返回一个更通用的错误消息。
    except DatabaseError as e: 
        return JsonResponse({'status': 'error', 'message': 'Database error occurred.'}, status=500)
    
# 获取原生数据表
def getGenomeIDList(request):
    # 从GET参数中获取关键字 
    # 请求api：
        # http://127.0.0.1:8080/searchDatabase/getGenomeIDList/

    try:    
        tableData = GT42GenomeID.objects.all() # 查询所有记录
    except DatabaseError as e: # 如果数据库查询出错，返回错误消息
        return JsonResponse({'status': 'error', 'message': 'Database error occurred.'}, status=500)
    
    dataItems = list(tableData.values()) # 将查询集转换为字典列表

    response_data = {
        'type': 'genomeIDList', # 前端根据这个字段来判断是哪种数据表
        'data': dataItems,
    }
    return JsonResponse(response_data, safe=False)  # 返回序列化的数据


def getGT42NextID(request):
    # 请求api：http://127.0.0.1:8080/searchDatabase/getGT42NextID/?currentIDIndex=1
    currentIDIndex = request.GET.get('currentIDIndex', '') # 从GET参数中获取关键字
    if not currentIDIndex: # 如果没有提供关键字，返回400错误
        return JsonResponse({'status': 'error', 'message': 'Current ID Index is required.'}, status=400)
    
    genomeID = ''

    try:
        if currentIDIndex.isdigit() or currentIDIndex == '-1':
            # 如果只有数字，转换成整数
            currentIDIndex = int(currentIDIndex)
        else: 
            # 如果不是数字，证明用户当前是想通过ID来查询其对应的索引值，而不是通过ID的索引来查询
            genomeID = currentIDIndex
            currentIDIndex = GT42NextID.objects.get(nextID=genomeID).id - 1 # 查询数据库，获取ID的索引，并减1，这样能够获取到当前ID的上一个ID的索引，兼容接下来的currentIDIndex + 1
    except GT42NextID.DoesNotExist: # 如果未找到，返回错误消息
        message = 'ID Index: ' + str(currentIDIndex) + ' not found!'
        return JsonResponse({'status': 'error', 'message': message}, status=404)
    
    nextIDIndex = currentIDIndex + 1 # 计算下一个ID的索引
    # 如果下一个ID的索引为0，则重置为表格最大ID的索引，相当于循环
    if nextIDIndex == 0:
        nextIDIndex = GT42NextID.objects.all().count()
    # 如果下一个ID的索引大于数据库表格的最大ID的索引，则重置为1
    if nextIDIndex > GT42NextID.objects.all().count():
        nextIDIndex = 1

    try:
        obj = GT42NextID.objects.get(id=nextIDIndex) # 查询数据库
        return JsonResponse({'status': 'success', 'id': obj.id, 'nextID': obj.nextID , 'type': obj.type}) # 如果找到，返回ID和ID的类型
    except GT42NextID.DoesNotExist: # 如果未找到，返回错误消息
        message = 'ID Index: ' + str(nextIDIndex) + ' not found!'
        return JsonResponse({'status': 'error', 'message': message}, status=404)
    except DatabaseError as e: # 如果数据库查询出错，返回错误消息
        return JsonResponse({'status': 'error', 'message': 'Database error occurred.'}, status=500)
    
# 获取Hub网络图JSON数据
def getNetworkGraphJSONFile(request):
    # 请求api：http://127.0.0.1:8080/searchDatabase/getNetworkGraphJSONFile/?type=mosaic
    graphType = request.GET.get('type', '') # 从GET参数中获取关键字
    if not graphType: # 如果没有提供关键字，返回400错误
        return JsonResponse({'error': 'Graph type is required!'}, status=400)
    
    filePath = network_graph_json_path_map.get(graphType) # 根据graphType获取相应的JSON文件路径

    with open(filePath, 'r') as file:
        data = json.load(file)

    return JsonResponse(data)



def getNetworkGraphJSON(request):
    # 请求api：http://127.0.0.1:8080/searchDatabase/getNetworkGraphJSON/?type=mosaic&searchKeyword=GT42G000001
    dataType = request.GET.get('type', '') # 从GET参数中获取关键字
    if not dataType: # 如果没有提供关键字，返回400错误
        return JsonResponse({'error': 'Type is required!'}, status=400)
    
    searchKeyword = request.GET.get('searchKeyword', '') # 从GET参数中获取关键字
    if not searchKeyword: # 如果没有提供关键字，返回400错误
        return JsonResponse({'error': 'Search keyword is required!'}, status=400)
    
    network_nodes_model = mosaic_network_nodes_model_map.get(dataType)  # 根据genome获取相应的模型
    network_edges_model = mosaic_network_edges_model_map.get(dataType)  # 根据genome获取相应的模型
    if not network_nodes_model or not network_edges_model:
        return JsonResponse({'error': 'Invalid genome type'}, status=400)

    # 数据库查询       
    filter_kwargs = Q(name=searchKeyword) # 先找到这个点的节点信息
    nodesTableData = network_nodes_model.objects.filter(filter_kwargs) # 字典展开操作符，它将filter_kwargs字典的键值对展开为函数的参数。这意味着如果filter_kwargs为{'mosaicID': 'GT42G000001'}，则**filter_kwargs会被解释为mosaicID='GT42G000001'。
    adjacencies = nodesTableData[0].adjacency.split(', ') if nodesTableData else [] # 找到这个点的邻接点信息

    filter_kwargs = Q(source=searchKeyword) | Q(target=searchKeyword) # 找到所有指向这个点的边和这个点指向的边
    edgesTableData = network_edges_model.objects.filter(filter_kwargs)

    for i in range(len(adjacencies)): # 遍历邻接点
        adjacency = adjacencies[i]
        if adjacency: # 防止只有一个邻接点的时候split后包含空字符串
            filter_kwargs = Q(name=adjacency) # 找到邻接点的节点信息
            nodesTableData |= network_nodes_model.objects.filter(filter_kwargs) # |= 是查询集的合并操作符，它用于将后续查询的结果添加到nodesTableData查询集中
        # for j in range(i+1, len(adjacencies)): # 找到其余邻接点之间的边，确保出现在网络图中的点之间的边都显示
        #     left_adjacency = adjacencies[j]
        #     if left_adjacency:
        #         filter_kwargs = Q(source=adjacency, target=left_adjacency) | Q(source=left_adjacency, target=adjacency) 
        #         edgesTableData |= network_edges_model.objects.filter(filter_kwargs)
            filter_kwargs = Q(source=adjacency) | Q(target=adjacency) # 找到邻接点指出和指向的边，需要优化
            edgesTableData |= network_edges_model.objects.filter(filter_kwargs)

    if not nodesTableData:
        return JsonResponse({'error': 'No nodesTableData found!'}, status=404)
    if not edgesTableData:
        return JsonResponse({'error': 'No edgesTableData found!'}, status=404)

    # 转换tableData为所需的JSON格式
    graph = {
        'nodes': [
            {
                'name': node.name,
                'symbolSize': node.symbolSize,
                'itemStyle': {
                    'color': node.color
                },
                'totalDegree': node.totalDegree,
                'inDegree': node.inDegree,
                'outDegree': node.outDegree,
                'adjacency': node.adjacency.split(', ')
            } for node in nodesTableData
        ],
        'edges': [
            {
                'source': edge.source,
                'target': edge.target,
                'lineStyle': {
                    'width': edge.width,
                    'color': edge.color
                }
            } for edge in edgesTableData
        ]
    }
    
    # 封装
    response_data = {
        'type': dataType + 'NetworkGraphJSON', # 前端根据这个字段来判断是哪种数据表
        'data': graph,
    }

    return JsonResponse(response_data)



def getNetworkNodesTableByPage(model, paginationType, request, itemsPerPage=10):
    # 请求api：
    # http://127.0.0.1:8080/searchDatabase/getMosaicNetworkNodesTableByPage/?searchKeyword=GT42G000001&page=1
    # http://127.0.0.1:8080/searchDatabase/getXenologousNetworkNodesTableByPage/?searchKeyword=GT42G000001.SO&page=1
    # http://127.0.0.1:8080/searchDatabase/getGeneNetworkNodesTableByPage/?searchKeyword=GT42G000103.SO.1&page=1

    searchKeyword = request.GET.get('searchKeyword', '')
    if not searchKeyword:
        return JsonResponse({'error': 'Search keyword is required!'}, status=400)
    
    # 从GET参数中获取请求分页的页码，默认为第一页
    page = request.GET.get('page', 1) 
    
    # 初始查询，获取节点和邻接点信息
    nodesTableData = model.objects.filter(name=searchKeyword)
    if not nodesTableData.exists():
        return JsonResponse({'error': 'No nodes found with the specified search keyword'}, status=404)

    # 获取邻接点信息并进行合并查询
    adjacencies = nodesTableData[0].adjacency.split(', ') if nodesTableData[0].adjacency else []
    nodesTableData = model.objects.filter(name__in=adjacencies + [searchKeyword]).values() # 使用 + 来将当前点合并进列表，并将查询集转换为字典列表

    # 分页逻辑
    paginator = Paginator(nodesTableData, itemsPerPage)
    try:
        data = paginator.page(page)
    except PageNotAnInteger: # 如果页码不是一个整数，则展示第一页
        data = paginator.page(1)
    except EmptyPage: # 如果页码超出范围，则展示最后一页的结果
        if paginator.num_pages > 0:
            data = paginator.page(paginator.num_pages)
        else: # 如果没有数据，返回404错误
            return JsonResponse({'error': 'No pages available'}, status=404)

    # 构造响应数据
    response_data = {
        'numPages': paginator.num_pages, # 总页数
        'currentPage': data.number, # 当前页码
        'pageSize': itemsPerPage, # 每页记录数
        'totalRecords': len(nodesTableData), # 总记录数
        'searchKeyword': searchKeyword,
        'type': paginationType,
        'data': list(data.object_list)  # 直接使用已经是字典的列表
    }

    return JsonResponse(response_data)


def getNetworkEdgesTableByPage(model, paginationType, request, itemsPerPage=10):
    # 请求api：
    # http://127.0.0.1:8080/searchDatabase/getMosaicNetworkEdgesTableByPage/?searchKeyword=GT42G000001&page=1
    # http://127.0.0.1:8080/searchDatabase/getXenologousNetworkEdgesTableByPage/?searchKeyword=GT42G000001.SO&page=1
    # http://127.0.0.1:8080/searchDatabase/getGeneNetworkEdgesTableByPage/?searchKeyword=GT42G000103.SO.1&page=1

    searchKeyword = request.GET.get('searchKeyword', '') # 从GET参数中获取关键字
    if not searchKeyword: # 如果没有提供关键字，返回400错误
        return JsonResponse({'error': 'Search keyword is required!'}, status=400)
    
    # 从GET参数中获取请求分页的页码，默认为第一页
    page = request.GET.get('page', 1) 

    # 找到所有指向这个点的边和这个点指向的边
    filter_kwargs = Q(source=searchKeyword) | Q(target=searchKeyword) 
    edgesTableData = model.objects.filter(filter_kwargs).values() # 将查询集转换为字典列表

    if not edgesTableData:
        return JsonResponse({'error': 'No edgesTableData found!'}, status=404)

    # 分页逻辑
    paginator = Paginator(edgesTableData, itemsPerPage)
    try:
        data = paginator.page(page)
    except PageNotAnInteger: # 如果页码不是一个整数，则展示第一页
        data = paginator.page(1)
    except EmptyPage: # 如果页码超出范围，则展示最后一页的结果
        if paginator.num_pages > 0:
            data = paginator.page(paginator.num_pages)
        else: # 如果没有数据，返回404错误
            return JsonResponse({'error': 'No pages available'}, status=404)

    response_data = {
        'numPages': paginator.num_pages, # 总页数
        'currentPage': data.number, # 当前页码
        'pageSize': itemsPerPage,
        'totalRecords': edgesTableData.count(), # 总记录数
        'searchKeyword': searchKeyword,
        'type': paginationType,
        'data': list(data.object_list)  # 直接使用已经是字典的列表
    }

    return JsonResponse(response_data, safe=False)

def getMosaicNetworkNodesTableByPage(request):
    return getNetworkNodesTableByPage(GT42MosaicNetworkNodes, 'mosaicNetworkNodesPagination', request)

def getMosaicNetworkEdgesTableByPage(request):
    return getNetworkEdgesTableByPage(GT42MosaicNetworkEdges, 'mosaicNetworkEdgesPagination', request)

def getXenologousNetworkNodesTableByPage(request):
    return getNetworkNodesTableByPage(GT42XenologousNetworkNodes, 'xenologousNetworkNodesPagination', request)

def getXenologousNetworkEdgesTableByPage(request):
    return getNetworkEdgesTableByPage(GT42XenologousNetworkEdges, 'xenologousNetworkEdgesPagination', request)

def getGeneNetworkNodesTableByPage(request):
    return getNetworkNodesTableByPage(GT42GeneNetworkNodes, 'geneNetworkNodesPagination', request)

def getGeneNetworkEdgesTableByPage(request):
    return getNetworkEdgesTableByPage(GT42GeneNetworkEdges, 'geneNetworkEdgesPagination', request)


def getHomologousIDSet(request):
    # 请求api：http://127.0.0.1:8080/searchDatabase/getHomologousIDSet/?searchKeyword=GT42G000001
    searchKeyword = request.GET.get('searchKeyword', '') # 从GET参数中获取关键字
    if not searchKeyword: # 如果没有提供关键字，返回400错误
        return JsonResponse({'error': 'Search keyword is required!'}, status=400)
    
    # 数据库查询
    filter_kwargs = Q(genomeID=searchKeyword) # 找到所有同源ID为searchKeyword的记录
    tableData = GT42HomologousID.objects.filter(filter_kwargs).values() # 将查询集转换为字典列表

    if not tableData:
        return JsonResponse({'error': 'No homologousIDSet found!'}, status=404)
    
    # 对查询结果的第二列元素进行拆分，先按照';'分隔为四个部分，分别为mosaic, xenologous, gene, transcript，在填充JSON格式的时候再按照','分隔为具体的ID列表
    mosaicID_list_sequence, xenologousID_list_sequence, geneID_list_sequence, transcriptID_list_sequence = tableData[0].get('homologousIDSet').split(';')

    # 转换为JSON格式
    response_data = {
        'mosaic': mosaicID_list_sequence.split(','),
        'xenologous': xenologousID_list_sequence.split(','),
        'gene': geneID_list_sequence.split(','),
        'transcript': transcriptID_list_sequence.split(','),
    }

    return JsonResponse(response_data)
