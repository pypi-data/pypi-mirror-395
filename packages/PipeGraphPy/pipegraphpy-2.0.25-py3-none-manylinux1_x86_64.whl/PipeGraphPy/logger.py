#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import time
from logging.handlers import TimedRotatingFileHandler
from PipeGraphPy.config import settings
from PipeGraphPy.db.models import PredictRecordTB, OnlineGraphsPredictRecordTB, RunRecordTB, BacktestRecordTB, EvaluateRecordTB, OnlineGraphsEvaluateRecordTB, StopException

class RecordHandler(logging.Handler, object):
    """
    自定义日志handler
    """
    def __init__(self, name, other_attr=None, **kwargs):
        logging.Handler.__init__(self)
        self.kw = kwargs

    def emit(self, record):
        """
        emit函数为自定义handler类时必重写的函数，这里可以根据需要对日志消息做一些处理
        """
        try:
            msg = self.format(record)
            # if not settings.SDK_CLOSE_LOG:
            #     print(msg)
            if self.kw.get("plog_record_id"):
                PredictRecordTB.add_log(id=self.kw["plog_record_id"], msg=msg)
            if self.kw.get("rlog_record_id"):
                RunRecordTB.add_log(id=self.kw["rlog_record_id"], msg=msg)
            if self.kw.get("online_plog_record_id"):
                OnlineGraphsPredictRecordTB.add_log(id=self.kw["online_plog_record_id"], msg=msg)
            if self.kw.get("backtest_record_id"):
                BacktestRecordTB.add_log(id=self.kw["backtest_record_id"], msg=msg)
            if self.kw.get("evaluate_record_id"):
                EvaluateRecordTB.add_log(id=self.kw["evaluate_record_id"], msg=msg)
            if self.kw.get("online_evaluate_record_id"):
                OnlineGraphsEvaluateRecordTB.add_log(id=self.kw["online_evaluate_record_id"], msg=msg)
        except StopException as e:
            raise e
        except Exception:
            print("error!")
            print(record)


def get_pgp_logger(log_name='', logfile='', level=logging.INFO,
        backup_count=7, handlers=['console'], **kwargs):
    # 创建logger对象。传入logger名字
    logger = logging.getLogger(log_name)
    # 设置日志记录等级
    logger.setLevel(level)
    if 'file' in handlers:
        # interval 滚动周期，
        # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
        # backupCount  表示日志保存个数
        file_handler = TimedRotatingFileHandler(
            filename=logfile, when="MIDNIGHT", interval=1, backupCount=backup_count, encoding="utf-8"
        )
        # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
        file_handler.suffix = "%Y-%m-%d.log"
        # extMatch是编译好正则表达式，用于匹配日志文件名后缀
        # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # 定义日志输出格式
        file_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(process)d] [%(levelname)s] - %(message)s"
            )
        )
        logger.addHandler(file_handler)
    if 'console' in handlers:
        logger.addHandler(logging.StreamHandler())
    if 'record' in handlers:
        logger.addHandler(RecordHandler(log_name, **kwargs))
    return logger


def log_dec(level):
    def wrapper(func):
        def _(cls, *msg, **extra):
            try:
                msg = '\n'.join([str(i) for i in msg])
                if not hasattr(cls, "logger") or cls.logger is None:
                    log_name = extra.get("pgp_log_name") or "pgp_"+str(time.time()).replace('.', '')
                    cls.logger = get_pgp_logger(
                        logfile=extra.get("pgp_logfile") or "",
                        log_name=log_name,
                        level=extra.get("pgp_level") or logging.INFO,
                        backup_count=extra.get("pgp_backup_count") or 7,
                        handlers=extra.get("pgp_handlers") or ["console"],
                        **extra
                    )
                f = getattr(cls.logger, level)
                f(msg)
            except StopException as e:
                raise e
            except Exception:
                pass
        return _
    return wrapper


def get_logger(folder="run"):
    # 不需要mq消息记录日志
    return logging.getLogger(folder)


class LogBase(object):
    __function__ = None

    @classmethod
    def init(cls, pgp_handlers, **extra):
        if hasattr(cls, "logger"):
            cls.logger = None
        log_name = extra.get("pgp_log_name") or "pgp_"+str(time.time()).replace('.', '')
        cls.logger = get_pgp_logger(
            logfile=extra.get("pgp_logfile") or "",
            log_name=log_name,
            level=extra.get("pgp_level") or logging.INFO,
            backup_count=extra.get("pgp_backup_count") or 7,
            handlers=pgp_handlers,
            **extra
        )

    @classmethod
    @log_dec("info")
    def info(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("error")
    def error(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("warning")
    def warning(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("warn")
    def warn(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("debug")
    def debug(cls, msg, **extra):
        pass


class plog(LogBase):
    """预测使用的log"""

    __function__ = "predict"
    logger = None

    @classmethod
    def log(cls, level, msg, **kwargs):
        if hasattr(cls, level):
            f = getattr(cls, level)
            f(msg, **kwargs)


class rlog(LogBase):
    """运行使用的log"""

    __function__ = "run"
    logger = None


class log(LogBase):
    """一般log"""
    logger = None



if __name__ == "__main__":
    test_log = get_pgp_logger("test")
    test_log.info('test')
