#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import json
import pandas as pd
from rabbitmqpy import Puber
from datetime import datetime, timedelta
from PipeGraphPy.logger import log
from PipeGraphPy.config import settings
from PipeGraphPy.db.models import MqTB
from PipeGraphPy.utils.format import pretty_data, now_time



def publish_predict_output_mq(graph_id, predict_output_data, include_index=True, **kwargs):
    # global puber
    puber = None
    exchange = settings.PREDICT_OUTPUT_EXCHANGE
    routing_key = settings.PREDICT_OUTPUT_ROUTING_KEY
    try:
        try:
            puber = Puber(
                settings.AMQP_URL,
                exchange,
                'direct',
                routing_key=routing_key
            )
        except:
            puber = None
        if puber is not None:
            if isinstance(predict_output_data, pd.DataFrame):
                if include_index:
                    output_data = pretty_data(predict_output_data.reset_index().to_dict(orient="records"))
                else:
                    output_data = pretty_data(predict_output_data.to_dict(orient="records"))
            elif isinstance(predict_output_data, dict):
                output_data = pretty_data(predict_output_data)
            else:
                output_data = pretty_data(predict_output_data)
            ext_info = kwargs
            send_data = {
                "graph_id": graph_id,
                "ext_info": ext_info,
                "data": output_data
            }
            puber.send(send_data)
            log_info = '发送MQ：exchange=%s,routing_key=%s,body=%s' % (
                exchange, routing_key, str(send_data)[:100]
            )
            if ext_info.get("use_db"):
                MqTB.add(
                    pubdate=int(now_time(is_str=True, format="%Y%m%d")),
                    graph_id=graph_id,
                    exchange=exchange,
                    queue="",
                    route_key=routing_key,
                    clock=kwargs.get("clock", "12"),
                    ext_info=str(ext_info),
                    kind = 1
                )
            log.info(log_info)
    except Exception:
        log.error(traceback.format_exc())
