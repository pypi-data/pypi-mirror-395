#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import traceback
import os
from PipeGraphPy.storage.base import ParamsPoolBase
from collections import defaultdict
from PipeGraphPy.config import settings
from PipeGraphPy.utils.file_operate import pickle_dumps, pickle_loads
from PipeGraphPy.utils.str_handle import generate_random_str
from PipeGraphPy.constants import (
        NODE_OUTPUT_KEY, MOD_RETURN_RESULT,
        ALGO_MOD_TYPE, MODULES, SCENETYPE)
from PipeGraphPy.logger import log
from PipeGraphPy.utils.format import now_time

ttl = 7


class ParamsPool(ParamsPoolBase):
    """传参池"""

    def __init__(self, graph_id, object_id, ref='dev', is_predict=False):
        self.graph_id = graph_id
        self.object_id = object_id
        self.ref = ref
        self.is_predict = is_predict

    def add_params(self, node, anchor, data):
        """添加传参值"""
        save_params(self.graph_id, self.object_id, node.id, anchor, data, self.is_predict, ref=self.ref)

    def get_params(self, node, anchor):
        """获取传参值"""
        res = get_params(
            self.graph_id, self.object_id, node.id, anchor, is_pd=True, is_predict=self.is_predict, ref=self.ref
        )
        return res

    def add_params_by_list(self, node, data_list):
        """通过数据列表添加传参"""
        for idx, data in enumerate(data_list):
            anchor = node.outidx_to_outanchor(idx)
            self.add_params(node, anchor, data)

    def is_end(self, node):
        """判断节点是否已运行完"""
        return (
            True if self.get_params(node, node.anchors[1][0].anc) is not None else False
        )

    def check_pass_params(self, fathers):
        """循环父节点判断父节点是否已结束"""
        return all([self.is_end(i) for i in fathers])

    def gen_pass_params(self, nodes_group, node, fathers):
        """生成节点要传入的参数"""
        input_output_dict = defaultdict(list)
        input_output_list = list()
        # 循环所有父节点, 组合node和anchor值
        for n in fathers:
            output_anchor, input_anchor = nodes_group[(n.id, node.id)]
            input_output_list.extend(
                zip(list(input_anchor), [(n, int(i)) for i in output_anchor])
            )

        for i, o in input_output_list:
            input_output_dict[int(i)].append(o)

        # 根据node和anchor获取节点,识别列表，把接口是列表类型的数据放入一个列表中
        input_params_list = list()
        for k, v in input_output_dict.items():
            if len(v) > 1:
                input_params_list.append((k, [self.get_params(*i) for i in v]))
            elif len(v) == 1:
                input_params_list.append((k, self.get_params(*v[0])))
            else:
                raise Exception("传参错误")
        # 参数排序
        input_params_list.sort(key=lambda x: x[0])
        arg = [i[1] for i in input_params_list]
        # 当list输入为1个元素时要转成list
        for i, item in enumerate(node.INPUT):
            if item.startswith("list") and not isinstance(arg[i], list):
                arg[i] = [arg[i]]
        return arg


def save_params(graph_id, object_id, node_id, anchor, data, is_predict=False, ref='dev'):
    """保存图模块输出结果到文件中"""
    key = NODE_OUTPUT_KEY.format(graph_id=graph_id, node_id=node_id, anchor=anchor)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id)
    pickle_dumps(os.path.join(folder_path, key), data)


def get_params(graph_id, object_id, node_id, anchor, is_pd=False, is_predict=False, ref='dev'):
    """获取图模块输出结果从文件中"""
    key = NODE_OUTPUT_KEY.format(graph_id=graph_id, node_id=node_id, anchor=anchor)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id)
    return pickle_loads(os.path.join(folder_path, key))


def delete_params(graph_id, object_id, is_predict=False, ref='dev'):
    """删除所有模块输出结果从文件中"""
    try:
        key = NODE_OUTPUT_KEY.format(graph_id=graph_id, node_id="", anchor="")
        find_key = key[:-1]
        if ref:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id, ref)
        else:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph_id, object_id)
        # 用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
        for foldName, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:  # 遍历列表下的所有文件名
                if filename.find(find_key) != -1:  # 当文件名不为
                    os.remove(os.path.join(foldName, filename))  # 删除符合条件的文件
    except Exception:
        log.error(traceback.format_exc())


