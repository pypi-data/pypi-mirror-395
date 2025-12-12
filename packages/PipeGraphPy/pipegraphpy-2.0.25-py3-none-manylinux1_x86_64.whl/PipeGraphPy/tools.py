#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import signal
import copy
import time
import json
import pandas as pd
from contextlib import  contextmanager
from PipeGraphPy.db.models import GraphsTB, PredictRecordTB, BacktestRecordTB, ObjectGraphsTB
from PipeGraphPy.config import settings
from PipeGraphPy.db.utils import update_node_params
from PipeGraphPy.constants import MODULES, STATUS
from PipeGraphPy.common import multi_graph
from PipeGraphPy.logger import log
from PipeGraphPy.utils.file_operate import pickle_loads
from PipeGraphPy.utils.format import now_time


def print_to_run_log(*args, graph_id=None, rlog_record_id=None):
    '''将内容输出到run_log里，前端来展示
    params:
        args: 要打印的内容
        graph_id: 运行图id
        rlog_record_id: 运行记录id
    '''
    assert graph_id, 'graph_id必传'
    msg = '\n'.join([str(i) for i in args])
    # if not settings.SDK_CLOSE_LOG:
    #     print(msg)
    if isinstance(graph_id, int):
        GraphsTB.add_log(graph_id, msg)
    if rlog_record_id:
        log.info(msg)

def print_to_predict_log(*args, plog_record_id=None):
    '''将内容输出到预测日志里，前端来展示
    params:
        args: 要打印的内容
        plog_record_id: 预测记录id
    '''
    assert plog_record_id, 'plog_record_id必传'
    PredictRecordTB.add_log(plog_record_id, '\n'.join([str(i) for i in args]))

def update_params_value(key, value, node):
    """更新当前节点参数"""
    node.params[key] = value
    graph = multi_graph.get(node.graph_info["id"])
    if graph.use_db:
        update_node_params(node.id, key, value)
    return 1

def update_params_source(key, value, node):
    """更新当前节点参数source"""
    graph = multi_graph.get(node.graph_info["id"])
    if graph.use_db:
        update_node_params(node.id, key, value, value_key="source")
    return 1


def predict_to_csv(datas, filename="",
        graph_id='', object_id='', node_id='',
        plog_record_id='', online_plog_record_id="",
        filepath=""):
    # 取出节点的数据导入节点
    assert isinstance(datas, pd.DataFrame), "预测保存的数据必须是DataFrame"
    assert graph_id, "未传graph_id"
    assert object_id, "未传object_id"
    assert node_id, "未传node_id"
    if filepath:
        if not filepath.endswith(".csv"):
            raise Exception("预测数据只能保存csv文件")
        datas.to_csv(filepath, encoding="utf_8", index=False)
    else:
        if not plog_record_id and not online_plog_record_id:
            return 0
        predict_save_path = os.path.join(
                settings.PREDICT_RESULT_SAVE_PATH,
                str(graph_id),
                str(object_id))
        if not os.path.exists(predict_save_path):
            os.makedirs(predict_save_path)
        if filename:
            predict_filename = filename
        else:
            if online_plog_record_id:
                auto_file_name_prefix = "online_predict_%s" % online_plog_record_id
            else:
                auto_file_name_prefix = "predict_%s" % plog_record_id
            predict_filename = "%s_%s_%s_%s_%s.csv" % (
                    auto_file_name_prefix,
                    str(graph_id),
                    str(object_id),
                    str(node_id),
                    now_time(is_str=True, format="%Y%m%d%H%M%S"))
        datas.to_csv(os.path.join(predict_save_path, predict_filename), encoding="utf_8", index=False)
    return 1


