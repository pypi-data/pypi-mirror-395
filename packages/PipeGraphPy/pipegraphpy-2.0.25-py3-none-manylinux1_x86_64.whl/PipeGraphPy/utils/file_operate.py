import pickle
import traceback
import shutil
import joblib
import os
from datetime import datetime, timedelta
from PipeGraphPy.db.models import PredictRecordTB


def joblib_dumps(file_path, data):
    """joblib文件的保存"""
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    joblib.dump(data, file_path)


def joblib_loads(file_path):
    """载入joblib模型文件"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError("模型文件不存在: %s" % file_path)
    try:
        data = joblib.load(file_path)
        return data
    except Exception as e:
        raise Exception(f"载入joblib文件失败:{file_path}, 请检查文件的正确性")


def pickle_dumps(file_path, data):
    """pickle文件的保存"""
    if os.path.isfile(file_path):
        os.remove(file_path)
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def pickle_loads(file_path):
    """载入pickle文件"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError("pickle文件不存在: %s" % file_path)
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
            return data
    except Exception as e:
        error = traceback.format_exc()
        raise Exception(f"载入pickle文件失败:{file_path}, 请检查文件的正确性\n{error}")


def get_file_path(root_path):
    """获取该目录下所有的文件名称和目录名称"""
    dir_list, file_list = [], []

    def add_path(dir):
        nonlocal dir_list
        nonlocal file_list
        for dir_file in os.listdir(dir):
            # 删除七天以前的预测记录
            del_date = ((datetime.utcnow()+timedelta(hours=8)) - timedelta(days=7)).strftime("%Y-%m-%d")
            # PredictRecordTB.rm(ctime=("<", del_date))
            # 删除之前的缓存气象目录
            dir_file_path = os.path.join(dir, dir_file)
            if os.path.isdir(dir_file_path):
                dir_list.append(dir_file_path)
                add_path(dir_file_path)
            else:
                file_list.append(dir_file_path)

    add_path(root_path)
    return dir_list, file_list


def get_file_path_walk(root_path):
    """获取该目录下所有的文件名称和目录名称"""
    dir_list, file_list = [], []
    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            dir_list.append(os.path.join(root, dir))
        for file in files:
            file_list.append(os.path.join(root, file))
    return dir_list, file_list


def delete_filepath(paths):
    """删除路径或文件列表

    Args:
        paths (list): 路径或文件列表
    """
    assert isinstance(paths, list), TypeError("paths必须是列表")
    for p in paths:
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.isfile(p):
            os.remove(p)
        else:
            pass