def save_graph(graph, file_path=False):
    """保存图到pickle文件里"""
    if file_path:
        folder_path = os.path.dirname(file_path)
        dl_folder_path = os.path.join(
                settings.SDK_MODEL_SAVE_PATH,
                str(graph.id))
        if not os.path.exists(dl_folder_path):
            os.makedirs(dl_folder_path)
        trans_deeplearning_algo_model(graph, dl_folder_path, is_load=False)
        pickle_dumps(file_path, graph)
    else:
        model_name = settings.MODEL_SAVE_NAME.format(graph_id=graph.id, object_id=graph.object_id)
        if graph.ref:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph.id, graph.object_id, graph.ref)
        else:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, graph.id, graph.object_id)
        file_path = os.path.join(folder_path, model_name)
        trans_deeplearning_algo_model(graph, folder_path, is_load=False)
        pickle_dumps(file_path, graph)


def load_graph(graph_id=None, object_id=None, file_path=None, use_predict_model=False, ref='dev'):
    """获取图从pickle文件里"""
    if file_path:
        folder_path = os.path.dirname(file_path)
        graph = pickle_loads(file_path)
        dl_folder_path = os.path.join(settings.SDK_MODEL_SAVE_PATH, str(graph.id))
        trans_deeplearning_algo_model(graph, dl_folder_path, is_load=True)
        return graph
    else:
        assert graph_id, ValueError("转入图模型必须传graph_id")
        assert object_id, ValueError("转入图模型必须传object_id")
        model_name = settings.MODEL_SAVE_NAME.format(graph_id=graph_id, object_id=object_id)
        if ref:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
        else:
            folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
        predict_folder_path = os.path.join(settings.PREDICT_MODEL_SAVE_PATH, str(graph_id))
        predict_file_path = os.path.join(predict_folder_path, model_name)
        if use_predict_model and os.path.exists(predict_file_path):
            try:
                graph = pickle_loads(file_path)
                trans_deeplearning_algo_model(graph, predict_folder_path, is_load=True)
                return graph
            except Exception:
                pass
        file_path = os.path.join(folder_path, model_name)
        graph = pickle_loads(file_path)
        trans_deeplearning_algo_model(graph, folder_path, is_load=True)
        return graph


def has_graph(graph_id, object_id, is_predict=False, ref='dev'):
    """判断图模型是否存在"""
    model_name = settings.MODEL_SAVE_NAME.format(graph_id=graph_id, object_id=object_id)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
    model_path = os.path.join(folder_path, model_name)
    return os.path.exists(model_path)


def push_result(graph_id, object_id, data, is_predict=False, ref='dev'):
    """增加模块进行结果到文件中"""
    key = MOD_RETURN_RESULT.format(graph_id=graph_id)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
    result_folder_path = os.path.join(folder_path, key)
    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)
    now = now_time().strftime("%Y%m%d%H%M%S%f")
    filename = generate_random_str(16) + now + "0"

    def gen_no_repeat_file_path(file_path):
        if not os.path.isfile(file_path):
            return file_path
        file_path = file_path + str(int(file_path[-1]) + 1)
        return gen_no_repeat_file_path(file_path)

    file_path = os.path.join(result_folder_path, filename)
    # 找到无重复的文件名
    file_path = gen_no_repeat_file_path(file_path)
    # 执行保存
    pickle_dumps(file_path, data)


def pop_result(graph_id, object_id, is_predict=False, ref='dev'):
    """从文件中获取模块运行结果"""
    key = MOD_RETURN_RESULT.format(graph_id=graph_id)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
    result_folder_path = os.path.join(folder_path, key)
    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)
    file_path = None
    for fold_name, subfolders, filenames in os.walk(result_folder_path):
        if filenames:
            file_path = os.path.join(fold_name, filenames[0])
        else:
            return None
    # 获取数据
    res = pickle_loads(file_path)
    os.remove(file_path)
    return res


def clear_result(graph_id, object_id, is_predict=False, ref='dev'):
    """从文件中清空所有模块运行结果"""
    key = MOD_RETURN_RESULT.format(graph_id=graph_id)
    if ref:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
    else:
        folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
    result_folder_path = os.path.join(folder_path, key)
    if os.path.exists(result_folder_path):
        shutil.rmtree(result_folder_path)


