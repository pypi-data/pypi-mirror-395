#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pandas as pd
from collections import defaultdict
from PipeGraphPy.core.node import Node
from PipeGraphPy.db.models import NodesTB, EdgesTB
from PipeGraphPy.core.module import get_template_type

# from prettytable import PrettyTable


def get_start_and_end(nodes_group_dict):
    """找到所有开始节点和结束节点
    parameters:
        nodes_group_dict: dict 节点关系列表(直接从数据库取出的列表)
    return
        开始节点集和结束节点集
    """
    from_set, to_set = set(), set()
    for source_id, target_id in nodes_group_dict.keys():
        from_set.add(source_id)
        to_set.add(target_id)
    return from_set - to_set, to_set - from_set


def group_by_source_node(nodes_group_dict):
    """统计每个节点下子节点
    parameters:
        edges_dict: dict 节点关系列表

    """
    # 统计每个节点下的所有子节点
    source_nodes_group = defaultdict(list)
    for source_id, target_id in nodes_group_dict.keys():
        source_nodes_group[source_id].append(target_id)
    return source_nodes_group


def is_cycle2(edges, nodes):
    """判断是否有环：单个节点在一个单向线路中只能出现一回
    parameters:
        edges: list 边列表
        nodes: list 节点列表
    return
        Boolen
    """
    nodes_dict = {i["id"]: i for i in nodes}
    nodes_group_dict = gen_nodes_group_dict2(edges, nodes_dict)

    # 找出开始节点
    start_set, end_set = get_start_and_end(nodes_group_dict)
    if not start_set or not end_set:
        return True
    # 统计每个节点下的所有子节点
    source_nodes_group = group_by_source_node(nodes_group_dict)
    # 循环查看单向线路中节点是否重复出现
    res = False
    node_set = set()

    def _loop(node):
        nonlocal res, node_set, source_nodes_group
        if node in node_set:
            res = True
            return
        node_set.add(node)
        for i in source_nodes_group[node]:
            _loop(i)
            if res:
                return
            node_set.remove(i)

    # 以开始节点作业起点判断
    for head in start_set:
        if res:
            break
        _loop(head)

    return res


def is_cycle(graph_id, edges_info=None, nodes_info=None):
    """判断是否有环：单个节点在一个单向线路中只能出现一回
    parameters:
        graph_id: int 图id
        edges_info: list 边列表
        nodes_info: list 节点列表
    return
        Boolen
    """
    if not edges_info:
        edges_info = EdgesTB.find(graph_id=graph_id)
    if not nodes_info:
        nodes_info = NodesTB.find(graph_id=graph_id)
    if not edges_info or not nodes_info:
        return False
    nodes_info_dict = {i["id"]: i for i in nodes_info}
    nodes_group_dict = gen_nodes_group_dict(edges_info, nodes_info_dict)

    # 找出开始节点
    start_set, end_set = get_start_and_end(nodes_group_dict)
    if not start_set or not end_set:
        return True
    # 统计每个节点下的所有子节点
    source_nodes_group = group_by_source_node(nodes_group_dict)
    # 循环查看单向线路中节点是否重复出现
    res = False
    node_set = set()

    def _loop(node):
        nonlocal res, node_set, source_nodes_group
        if node in node_set:
            res = True
            return
        node_set.add(node)
        for i in source_nodes_group[node]:
            _loop(i)
            if res:
                return
            node_set.remove(i)

    # 以开始节点作业起点判断
    for head in start_set:
        if res:
            break
        _loop(head)

    return res


def _add_node_loop(head, relation_dict, all_node, node_dict, graph_info):
    """递归添加节点"""
    if not relation_dict[head.id]:
        return
    for i in relation_dict[head.id]:
        child_element = Node(i, info=node_dict[i], graph_info=graph_info)
        # 如果已添加过，使用之前的对像
        if all_node.get(child_element) is not None:
            child_element = all_node[child_element]
        else:
            all_node[child_element] = child_element
        if head not in child_element.fathers:
            child_element.add_one_father(head)
        if child_element not in head.children:
            head.add_one_child(child_element)
        _add_node_loop(child_element, relation_dict, all_node, node_dict, graph_info)


def gen_node_heads(nodes_group_dict, nodes_info_dict, graph_info):
    """生成节点并返回头节点
    parameters:
        edges_dict: dict 节点边列表
    return:
        头节点列表
    """
    # 找出开始节点
    start_set, _ = get_start_and_end(nodes_group_dict)

    # 统计每个节点下的所有子节点
    source_nodes_group = group_by_source_node(nodes_group_dict)

    head_list = [
        Node(i, info=nodes_info_dict[i], graph_info=graph_info) for i in start_set
    ]
    head_list_copy = head_list
    # 以头节点为开始节点循环添加子节点
    all_node = dict()
    for head in head_list:
        _add_node_loop(head, source_nodes_group, all_node, nodes_info_dict, graph_info)
    return head_list_copy


def load_obj(source_str):
    tmp_path = source_str.split(".")
    op_str = tmp_path.pop()
    import_str = ".".join(tmp_path)
    try:
        exec("from {} import {}".format(import_str, op_str))
        op_obj = eval(op_str)
    except Exception as e:
        raise Exception(e)

    return op_obj


def outanchor_to_outidx(node_info, outanchor):
    """输出的锚点转成输出的索引"""
    input_data_type = get_template_type(node_info["mod_id"], "INPUT")
    return outanchor - len(input_data_type)


def outanchor_to_outidx2(node, outanchor):
    """输出的锚点转成输出的索引"""
    return node.outanchor_to_outidx(outanchor)


def outidx_to_outanchor(node_info, outidx):
    """输出的索引转成输出的锚点"""
    input_data_type = get_template_type(node_info["mod_id"], "INPUT")
    return outidx + len(input_data_type)


def gen_nodes_group_dict(edges_info, nodes_info_dict):
    """组合节点传参
    return:
        {(source_id, target_id): pass_idx}
    """
    out_idx = defaultdict(list)
    in_idx = defaultdict(list)
    for edge_info in edges_info:
        # source_id找到对应结点类型
        out_idx[(edge_info["source_id"], edge_info["target_id"])].append(
            str(
                outanchor_to_outidx(
                    nodes_info_dict[edge_info["source_id"]], edge_info["source_anchor"]
                )
            )
        )
        in_idx[(edge_info["source_id"], edge_info["target_id"])].append(
            str(edge_info["target_anchor"])
        )
    nodes_group_dict = {
        k: ",".join(v) + "-" + ",".join(in_idx[k]) for k, v in out_idx.items()
    }
    return nodes_group_dict


def gen_nodes_group_dict2(edges, nodes_dict):
    """组合节点传参
    return:
        {(source_id, target_id): pass_idx}
    """
    out_idx = defaultdict(list)
    in_idx = defaultdict(list)
    for edge in edges:
        # source_id找到对应结点类型
        out_idx[(edge.info["source_id"], edge.info["target_id"])].append(
            str(
                nodes_dict[edge.info["source_id"]].outanchor_to_outidx(
                    edge.info["source_anchor"]
                )
            )
        )
        in_idx[(edge.info["source_id"], edge.info["target_id"])].append(
            str(edge.info["target_anchor"])
        )
    nodes_group_dict = {
        k: ",".join(v) + "-" + ",".join(in_idx[k]) for k, v in out_idx.items()
    }
    return nodes_group_dict


def cal_score_by_groupby(
    df,
    scorer,
    unit="day",
    y_ture_col="power",
    y_pred_col="power_predict",
    cap=None,
):
    """通过groupby计算日月年的单位评分

    Args:
        df (DataFrame): 要计算的数据
        scorer (func): 要使用的评价函数
        unit (str, optional): 评价单位. Defaults to "day".
        y_ture_col (str, optional): 要使用的真值列. Defaults to "r_apower".
        y_pred_col (str, optional): 要使用的预测值列. Defaults to "r_apower_predict".
        cap (num, optional): 场站发电容量. Defaults to None.

    Returns:
        [type]: 单位和评分值
    """
    res = list()
    dfc = df.copy()
    if isinstance(dfc.index[0], str):
        dfc.index = dfc.index.map(pd.to_datetime)
    if unit == "day":
        dfc[unit] = pd.to_datetime(dfc.index.strftime("%Y-%m-%d"))
    elif unit == "month":
        dfc[unit] = pd.to_datetime(dfc.index.strftime("%Y-%m"))
    elif unit == "year":
        dfc[unit] = pd.to_datetime(dfc.index.strftime("%Y-%m"))
    else:
        raise ValueError("unit值错误%s" % unit)
    for i in dfc.groupby(dfc[unit]):
        if cap:
            try:
                score = round(float(scorer(i[1][y_ture_col], i[1][y_pred_col], cap,)), 3,)
            except:
                score = round(float(scorer(i[1][y_ture_col], i[1][y_pred_col])), 3)
        else:
            score = round(float(scorer(i[1][y_ture_col], i[1][y_pred_col])), 3)
        res.append([i[0], score])
    return res
