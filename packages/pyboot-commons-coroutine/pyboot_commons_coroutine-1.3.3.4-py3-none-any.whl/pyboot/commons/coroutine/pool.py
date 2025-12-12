import asyncio
import threading
import time
from multiprocessing import Value

from typing import Any, Callable, Dict, Generic, Optional, TypeVar
from contextlib import asynccontextmanager

from pyboot.commons.utils.log import Logger

from pyboot.commons.coroutine.tools import await_loop_complete
from abc import ABC, abstractmethod
from enum import Enum

_logger = Logger('dataflow.utils.coroutine.pool')

"""共享内存+锁的分布式方案"""
class DistributedSharedState:
    def __init__(self):
        # 使用 multiprocessing 的共享内存
        self._counter = Value('i', 0)  # 整型计数器
        self._lock = threading.RLock()  # 可重入锁
        
        # 用于复杂数据结构的共享字典（需要额外同步）
        self._shared_dict = {}
        self._dict_lock = threading.RLock()
    
    def increment_counter(self) -> int:
        """原子递增计数器"""
        with self._counter.get_lock():
            self._counter.value += 1
            return self._counter.value
    
    def get_counter(self) -> int:
        """获取计数器值"""
        return self._counter.value
    
    def set_value(self, key: str, value: any):
        """设置共享字典值"""
        with self._dict_lock:
            self._shared_dict[key] = value
    
    def get_value(self, key: str, default: any = None) -> any:
        """获取共享字典值"""
        with self._dict_lock:
            return self._shared_dict.get(key, default)
    
    def increment_with_retry(self, max_retries: int = 3) -> int:
        """带重试的递增（处理锁竞争）"""
        for attempt in range(max_retries):
            try:
                with self._lock:
                    return self.increment_counter()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(0.001 * (attempt + 1))  # 指数退避
        return -1

"""支持异步操作的分布式共享状态"""
class AsyncDistributedSharedState:        
    def __init__(self):
        self._state = DistributedSharedState()
        self._loop = asyncio.get_event_loop()
    
    async def increment_counter(self) -> int:
        """异步递增计数器"""
        # 在线程池中执行阻塞操作
        return await self._loop.run_in_executor(
            None, self._state.increment_counter
        )
    
    async def get_counter(self) -> int:
        """异步获取计数器"""
        return await self._loop.run_in_executor(
            None, self._state.get_counter
        )
    
    async def set_value(self, key: str, value: any):
        """异步设置值"""
        await self._loop.run_in_executor(
            None, lambda: self._state.set_value(key, value)
        )
    
    async def get_value(self, key: str, default: any = None) -> any:
        """异步获取值"""
        return await self._loop.run_in_executor(
            None, lambda: self._state.get_value(key, default)
        )
        
class PoolState(Enum):
    """对象池状态"""
    UNINITIALIZED = "Uninitialized"
    RUNNING = "Running"
    CLOSING = "Closing"
    CLOSED = "Closed"

T = TypeVar('T')

