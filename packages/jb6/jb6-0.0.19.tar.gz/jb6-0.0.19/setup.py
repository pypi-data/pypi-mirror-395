# _*_ coding: utf-8 _*_
# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="jb6",  # 这里是pip项目发布的名称
    version="0.0.19",  # 版本号，数值大的会优先被pip
    keywords=["pip", "SongUtils"],  # 关键字
    description="jb6自用",  # 描述
    long_description="jb6自用",
    license="MIT Licence",  # 许可证
    author="jb6",  # 作者
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["zhon", "motor", "typing", "loguru", "pymongo", "curl_cffi", "json_repair"],  # 这个项目依赖的第三方库
    python_requires='>=3.8',
)
