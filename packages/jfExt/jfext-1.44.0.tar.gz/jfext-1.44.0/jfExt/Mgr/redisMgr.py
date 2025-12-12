# -*- coding: utf-8 -*-
"""
msab.common.redisMgr.py
v1.0
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

from redis import Redis
from flask_redis import FlaskRedis

from ..SingletonExt import Singleton


@Singleton
class RedisMgr():
    """
    >>> Redis Manager
    """

    def __init__(self):
        self._client = None

    @property
    def client(self):
        assert(self._client)    # ❗️❗️未初始化 Redis Client
        return self._client

    @client.setter
    def client(self, client):
        if isinstance(client, FlaskRedis):
            self._client = client
        elif isinstance(client, Redis):
            self._client = client

    def set_value(self, key, value, expire_time=864000):
        """
        >>> 设置key value
        :param {String} key: 键名称
        :param {String} value: 键值
        :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
        :returns {}:
        """
        if isinstance(key, str):
            self.client.set(key, value)
            self.client.expire(key, expire_time)
            return self.client.get(key)
        return None

    def get_value(self, key):
        """
        >>> 获取key value
        :param {String} key: 键名称
        :returns {String}: 键值
        """
        return self.client.get(key)

    def get_value_by_prefix(self, key_prefix):
        """
        >>> 通配符获取 Key Value
        :param {String} key_prefix: 键名 通配符
        :returns {List<String>}: list<键名key>
        """
        return self.client.keys(pattern="{}*".format(key_prefix))

    def insert_set(self, key, value, expire_time=8640000):
        """
        >>> 插入 set 值
        :param {String} key: set键名称
        :param {String} value: 键值
        :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
        :returns {Boolean}: 插入结果
        """
        if isinstance(key, str):
            self.client.sadd(key, value)
            self.client.expire(key, expire_time)
            return True
        return None

    def get_set(self, key):
        """
        >>> 获取 set 内容
        :param {String} key: set键名称
        :param {String} value: 键值
        :returns {List<String>}: set 值
        """
        return self.client.smembers(key)

    def insert_list(self, key, values, expire_time=864000):
        """
        >>> 插入队列
        :param {String} key: 键名称
        :param {String} value: 键值
        :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
        :returns {list<>}: 插入后队列内容
        """
        if isinstance(key, str):
            # 如果传入的是字符串, 转换成 list
            if isinstance(values, str):
                values = [values]
            # 如果传入的是 list, 则直接插入
            if isinstance(values, list) and values:
                self.client.lpush(key, *values)
                self.client.expire(key, expire_time)
                return self.get_list(key)
        return None

    def pop_list(self, key):
        """
        >>> 出队
        :param {String} key: set键名称
        :returns {List<String>}: set
        """
        return self.client.lpop(key)

    def get_list(self, key):
        """
        >>> 获取队列内容
        :param {String} key: set键名称
        :returns {List<String>}: set
        """
        llen = self.client.llen(key)
        return self.client.lrange(key, 0, llen)

    def incr(self, key):
        """
        >>> 自增键值
        :param {String} key: 键名称
        :returns {Int}: 自增后键值
        """
        return self.client.incr(key)

    def incr_by(self, key, amount=1):
        """
        >>> 自增键值
        :param {String} key: 键名称
        :param {Int} amount: 自增数量 (default 1)
        :returns {Int}: 自增后键值
        """
        return self.client.incrby(key, amount)

    # ---------------------------------------------------------------
    # 新增：获取 pipeline 对象
    # ---------------------------------------------------------------
    def pipeline(self, transaction=False):
        """
        >>> 获取 pipeline 对象
        :param transaction: 是否开启事务，默认关闭（更快）
        """
        return self.client.pipeline(transaction=transaction)

    # ---------------------------------------------------------------
    # 新增：批量 set key/value (使用 Pipeline)
    # ---------------------------------------------------------------
    def set_batch(self, items, expire_time=864000, batch_size=1000):
        """
        >>> 批量写入 key=value
        :param items: list[(key, value)]
        :param expire_time: 过期时间
        :param batch_size: 每多少条执行一次 pipeline
        """
        pipe = self.pipeline()
        count = 0

        for key, value in items:
            pipe.set(key, value)
            pipe.expire(key, expire_time)
            count += 1

            if count % batch_size == 0:
                pipe.execute()
                pipe = self.pipeline()

        pipe.execute()   # 收尾执行

    # ---------------------------------------------------------------
    # 新增：执行 pipeline（可选）
    # ---------------------------------------------------------------
    def exec_pipeline(self, pipe):
        """
        >>> 执行 pipeline
        """
        return pipe.execute()

    def remaining(self, key):
        """
        >>> 查询过期时间
        :param {String} key: 键名称
        :param {Int}: 过期时间
        """
        return self.client.ttl(key)

    def rm_key(self, key):
        """
        >>> 删除键
        :param {String} key: 键名称
        :returns {Boolean}: 插入结果
        """
        return self.client.delete(key)

    def rm_keys(self, key_prefix):
        """
        >>> 删除一组键值对
        :param {String} key_prefix: 键名称 prefix
        :returns {Boolean}: 插入结果
        """
        keys = self.client.keys("{}*".format(key_prefix))
        for key in keys:
            self.client.delete(key)

    def flush_db(self):
        """
        >>> 清空应用 cache
        """
        cache_keys = self.keys("msab.cache*")
        for i in cache_keys:
            self.client.delete(i)
