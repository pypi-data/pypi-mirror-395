#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from PipeGraphPy.utils.str_handle import filter_fields
from PipeGraphPy.utils.handle_graph import stop_running_with_exception


class Base(object):
    pass


class MBase(object):
    params_rules = {}

    def __init__(self, **kwargs):
        self.params = kwargs

    def stop_run(self, err):
        """停止运行"""
        stop_running_with_exception(self.params.graph_info["id"], err=err)

    def get_X_y(self, df):
        """获取X和y值从df中"""
        if self.params.get("feature_columns"):
            X = df[filter_fields(df.columns, self.params.get("feature_columns"))]
        else:
            X = df
        # 取出要传递的y值
        if self.params.get("label_columns"):
            y = df[filter_fields(df.columns, self.params.get("label_columns"))]
        else:
            y = None
        return X, y

    def check_params(self):
        params = self.params
        if self.params_rules:
            for k, v in self.params_rules.items():
                if v.get("need") and params.get(k) is None:
                    raise Exception("(%s)值必传" % v["name"])
                if (
                    v.get("type")
                    and params.get(k)
                    and not isinstance(params[k], v["type"])
                ):
                    raise Exception("(%s)值类型错误, 必须为(%s)型" % (v["name"], str(v["type"])))
                if (
                    v.get("range")
                    and params.get(k)
                    and not params[k] >= v["range"][0]
                    and not params[k] <= v["range"][1]
                ):
                    raise Exception(
                        "(%s)取值范围错误, 必须在(%s)之间" % (v["name"], str(v["range"]))
                    )
                if v.get("source") and params.get(k):
                    v_lst = params[k] if isinstance(params[k], list) else [params[k]]
                    for i in v_lst:
                        if i not in v["source"]:
                            raise Exception(
                                "(%s)取值错误，必须在(%s)之间选值" % (v["name"], str(v["source"]))
                            )


