import random
import string
import json
import uuid
import time


def generate_random_str(length):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    return "".join(
        [random.choice(string.digits + string.ascii_letters) for i in range(length)]
    )


def uid(x=None):
    return uuid.uuid4().hex[:x] if x else uuid.uuid4().hex


def tid(x=15, rand=0):
    """返回时间戳和随机整数的拼接数字符串

    Args:
        x (int, optional): 时间戳的后几位. Defaults to 14.
        rand (int, optional): 随机数的位数. Defaults to 2.
    Example:
        >>> tid()
        '52585086'
        >>> tid(7,2)
        '393869947'
        >>> tid(7,3)
        '2783550195'
        >>> tid(0,3)
        '694'
        >>> tid(4,3)
        '7283087'
    """
    rand_time = (
        str(time.time()).replace(".", "").ljust(17, "0")[0 - x :] if x > 0 else ""
    )
    randint_str = (
        str(random.randint(0, 10 ** rand - 1)).rjust(rand, "0") if rand > 0 else ""
    )
    tid = f"{rand_time}{randint_str}"
    return tid


def deep_json_loads(data):
    """深度使用json.loads"""
    try:
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = deep_json_loads(v)
            return data
        elif isinstance(data, list):
            return [deep_json_loads(i) for i in data]
        elif isinstance(data, str):
            if (data.startswith("[{") and data.endswith("}]")) or (
                data.startswith("{") and data.endswith("}")
            ):
                if data.find('"') == -1:
                    data = data.replace("'", '"')
                return deep_json_loads(json.loads(data))
            elif data.startswith("[") and data.endswith("]"):
                return deep_json_loads(eval(data))
            else:
                return data
        elif isinstance(data, int) or isinstance(data, float):
            return data
        elif data is None:
            return data
        else:
            raise ValueError("数据格式不正确, deep_json_loads失败")
    except Exception as e:
        raise e


def filter_fields(org_fields, filter_pattern):
    """通过filter_pattern过滤
    paramaters:
        org_fields: list 原始字段名
        filter_pattern: list or str:
            支持*号语法
    """
    if filter_pattern == "__all__":
        return org_fields

    def is_right(field, pattern):
        pattern = "<<head>>%s<<tail>>" % str(pattern)
        field = "<<head>>%s<<tail>>" % str(field)
        if pattern.find("*") == -1:
            return True if field == pattern else False
        else:
            ps = [i for i in pattern.split("*") if str(i).strip()]
            last_index = 0
            for p in ps:
                index = str(field).find(p)
                if index == -1:
                    return False
                if index < last_index:
                    return False
                last_index = index
            return True

    all_fields = list()

    def _filter(fields, pattern):
        nonlocal all_fields
        if isinstance(pattern, list):
            return [_filter(fields, i) for i in pattern]
        if isinstance(pattern, str):
            all_fields.extend(list(filter(lambda x: is_right(x, pattern), org_fields)))

    _filter(org_fields, filter_pattern)

    all_fields = list(set(all_fields))
    all_fields.sort()

    return all_fields