# 事件循环内多协程安全访问的对象池
class ObjectPool(Generic[T]):
    """
    事件循环内多协程安全访问的对象池
    
    特性：
    - 协程安全的对象获取和归还
    - 支持对象创建工厂和销毁函数
    - 支持最大池大小和最小空闲对象数
    - 支持对象验证和健康检查
    - 支持异步上下文管理器
    - 统计信息收集
    """
    
    def __init__(
        self,
        create_factory: Callable[[], T],
        kargs:dict = None,        
        max_size: int = 10,
        min_idle: int = 1,
        max_idle: int = 5,        
        validation_func: Optional[Callable[[T], bool]] = None,
        destroy_func: Optional[Callable[[T], None]] = None,
        reset_func: Optional[Callable[[T], None]] = None
        
    ):
        """
        初始化对象池
        
        Args:
            create_factory: 对象创建工厂函数
            max_size: 池中最大对象数量
            min_idle: 最小空闲对象数
            max_idle: 最大空闲对象数
            validation_func: 对象验证函数，返回True表示对象有效
            destroy_func: 对象销毁函数
            reset_func: 对象重置函数（归还时调用）
        """
        # _logger.DEBUG(f'create_factory={create_factory} validation_func={validation_func} destroy_func={destroy_func} reset_func={reset_func}')
        
        self._create_factory = create_factory
        self._create_factory_kargs = kargs or {}
        self._max_size = max_size
        self._min_idle = min_idle
        self._max_idle = max_idle
        self._validation_func = validation_func
        self._destroy_func = destroy_func
        self._reset_func = reset_func
        
        # 对象存储
        self._available_objects: asyncio.Queue = asyncio.Queue()
        self._in_use_objects: dict[T, float] = {}
        
        # 同步原语
        self._lock = asyncio.Lock()
        self._condition = asyncio.Condition()
        
        # 统计信息
        self._stats = {
            'created': 0,
            'destroyed': 0,
            'acquired': 0,
            'released': 0,
            'validation_failed': 0,
            'peak_usage': 0,
            'wait_time_total': 0.0,
            'wait_count': 0
        }
        
        # 状态标志
        self._closed = False
        self._initialized = False
        self._state = PoolState.UNINITIALIZED
    
    async def initialize(self):
        """初始化对象池，创建最小空闲对象"""
        if self._state != PoolState.UNINITIALIZED:
            return
        
        async with self._lock:
            if self._state != PoolState.UNINITIALIZED:
                return
            
            for _ in range(self._min_idle):
                obj = await self._create_object()
                await self._available_objects.put(obj)            
            self._initialized = True
            self._state = PoolState.RUNNING
            
        _logger.DEBUG(f'对象池初始化成功 {self.get_stats()}')
        # 等待
        await asyncio.sleep(0.01)
        
    
    async def _create_object(self) -> T:
        """创建新对象"""
        try:
            if asyncio.iscoroutinefunction(self._create_factory):
                await self._create_factory(**self._create_factory_kargs)
            else:
                self._create_factory(**self._create_factory_kargs)
        except Exception as e:
            # _logger.ERROR(f"创建对象失败: {e}")
            raise ValueError(f"创建对象失败: {e}")
                
        obj = self._create_factory()
        self._stats['created'] += 1
        return obj
    
    async def _destroy_object(self, obj: T):
        """销毁对象"""
        _logger.DEBUG(f'销毁对象 = {obj}')
        if self._destroy_func:
            try:
                if asyncio.iscoroutinefunction(self._destroy_func):
                    await self._destroy_func(obj)
                else:
                    self._destroy_func(obj)
            except Exception as e:
                # _logger.ERROR(f"销毁对象失败: {e}")
                raise ValueError(f"销毁对象失败: {e}")
        
        self._stats['destroyed'] += 1
        
    async def _destroy_object_safe(self, obj: T):
        """销毁对象"""
        _logger.DEBUG(f'销毁对象 = {obj}')
        if self._destroy_func:
            try:
                if asyncio.iscoroutinefunction(self._destroy_func):
                    await self._destroy_func(obj)
                else:
                    self._destroy_func(obj)
            except Exception as e:
                _logger.WARN(f"销毁对象失败: {e}")
                # raise ValueError(f"销毁对象失败: {e}")
        
        self._stats['destroyed'] += 1
    
    async def _validate_object(self, obj: T) -> bool:
        """验证对象是否有效"""
        _logger.DEBUG(f'验证对象是否有效 = {obj}')
        
        if not self._validation_func:
            return True
        
        try:
            if asyncio.iscoroutinefunction(self._validation_func):
                return await self._validation_func(obj)
            else:
                return self._validation_func(obj)
        except Exception as e:
            # _logger.ERROR(f"校验对象失败: {e}")
            raise ValueError(f"校验对象失败: {e}")
            # return False
    
    async def _reset_object(self, obj: T):
        _logger.DEBUG(f'重置对象状态 = {obj}')
        """重置对象状态"""
        if self._reset_func:
            try:
                if asyncio.iscoroutinefunction(self._reset_func):
                    await self._reset_func(obj)
                else:                    
                    self._reset_func(obj)
            except Exception as e:
                # _logger.ERROR(f"重归对象失败: {e}")
                raise ValueError(f"重归对象失败: {e}")
    
    @asynccontextmanager
    async def acquire(self, timeout: Optional[float] = None) -> T:
        """
        获取对象的异步上下文管理器
        
        Args:
            timeout: 获取超时时间（秒），None表示无限等待
            
        Yields:
            池中的对象
            
        Raises:
            asyncio.TimeoutError: 超时未获取到对象
            RuntimeError: 对象池已关闭
        """
        if self._closed:
            raise RuntimeError("对象池已经关闭")
        
        taskno = asyncio.current_task().get_name()
        try:
            _logger.DEBUG(f'{taskno} 开始获取{timeout}')            
            obj = await self._acquire(timeout)            
            _logger.DEBUG(f'{taskno} 获取对象{obj}')
        except Exception as e:
            _logger.DEBUG(f'{taskno} 获取对象失败,{e}')
            raise e
                        
        try:
            yield obj        
        finally:
            await self._release(obj)
            # 避免连续调用长期占用
            await asyncio.sleep(0.00000001)
    
    async def _acquire(self, timeout: Optional[float] = None) -> T:
        """获取对象的核心逻辑"""
        """获取对象的核心逻辑"""
        if self._state in (PoolState.CLOSING, PoolState.CLOSED):
            raise RuntimeError("对象池已经关闭")
        
        start_time = time.monotonic()
        waited = False
        try:
            async with self._condition:
                # 等待直到有可用对象或可以创建新对象
                while True:                
                    if self._state in (PoolState.CLOSING, PoolState.CLOSED):
                        raise RuntimeError("对象池已经关闭")
                            
                    # if self._closed:
                    #     raise RuntimeError("对象池已经关闭")
                    
                    # 尝试从可用队列获取对象
                    if not self._available_objects.empty():
                        try:
                            obj = self._available_objects.get_nowait()
                            if await self._validate_object(obj):
                                get_time = time.monotonic()
                                self._in_use_objects[obj]=get_time
                                self._stats['acquired'] += 1
                                
                                # 更新峰值使用统计
                                current_usage = len(self._in_use_objects)
                                if current_usage > self._stats['peak_usage']:
                                    self._stats['peak_usage'] = current_usage
                                
                                return obj
                            else:
                                # 对象无效，销毁并继续
                                await self._destroy_object(obj)
                                self._stats['validation_failed'] += 1
                                continue
                        except asyncio.QueueEmpty:
                            pass
                        except Exception as e:
                            _logger.WARN(f'尝试从可用队列获取对象出错{e}')
                            raise e
                    
                    # 检查是否可以创建新对象
                    total_objects = len(self._in_use_objects) + self._available_objects.qsize()
                    if total_objects < self._max_size:
                        obj = await self._create_object()
                        get_time = time.monotonic()
                        self._in_use_objects[obj]=get_time
                        self._stats['acquired'] += 1
                        
                        # 更新峰值使用统计
                        current_usage = len(self._in_use_objects)
                        if current_usage > self._stats['peak_usage']:
                            self._stats['peak_usage'] = current_usage
                            
                        return obj
                    
                    waited = True
                    # 等待对象可用
                    if timeout is not None:
                        remaining = timeout - (time.monotonic() - start_time)
                        if remaining <= 0:
                            raise asyncio.TimeoutError("等待对象超时")
                        
                        try:
                            await asyncio.wait_for(self._condition.wait(), timeout=remaining)
                        except asyncio.TimeoutError:
                            raise asyncio.TimeoutError("等待对象超时")
                    else:
                        await self._condition.wait()
        finally:
            if waited:
                self._stats['wait_count'] += 1
                waited_time = time.monotonic() - start_time
                self._stats['wait_time_total'] += waited_time
                
        
    
    async def _release(self, obj: T):
        """归还对象的核心逻辑"""
        if obj not in self._in_use_objects:
            return  # 对象不在使用中
        
        self._in_use_objects.pop(obj)
        self._stats['released'] += 1
        
        # 如果池正在关闭或已关闭，直接销毁对象
        if self._state in (PoolState.CLOSING, PoolState.CLOSED):
            await self._destroy_object(obj)
            return
        
        # 决定是放回池中还是销毁
        current_idle = self._available_objects.qsize()
        # total_objects = len(self._in_use_objects) + current_idle
        total_objects = len(self._in_use_objects) + current_idle
        if current_idle < self._max_idle and total_objects < self._max_size and await self._validate_object(obj):
            # 重置对象状态
            await self._reset_object(obj)
            await self._available_objects.put(obj)
        else:
            await self._destroy_object(obj)
        
        # 通知等待的协程
        async with self._condition:
            self._condition.notify()
    
    def is_closed(self):
        return self._closed
    
    async def close(self, timeout: Optional[float] = 30.0):
        async with self._lock:            
            """关闭对象池，销毁所有对象"""
            if self._state in (PoolState.CLOSING, PoolState.CLOSED):
                return
            
            self._state = PoolState.CLOSING            
            self._closed = True
            
            # 第一步：等待所有已借出对象被归还（带超时）
            start_time = time.monotonic()
            while self._in_use_objects and timeout is not None:
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    _logger.WARN(f"等待已借出{len(self._in_use_objects)}个对象没有归还，已经超时，等待强制关闭")
                    break
                
                remaining = timeout - elapsed
                _logger.WARN(f"等待已借出{len(self._in_use_objects)}个对象没有归还, {remaining:.1f}秒后将超时")
                await asyncio.sleep(0.5)
                
                
            # 第二步：强制销毁所有剩余对象
            if self._in_use_objects:
                self._stats['leaked_objects'] = len(self._in_use_objects)                
                _logger.WARN(f"等待已借出{len(self._in_use_objects)}个对象未被归还，已经超时，进行强制关闭")
                # 记录泄漏对象的详细信息
                for obj, info in self._in_use_objects.items():
                    _logger.WARN(f"已借出对象: {obj}, 已经借出时间{time.time() - info:.1f}秒，进行强制关闭")
                    # 强制销毁所有使用中的对象
                    await self._destroy_object_safe(obj)                
                _logger.WARN(f"已借出{len(self._in_use_objects)}个对象未被归还，已经强制关闭")
                self._in_use_objects.clear()                
            else:
                _logger.WARN("已借出对象已经全部关闭")
            
            # 销毁所有可用对象
            while not self._available_objects.empty():
                try:
                    obj = self._available_objects.get_nowait()
                    # 销毁所有可用对象
                    _logger.WARN(f"可使用对象:{obj}，进行关闭")
                    await self._destroy_object_safe(obj)
                except asyncio.QueueEmpty:
                    break
            _logger.WARN("可使用对象已经全部关闭")
            
            # 通知所有等待的协程
            async with self._condition:
                self._condition.notify_all()
            
            self._state = PoolState.CLOSED
            _logger.DEBUG('关闭对象池，销毁所有对象')
            
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self._stats.copy()
        stats.update({
            'available_count': self._available_objects.qsize(),
            'in_use_count': len(self._in_use_objects),
            'total_objects': self._available_objects.qsize() + len(self._in_use_objects),
            'closed': self._closed,
            'initialized': self._initialized,
            'state':self._state
        })
        
        # 计算平均等待时间
        if stats['wait_count'] > 0:
            stats['avg_wait_time'] = stats['wait_time_total'] / stats['wait_count']
        else:
            stats['avg_wait_time'] = 0.0
            
        return stats
    
    async def __aenter__(self) -> 'ObjectPool':
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