def save_algo_model(graph_id, object_id, node_id, algo_mod_type, model, folder_path=None, ref='dev'):
    """保存深度学习模型图到文件里"""
    try:
        res = list()
        if not folder_path:
            if ref:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
            else:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
        if algo_mod_type == ALGO_MOD_TYPE.TENSORFLOW:
            try:
                import tensorflow as tf
            except:
                raise ImportError("载入tensorflow error")
            saver = tf.compat.v1.train.Saver()
        elif algo_mod_type == ALGO_MOD_TYPE.KERAS:
            pass
        elif algo_mod_type == ALGO_MOD_TYPE.PYTORCH:
            try:
                import torch
            except:
                raise ImportError("载入torch")
        else:
            return model
        models = model if isinstance(model, list) else [model]
        for idx, m in enumerate(models):
            if m is None or isinstance(m, (str, list, tuple, int, dict, float)):
                continue
            model_name = settings.ALGO_MODEL_SAVE_NAME.format(
                    graph_id=graph_id,
                    node_id=node_id,
                    algo_mod_type=algo_mod_type,
                    idx=idx
                    )
            if algo_mod_type == ALGO_MOD_TYPE.TENSORFLOW:
                model_name = f"{model_name}.ckpt"
                saver.save(m, os.path.join(folder_path, model_name))
            elif algo_mod_type == ALGO_MOD_TYPE.KERAS:
                model_name = f"{model_name}.h5"
                m.save(os.path.join(folder_path, model_name))
            elif algo_mod_type == ALGO_MOD_TYPE.PYTORCH:
                model_name = f"{model_name}.pt"
                torch.save(m, os.path.join(folder_path, model_name))
            else:
                raise ValueError("algo_mod_type(%s) error" % algo_mod_type)
            res.append(model_name)
        return res[0] if len(res) == 1 else res
    except Exception:
        raise Exception("无法保存深度学习模型:\n" + str(traceback.format_exc()))


def load_algo_model(graph_id, object_id, node_id, algo_mod_type, model_name, folder_path=None, ref='dev'):
    """获取深度学习模型从文件里"""
    try:
        res = list()
        if not folder_path:
            if ref:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id, ref)
            else:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph_id), object_id)
        if algo_mod_type == ALGO_MOD_TYPE.TENSORFLOW:
            try:
                import tensorflow as tf
            except:
                raise ImportError("载入tensorflow error")
            saver = tf.compat.v1.train.Saver()
        elif algo_mod_type == ALGO_MOD_TYPE.KERAS:
            try:
                from tensorflow.keras.models import load_model
            except:
                raise ImportError("载入keras.load_model error")
        elif algo_mod_type == ALGO_MOD_TYPE.PYTORCH:
            try:
                import torch
            except:
                raise ImportError("载入torch")
        else:
            return model_name
        model_names = model_name if isinstance(model_name, list) else [model_name]
        for idx, mn in enumerate(model_names):
            if algo_mod_type == ALGO_MOD_TYPE.TENSORFLOW:
                with tf.Seesion() as sess:
                    model = saver.resore(sess, os.path.join(folder_path, mn))
            elif algo_mod_type == ALGO_MOD_TYPE.KERAS:
                model = load_model(os.path.join(folder_path, mn))
            elif algo_mod_type == ALGO_MOD_TYPE.PYTORCH:
                model = torch.load(os.path.join(folder_path, mn))
            else:
                raise ValueError("algo_mod_type(%s) error" % algo_mod_type)
            res.append(model)
        return res[0] if len(res) == 1 else res
    except Exception:
        raise Exception("无法载入深度学习模型:\n" + traceback.format_exc())


def trans_deeplearning_algo_model(graph, folder_path=None, is_load=False):
    # 判断是否有深度学习算法, 深度学习算法在模型和字符串之间转换
    if not folder_path:
        if graph.scene == SCENETYPE.SDKTEST:
            folder_path = os.path.join(
                settings.SDK_MODEL_SAVE_PATH, str(graph.id), str(graph.info["object_id"]))
        elif graph.scene == SCENETYPE.ONLINE:
            if graph.ref:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph.id), graph.object_id, graph.ref)
            else:
                folder_path = os.path.join(settings.RUN_MODEL_SAVE_PATH, str(graph.id), graph.object_id)
    for k, v in graph.a.nodes_dict.items():
        if v.module.parent.info["cls_name"] == MODULES.DEEPLEARNING:
            if v.module.info.get("algo_type_id"):
                algo_mod_type_name = v.module.info.get('algo_mod_type_name')
                if algo_mod_type_name and hasattr(v.algo_instance, "model"):
                    func = None
                    if is_load:
                        if isinstance(v.algo_instance.model, str):
                            func = load_algo_model
                    else:
                        if not isinstance(v.algo_instance.model, str):
                            func = save_algo_model
                    if func is not None:
                        v.algo_instance.model = func(
                            graph.id,
                            v.info['id'],
                            algo_mod_type_name,
                            v.algo_instance.model,
                            folder_path,
                        )


