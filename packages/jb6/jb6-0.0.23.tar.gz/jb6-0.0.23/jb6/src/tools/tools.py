# _*_ coding: utf-8 _/*_# 个人仓库
import asyncio
import functools
import os
import string
import time
from typing import List
import traceback
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from zhon.hanzi import punctuation
from pymongo import MongoClient


def is_docker():
    """判断当前环境是否运行在Docker容器中

    :return: True表示在Docker环境中，否则False
    """
    # 检查Docker特有文件或进程信息
    path = '/proc/self/cgroup'
    return (os.path.exists('/.dockerenv') or
            os.path.isfile(path) and any('docker' in line for line in open(path)))


def filter_punctuations(text):
    """清除文本中的标点符号（中英文）

    :param text: 需处理的原始文本
    :return: 移除所有标点后的干净文本
    """
    # 清理英文标点
    for i in string.punctuation:
        text = text.replace(i, "")
    # 清理中文标点
    for i in punctuation:
        text = text.replace(i, "")
    return text


def replace_name(value):
    """清理文件名中的非法字符（用于文件系统安全）

    :param value: 待清理的字符串
    :return: 移除非法字符后的安全字符串
    """
    # 移除文件系统禁止字符（\ / : * ? " < > | 换行 空格）
    value = value.replace('\\', '')
    value = value.replace('/', '')
    value = value.replace(':', '')
    value = value.replace('*', '')
    value = value.replace('?', '')
    value = value.replace('"', '')
    value = value.replace('<', '')
    value = value.replace('>', '')
    value = value.replace('|', '')
    value = value.replace('\n', '')
    value = value.replace(' ', '')
    return value