def read_predict_csv(graph_id, object_id,  start_date=None, end_date=None):
    """读取模型历史的预测数据
    args:
        graph_id：预测模型的id
        object_id, 建模对象id,
        start_date: 预测数据批次的开始日期 (包含), 不传的话只返回最近的一次数据, 格式：YYYYmmdd or YYYY-mm-dd
        end_date: 预测数据批次的结束日期（包含）, 不传的话只返回最近的一次数据, 格式：YYYYmmdd or YYYY-mm-dd
    """
    datas = pd.DataFrame()
    predict_save_path = os.path.join(settings.PREDICT_RESULT_SAVE_PATH, str(graph_id), str(object_id))
    if not os.path.exists(predict_save_path):
        return datas
    file_list = os.listdir(predict_save_path)
    file_time_dict = {(i.split("_")[-1]).replace(".csv", ""):i for i in file_list}
    time_list = list(file_time_dict.keys())
    if settings.RUN_ENV != "image":
        if start_date and end_date:
            start_date = str(start_date).replace('-', "")
            end_date = str(end_date).replace('-', "")
            daterange = pd.date_range(start_date, end_date, freq="D").to_list()
            for d in daterange:
                match_times = [i for i in time_list if i.startswith(d.strftime("%Y%m%d"))]
                match_time = None
                if len(match_times) > 1:
                    match_time = str(max(list(map(int, match_times))))
                elif len(match_times) == 1:
                    match_time = match_times[0]
                else:
                    continue
                df = pd.read_csv(os.path.join(predict_save_path, file_time_dict[match_time]))
                df["file_date"] = match_time[:8]
                datas = datas.append(df)
            return datas
        else:
            match_time = str(max(list(map(int, time_list))))
            datas = pd.read_csv(os.path.join(predict_save_path, file_time_dict[match_time]))
            datas["file_date"] = match_time[:8]
            return datas
    else:
        # 请求NPMOS的接口
        pass


def train_to_csv(datas, graph_id='', node_id=''):
    # 取出节点的数据导入节点
    assert isinstance(datas, pd.DataFrame), "预测保存的数据必须是DataFrame"
    assert graph_id, "未传graph_id"
    assert node_id, "未传node_id"
    run_save_path = os.path.join(
            settings.RUN_RESULT_SAVE_PATH,
            str(graph_id))
    if not os.path.exists(run_save_path):
        os.makedirs(run_save_path)
    run_filename = "run_%s.csv" % str(node_id)
    datas.to_csv(os.path.join(run_save_path, run_filename), encoding="utf_8", index=False)
    return 1


def read_train_csv(graph_id, node_id):
    """读取模型历史的预测数据
    args:
        graph_id：预测模型的id
        node_id: 节点
    """
    run_save_path = os.path.join(settings.RUN_RESULT_SAVE_PATH, str(graph_id))
    file_list = os.listdir(run_save_path)
    datas = pd.DataFrame()
    if node_id:
        file_list = [f for f in file_list if int(str(str(f).split("-")[-1]).replace(".csv", "")) == int(node_id)]
    for f in file_list:
        df = pd.read_csv(os.path.join(run_save_path, f))
        df["node_id"] = str(str(f).split("-")[-1]).replace(".csv", "")
        datas = datas.append(df)
    return datas


