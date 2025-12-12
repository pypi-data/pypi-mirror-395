# coding: utf8

# import time
# import uuid
# import redis
# import pickle
# import traceback
# import math
#
# from PipeGraphPy.config import settings
# from PipeGraphPy.logger import log
# from contextlib import contextmanager
# from PipeGraphPy.exceptions import LockAcquireTimeout
#
#
# redis_conf = dict(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
# )
# redis_key_ttl = settings.REDIS_KEY_TTL
#
# redis_client = redis.Redis(
#     host=redis_conf["host"], port=redis_conf["port"], db=redis_conf["db"]
# )
#
#
# def pickle_dumps(key, data):
#     """pickle文件保存到redis"""
#     try:
#         bytes_str = pickle.dumps(data)
#         res = redis_client.set(name=key, value=bytes_str, ex=settings.REDIS_KEY_TTL)
#         if not res:
#             raise Exception("保存数据到redis发生错误")
#         return 1
#     except Exception:
#         log.error(traceback.format_exc())
#         raise Exception("保存pickle数据到redis失败")
#
#
# def pickle_loads(key):
#     try:
#         res = redis_client.get(name=key)
#         if not res:
#             raise Exception("redis未找到对应的数据")
#         res = pickle.loads(res)
#         return res
#     except Exception:
#         log.error(traceback.format_exc())
#         raise Exception("从redis获取pickle数据失败")
#
#
# class Lock(object):
#     def __init__(self, lock_name, acquire_timeout=60, lock_timeout=30):
#         self._lock_name = lock_name
#         self._acquire_timeout = acquire_timeout
#         self._lock_timeout = lock_timeout
#
#     def get_lock_value(self):
#         return redis_client.get(self._lock_name)
#
#     def acquire_lock(self):
#         identifier = str(uuid.uuid4())
#         lock_timeout = int(math.ceil(self._lock_timeout))
#
#         end = time.time() + self._acquire_timeout
#
#         while time.time() < end:
#             # 如果不存在这个锁则加锁并设置过期时间，避免死锁
#             if redis_client.setnx(self._lock_name, identifier):
#                 redis_client.expire(self._lock_name, lock_timeout)
#                 return identifier
#             # 如果存在锁，且这个锁没有过期时间则为其设置过期时间，避免死锁
#             elif redis_client.ttl(self._lock_name) == -1:
#                 redis_client.expire(self._lock_name, lock_timeout)
#
#             time.sleep(0.01)
#         return False
#
#     def release_lock(self, identifier):
#         """
#         释放锁
#
#         :param identifier: 锁的标识
#         :return:
#         """
#         lock_value = self.get_lock_value()
#         if not lock_value:
#             raise Exception("不存在此锁")
#         if lock_value.decode("utf-8") != identifier:
#             raise Exception("锁的标识不匹配")
#         res = redis_client.delete(self._lock_name)
#         if res:
#             return True
#         return False
#
#
# @contextmanager
# def redis_lock(lock_name, acquire_timeout=60, lock_timeout=30):
#     try:
#         identifier = None
#         lock = Lock(lock_name, acquire_timeout, lock_timeout)
#         identifier = lock.acquire_lock()
#         if identifier:
#             yield identifier
#         else:
#             raise LockAcquireTimeout(f"{lock_name},分布式锁获取超时")
#     except Exception as e:
#         raise e
#     finally:
#         if identifier is not None and Lock(lock_name).get_lock_value:
#             try:
#                 lock.release_lock(lock_name, str(identifier))
#             except Exception:
#                 pass
#
#
# def acquire_lock_with_timeout(lock_name, acquire_timeout=60, lock_timeout=30):
#     """
#     基于 Redis 实现的分布式锁
#
#     :param lock_name: 锁的名称
#     :param acquire_timeout: 获取锁的超时时间，默认 3 秒,
#                             设置准则, 同一时间线程数 x 单个任务执行时长
#                             也就是同一时间最后一个获取锁的时间
#     :param lock_timeout: 锁的超时时间，默认 2 秒,
#                          设置准则：大于单个任务执行的最大时长
#     :return:
#     """
#
#     identifier = str(uuid.uuid4())
#     lock_name = f"lock:{lock_name}"
#     lock_timeout = int(math.ceil(lock_timeout))
#
#     end = time.time() + acquire_timeout
#
#     while time.time() < end:
#         # 如果不存在这个锁则加锁并设置过期时间，避免死锁
#         if redis_client.setnx(lock_name, identifier):
#             redis_client.expire(lock_name, lock_timeout)
#             return identifier
#         # 如果存在锁，且这个锁没有过期时间则为其设置过期时间，避免死锁
#         elif redis_client.ttl(lock_name) == -1:
#             redis_client.expire(lock_name, lock_timeout)
#
#         time.sleep(0.001)
#
#     return False
#
#
# def release_lock(lock_name, identifier):
#     """
#     释放锁
#
#     :param lock_name: 锁的名称
#     :param identifier: 锁的标识
#     :return:
#     """
#     # python 中 redis 事务是通过pipeline的封装实现的
#     with redis_client.pipeline() as pipe:
#         lock_name = f"lock:{lock_name}"
#
#         while True:
#             try:
#                 # watch 锁, multi 后如果该 key 被其他客户端改变, 事务操作会抛出 WatchError 异常
#                 pipe.watch(lock_name)
#                 iden = pipe.get(lock_name)
#                 if iden and iden.decode("utf-8") == identifier:
#                     # 事务开始
#                     pipe.multi()
#                     pipe.delete(lock_name)
#                     pipe.execute()
#                     return True
#
#                 pipe.unwatch()
#                 break
#             except redis.WatchError as e:
#                 raise e
#         return False
#
#
# @contextmanager
# def get_lock(lock_name, acquire_timeout=60, lock_timeout=30):
#     try:
#         identifier = None
#         identifier = acquire_lock_with_timeout(lock_name, acquire_timeout, lock_timeout)
#         if identifier:
#             yield identifier
#         else:
#             raise LockAcquireTimeout(f"{lock_name},分布式锁获取超时")
#     except Exception as e:
#         raise e
#     finally:
#         if identifier is not None:
#             release_lock(lock_name, str(identifier))
