#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import signal
from PipeGraphPy.logger import log
from PipeGraphPy.common import multi_graph


def stop_running_with_exception(graph_id, err):
    """停止运行"""
    graph = multi_graph[graph_id]
    graph.stop_run(err)


class HandleGraph(object):
    def __init__(self, id):
        self.id = id
        self.graph = multi_graph[self.id]

    def __getattr__(self, name):
        return getattr(self.graph, name)


def kill_pid(pid):
    """强制kill某个pid"""
    try:
        a = os.kill(pid, signal.SIGKILL)
        # a = os.kill(pid, signal.9) #　与上等效
        log.info("已杀死pid为%s的进程,　返回值是:%s" % (pid, a))
    except Exception:
        log.error("没有如此进程!!!")
