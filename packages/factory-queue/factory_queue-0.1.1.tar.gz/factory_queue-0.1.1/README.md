# Factory Queue

[![PyPI version](https://badge.fury.io/py/factory-queue.svg)](https://badge.fury.io/py/factory-queue)
[![Python](https://img.shields.io/pypi/pyversions/factory-queue.svg)](https://pypi.org/project/factory-queue/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

生产者-消费者工厂模块，支持多生产者、多消费者、多队列、资源控制、磁盘溢出。

## 功能特性

- ✅ **多生产者/多消费者** - 支持并发处理，自由配置线程数
- ✅ **多队列管理** - 一个生产者可输出到多个队列
- ✅ **自动绑定** - 消费者自动绑定生产者，简化配置
- ✅ **资源控制** - 可设置内存上限、队列大小
- ✅ **磁盘溢出** - 内存不足时自动写入磁盘，防止OOM
- ✅ **优雅退出** - 完整的生产者-消费者同步机制
- ✅ **批量消费** - 支持按批次处理数据
- ✅ **实时监控** - 定时输出队列和工作者状态
- ✅ **彩色日志** - 不同级别日志使用不同颜色显示

## 安装

```bash
pip install factory-queue
```

## 快速开始

```python
from factory_queue import Factory, ResourceConfig
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 定义处理函数
def my_process(data, producer):
    """生产者处理函数"""
    result = {"consumer_a": None, "consumer_b": None}
    processed = data * 2
    
    if processed % 2 == 0:
        result["consumer_a"] = processed
    else:
        result["consumer_b"] = processed
    
    return result

def my_consume_a(data, consumer):
    """消费者A处理函数"""
    print(f"消费者A处理: {data}")

def my_consume_b(data, consumer):
    """消费者B处理函数"""
    print(f"消费者B处理: {data}")

# 创建工厂
config = ResourceConfig(
    max_memory_mb=512,
    max_queue_size=1000,
    temp_dir="./temp_queue"
)

with Factory(resource_config=config) as factory:
    # 创建输入队列
    factory.create_queue("input")
    
    # 创建生产者组
    factory.create_producer_group(
        name="main_producer",
        input_queue_name="input",
        output_consumer_names=["consumer_a", "consumer_b"],
        process_func=my_process,
        num_workers=2
    )
    
    # 创建消费者组（自动创建队列，自动绑定生产者）
    factory.create_consumer_group(
        name="consumer_a",
        consume_func=my_consume_a,
        num_workers=2,
        batch_size=5000
    )
    
    factory.create_consumer_group(
        name="consumer_b",
        consume_func=my_consume_b,
        num_workers=1
    )
    
    # 启动工厂
    factory.start()
    
    # 投放数据
    for i in range(100):
        factory.feed("input", i)
    
    # 通知生产者：没有更多数据了
    factory.end_feed(name="main_producer")
    
    # 等待完成
    factory.wait_complete()
```

## 主要类说明

### Factory

工厂主类，管理整个生产消费流程。

**主要方法：**
- `create_queue(name)` - 创建队列
- `create_producer_group(...)` - 创建生产者组
- `create_consumer_group(...)` - 创建消费者组
- `feed(queue_name, data)` - 投放数据
- `end_feed(name)` - 通知生产者结束
- `start()` - 启动工厂
- `wait_complete()` - 等待完成

### ResourceConfig

资源配置类。

**参数：**
- `max_memory_mb` - 最大内存使用量(MB)，默认1024
- `max_queue_size` - 队列最大长度，默认10000
- `disk_overflow_threshold` - 磁盘溢出阈值，默认0.8
- `temp_dir` - 临时目录，默认系统临时目录

## 高级功能

### 共享属性

```python
# 设置所有工作者共享的属性
factory.set_shared_attr("multiplier", 3)

# 在处理函数中获取
def my_process(data, producer):
    multiplier = producer.get_attr("multiplier", 1)
    return {"result": data * multiplier}
```

### 本地属性

```python
# 设置单个生产者的本地属性
producer.set_attr("name", "producer_1")

# 本地属性优先于共享属性
value = producer.get_attr("name")
```

### 批量消费

```python
factory.create_consumer_group(
    name="consumer",
    consume_func=my_consume,
    batch_size=5000,  # 每5000条批量处理
    batch_timeout=5.0  # 超时5秒也处理
)
```

## 许可证

MIT License

## 作者

stabvale

## 贡献

欢迎提交 Issue 和 Pull Request！