class AioMongoTool(object):
    """异步MongoDB工具类（基于motor）

    单例模式实现，提供MongoDB的异步操作接口
    """
    _mongo: AsyncIOMotorClient = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式实现（确保全局唯一连接）"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = args[0]
            cls._instance.db = args[1]
        return cls._instance

    def __init__(self, uri: str, db: str):
        """初始化MongoDB连接

        :param uri: MongoDB连接字符串
        :param db: 目标数据库名
        """
        self.connect(uri, db)

    def connect(self, uri: str, db: str):
        """建立MongoDB连接

        :param uri: MongoDB连接字符串
        :param db: 目标数据库名
        """
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db]

    async def close(self) -> None:
        """关闭MongoDB连接（异步）"""
        if self.client:
            await self.client.close()

    async def find_one(self, collection_name: str, filter: dict) -> dict:
        """查找单条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: 匹配的第一条文档（不含_id字段）
        """
        collection = self.db[collection_name]
        result = await collection.find_one(filter, {"_id": False})
        return result

    async def find_many(self, collection_name: str, filter: dict) -> List[dict]:
        """查找多条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: 匹配的文档列表
        """
        collection = self.db[collection_name]
        result = []
        async for doc in collection.find(filter):
            result.append(doc)
        return result

    async def insert_one(self, collection_name: str, document: dict):
        """插入单条文档（异步）

        :param collection_name: 集合名称
        :param document: 要插入的文档
        :return: True表示插入成功，False表示失败（重复键/异常）
        """
        collection = self.db[collection_name]
        try:
            result = await collection.insert_one(document)
            if result:
                return True
            else:
                return False
        except DuplicateKeyError as e:
            logger.error(f"重复键错误: {e.details}")
            logger.error(f"重复数据: {document.get('_id')}")
            return False
        except Exception as e:
            logger.error(f"插入数据时发生错误: {e}, 文档: {document}")
            return False

    async def insert_many(self, collection_name: str, document: List[dict]):
        """批量插入文档（异步）

        :param collection_name: 集合名称
        :param document: 文档列表
        :return: True表示插入成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.insert_many(document)
        if result:
            return True
        else:
            return False

    async def update_one(self, collection_name: str, filter: dict, update: dict):
        """更新单条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :param update: 更新操作（$set等）
        :return: True表示更新成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.update_one(filter, update)
        if result:
            return True
        else:
            return False

    async def update_many(self, collection_name: str, filter: dict, update: dict):
        """批量更新文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :param update: 更新操作
        :return: True表示更新成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.update_many(filter, update)
        if result:
            return True
        else:
            return False

    async def delete_one(self, collection_name: str, filter: dict):
        """删除单条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: True表示删除成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.delete_one(filter)
        if result:
            return True
        else:
            return False

    async def delete_many(self, collection_name: str, filter: dict):
        """批量删除文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: True表示删除成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.delete_many(filter)
        if result:
            return True
        else:
            return False


class MongoTool(object):
    """同步MongoDB工具类（基于pymongo）

    注意：虽然类名含"MongoTool"，但内部实现仍使用异步操作
    """
    _mongo: AsyncIOMotorClient = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = args[0]
            cls._instance.db = args[1]
        return cls._instance

    def __init__(self, uri: str, db: str):
        """初始化MongoDB连接（同步模式）"""
        self.connect(uri, db)

    def connect(self, uri: str, db: str):
        """建立MongoDB连接（同步）"""
        self.client = MongoClient(uri)
        self.db = self.client[db]

    async def close(self) -> None:
        """关闭MongoDB连接（异步）"""
        if self.client:
            await self.client.close()

    def find_one(self, collection_name: str, filter: dict) -> dict:
        """同步查找单条文档

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: 匹配的第一条文档（不含_id字段）
        """
        collection = self.db[collection_name]
        result = collection.find_one(filter, {"_id": False})
        return result

    async def find_many(self, collection_name: str, filter: dict) -> List[dict]:
        """查找多条文档（异步实现）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: 匹配的文档列表
        """
        collection = self.db[collection_name]
        result = []
        async for doc in collection.find(filter):
            result.append(doc)
        return result

    def insert_one(self, collection_name: str, document: dict):
        """同步插入单条文档

        :param collection_name: 集合名称
        :param document: 要插入的文档
        :return: True表示插入成功，False表示失败（重复键/异常）
        """
        collection = self.db[collection_name]
        try:
            result = collection.insert_one(document)
            if result:
                return True
            else:
                return False
        except DuplicateKeyError as e:
            logger.error(f"重复键错误: {e.details}")
            logger.error(f"重复数据: {document.get('_id')}")
            return False
        except Exception as e:
            logger.error(f"插入数据时发生错误: {e}, 文档: {document}")
            return False

    async def insert_many(self, collection_name: str, document: List[dict]):
        """批量插入文档（异步实现）

        :param collection_name: 集合名称
        :param document: 文档列表
        :return: True表示插入成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.insert_many(document)
        if result:
            return True
        else:
            return False

    async def update_one(self, collection_name: str, filter: dict, update: dict):
        """更新单条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :param update: 更新操作
        :return: True表示更新成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.update_one(filter, update)
        if result:
            return True
        else:
            return False

    async def update_many(self, collection_name: str, filter: dict, update: dict):
        """批量更新文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :param update: 更新操作
        :return: True表示更新成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.update_many(filter, update)
        if result:
            return True
        else:
            return False

    async def delete_one(self, collection_name: str, filter: dict):
        """删除单条文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: True表示删除成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.delete_one(filter)
        if result:
            return True
        else:
            return False

    async def delete_many(self, collection_name: str, filter: dict):
        """批量删除文档（异步）

        :param collection_name: 集合名称
        :param filter: 查询条件
        :return: True表示删除成功，False表示失败
        """
        collection = self.db[collection_name]
        result = await collection.delete_many(filter)
        if result:
            return True
        else:
            return False


class useRetry(object):
    """函数重试装饰器（支持异步函数）

    用于自动重试失败的函数调用，避免瞬时错误导致失败

    :param max_retry: 最大重试次数（默认3次）
    :param retry_interval: 重试间隔（秒，默认1秒）
    :param retry_exceptions: 需要重试的异常类型（默认Exception）
    """

    def __init__(self, max_retry=3, retry_interval=1, retry_exceptions=None):
        self.max_retry = max_retry
        self.retry_interval = retry_interval
        self.retry_exceptions = retry_exceptions or (Exception,)

    def __call__(self, func):
        """装饰器实现

        :param func: 需要重试的函数
        :return: 重试后的包装函数
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry = 0
            while retry < self.max_retry:
                try:
                    return func(*args, **kwargs)
                except self.retry_exceptions as e:
                    retry += 1
                    if retry >= self.max_retry:
                        logger.error(e)
                        traceback.print_exc()
                    else:
                        time.sleep(self.retry_interval)
            return None

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            retry = 0
            while retry < self.max_retry:
                try:
                    return await func(*args, **kwargs)
                except self.retry_exceptions as e:
                    retry += 1
                    if retry >= self.max_retry:
                        logger.error(e)
                        traceback.print_exc()
                    else:
                        await asyncio.sleep(self.retry_interval)
            return None

        # 根据函数是否为异步自动选择包装器
        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper
