#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import redis
# import pickle
# import traceback
# from PipeGraphPy.storage.base import ParamsPoolBase
# from PipeGraphPy.utils.format import binary_to_utf8
# from collections import defaultdict
# from PipeGraphPy.config import settings
# from PipeGraphPy.utils.redis_operate import pickle_dumps, pickle_loads
# from PipeGraphPy.constants import (NODE_STATUS_KEY, NODE_OUTPUT_KEY,
#                             GRAPH_STATUS_KEY, GRAPH_KEY, MOD_RETURN_RESULT)
#
# from PipeGraphPy.logger import log
# redis_conf = dict(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
# )
# redis_key_ttl = settings.REDIS_KEY_TTL
#
#
# redis_conn = redis.Redis(
#     host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])
#
#
# class ParamsPool(ParamsPoolBase):
#     '''传参池'''
#
#     def __init__(self, graph_id, is_predict=False):
#         self.graph_id = graph_id
#         self.is_predict = is_predict
#
#     def add_params(self, node, idx, data):
#         '''添加传参值'''
#         save_params(self.graph_id, node.id, idx, data, self.is_predict)
#
#     def get_params(self, node, idx):
#         '''获取传参值'''
#         res = get_params(self.graph_id, node.id, idx,
#                          is_pd=True, is_predict=self.is_predict)
#         return res
#
#     def add_params_by_list(self, node, data_list):
#         '''通过数据列表添加传参'''
#         for idx, data in enumerate(data_list):
#             self.add_params(node, idx, data)
#
#     def is_end(self, node):
#         '''判断节点是否已运行完'''
#         return True if self.get_params(node, 0) is not None else False
#
#     def check_pass_params(self, node):
#         '''循环父节点判断父节点是否已结束'''
#         return all([self.is_end(i) for i in node.fathers])
#
#     def gen_pass_params(self, edges_dict, node):
#         '''生成节点要传入的参数'''
#         input_output_dict = defaultdict(list)
#         input_output_list = list()
#         # 循环所有父节点, 组合node和idx值
#         for n in node.fathers:
#             pass_idx = edges_dict[(n.id, node.id)]
#             out_idx_str, input_idx_str = pass_idx.split('-')
#             input_output_list.extend(zip(input_idx_str.split(
#                 ','), [(n, int(i)) for i in out_idx_str.split(',')]))
#
#         for i, o in input_output_list:
#             input_output_dict[int(i)].append(o)
#
#         # 根据node和idx获取节点,识别列表，把接口是列表类型的数据放入一个列表中
#         input_params_list = list()
#         for k, v in input_output_dict.items():
#             if len(v) > 1:
#                 input_params_list.append((k, [self.get_params(*i) for i in v]))
#             elif len(v) == 1:
#                 input_params_list.append((k, self.get_params(*v[0])))
#             else:
#                 raise Exception('传参错误')
#         # 参数排序
#         input_params_list.sort(key=lambda x: x[0])
#         arg = [i[1] for i in input_params_list]
#         # 当list输入为1个元素时要转成list
#         for i, item in enumerate(node.input_data_type):
#             if item.startswith('list') and not isinstance(arg[i], list):
#                 arg[i] = [arg[i]]
#         return arg
#
#
# def save_node_status(node, is_predict=False):
#     '''保存节点到redis'''
#     key = NODE_STATUS_KEY.format(graph_id=node.info['graph_id'],
#                                  node_id=node.id)
#     redis_conn.hmset(key, node.to_dict())
#
#
# def get_node_status(graph_id, node_id, is_predict=False):
#     '''获取节点状态到从redis'''
#     fields = ['val', 'is_pass', 'status', 'run_log']
#     key = NODE_STATUS_KEY.format(graph_id=graph_id, node_id=node_id)
#     res = redis_conn.hmget(key, fields)
#     return dict(zip(fields, binary_to_utf8(res)))
#
#
# def save_graph_status(graph_id, is_predict=False):
#     '''保存图的状态到redis'''
#     key = GRAPH_STATUS_KEY.format(graph_id=graph_id)
#     redis_conn.hmset(key, graph_id)
#
#
# def get_graph_status(graph_id, is_predict=False):
#     '''获取图状态到从redis'''
#     fields = ['pid', 'status', 'run_log']
#     key = GRAPH_STATUS_KEY.format(graph_id=graph_id)
#     res = redis_conn.hmget(key, fields)
#     return dict(zip(fields, binary_to_utf8(res)))
#
#
# def save_params(graph_id, node_id, idx, data, is_predict=False):
#     '''保存图模块输出结果到redis'''
#     key = NODE_OUTPUT_KEY.format(graph_id=graph_id,
#                                  node_id=node_id,
#                                  idx=idx)
#     pickle_dumps(redis_conn, key, data)
#
#
# def get_params(graph_id, node_id, idx, is_pd=False, is_predict=False):
#     '''获取图模块输出结果从redis'''
#     key = NODE_OUTPUT_KEY.format(graph_id=graph_id,
#                                  node_id=node_id,
#                                  idx=idx)
#     return pickle_loads(redis_conn, key)
#
#
# def delete_params(graph_id, is_predict=False):
#     '''删除所有模块输出结果从redis'''
#     try:
#         pattern_key = 'graph_output_%s_*' % graph_id
#         key_list = redis_conn.keys(pattern=pattern_key)
#         if key_list:
#             res = redis_conn.delete(*key_list)
#             return res
#         return 1
#     except Exception:
#         log.error(
#             traceback.format_exc(),
#             graph_id=graph_id)
#
#
# def save_graph(graph_id, data, is_predict=False):
#     '''保存图到redis'''
#     key = GRAPH_KEY.format(graph_id=graph_id)
#     pickle_dumps(redis_conn, key, data)
#
#
# def get_graph(graph_id, is_predict=False):
#     '''获取图从redis'''
#     key = GRAPH_KEY.format(graph_id=graph_id)
#     return pickle_loads(redis_conn, key)
#
#
# def push_result(graph_id, data, is_predict=False):
#     '''增加模块进行结果到redis'''
#     key = MOD_RETURN_RESULT.format(graph_id=graph_id)
#     pd_bytes = pickle.dumps(data)
#     res = redis_conn.lpush(key, pd_bytes)
#     if not res:
#         raise Exception('保存数据到redis发生错误')
#     return res
#
#
# def pop_result(graph_id, is_predict=False):
#     '''从redis获取模块运行结果'''
#     try:
#         key = MOD_RETURN_RESULT.format(graph_id=graph_id)
#         res = redis_conn.rpop(name=key)
#         if not res:
#             return None
#         res = pickle.loads(res)
#         return res
#     except Exception:
#         log.error(traceback.format_exc(), graph_id=graph_id)
