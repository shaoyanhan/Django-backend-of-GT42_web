from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("getHaplotypeTable/", views.getHaplotypeTable, name="getHaplotypeTable"),
    path("getSNPTable/", views.getSNPTable, name="getSNPTable"),
    path("getTranscriptTable/", views.getTranscriptTable, name="getTranscriptTable"),
    path("getMosaicTPMTable/", views.getMosaicTPMTable, name="getMosaicTPMTable"),
    path("getXenologousTPMTable/", views.getXenologousTPMTable, name="getXenologousTPMTable"),
    path("getGeneTPMTable/", views.getGeneTPMTable, name="getGeneTPMTable"),
    path("getTranscriptTPMTable/", views.getTranscriptTPMTable, name="getTranscriptTPMTable"),

    path("getHaplotypeTableByPage/", views.getHaplotypeTableByPage, name="getHaplotypeTableByPage"),
    path("getSNPTableByPage/", views.getSNPTableByPage, name="getSNPTableByPage"),
    path("getTranscriptTableByPage/", views.getTranscriptTableByPage, name="getTranscriptTableByPage"),
    path("getMosaicTPMTableByPage/", views.getMosaicTPMTableByPage, name="getMosaicTPMTableByPage"),
    path("getXenologousTPMTableByPage/", views.getXenologousTPMTableByPage, name="getXenologousTPMTableByPage"),
    path("getGeneTPMTableByPage/", views.getGeneTPMTableByPage, name="getGeneTPMTableByPage"),
    path("getTranscriptTPMTableByPage/", views.getTranscriptTPMTableByPage, name="getTranscriptTPMTableByPage"),

    path("validateGenomeID/", views.validateGenomeID, name="validateGenomeID"),
    path("getGenomeIDList/", views.getGenomeIDList, name="getGenomeIDList"),
    path("getGT42NextID/", views.getGT42NextID, name="getGT42NextID"),

    path('getNetworkGraphJSONFile/', views.getNetworkGraphJSONFile, name='getNetworkGraphJSONFile'),

    path('getNetworkGraphJSON/', views.getNetworkGraphJSON, name='getNetworkGraphJSON'),

    path('getMosaicNetworkNodesTableByPage/', views.getMosaicNetworkNodesTableByPage, name='getMosaicNetworkNodesTableByPage'),
    path('getMosaicNetworkEdgesTableByPage/', views.getMosaicNetworkEdgesTableByPage, name='getMosaicNetworkEdgesTableByPage'),
    path('getXenologousNetworkNodesTableByPage/', views.getXenologousNetworkNodesTableByPage, name='getXenologousNetworkNodesTableByPage'),
    path('getXenologousNetworkEdgesTableByPage/', views.getXenologousNetworkEdgesTableByPage, name='getXenologousNetworkEdgesTableByPage'),
    path('getGeneNetworkNodesTableByPage/', views.getGeneNetworkNodesTableByPage, name='getGeneNetworkNodesTableByPage'),
    path('getGeneNetworkEdgesTableByPage/', views.getGeneNetworkEdgesTableByPage, name='getGeneNetworkEdgesTableByPage'),

    path('getHomologousIDSet/', views.getHomologousIDSet, name='getHomologousIDSet'),

]