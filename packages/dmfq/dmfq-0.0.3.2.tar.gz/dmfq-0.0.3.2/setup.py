#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

setup(
    name='dmfq',
    version='0.0.3.2',
    author='alex',
    author_email='371401439@qq.com',
    url='https://pypi.org/project/docxt',
    description='dai ma fei qi',
    # 需要打包的目录，只有这些目录才能 from import
    packages=['dmfq', 'dmfq.utils'],
    # 安装此包时需要同时安装的依赖包
    install_requires=['numpy'],
)
