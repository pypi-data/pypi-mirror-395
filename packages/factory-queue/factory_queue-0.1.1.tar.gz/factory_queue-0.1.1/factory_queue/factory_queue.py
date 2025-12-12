# -*- coding: utf-8 -*-
"""
生产者-消费者工厂模块
支持多生产者、多消费者、多队列、资源控制、磁盘溢出
"""
import json
import logging
import pickle
import tempfile
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from queue import Queue, Empty, Full
from typing import Any, Dict, List, Optional, Callable

import psutil


# 定义颜色代码
class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',  # 青色
        'INFO': '\033[0m',  # 亮白色
        'WARNING': '\033[93m',  # 亮黄色
        'ERROR': '\033[91m',  # 亮红色
        'CRITICAL': '\033[95m',  # 亮紫色
        'RESET': '\033[0m'  # 重置
    }

    def format(self, record):
        # 保存原始的levelname和msg
        levelname_orig = record.levelname
        msg_orig = record.msg

        # 获取日志级别对应的颜色
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])

        # 只给日志级别添加颜色
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"

        # 格式化消息（包含时间戳等）
        formatted = super().format(record)

        # 恢复原始值
        record.levelname = levelname_orig
        record.msg = msg_orig

        # 给消息部分添加颜色（消息在最后，从' - '之后开始）
        parts = formatted.rsplit(' - ', 1)
        if len(parts) == 2:
            return f"{parts[0]} - {color}{parts[1]}{self.COLORS['RESET']}"
        return formatted


logger = logging.getLogger(__name__)


@dataclass
class ResourceConfig:
    """资源配置"""
    max_memory_mb: int = 1024  # 最大内存使用量(MB)，超过此限制才使用磁盘
    max_queue_size: int = 10000  # 队列最大长度，满了则阻塞等待
    temp_dir: Optional[str] = None  # 磁盘溢出时的临时目录
    check_interval: float = 1.0  # 资源检查间隔(秒)

    def __post_init__(self):
        if self.temp_dir is None:
            self.temp_dir = tempfile.gettempdir()
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)


