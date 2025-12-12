# coding: utf8
from PipeGraphPy.config import settings

class ENUMSBASE:
    @classmethod
    def values(cls):
        if hasattr(cls, "_values"):
            return getattr(cls, "_values")
        _values = [
            getattr(cls, i) for i in list(cls.__dict__.keys()) if str(i).isupper()
        ]
        setattr(cls, "_values", _values)
        return _values

    @classmethod
    def keys(cls):
        if hasattr(cls, "_keys"):
            return getattr(cls, "_keys")
        _keys = [i for i in list(cls.__dict__.keys()) if str(i).isupper()]
        setattr(cls, "_keys", _keys)
        return _keys


class DB:
    dbPipeGraphPy = settings.DBPOOL_SERVER_NAME

    @classmethod
    def tolist(cls):
        return [cls.dbPipeGraphPy]


# 场站类型：

class GRAPH_VAR(object):
    graph_predict_type = 1 # 1:预测，2:评估，3:回测，4:回算

class GRAPH_PREDICT_TYPE():
    PREDICT = 1
    EVALUATE = 2
    BACKTEST = 3
    CAL = 4


class GRAPH_EXE_TYPE():
    RUN = 'run'
    PREDICT = 'predict'
    EVALUATE = 'evaluate'
    BACKTEST = 'backtest'
    CAL = 'cal'


class FARMTYPE(object):
    WIND = "W"
    PV = "S"


class MTYPE(object):
    NON_CUSTOM       = 0  # 非自定义类
    CUSTOM           = 1  # 自定义类
    INNER_NON_CUSTOM = 10 # 内部不可自定义组件
    INNER_CUSTOM     = 11 # 内部可自定义组件
    OUTER            = 20 # 外部组件


# 模块类型
class MODULES(object):
    IMPORT        = "ImportData"
    EXPORT        = "ExportData"
    PREPROCESSOR  = "Preprocessor"
    SELECTOR      = "Selector"
    TRANSFORMER   = "Transformer"
    REGRESSOR     = "Regressor"
    CLASSIFIER    = "Classifier"
    DEEPLEARNING  = "DeepLearning"
    DATACHART     = "DataCharts"
    POSTPROCESSOR = "Postprocessor"
    SPECIAL       = "Special"
    ENSEMBLE      = "Ensemble"
    METRICS       = "Metrics"
    EVALUATE      = "Evaluate"
    MERGE         = "Merge"
    SPLIT         = "Split"
    THEORYDATA    = "TheoryData"
    BRANCHSELECT  = "BranchSelect"
    GRAPH_MOD     = "GraphMod"
    PYTHONSCRIPT  = "PythonScript"
    CLUSTER       = "Cluster"
    STARTSCRIPT   = "StartScript"
    HANDLESCRIPT  = "HandleScript"
    SPLITSCRIPT   = "SplitScript"
    MERGESCRIPT   = "MergeScript"
    SELECTSCRIPT  = "SelectScript"
    ENDSCRIPT     = "EndScript"

MODULES_ID = {
    MODULES.IMPORT        : 1,
    MODULES.EXPORT        : 2,
    MODULES.PREPROCESSOR  : 3,
    MODULES.SELECTOR      : 4,
    MODULES.TRANSFORMER   : 5,
    MODULES.REGRESSOR     : 6,
    MODULES.CLASSIFIER    : 7,
    MODULES.CLUSTER       : 8,
    MODULES.POSTPROCESSOR : 9,
    MODULES.DATACHART     : 10,
    MODULES.ENSEMBLE      : 11,
    MODULES.DEEPLEARNING  : 12,
    MODULES.SPECIAL       : 13,
    MODULES.METRICS       : 14,
    MODULES.MERGE         : 15,
    MODULES.SPLIT         : 16,
    MODULES.EVALUATE      : 17,
    MODULES.BRANCHSELECT  : 18,
    MODULES.PYTHONSCRIPT  : 19,
    MODULES.STARTSCRIPT   : 20,
    MODULES.HANDLESCRIPT  : 21,
    MODULES.SPLITSCRIPT   : 22,
    MODULES.MERGESCRIPT   : 23,
    MODULES.SELECTSCRIPT  : 24,
    MODULES.ENDSCRIPT     : 25,
}


ESTIMATOR_MODULES = [MODULES.CLASSIFIER, MODULES.REGRESSOR, MODULES.DEEPLEARNING]
TRANSFORMER_MODULES = [MODULES.PREPROCESSOR, MODULES.SELECTOR, MODULES.TRANSFORMER]
RUN_CUSTOM_MODULES = [MODULES.IMPORT, MODULES.ENSEMBLE,
        MODULES.MERGE, MODULES.SPLIT, MODULES.BRANCHSELECT, MODULES.EXPORT]
