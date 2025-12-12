#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from PipeGraphPy.db.models import GraphsTB, NodesTB, EdgesTB, ModulesTB
from PipeGraphPy.constants import GRAPHTYPE
from PipeGraphPy.storage import store
from PipeGraphPy.logger import log
from PipeGraphPy.core.module import get_template_type, Module


def node_is_passed(node):
    """判断节点是否已被过滤"""
    able_node = NodesTB.find(id=node.id, is_pass=0)
    return True if not able_node else False


# def check_before_evaluate(graph_id):
#     """在生成评估图之前检查
#     parameters:
#         graph_id: int, 图id
#     return:
#         如果不成功，则返回Exception报错信息，报错信息中包含不成功原因;
#         如果成功，则返回True
#     """
#     try:
#         graph_info = GraphsTB.find_one(id=graph_id)
#         if not graph_info:
#             raise Exception("数据库不存在该模型信息")
#         if graph_info["category"] != GRAPHTYPE.TRAIN:
#             raise Exception("只有一般图模型才能生成评估模型")
#         # if not check_graph_run_success(graph_id):
#         #     raise Exception('该模型还未训练成功，不能生成评估图')
#         graph_model = store.load_graph(graph_id)
#         pg_list = [
#             graph_model.multi_pg.get(i)
#             for i in graph_model.estimator_set
#             if not node_is_passed(i)
#         ]
#         if len(pg_list) == 0:
#             raise Exception("该模型不存在可用的优化器, 不能生成评估模型")
#         if len(pg_list) > 1:
#             raise Exception("该模型存在多个可用优化器，必须有且仅有一个可用优化器才能生成评估模型")
#         return True
#     except FileNotFoundError:
#         log.error("模型文件不存在", graph_id=graph_id)
#         raise Exception("模型文件不存在")
#     except Exception as e:
#         log.error(traceback.format_exc(), graph_id=graph_id)
#         raise e


# def check_before_predict(graph_id):
#     """在执行预测之前检查模型
#     parameters:
#         graph_id: int, 图id
#     return:
#         如果不成功，则返回Exception报错信息，报错信息中包含不成功原因;
#         如果成功，则返回True
#     """
#     try:
#         graph_info = GraphsTB.find_one(id=graph_id)
#         if not graph_info:
#             raise Exception("数据库不存在该模型(%s)信息" % graph_id)
#         if graph_info.category != GRAPHTYPE.TRAIN:
#             raise Exception("%s 只有训练模型才能执行预测" % graph_id)
#         # 训练不成功的也能预测，只要存在训练模型
#         if not store.has_graph(graph_id):
#             raise Exception("%s 不存在训练好的模型" % graph_id)
#         # if not check_graph_run_success(graph_id):
#         #     raise Exception('该模型还未训练成功，不能执行预测')
#         # graph_model = store.load_graph(graph_id)
#         # pg_list = [graph_model.multi_pg.get(i) for
#         #             i in graph_model.estimator_set if not node_is_passed(i)]
#         # if len(pg_list) == 0:
#         #     raise Exception('该模型不存在可用的优化器, 不能执行预测')
#         # if len(pg_list) > 1:
#         #     raise Exception('该模型存在多个可用优化器，必须有且仅有一个可用优化器才能执行预测')
#         return True
#     except FileNotFoundError:
#         raise Exception("模型文件不存在")
#     except Exception as e:
#         raise e


def check_edge(
    graph_id,
    source_id,
    target_id,
    source_anchor=0,
    target_anchor=0,
    nodes_info_dict=None,
    is_run=False,
):
    """检查edge的合理性
    parameters:
        graph_id: int, 图id
        source_id: int, 起始节点id
        target_id：int, 结尾结点id
        source_anchor: int, 起始节点连接锚点
        target_anchor: int, 结尾节点连接锚点
        nodes_info_dict: dict, 所有节点信息, 此参数可以不传
    return:
        如果不成功，则返回Exception报错信息，报错信息中包含不成功原因;
        如果成功，则返回True
    """
    # 是否是同一个节点
    if source_id == target_id:
        raise Exception("起始节点和结尾节点不能是同一个节点")
    if not nodes_info_dict:
        # 这两个节点是否已经存在连线(运行时不需要验证这个)
        edges_info = EdgesTB.find(
            graph_id=graph_id, source_id=source_id, target_id=target_id
        )
        if len(edges_info) != 0:
            raise Exception("这两个节点间已经存在一条连线")
        nodes_info = NodesTB.find(graph_id=graph_id)
        nodes_info_dict = {i["id"]: i for i in nodes_info}
    source_data_type, target_data_type = None, None
    for idx, (node_id, anchor) in enumerate(
        [(source_id, source_anchor), (target_id, target_anchor)]
    ):
        name = "结尾" if idx else "起始"
        if anchor < 0:
            raise Exception("%s锚点值不能小于零(%s)" % (name, anchor))
        # 节点是否存在
        node_info = nodes_info_dict.get(node_id)
        if not node_info:
            raise Exception("未找到%s节点信息: %s " % (name, node_id))
        # 节点对应组件是否存在
        module_info = ModulesTB.find_one(id=node_info["mod_id"])
        if not module_info:
            raise Exception("未找到%s节点对应的组件信息: %s " % (name, node_id))
        template_type = get_template_type(node_info["mod_id"])
        # 是否存在输入配置信息
        if template_type["INPUT"] is None:
            raise Exception("没有%s节点(%s)的输入配置信息" % (name, node_id))
        if template_type["OUTPUT"] is None:
            raise Exception("没有%s节点(%s)的输出配置信息" % (name, node_id))
        # 起始节点是否是输出节点
        total_anchor = len(template_type["INPUT"]) + len(template_type["OUTPUT"])
        if anchor > total_anchor:
            raise Exception("%s节点的锚点(%s)超出了锚点范围(%s)" % (name, anchor, total_anchor))
        if idx:
            if anchor > len(template_type["INPUT"]):
                raise Exception("结尾节点的锚点(%s)必须是图输入锚点" % anchor)
            target_data_type = template_type["INPUT"][anchor]
        else:
            if anchor - len(template_type["INPUT"]) < 0:
                raise Exception("起始节点的锚点(%s)不能是输入锚点" % anchor)
            source_data_type = template_type["OUTPUT"][
                anchor - len(template_type["INPUT"])
            ]
    # 节点的起始节点的数据类型和结尾结点的数据类型是否匹配
    if target_data_type.find(source_data_type) == -1:
        raise Exception("起始节点%s和结尾节点的数据类型不匹配%s" % (source_data_type, target_data_type))
    # 检验一个节点是否能接收两个节点的数据
    if not is_run:
        if target_data_type.find("list") == -1:
            edge_info = EdgesTB.find(
                graph_id=graph_id, target_id=target_id, target_anchor=target_anchor
            )
            if edge_info:
                raise Exception("目标节点的锚点只接收一个数据")
    # 是否有环在运行的时候校验，在此处不做检验
    return True


def check_node(graph_id):
    """检查节点的合理性"""
    pass


def check_module_code(module_id):
    """检查自定义组件是否合理
    module_id: 组件id
    """
    module = Module(module_id)
    return module.check_code()