class ABCObjectPool(ABC, ObjectPool[T]):
    @abstractmethod
    def create_one(self, **kargs):...
    
    @abstractmethod
    def validation_one(self, obj: T):...
    
    @abstractmethod
    def destory_one(self, obj: T):...
    
    @abstractmethod
    def reset_one(self, obj: T):...
    
    def __init__(self, max_size = 10, min_idle = 1, max_idle = 5, **kargs):
        create_factory = self.create_one        
        validation_func = self.validation_one
        destroy_func = self.destory_one
        reset_func = self.reset_one
        
        # _logger.DEBUG(f'create_factory={create_factory} validation_func={validation_func} destroy_func={destroy_func} reset_func={reset_func}')
        
        super().__init__(create_factory, kargs, max_size, min_idle, max_idle, validation_func, destroy_func, reset_func)

if __name__ == "__main__":        
    
    class Object:
        def __init__(self, start_time):
            self.start_time = start_time
        def __repr__(self):
            return f'start_time={self.start_time}'
    
    class DemoObjectPool(ABCObjectPool[Object]):
        def create_one(self, **kargs)->str:
            start_time = time.monotonic()
            obj = Object(start_time)            
            _logger.DEBUG(f'进行create_one={obj}')
            time.sleep(0.001)
            return obj
        
        def validation_one(self, obj: Object):
            _logger.DEBUG(f'进行validation_one={obj}')
            return True
        
        def reset_one(self, obj: Object):
            _logger.DEBUG(f'进行reset_one={obj}')
            
        def destory_one(self, obj: Object):
            _logger.DEBUG(f'进行destory_one={obj}')            

    demo = DemoObjectPool(max_size=5, max_idle=2, min_idle=1)
    
    async def testPool(no:str):
        _logger.DEBUG(f'开始 {no}')
        n = 4
        try:
            async with demo.acquire() as obj:
                _logger.DEBUG(f'{no}: 第一次获取值={obj}, 休眠{n}秒')
                await asyncio.sleep(n)
                
            _logger.DEBUG(f'[1]{asyncio.current_task().get_name()} : {demo.get_stats()}')
                
            async with demo.acquire() as obj:
                _logger.DEBUG(f'{no}: 第二次获取值={obj}, 休眠{n}秒')
                await asyncio.sleep(n)
                
            _logger.DEBUG(f'[2]{asyncio.current_task().get_name()} : {demo.get_stats()}')
        except Exception as e:
            _logger.DEBUG(f'testpool 错误 {e}')
            raise e
    
    async def main():
        await demo.initialize()
        n = 10
        for i in range(n):            
            asyncio.get_event_loop().create_task(testPool(f'No-{i+1}',), name=f'WorkTask-{i+1}')
        
        # asyncio.get_event_loop().create_task(print_info())
        # all_task = asyncio.all_tasks(asyncio.get_event_loop())
        # _logger.DEBUG(f'111 {asyncio.get_event_loop()}={all_task}')
        # await asyncio.sleep(1)
        
        # 安全关闭
        await await_loop_complete(None,None,[demo.close()])
        
        #测试直接关闭
        # asyncio.get_event_loop().create_task(demo.close())
        # await await_loop_complete()
        # _logger.DEBUG('开始关闭====================')        
        # await demo.close()
        
        
        
    asyncio.run(main())
    # asyncio.run(testPool('No-1'))
                        
        
        
        