RUN_MODULES = [MODULES.EVALUATE, MODULES.PYTHONSCRIPT, MODULES.STARTSCRIPT, MODULES.HANDLESCRIPT,
        MODULES.SPLITSCRIPT, MODULES.MERGESCRIPT, MODULES.SELECTSCRIPT, MODULES.ENDSCRIPT]

# 自定义模块
CUSTOM_MODULES = [
    MODULES.IMPORT,
    MODULES.PREPROCESSOR,
    MODULES.SELECTOR,
    MODULES.TRANSFORMER,
    MODULES.REGRESSOR,
    MODULES.CLASSIFIER,
    MODULES.DEEPLEARNING,
    MODULES.POSTPROCESSOR,
    MODULES.ENSEMBLE,
    MODULES.METRICS,
    MODULES.EVALUATE,
    MODULES.BRANCHSELECT,
]
CUSTOM_MODULES.extend(ESTIMATOR_MODULES)
CUSTOM_MODULES.extend(TRANSFORMER_MODULES)
CUSTOM_MODULES.extend(RUN_CUSTOM_MODULES)
CUSTOM_MODULES.extend(RUN_MODULES)

# 图模型
GRAPH_MOD = "GraphMod"
MODEL_SELECTOR = "ModelSelector"


# 节点状态
class STATUS(object):
    NONE    = 0  # 无状态
    RUNNING = 1  # 正在运行
    SUCCESS = 2  # 运行成功
    WARNING = 3  # 运行告警
    ERROR   = 4  # 错误
    WAITRUN = 5  # 未发送任务等待运行
    WAITEXE = 6  # 已发送任务等待运行


# 模型状态
class MODELSTATUS(object):
    NONE          = 0  # 无模型
    NORMAL        = 1  # 模型正常
    LOAD_ERROR    = 11 # 模型载入报错
    PREDICT_ERROR = 12 # 模型预测过程报错
    ERROR         = 4  # 错误


# 图类型
class GRAPHTYPE(object):
    TRAIN              = 1   # 训练图
    EVALUATE           = 2   # 评估图
    SCHEDULE           = 3   # 调度任务
    WIND_EVAL_TEMPLATE = 100 # 风电场评估图模板
    PV_EVAL_TEMPLATE   = 101 # 光伏电场评估图模板
    WIND_TEMPLATE      = 110 # 风电场训练图模板
    PV_TEMPLATE        = 111 # 光伏电场训练图模板


# 组件输入输出类型
class DATATYPE(ENUMSBASE):
    LIST           = "list"
    DICT           = "dict"
    FLOAT          = "float"
    FLOAT_LIST     = "list(float)"
    INT            = "int"
    INT_LIST       = "list(int)"
    STR            = "str"
    STR_LIST       = "list(str)"
    NUMBER         = "number"
    NUMBER_LIST    = "list(number)"
    DATAFRAME      = "DataFrame"
    DATAFRAME_LIST = "list(DataFrame)"
    OBJECT         = "object"
    OBJECT_LIST    = "list(object)"


NODE_STATUS_KEY      = "node_status_{graph_id}_{node_id}"
NODE_OUTPUT_KEY      = "node_output_{graph_id}_{node_id}_{anchor}"
GRAPH_STATUS_KEY     = "graph_status_{graph_id}"
GRAPH_KEY            = "graph_{graph_id}"
MOD_RETURN_RESULT    = "mod_result_{graph_id}"
PREDICT_RABBITMQ_KEY = "PipeGraphPy_predict"
RABBITMQ_EXCHANGE    = "PipeGraphPy-2"

EVALUATE_RECORD_RESERVE_NUM = 10

UID_NUM = 10


class BIZ_TYPE(ENUMSBASE):
    WFID = "wfid"
    WEATHER = "weather"
    CUSTOM = "custom"
    MLT = "mlt"
    ALERT = "alert"
    MLT_MONTH = "mlt_month"
    MLT_HOUR = "mlt_hour"
    MONTH_CURVE = "month_curve"
    PRICE_PREDICT = "price_predict"
    LOAD_PREDICT = "load_predict"


# class JUPYTER_TYPE(ENUMSBASE):
#     LAB = NotebookType.JUPYTER_LAB
#     NOTEBOOK = NotebookType.JUPYTER_NOTEBOOK


# 算法所使用的外部库
class ALGO_MOD_TYPE(ENUMSBASE):
    SKLEARN    = "sklearn"
    XGBOOST    = "xgboost"
    TENSORFLOW = "tensorflow"
    KERAS      = "keras"
    PYTORCH    = "torch"


# graph使用场景
class SCENETYPE(ENUMSBASE):
    SDKTEST = "sdk_test" # sdk测试场景,不使用sql
    SDKSQL  = "sdk_sql"  # sdk线下运行,使用sql
    ONLINE  = "online"   # 线上运行

