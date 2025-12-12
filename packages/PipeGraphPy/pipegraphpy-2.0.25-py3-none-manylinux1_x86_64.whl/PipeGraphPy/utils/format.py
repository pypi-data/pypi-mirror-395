# coding:utf-8

import re
import json
import copy
import datetime
import io
import contextlib
import pandas as pd
from decimal import Decimal
from PipeGraphPy.constants import GRAPH_DICT_FORMAT


def replace_json(data):
    """替换json数据

    Example: >>> data = u'[{"rid": "46", "cap": "30000", \
        "nwp_config": {"GFS": "001"}, "layer": "70"}, \
            {"rid": "46", "cap": "30000", \
                "nwp_config": {"GFS": "001"}, "layer": "70"}]'
             >>> replace_json(data)

    Return: >>>
    """

    for k, v in data.items():
        try:
            row = json.loads(v)
            data[k] = row
        except Exception:
            pass

    return data


def binary_to_utf8(data):
    """
    二进制编码转成utf-8编码
    >>> binary_to_utf8(b'example')
    'example'
    >>> binary_to_utf8([b'aa', b'bb', b'cc'])
    ['aa', 'bb', 'cc']
    """
    if isinstance(data, list):
        return [binary_to_utf8(i) for i in data]
    else:
        try:
            return str(data, 'utf-8')
        except Exception:
            return data


def filter_keys(data, keys):
    """
    字典过滤keys
    """
    if isinstance(data, list):
        return [filter_keys(i, keys) for i in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k in keys}
    else:
        return data


def filter_keys_pass(data, keys):
    """
    字典过滤掉keys
    """
    if isinstance(data, list):
        return [filter_keys_pass(i, keys) for i in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in keys}
    else:
        return data


#  LOG = logging.getLogger('ATP.WebApi')
#
#  def log(func):
#      """log wrapper"""
#      def wrapper(*args, **kw):
#          try:
#              res = func(*args, **kw)
#              return res
#          except Exception as e:
#              errInfo = '(%s),详细错误:%s'%(func.__name__, e)
#              err_msg = '%s --- 错误代码 --- %s'%(errInfo, traceback.format_exc())
#              LOG.error(err_msg)
#              return json.dumps({'message':'接口异常请联系管理员', 'status':0})
#      return wrapper
#
#  def sql_filter(sql, max_length=1000):
#      dirty_stuff = ["select", "delete", "update", "insert"]
#      for stuff in dirty_stuff:
#          sql = sql.replace(stuff, "")
#      return sql[:max_length]

