# -*- coding: utf-8 -*-
"""
Factory Queue - 生产者-消费者工厂模块
支持多生产者、多消费者、多队列、资源控制、磁盘溢出
"""

from .factory_queue import (
    # 配置类
    ResourceConfig,
    SharedConfig,
    
    # 核心类
    DiskBackedQueue,
    Producer,
    Consumer,
    ProducerGroup,
    ConsumerGroup,
    Factory,
    
    # 工具类
    ColoredFormatter,
)

__version__ = '0.1.1'
__author__ = 'Your Name'
__all__ = [
    'ResourceConfig',
    'SharedConfig',
    'DiskBackedQueue',
    'Producer',
    'Consumer',
    'ProducerGroup',
    'ConsumerGroup',
    'Factory',
    'ColoredFormatter',
]