class ONLINE_ENV(ENUMSBASE):
    AWS = 'aws'
    LOCAL = 'local'

NODE_DATA_RESERVE = 20
NOT_CUT_MODULES = []


GRAPH_DICT_FORMAT = {
    "id": {
        "required": True,
        "type": str,
        "dest": "",
        "help": "必传,不能包含中文",
    },
    "name": {
        "required": False,
        "type": str,
        "dest": "",
        "help": "非必传,不传参时,使用id的值",
        "fillnone": "id",
    },
    "version": {
        "required": False,
        "default": "v0.0.1",
        "type": str,
        "dest": "",
        "help": "非必传, 版本号",
    },
    "author": {
        "required": False,
        "default": "",
        "type": str,
        "dest": "username",
        "help": "非必传,作者",
    },
    "update_time": {
        "required": False,
        "type": str,
        "dest": "utime",
        "help": "非必传,更新时间",
    },
    "params": {
        "required": False,
        "default": {},
        "type": dict,
        "dest": "run_params",
        "help": "非必传，模型全局传参",
    },
    "nodes":{
        "required": True,
        "type": list,
        "dest": "",
        "help": "模型节点列表",
        "elements": {
            "required": True,
            "type": dict,
            "elements": {
                "id": {
                    "required": True,
                    "type": str,
                    "dest": "",
                    "help": "必传,不能包含中文",
                },
                "name": {
                    "required": False,
                    "type": str,
                    "dest": "",
                    "help": "非必传,不传参时,使用id的值",
                    "fillnone": "id",
                },
                "version": {
                    "required": False,
                    "type": str,
                    "help": "版本号",
                },
                "update_time": {
                    "required": False,
                    "type": str,
                    "help": "代码更新时间, 格式：%Y-%m-%d %H:%M:%S",
                },
                "classification": {
                    "required": False,
                    "type": str,
                    "help": "classification和module_classification必传其中一个,多级时用‘/’分割",
                },
                "cls_name": {
                    "required": False,
                    "type": str,
                    "help": "cls_name和module_cls_name必传其中一个,节点入口类的类名, 文件名为类名的小写",
                },
                "module_classification": {
                    "required": False,
                    "type": str,
                    # "dest": "parent_cls_name",
                    "help": "classification和module_classification必传其中一个,多级时用‘/’分割",
                },
                "module_cls_name": {
                    "required": False,
                    "type": str,
                    # "dest": "cls_name",
                    "help": "cls_name和module_cls_name必传其中一个,节点入口类的类名, 文件名为类名的小写",
                },
                "params": {
                    "required": False,
                    "default": {},
                    "type": dict,
                    "help": "必传,节点传参",
                }
            }
        }
    },
    "edges":{
        "required": False,
        "default": [],
        "type": list,
        "dest": "",
        "help": "模型连线列表",
        "elements": {
            "required": True,
            "type": dict,
            "elements": {
                "source": {
                    "required": True,
                    "type": str,
                    "dest": "source_id",
                    "alias": "source_id",
                    "help": "必传,起始节点id, 必须在nodes能找到对应id",
                },
                "target": {
                    "required": True,
                    "type": str,
                    "dest": "target_id",
                    "alias": "target_id",
                    "help": "必传,目标节点id, 必须在nodes能找到对应id",
                },
                "source_anchor": {
                    "required": False,
                    "default": 1,
                    "type": int,
                    "help": "必传,起始节点锚点,默认是1",
                },
                "target_anchor": {
                    "required": False,
                    "default": 1,
                    "type": int,
                    "help": "必传,目标节点锚点,默认是1",
                }
            }
        }
    },
    "objects":{
        "required": True,
        "dest": "object_infos",
        "type": list,
        "help": "模型对象信息",
        "elements": {
            "required": True,
            "type": dict,
            "elements": {
                "id": {
                    "required": True,
                    "type": str,
                    "dest": "",
                    "help": "必传,不能包含中文",
                },
                "name": {
                    "required": False,
                    "type": str,
                    "dest": "",
                    "help": "非必传,不传参时,使用id的值",
                    "fillnone": "id",
                }
            }
        }
    }
}


EXECUTOR_DICT_FORMAT = {
    "executor":{
        "required": False,  # 没有执行器的时候模型安顺序执行
        "default": [],
        "type": list,
        "help": "执行器,标识模型执行顺序",
        "elements": {
            "required": True,
            "type": dict,
            "elements": {
                "source": {
                    "required": True,
                    "type": str,
                    "dest": "source_graph_id",
                    "alias": "source_id",
                    "help": "必传,起始模型id",
                },
                "target": {
                    "required": True,
                    "type": str,
                    "dest": "target_graph_id",
                    "alias": "target_id",
                    "help": "必传,目标模型id",
                }
            }
        }
    }
}