def read_backtest_data(graph_id, object_id, start_date=None, end_date=None, record_id=None):
    """读取回测数据结果
    args:
        graph_id：回测模型的id, 必传
        object_id: 回测建模对象id，必传
        start_date: 回测的开始日期 (包含), 不传的话读取最近的一次批次或指定record_id的回测, 格式：YYYY-mm-dd
        end_date: 回测的结束日期 (包含), 不传的话读取最近的一次批次或指定record_id的回测, 格式：YYYY-mm-dd
        record_id: 回测记录的记录id, start_date, end_date, record_id都不传的情况会读取最近一次回测结果
    example:
        >>> first_backtest = read_backtest_data(1371, '2023-07-01', '2023-07-26')
        >>> first_backtest
                             power  power_predict
        time
        2023-07-01 00:45:00    0.0            0.0
        2023-07-01 01:00:00    0.0            0.0
        2023-07-01 01:15:00    0.0            0.0
        2023-07-01 01:30:00    0.0            0.0
        2023-07-01 01:45:00    0.0            0.0
        ...                    ...            ...
        2023-07-26 22:45:00    0.0            0.0
        2023-07-26 23:00:00    0.0            0.0
        2023-07-26 23:15:00    0.0            0.0
        2023-07-26 23:30:00    0.0            0.0
        2023-07-26 23:45:00    0.0            0.0

        [2492 rows x 2 columns]
        >>> second_backtest = read_backtest_data(1371, '2023-06-01', '2023-07-26')
        >>> second_backtest
                             power  power_predict
        time
        2023-06-01 00:45:00    0.0            0.0
        2023-06-01 01:00:00    0.0            0.0
        2023-06-01 01:15:00    0.0            0.0
        2023-06-01 01:30:00    0.0            0.0
        2023-06-01 01:45:00    0.0            0.0
        ...                    ...            ...
        2023-07-26 22:45:00    0.0            0.0
        2023-07-26 23:00:00    0.0            0.0
        2023-07-26 23:15:00    0.0            0.0
        2023-07-26 23:30:00    0.0            0.0
        2023-07-26 23:45:00    0.0            0.0

        [5372 rows x 2 columns]
        >>> backtest_by_record_id = read_backtest_data(1371, record_id=302)
        >>> backtest_by_record_id
                             power  power_predict
        time
        2023-07-01 00:45:00    0.0            0.0
        2023-07-01 01:00:00    0.0            0.0
        2023-07-01 01:15:00    0.0            0.0
        2023-07-01 01:30:00    0.0            0.0
        2023-07-01 01:45:00    0.0            0.0
        ...                    ...            ...
        2023-07-26 22:45:00    0.0            0.0
        2023-07-26 23:00:00    0.0            0.0
        2023-07-26 23:15:00    0.0            0.0
        2023-07-26 23:30:00    0.0            0.0
        2023-07-26 23:45:00    0.0            0.0

        [2492 rows x 2 columns]
        >>> last_backtest_data = read_backtest_data(1371)
        >>> last_backtest_data
                             power  power_predict
        time
        2023-06-01 00:45:00    0.0            0.0
        2023-06-01 01:00:00    0.0            0.0
        2023-06-01 01:15:00    0.0            0.0
        2023-06-01 01:30:00    0.0            0.0
        2023-06-01 01:45:00    0.0            0.0
        ...                    ...            ...
        2023-07-26 22:45:00    0.0            0.0
        2023-07-26 23:00:00    0.0            0.0
        2023-07-26 23:15:00    0.0            0.0
        2023-07-26 23:30:00    0.0            0.0
        2023-07-26 23:45:00    0.0            0.0

        [5372 rows x 2 columns]
    """
    datas = pd.DataFrame()
    if start_date and end_date:
        graph_info = GraphsTB.get(id=graph_id)
        if graph_info["status"] != STATUS.SUCCESS:
            raise Exception("该模型%s还未训练成功" % graph_id)
        if graph_info["b_status"] in [STATUS.WAITRUN, STATUS.WAITEXE]:
            raise Exception("模型%s正在等待回测，无法再次回测" % graph_id)
        if graph_info["b_status"] in [STATUS.RUNNING]:
            raise Exception("模型%s正在回测，无法再次回测" % graph_id)
        ObjectGraphsTB.set(
            b_status=STATUS.WAITRUN,
            backtest_params=json.dumps({"start_dt": start_date, "end_dt":end_date})
            ).where(graph_id=graph_id, object_id=object_id)
        while True:
            time.sleep(5)
            b_status = ObjectGraphsTB.map_one("b_status").where(graph_id=graph_id, object_id=object_id)
            if b_status == STATUS.ERROR:
                backtest_record_id = ObjectGraphsTB.map_one("backtest_record_id").where(graph_id=graph_id, object_id=object_id)
                if backtest_record_id:
                    record_log = BacktestRecordTB.map_one("log").where(id=backtest_record_id)
                    raise Exception("模型%s回测报错，回测日志：\n%s" % (graph_id, record_log))
                raise Exception("模型%s回测报错" % graph_id)
            elif b_status == STATUS.SUCCESS:
                break
            else:
                continue
    if record_id:
        backtest_record_id = record_id
    else:
        backtest_record_id = ObjectGraphsTB.map_one("backtest_record_id").where(graph_id=graph_id, object_id=object_id)
        if not backtest_record_id:
            raise Exception("模型%s没有获取到回测记录" % graph_id)
    backtest_save_path = os.path.join(settings.BACKTEST_RESULT_SAVE_PATH, str(graph_id))
    backtest_save_file = os.path.join(backtest_save_path, "backtest_%s.pkl" % backtest_record_id)
    if not os.path.isfile(backtest_save_file):
        raise Exception("模型%s没有回测记录%s的回测数据" % (graph_id, record_id))
    datas = pickle_loads(backtest_save_file)
    label_columns = datas.get("label_columns")
    if label_columns:
        y_true_column = label_columns[0] if isinstance(label_columns, list) else label_columns
        y_pred_column = y_true_column + "_predict"
        if y_true_column not in datas["data"].columns:
            raise Exception("模型%s回测数据里未找到真实值%s" % (graph_id, y_true_column))
        if y_pred_column not in datas["data"].columns:
            raise Exception("模型%s回测数据里未找到预测值%s" % (graph_id, y_pred_column))
    else:
        y_pred_columns = [i for i in datas["data"].columns if str(i).endswith("_predict")]
        if len(y_pred_columns) > 1:
            raise Exception("回测结果有多个_predict列")
        if len(y_pred_columns) == 0:
            raise Exception("回测结果中未找到_predict列")
        y_pred_column = y_pred_columns[0]
        y_true_column = str(y_pred_column).replace("_predict", "")
    return datas["data"][[y_true_column,y_pred_column]]