def pretty_data(obj):
    '''转换数据'''
    if isinstance(obj, float):
        return round(obj, 4)
    elif isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Decimal):
        return round(float(obj), 4)
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, dict):
        return dict((pretty_data(k), pretty_data(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return [pretty_data(i) for i in obj]
    return obj


def format_response(data, index_as_column=False):
    '''格式化rpc和http返回数据, DataFrame转dict'''
    if isinstance(data, pd.DataFrame):
        data = data.where(pd.notnull(data), None)
        if index_as_column:
            data = data.reset_index()
        data = data.to_dict(orient='index')
    return pretty_data(data)


def is_valid_foldername(foldername):
    # 文件夹名长度限制（根据操作系统的不同，最大长度可能会有所不同）
    if len(foldername) > 255:
        return False

    # 不能包含中文
    if re.search(r'[\u4e00-\u9fff]+', foldername):
        return False

    # 无效字符：在Windows中，文件夹名不能包含以下字符
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    if re.search(invalid_chars, foldername):
        return False

    # 不能存在空格
    if foldername.find(" ") != -1:
        return False

    # 检查是否以空格、点或其他不符合规范的字符开头或结尾
    if foldername.startswith(" ") or foldername.endswith(" ") or foldername.startswith(".") or foldername.endswith("."):
        return False

    return True


def verify_graph_dict_format(kw:dict):
    assert isinstance(kw, dict), Exception("模型只接收dict类型构建")
    value_local = ["kw"]
    def verify_one(key:str, rule:dict, v_kw:dict):
        if not rule:
            if v_kw.get(key):
                return {key:k_kw[key]}
            else:
                return None
        nonlocal value_local
        verify_kw = {}

        # 别名取值
        real_key = key
        value = None
        keys = [key, rule["alias"]] if rule.get("alias") else [key]
        for k in keys:
            if v_kw.get(k) is not None:
                real_key = k
                value = v_kw[k]

        value_local.append("['%s']" % real_key)
        local_str = "".join(value_local)
        dest_key = rule.get("dest") or real_key

        # 判断必传
        if rule.get("required"):
            if value is None:
                raise Exception("必传值%s不存在" % local_str)

        # 没有值就直接返回,不再继续验证，存在值则继续验证
        if value is None:
            if rule.get("default") is not None:
                verify_kw[dest_key] = rule["default"]
            elif rule.get("fillnone") is not None:
                verify_kw[dest_key] = v_kw.get(rule["fillnone"])
            else:
                value_local.pop()
                return None
        else:
            if rule.get("type"):
                if not isinstance(value, rule["type"]):
                    raise Exception("传值%s类型错误, 应该是%s" % (local_str, str(rule["type"])))

            if rule.get("type") == list:
                verify_kw[dest_key] = list()
                if rule["elements"].get("required"):
                    if not value:
                        raise Exception("传值%s列表不能为空" % local_str)
                for n, el in enumerate(value):
                    value_local.append("[%s]" % n)
                    local_str = "".join(value_local)
                    # 验证类型
                    if rule["elements"].get("type"):
                        if not isinstance(el, rule["elements"]["type"]):
                            raise Exception("传值%s类型错误, 应该是%s" % (
                                local_str, rule["elements"]["type"]))
                    if rule["elements"].get("type") == dict:
                        verify_el = {}
                        for k, v in rule["elements"]["elements"].items():
                            verify_res = verify_one(k,v,el)
                            if verify_res:
                                verify_el.update(verify_res)
                        verify_kw[dest_key].append(verify_el)
                    else:
                        verify_kw[dest_key].append(value)
                    value_local.pop()
            elif rule.get("type") == dict:
                verify_kw[dest_key] = dict()
                if rule.get("elements"):
                    for k, v in rule["elements"].items():
                        verify_res = verify_one(k,v,value)
                        if verify_res:
                            verify_kw[dest_key].update(verify_res)
                else:
                    verify_kw[dest_key] = value
            else:
                verify_kw[dest_key] = value

        value_local.pop()
        return verify_kw

    verify_dict = {}
    for k, v in GRAPH_DICT_FORMAT.items():
        verify_res = verify_one(k, v, kw)
        if verify_res is not None:
            verify_dict.update(verify_res)

    # # 验证模型id不能重复
    # graph_ids = [i["id"] for i in verify_dict["graphs"]]
    # if len(set(graph_ids)) < len(verify_dict["graphs"]):
    #     raise Exception("模型id存在重复")

    # 验证节点id不能重复
    # for g in verify_dict["graphs"]:
    #     node_ids = [i["id"] for i in g["nodes"]]
    #     if len(set(node_ids)) < len(g["nodes"]):
    #         raise Exception("模型%s的节点id存在重复" % g["id"])
    #     # 验证边的id都在节点id里面
    #     edge_node_ids = []
    #     edge_node_ids.extend([i["source_id"] for i in g["edges"]])
    #     edge_node_ids.extend([i["target_id"] for i in g["edges"]])
    #     outoff_node_ids = set(edge_node_ids) - set(node_ids)
    #     if outoff_node_ids:
    #         raise Exception("模型%s的edges配置的%s在nodes里未找到" % (g["id"], outoff_node_ids))

    # 验证模型id是否符合命名规范
    if not is_valid_foldername(verify_dict["id"]):
        raise Exception("模型id：(%s) 不符合命名规范" % verify_dict["id"])

    # 验证节点id不能重复
    node_ids = [i["id"] for i in verify_dict["nodes"]]
    if len(set(node_ids)) < len(verify_dict["nodes"]):
        raise Exception("模型%s的节点id存在重复" % verify_dict["id"])
    # 验证边的id都在节点id里面
    edge_node_ids = []
    edge_node_ids.extend([i["source_id"] for i in verify_dict["edges"]])
    edge_node_ids.extend([i["target_id"] for i in verify_dict["edges"]])
    outoff_node_ids = set(edge_node_ids) - set(node_ids)
    if outoff_node_ids:
        raise Exception("模型%s的edges配置的%s在nodes里未找到" % (verify_dict["id"], outoff_node_ids))

    # 验证节点id是否符合命名规范
    for i in verify_dict["nodes"]:
        if not is_valid_foldername(i["id"]):
            raise Exception("节点id: (%s) 不符合命名规范" % i["id"])

    # 验证建模对象的id不能重复
    object_ids = [i["id"] for i in verify_dict["object_infos"]]
    if len(set(object_ids)) < len(verify_dict["object_infos"]):
        raise Exception("模型对象id存在重复")

    # 验证建模对象是否符合命名规范
    for i in verify_dict["object_infos"]:
        if not is_valid_foldername(i["id"]):
            raise Exception("建模对象id: (%s) 不符合命名规范" % i["id"])

    # 验证执行器的id都在模型id内
    # actuator_graph_ids = []
    # actuator_graph_ids.extend([i["source_graph_id"] for i in verify_dict["actuator"]])
    # actuator_graph_ids.extend([i["target_graph_id"] for i in verify_dict["actuator"]])
    # outoff_graph_ids = set(actuator_graph_ids) - set(graph_ids)
    # if outoff_graph_ids:
    #     raise Exception("actuator里配置的%s在graphs里未找到" % outoff_graph_ids)

    return verify_dict


def get_help_info(obj):
    # 创建 StringIO 对象以捕获输出
    output = io.StringIO()
    try:
        # 使用 contextlib.redirect_stdout 来捕获 help() 输出
        with contextlib.redirect_stdout(output):
            help(obj)
        # 从 StringIO 获取内容
        help_info = output.getvalue()
        return help_info
    except:
        return ""
    finally:
        # 关闭 StringIO 对象
        output.close()


def now_time(is_str=False, format="%Y-%m-%d %H:%M:%S"):
    now = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=8)
    if is_str:
        return now.strftime(format)
    else:
        return now

if __name__ == '__main__':
    data = {'algo_param': u'{"C":10, "gamma":20}',
            'region': u'[{"rid": "46", "cap": "30000", "nwp_config": \
                {"GFS": "001"}, "layer": "70"}, {"rid": "46", "cap": \
                    "30000", "nwp_config": {"GFS": "001"}, "layer": "70"}]'}
    replace_json(data)