@dataclass
class SharedConfig:
    """共享配置 - 所有生产者/消费者共用"""
    resource: ResourceConfig = field(default_factory=ResourceConfig)
    custom_attrs: Dict[str, Any] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def set(self, key: str, value: Any):
        """设置共享属性"""
        with self._lock:
            self.custom_attrs[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取共享属性"""
        with self._lock:
            return self.custom_attrs.get(key, default)


class DiskBackedQueue:
    """
    支持磁盘溢出的队列
    优先使用内存队列，队列满时阻塞等待
    只有当进程内存超过限制时才溢出到磁盘
    """

    def __init__(self, name: str, max_size: int = 10000,
                 temp_dir: str = None, max_memory_mb: int = 1024):
        self.name = name
        self.max_size = max_size
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.max_memory_mb = max_memory_mb  # 进程内存限制(MB)

        self._memory_queue = Queue(maxsize=max_size)
        self._disk_dir = Path(self.temp_dir) / f"queue_{name}_{uuid.uuid4().hex[:8]}"
        self._disk_dir.mkdir(parents=True, exist_ok=True)

        self._disk_files: List[Path] = []
        self._disk_lock = threading.RLock()  # 使用可重入锁，避免嵌套调用死锁
        self._disk_read_index = 0
        self._disk_write_index = 0

        self._use_disk = False
        self._closed = False
        self._total_put = 0
        self._total_get = 0

    def _should_use_disk(self) -> bool:
        """判断是否应该使用磁盘：只有进程内存超过限制时才用磁盘"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)
            return memory_mb > self.max_memory_mb
        except:
            return False  # 获取失败时不用磁盘

    def _write_to_disk(self, item: Any) -> Path:
        """写入磁盘"""
        with self._disk_lock:
            file_path = self._disk_dir / f"item_{self._disk_write_index}.pkl"
            self._disk_write_index += 1
            with open(file_path, 'wb') as f:
                pickle.dump(item, f)
            self._disk_files.append(file_path)
            return file_path

    def _read_from_disk_unlocked(self) -> Optional[Any]:
        """从磁盘读取（调用方需持有锁）"""
        if not self._disk_files:
            return None
        file_path = self._disk_files.pop(0)
        try:
            with open(file_path, 'rb') as f:
                item = pickle.load(f)
            file_path.unlink(missing_ok=True)
            return item
        except Exception as e:
            logger.error(f"读取磁盘数据失败: {e}")
            return None

    def _read_from_disk(self) -> Optional[Any]:
        """从磁盘读取"""
        with self._disk_lock:
            return self._read_from_disk_unlocked()

    def put(self, item: Any, timeout: float = None) -> bool:
        """放入数据：优先内存队列，队列满则阻塞等待，只有内存超限才用磁盘"""
        if self._closed:
            return False

        # 如果已经在磁盘模式，检查是否可以切回内存
        if self._use_disk:
            if not self._should_use_disk() and not self._memory_queue.full():
                self._use_disk = False
            else:
                # 继续使用磁盘
                self._write_to_disk(item)
                self._total_put += 1
                return True

        # 尝试放入内存队列
        try:
            # 队列满时阻塞等待，最多等待timeout秒
            self._memory_queue.put(item, timeout=timeout or 1.0)
            self._total_put += 1
            return True
        except Full:
            # 队列满且超时，检查是否需要用磁盘
            if self._should_use_disk():
                self._use_disk = True
                self._write_to_disk(item)
                self._total_put += 1
                logger.warning(f"队列 {self.name} 内存超限，启用磁盘模式")
                return True
            else:
                # 内存未超限，继续阻塞等待
                self._memory_queue.put(item)  # 无限等待
                self._total_put += 1
                return True

    def get(self, timeout: float = 1.0) -> Optional[Any]:
        """获取数据"""
        # 优先从磁盘读取（保证顺序）
        with self._disk_lock:
            if self._disk_files:
                item = self._read_from_disk_unlocked()
                if item is not None:
                    self._total_get += 1
                    # 检查是否可以切回内存模式
                    if not self._disk_files and not self._should_use_disk():
                        self._use_disk = False
                    return item

        try:
            item = self._memory_queue.get(timeout=timeout)
            self._total_get += 1
            return item
        except Empty:
            return None

    def get_batch(self, batch_size: int, timeout: float = 1.0) -> List[Any]:
        """批量获取数据，减少锁竞争"""
        result = []
        
        # 批量从磁盘读取
        with self._disk_lock:
            while len(result) < batch_size and self._disk_files:
                item = self._read_from_disk_unlocked()
                if item is not None:
                    self._total_get += 1
                    result.append(item)
            # 检查是否可以切回内存模式
            if not self._disk_files and not self._should_use_disk():
                self._use_disk = False
        
        # 从内存队列补充
        while len(result) < batch_size:
            try:
                item = self._memory_queue.get(timeout=timeout if not result else 0.01)
                self._total_get += 1
                result.append(item)
            except Empty:
                break
        
        return result

    def qsize(self) -> int:
        """队列大小"""
        with self._disk_lock:
            return self._memory_queue.qsize() + len(self._disk_files)

    def empty(self) -> bool:
        """是否为空"""
        with self._disk_lock:
            return self._memory_queue.empty() and len(self._disk_files) == 0

    def close(self):
        """关闭队列，清理磁盘文件"""
        self._closed = True
        with self._disk_lock:
            for f in self._disk_files:
                try:
                    f.unlink(missing_ok=True)
                except:
                    pass
            try:
                self._disk_dir.rmdir()
            except:
                pass

    @property
    def stats(self) -> Dict:
        """统计信息"""
        return {
            "name": self.name,
            "total_put": self._total_put,
            "total_get": self._total_get,
            "pending": self.qsize(),
            "use_disk": self._use_disk,
            "disk_files": len(self._disk_files)
        }


class BaseWorker(ABC):
    """工作者基类"""

    def __init__(self, worker_id: str, shared_config: SharedConfig):
        self.worker_id = worker_id
        self.shared_config = shared_config
        self._local_attrs: Dict[str, Any] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._processed_count = 0
        self._error_count = 0

    def set_attr(self, key: str, value: Any):
        """设置本地属性"""
        self._local_attrs[key] = value

    def get_attr(self, key: str, default: Any = None) -> Any:
        """获取属性（本地优先，否则共享）"""
        if key in self._local_attrs:
            return self._local_attrs[key]
        return self.shared_config.get(key, default)

    @property
    def stats(self) -> Dict:
        """统计信息"""
        return {
            "worker_id": self.worker_id,
            "running": self._running,
            "processed": self._processed_count,
            "errors": self._error_count
        }

    @abstractmethod
    def _run(self):
        """运行逻辑"""
        pass

    def start(self):
        """启动"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._safe_run, daemon=True)
        self._thread.start()

    def _safe_run(self):
        """安全运行"""
        try:
            self._run()
        except Exception as e:
            logger.exception(f"Worker {self.worker_id} 异常: {e}")
            self._error_count += 1
        finally:
            self._running = False

    def stop(self):
        """停止"""
        self._running = False

    def join(self, timeout: float = None):
        """等待结束"""
        if self._thread:
            self._thread.join(timeout=timeout)


class Producer(BaseWorker):
    """
    生产者
    从输入队列获取数据，加工后放入一个或多个输出队列
    """

    def __init__(self, worker_id: str, shared_config: SharedConfig,
                 input_queue: DiskBackedQueue,
                 output_queues: Dict[str, DiskBackedQueue],
                 process_func: Callable[[Any, 'Producer'], Dict[str, Any]] = None,
                 process_func_args: Dict[str, Any] = None):
        super().__init__(worker_id, shared_config)
        self.input_queue = input_queue
        self.output_queues = output_queues
        self._process_func = process_func
        self._process_func_args = process_func_args or {}  # 存储自定义参数
        self._finished_event = threading.Event()
        self._feed_ended = False  # 标记是否已结束投喷

    @property
    def finished_event(self) -> threading.Event:
        """生产完成事件"""
        return self._finished_event

    def process(self, data: Any) -> Dict[str, Any]:
        """
        加工数据
        返回格式: {"queue_name": processed_data, ...}
        可以返回多个队列的数据
        """
        if self._process_func:
            # 支持带参数的函数调用
            if hasattr(self, '_process_func_args') and self._process_func_args:
                return self._process_func(data, self, **self._process_func_args)
            else:
                return self._process_func(data, self)
        # 默认实现：发送到所有输出队列
        return {name: data for name in self.output_queues.keys()}

    def end_feed(self):
        """标记结束投喂，生产者处理完队列数据后自动结束"""
        self._feed_ended = True
        logger.info(f"生产者 {self.worker_id} 收到结束投喂信号")

    def _run(self):
        """运行生产者"""
        logger.info(f"生产者 {self.worker_id} 启动")

        while self._running:
            try:
                # 从输入队列获取数据
                data = self.input_queue.get(timeout=0.5)
                if data is None:
                    # 检查是否已结束投喂且队列为空
                    if self._feed_ended and self.input_queue.empty():
                        logger.info(f"生产者 {self.worker_id} 检测到投喂结束且队列为空，准备退出")
                        break
                    # 检查输入队列是否已关闭且为空
                    if self.input_queue.empty():
                        time.sleep(0.1)
                    continue

                # 加工数据
                try:
                    results = self.process(data)

                    # 分发到各输出队列
                    for queue_name, result_data in results.items():
                        if queue_name in self.output_queues and result_data is not None:
                            # 支持列表和单个值
                            if isinstance(result_data, list):
                                for item in result_data:
                                    self.output_queues[queue_name].put(item)
                            else:
                                self.output_queues[queue_name].put(result_data)

                    self._processed_count += 1
                except Exception as e:
                    logger.error(f"生产者 {self.worker_id} 处理数据失败: {e}")
                    self._error_count += 1

            except Exception as e:
                logger.error(f"生产者 {self.worker_id} 运行异常: {e}")
                time.sleep(0.1)

        logger.info(f"生产者 {self.worker_id} 结束，处理: {self._processed_count}")
        self._finished_event.set()


class Consumer(BaseWorker):
    """
    消费者
    从队列消费数据
    """

    def __init__(self, worker_id: str, shared_config: SharedConfig,
                 input_queue: DiskBackedQueue,
                 consume_func: Callable[[Any, 'Consumer'], None] = None,
                 batch_size: int = 1,
                 batch_timeout: Optional[float] = None,
                 setup_func: Callable[['Consumer'], None] = None,
                 teardown_func: Callable[['Consumer'], None] = None,
                 consume_func_args: Dict[str, Any] = None):
        super().__init__(worker_id, shared_config)
        self.input_queue = input_queue
        self._consume_func = consume_func
        self._consume_func_args = consume_func_args or {}  # 存储自定义参数
        self._setup_func = setup_func  # 初始化函数
        self._teardown_func = teardown_func  # 清理函数
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self._producer_finished_events: List[threading.Event] = []
        self._all_done = threading.Event()

    def setup(self):
        """
        初始化函数 - 消费者线程启动时调用一次
        用于初始化数据库连接、打开文件等资源
        """
        if self._setup_func:
            self._setup_func(self)

    def teardown(self):
        """
        清理函数 - 消费者线程结束时调用一次
        用于关闭数据库连接、关闭文件等资源
        """
        if self._teardown_func:
            self._teardown_func(self)

    def add_producer_event(self, event: threading.Event):
        """添加生产者完成事件"""
        self._producer_finished_events.append(event)

    def _all_producers_finished(self) -> bool:
        """检查所有生产者是否已完成"""
        if not self._producer_finished_events:
            return False
        return all(e.is_set() for e in self._producer_finished_events)

    def consume(self, data: Any):
        """消费单条数据"""
        if self._consume_func:
            # 支持带参数的函数调用
            if hasattr(self, '_consume_func_args') and self._consume_func_args:
                self._consume_func(data, self, **self._consume_func_args)
            else:
                self._consume_func(data, self)

    def consume_batch(self, batch: List[Any]):
        """批量消费数据 - 将整个批次传递给消费函数"""
        if self._consume_func:
            # 支持带参数的函数调用
            if hasattr(self, '_consume_func_args') and self._consume_func_args:
                self._consume_func(batch, self, **self._consume_func_args)
            else:
                self._consume_func(batch, self)

    def _run(self):
        """运行消费者"""
        logger.info(f"消费者 {self.worker_id} 启动")
        
        # 执行初始化函数（只执行一次）
        try:
            self.setup()
        except Exception as e:
            logger.error(f"消费者 {self.worker_id} 初始化失败: {e}")
            self._error_count += 1
            return
        
        batch = []
        last_batch_time = time.time()

        while self._running:
            try:
                if self.batch_size > 1:
                    # 批量模式：使用批量获取减少锁竞争
                    need_count = self.batch_size - len(batch)
                    items = self.input_queue.get_batch(need_count, timeout=0.5)
                    
                    if items:
                        batch.extend(items)
                        # 判断是否触发批处理
                        should_process = len(batch) >= self.batch_size
                        # 如果设置了超时，才检查超时条件
                        if self.batch_timeout is not None and batch and time.time() - last_batch_time > self.batch_timeout:
                            should_process = True
                        
                        if should_process:
                            try:
                                self.consume_batch(batch)
                                self._processed_count += len(batch)
                            except Exception as e:
                                logger.error(f"消费者 {self.worker_id} 批量消费失败: {e}")
                                self._error_count += len(batch)
                            batch = []
                            last_batch_time = time.time()
                    else:
                        # 队列为空，检查是否应该处理批次或结束
                        if batch:
                            should_flush = False
                            if self.batch_timeout is not None and time.time() - last_batch_time > self.batch_timeout:
                                should_flush = True
                            if self._all_producers_finished():
                                should_flush = True
                            
                            if should_flush:
                                try:
                                    self.consume_batch(batch)
                                    self._processed_count += len(batch)
                                except Exception as e:
                                    logger.error(f"消费者 {self.worker_id} 批量消费失败: {e}")
                                    self._error_count += len(batch)
                                batch = []
                                last_batch_time = time.time()
                        
                        # 检查是否所有生产者都已完成且队列为空
                        if self._all_producers_finished() and self.input_queue.empty():
                            if batch:
                                try:
                                    self.consume_batch(batch)
                                    self._processed_count += len(batch)
                                except Exception as e:
                                    logger.error(f"消费者 {self.worker_id} 最终批量消费失败: {e}")
                                    self._error_count += len(batch)
                            break
                else:
                    # 单条模式
                    data = self.input_queue.get(timeout=0.5)
                    if data is not None:
                        try:
                            self.consume(data)
                            self._processed_count += 1
                        except Exception as e:
                            logger.error(f"消费者 {self.worker_id} 消费失败: {e}")
                            self._error_count += 1
                    else:
                        # 检查是否所有生产者都已完成且队列为空
                        if self._all_producers_finished() and self.input_queue.empty():
                            break

            except Exception as e:
                logger.error(f"消费者 {self.worker_id} 运行异常: {e}")
                time.sleep(0.1)

        # 执行清理函数（只执行一次）
        try:
            self.teardown()
        except Exception as e:
            logger.error(f"消费者 {self.worker_id} 清理失败: {e}")
            self._error_count += 1

        logger.info(f"消费者 {self.worker_id} 结束，消费: {self._processed_count}")
        self._all_done.set()

    @property
    def done_event(self) -> threading.Event:
        """消费完成事件"""
        return self._all_done


class ProducerGroup:
    """生产者组 - 管理同类型的多个生产者"""

    def __init__(self, name: str, shared_config: SharedConfig,
                 input_queue: DiskBackedQueue,
                 output_queues: Dict[str, DiskBackedQueue],
                 process_func: Callable = None,
                 num_workers: int = 1,
                 process_func_args: Dict[str, Any] = None):
        self.name = name
        self.shared_config = shared_config
        self.input_queue = input_queue
        self.output_queues = output_queues
        self.process_func = process_func
        self.process_func_args = process_func_args or {}  # 存储自定义参数
        self.num_workers = num_workers

        self._producers: List[Producer] = []
        self._group_finished_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None

        self._create_producers()

    def _create_producers(self):
        """创建生产者"""
        for i in range(self.num_workers):
            producer = Producer(
                worker_id=f"{self.name}_producer_{i}",
                shared_config=self.shared_config,
                input_queue=self.input_queue,
                output_queues=self.output_queues,
                process_func=self.process_func,
                process_func_args=self.process_func_args  # 传递自定义参数
            )
            self._producers.append(producer)

    def start(self):
        """启动所有生产者"""
        for p in self._producers:
            p.start()
        # 启动监控线程
        self._monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self._monitor_thread.start()

    def _monitor(self):
        """监控所有生产者是否完成"""
        for p in self._producers:
            p.join()
        self._group_finished_event.set()
        logger.info(f"生产者组 {self.name} 全部完成")

    def end_feed(self):
        """通知所有生产者结束投喂"""
        for p in self._producers:
            p.end_feed()
        logger.info(f"生产者组 {self.name} 已通知所有生产者结束投喂")

    def stop(self):
        """停止所有生产者"""
        for p in self._producers:
            p.stop()

    def join(self, timeout: float = None):
        """等待所有生产者完成"""
        for p in self._producers:
            p.join(timeout=timeout)

    @property
    def finished_event(self) -> threading.Event:
        """生产者组完成事件"""
        return self._group_finished_event

    @property
    def stats(self) -> Dict:
        """统计信息"""
        return {
            "name": self.name,
            "num_workers": self.num_workers,
            "producers": [p.stats for p in self._producers],
            "finished": self._group_finished_event.is_set()
        }


class ConsumerGroup:
    """消费者组 - 管理同类型的多个消费者"""

    def __init__(self, name: str, shared_config: SharedConfig,
                 input_queue: DiskBackedQueue,
                 consume_func: Callable = None,
                 num_workers: int = 1,
                 batch_size: int = 1,
                 batch_timeout: Optional[float] = None,
                 setup_func: Callable = None,
                 teardown_func: Callable = None,
                 consume_func_args: Dict[str, Any] = None):
        self.name = name
        self.shared_config = shared_config
        self.input_queue = input_queue
        self.consume_func = consume_func
        self.consume_func_args = consume_func_args or {}  # 存储自定义参数
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.setup_func = setup_func
        self.teardown_func = teardown_func

        self._consumers: List[Consumer] = []
        self._group_finished_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None

        self._create_consumers()

    def _create_consumers(self):
        """创建消费者"""
        for i in range(self.num_workers):
            consumer = Consumer(
                worker_id=f"{self.name}_consumer_{i}",
                shared_config=self.shared_config,
                input_queue=self.input_queue,
                consume_func=self.consume_func,
                batch_size=self.batch_size,
                batch_timeout=self.batch_timeout,
                setup_func=self.setup_func,
                teardown_func=self.teardown_func,
                consume_func_args=self.consume_func_args
            )
            self._consumers.append(consumer)

    def bind_producer_group(self, producer_group: ProducerGroup):
        """绑定生产者组，监听其完成事件"""
        for consumer in self._consumers:
            consumer.add_producer_event(producer_group.finished_event)

    def bind_producer(self, producer: Producer):
        """绑定单个生产者"""
        for consumer in self._consumers:
            consumer.add_producer_event(producer.finished_event)

    def start(self):
        """启动所有消费者"""
        for c in self._consumers:
            c.start()
        # 启动监控线程
        self._monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self._monitor_thread.start()

    def _monitor(self):
        """监控所有消费者是否完成"""
        for c in self._consumers:
            c.join()
        self._group_finished_event.set()
        logger.info(f"消费者组 {self.name} 全部完成")

    def stop(self):
        """停止所有消费者"""
        for c in self._consumers:
            c.stop()

    def join(self, timeout: float = None):
        """等待所有消费者完成"""
        for c in self._consumers:
            c.join(timeout=timeout)

    @property
    def finished_event(self) -> threading.Event:
        return self._group_finished_event

    @property
    def stats(self) -> Dict:
        return {
            "name": self.name,
            "num_workers": self.num_workers,
            "consumers": [c.stats for c in self._consumers],
            "finished": self._group_finished_event.is_set()
        }


class Factory:
    """
    工厂类 - 管理整个生产消费流程
    """

    def __init__(self, resource_config: ResourceConfig = None, enable_monitor: bool = True, monitor_interval: float = 10.0):
        self.resource_config = resource_config or ResourceConfig()
        self.shared_config = SharedConfig(resource=self.resource_config)

        self._queues: Dict[str, DiskBackedQueue] = {}
        self._producer_groups: Dict[str, ProducerGroup] = {}
        self._consumer_groups: Dict[str, ConsumerGroup] = {}

        self._running = False
        self._enable_monitor = enable_monitor  # 是否启用监控
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitor_interval = monitor_interval  # 监控间隔时间（秒）

    def create_queue(self, name: str, max_size: int = None) -> DiskBackedQueue:
        """创建队列"""
        if name in self._queues:
            return self._queues[name]

        queue = DiskBackedQueue(
            name=name,
            max_size=max_size or self.resource_config.max_queue_size,
            temp_dir=self.resource_config.temp_dir,
            max_memory_mb=self.resource_config.max_memory_mb
        )
        self._queues[name] = queue
        return queue

    def get_queue(self, name: str) -> Optional[DiskBackedQueue]:
        """获取队列"""
        return self._queues.get(name)

    def create_producer_group(self, name: str,
                              input_queue_name: str,
                              output_consumer_names: List[str] = None,
                              process_func: Callable = None,
                              num_workers: int = 1,
                              process_func_args: Dict[str, Any] = None) -> ProducerGroup:
        """创建生产者组
        
        Args:
            name: 生产者组名称
            input_queue_name: 输入队列名称（应先通过factory.create_queue指定大小）
            output_consumer_names: 输出到哪些消费者组（使用消费者组名称作为队列名）
            process_func: 处理函数
            num_workers: 工作线程数
            process_func_args: 处理函数的自定义参数字典（可选）
        """
        input_queue = self._queues.get(input_queue_name)
        if not input_queue:
            input_queue = self.create_queue(input_queue_name)

        # 如果指定了消费者名称，自动创建对应的队列
        # 队列大小由消费者组在创建时指定
        output_queues = {}
        if output_consumer_names:
            for consumer_name in output_consumer_names:
                if consumer_name not in self._queues:
                    # 暂时使用默认大小，下次会被消费者的队列大小覆盖
                    self.create_queue(consumer_name)
                output_queues[consumer_name] = self._queues[consumer_name]

        group = ProducerGroup(
            name=name,
            shared_config=self.shared_config,
            input_queue=input_queue,
            output_queues=output_queues,
            process_func=process_func,
            num_workers=num_workers,
            process_func_args=process_func_args  # 传递自定义参数
        )
        self._producer_groups[name] = group
        return group

    def create_consumer_group(self, name: str,
                              consume_func: Callable = None,
                              num_workers: int = 1,
                              batch_size: int = 1,
                              batch_timeout: Optional[float] = None,
                              bind_producer_names: List[str] = None,
                              setup_func: Callable = None,
                              teardown_func: Callable = None,
                              consume_func_args: Dict[str, Any] = None) -> ConsumerGroup:
        """创建消费者组
        
        Args:
            name: 消费者组名称（同时作为输入队列名称）
            consume_func: 消费函数
            num_workers: 工作线程数
            batch_size: 批量大小
            batch_timeout: 批量超时时间
            bind_producer_names: 绑定的生产者组名称列表（可选，不指定则自动绑定所有输出到此队列的生产者）
            setup_func: 初始化函数
            teardown_func: 清理函数
            consume_func_args: 消费函数的自定义参数字典（可选）
        """
        # 使用消费者组名称作为队列名称
        input_queue = self._queues.get(name)
        if not input_queue:
            # 使用ResourceConfig中的默认配置
            input_queue = self.create_queue(name)

        group = ConsumerGroup(
            name=name,
            shared_config=self.shared_config,
            input_queue=input_queue,
            consume_func=consume_func,
            num_workers=num_workers,
            batch_size=batch_size,
            batch_timeout=batch_timeout,
            setup_func=setup_func,
            teardown_func=teardown_func,
            consume_func_args=consume_func_args  # 传递自定义参数
        )

        # 自动绑定生产者组
        if bind_producer_names:
            # 手动指定绑定
            for pg_name in bind_producer_names:
                if pg_name in self._producer_groups:
                    group.bind_producer_group(self._producer_groups[pg_name])
        else:
            # 自动绑定所有输出到此队列的生产者组
            for pg_name, pg in self._producer_groups.items():
                if name in pg.output_queues:
                    group.bind_producer_group(pg)
                    logger.info(f"消费者组 {name} 自动绑定生产者组 {pg_name}")

        self._consumer_groups[name] = group
        return group

    def set_shared_attr(self, key: str, value: Any):
        """设置共享属性"""
        self.shared_config.set(key, value)

    def get_shared_attr(self, key: str, default: Any = None) -> Any:
        """获取共享属性"""
        return self.shared_config.get(key, default)

    def feed(self, queue_name: str, data: Any) -> bool:
        """向队列投放数据"""
        queue = self._queues.get(queue_name)
        if queue:
            return queue.put(data)
        return False

    def feed_batch(self, queue_name: str, data_list: List[Any]):
        """批量投放数据"""
        queue = self._queues.get(queue_name)
        if queue:
            for data in data_list:
                queue.put(data)

    def end_feed(self, name: str):
        """结束指定生产者组的数据投喂
        
        Args:
            name: 生产者组名称
        """
        producer_group = self._producer_groups.get(name)
        if producer_group:
            producer_group.end_feed()
            logger.info(f"工厂通知生产者组 {name} 结束投喂")
        else:
            logger.warning(f"生产者组 {name} 不存在")

    def start(self):
        """启动工厂"""
        if self._running:
            return

        self._running = True
        logger.info("工厂启动...")

        # 如果启用监控，则启动监控线程
        if self._enable_monitor:
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            logger.info(f"监控已启用，监控间隔: {self._monitor_interval}秒")

        # 先启动消费者
        for cg in self._consumer_groups.values():
            cg.start()

        # 再启动生产者
        for pg in self._producer_groups.values():
            pg.start()

    def _monitor_loop(self):
        """监控循环"""
        while self._running:
            time.sleep(self._monitor_interval)
            if self._running:
                self._log_stats()

    def _log_stats(self):
        """输出统计信息"""
        stats = self.stats
        logger.info(f"=== 工厂状态 ===")
        for q_name, q_stats in stats["queues"].items():
            logger.info(f"队列 {q_name}: 待处理={q_stats['pending']}, "
                        f"入队={q_stats['total_put']}, 出队={q_stats['total_get']}, "
                        f"磁盘模式={q_stats['use_disk']}")
        for pg_name, pg_stats in stats["producer_groups"].items():
            total_processed = sum(p["processed"] for p in pg_stats["producers"])
            logger.info(f"生产者组 {pg_name}: 已处理={total_processed}, "
                        f"完成={pg_stats['finished']}")
        for cg_name, cg_stats in stats["consumer_groups"].items():
            total_consumed = sum(c["processed"] for c in cg_stats["consumers"])
            logger.info(f"消费者组 {cg_name}: 已消费={total_consumed}, "
                        f"完成={cg_stats['finished']}")

    def stop(self):
        """停止工厂"""
        logger.info("工厂停止中...")
        self._running = False

        # 停止生产者
        for pg in self._producer_groups.values():
            pg.stop()

        # 停止消费者
        for cg in self._consumer_groups.values():
            cg.stop()

    def wait_complete(self, timeout: float = None):
        """等待所有任务完成"""
        # 等待所有消费者完成
        for cg in self._consumer_groups.values():
            cg.join(timeout=timeout)

        self._running = False
        logger.info("工厂任务全部完成")

    def close(self):
        """关闭工厂，清理资源"""
        self.stop()
        for queue in self._queues.values():
            queue.close()
        logger.info("工厂已关闭")

    @property
    def stats(self) -> Dict:
        """工厂统计信息"""
        return {
            "queues": {name: q.stats for name, q in self._queues.items()},
            "producer_groups": {name: pg.stats for name, pg in self._producer_groups.items()},
            "consumer_groups": {name: cg.stats for name, cg in self._consumer_groups.items()}
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ============ 使用示例 ============

if __name__ == "__main__":
    # 设置彩色日志
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler]
    )


    # 定义处理函数
    def my_process(data: Any, producer: Producer, multiplier: int = 1, process_name: str = '加工日志') -> Dict[str, Any]:
        """生产者处理函数：将数据加工后分发到不同队列"""
        # 示例：根据数据类型分发
        producer_id = producer.worker_id
        result = {"consumer_a": None, "consumer_b": None}

        processed = data * 2 * multiplier  # 使用自定义参数multiplier
        time.sleep(0.1)

        # 可以访问共享属性
        logger.info(f"{process_name} {producer_id}处理: {data} -> {processed}")

        if processed % 2 == 0:
            result["consumer_a"] = processed
        else:
            result["consumer_b"] = processed

        return result


    def my_consume_a(data: Any, consumer: Consumer, log_prefix: str = "消费者A"):
        """消费者A处理函数 - 支持自定义参数"""
        logger.info(f"{log_prefix}-{consumer.worker_id}处理: {data}")


    def my_consume_b(data: Any, consumer: Consumer, log_prefix: str = "消费者B", tag: str = ""):
        """消费者B处理函数 - 支持自定义参数"""
        logger.info(f"{log_prefix}-{consumer.worker_id}{tag}处理: {data}")


    def setup_db_connection(consumer: Consumer):
        """
        消费者初始化函数 - 每个消费者线程启动时执行一次
        用于创建数据库连接、打开文件等资源
        """
        # 示例：创建数据库客户端
        db_client = {"connection": f"DB Connection for {consumer.worker_id}"}
        # 会存储到消费者对象，了后可以通过 consumer.get_attr() 访问
        consumer.set_attr("db_client", db_client)
        logger.info(f"消费者 {consumer.worker_id} 数据库连接建立成功")


    def teardown_db_connection(consumer: Consumer):
        """
        消费者清理函数 - 每个消费者线程结束时执行一次
        用于关闭数据库连接、关闭文件等资源
        """
        # 示例：关闭数据库客户端
        db_client = consumer.get_attr("db_client")
        if db_client:
            logger.info(f"消费者 {consumer.worker_id} 数据库连接已关闭")
            # 处理上传剩余数据等


    # 创建工厂
    config = ResourceConfig(
        max_memory_mb=512,  # 进程内存超过512MB才用磁盘
        max_queue_size=100000,  # 队列默认容量（主要用于消费者队列）
        temp_dir="./temp_queue"
    )

    with Factory(resource_config=config, enable_monitor=False) as factory:
        # 参数说明：
        # enable_monitor=True  - 启用监控（False 为禁用）
        # monitor_interval=10.0 - 监控间隔时间，单位秒，默认10秒
        # ... existing code ...

        # 创建生产者输入队列，指定较小的容量（只存文件名或ID）
        factory.create_queue("input", max_size=5000)

        # 创建生产者组：传入自定义参数process_func_args
        factory.create_producer_group(
            name="main_producer",
            input_queue_name="input",
            output_consumer_names=["consumer_a", "consumer_b"],
            process_func=my_process,
            num_workers=2,
            process_func_args={"multiplier": 3, "process_name": "生产加工"}  # 传入自定义参数
        )

        # 创建消费者组A：使用默认队列容量（100000）
        factory.create_consumer_group(
            name="consumer_a",
            consume_func=my_consume_a,
            setup_func=setup_db_connection,
            teardown_func=teardown_db_connection,
            num_workers=2,
            consume_func_args={"log_prefix": "消费者_A组"}  # 传入自定义参数
        )

        # 创建消费者组B：使用默认队列容量（100000）
        factory.create_consumer_group(
            name="consumer_b",
            consume_func=my_consume_b,
            num_workers=1,
            consume_func_args={"log_prefix": "消费者_B组", "tag": "[优先处理]"}  # 传入自定义参数
        )

        # 启动工厂
        factory.start()
        # 投放数据
        for i in range(100):
            factory.feed("input", i)

        # 通知生产者组：没有更多数据了
        factory.end_feed(name="main_producer")

        logger.info("已通知生产者结束投喂，等待处理完成...")

        # 等待完成
        factory.wait_complete(timeout=120)  # 增加超时时间

        # 输出最终统计
        logger.info("=== 最终统计信息 ===")
        stats_json = json.dumps(factory.stats, indent=2, ensure_ascii=False)
        print("\n" + stats_json)
        logger.info("任务全部完成")