def get_model_save_path(graph_id, object_id, node_id):
    """获取模型的自定义模型的保存路径
    args:
        graph_id：预测模型的id
        object_id: 建模对象id
        node_id: 节点id
    """
    if settings.RUN_ENV == 'sdk':
        model_save_path = settings.SDK_MODEL_SAVE_PATH
        nodes_model_save_path = os.path.join(model_save_path, str(graph_id), str(object_id), str(node_id))
    else:
        model_save_path = settings.RUN_MODEL_SAVE_PATH
        nodes_model_save_path = os.path.join(model_save_path, str(graph_id), str(object_id), 'nodes', node_id)
    return nodes_model_save_path


def update_nwp_config(nwp_config, node):
    # 取出节点的数据导入节点
    import_nodes = []
    graph = multi_graph.get(node.graph_info["id"])
    if graph is None:
        raise Exception("全局未找到graph")

    for n in graph.a._iter_fathers(node):
        if n.module.parent.info["cls_name"] == MODULES.IMPORT and n not in import_nodes:
            import_nodes.append(n)
    if len(import_nodes) > 1:
        raise Exception("导入数据节点有多个，只能更新一个导入数据节点的nwp_config")
    if len(import_nodes) == 0:
        raise Exception("未找到Algodata或StrategyAlgodata数据导入节点")
    import_node = import_nodes[0]
    if import_node.params.get("nwp_config") is None:
        raise Exception("数据导入节点%s没有nwp_config参数" % import_node.info["cls_name"])

    # 验证nwp_config的格式是否正确
    if not isinstance(nwp_config, dict):
        raise Exception("nwp_config格式不正确")
    if not nwp_config:
        raise Exception("nwp_config传值为空")
    # 更新节点里面的参数
    import_node.params["nwp_config"] = nwp_config
    if graph.use_db:
        # 更新数据库里面的参数
        update_node_params(import_node.id, "nwp_config", str(nwp_config))
    print_to_run_log("更新nwp_config为:%s" % str(nwp_config), graph_id=node.graph_info["id"])
    return 1

def get_nwp_config(node):
    # 取出节点的数据导入节点
    import_nodes = []
    graph = multi_graph.get(node.graph_info["id"])
    if graph is None:
        raise Exception("全局未找到graph")

    for n in graph.a._iter_fathers(node):
        if n.module.parent.info["cls_name"] == MODULES.IMPORT and n not in import_nodes:
            import_nodes.append(n)
    if len(import_nodes) == 0:
        raise Exception("未找到Algodata或StrategyAlgodata数据导入节点")
    nwp_configs = []
    for n in import_nodes:
        if n.params.get("nwp_config") is not None:
            nwp_configs.append(n.params["nwp_config"])

    if len(nwp_configs) > 1:
        raise Exception("数据导入节点存在多个nwp_config")

    if len(nwp_configs) == 0:
        raise Exception("数据导入节点不存在nwp_config参数")

    return nwp_configs[0]


@contextmanager
def timeout(duration):
    def timeout_handler(signum, frame):
        raise TimeoutError(f'block timedout after {duration} seconds')
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(duration)
    yield
    signal.alarm(0)
