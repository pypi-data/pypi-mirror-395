import asyncio
import typing
import signal
import inspect
from pyboot.commons.utils.log import Logger
from pyboot.commons.utils.utils import isWin
from typing import Callable
import threading
import sys
import multiprocessing

_logger = Logger('dataflow.utils.coroutine.tools')

EOF = ''

# 线程版本 有个问题，就是线程只能在父线程退出才能作为Daemon才能安全退出
class AsyncStdin:
    def __init__(self, loop: asyncio.AbstractEventLoop = None):                        
        if loop is None:
            loop, _ = getOrCreate_eventloop()
        
        self._loop = loop
        self._q: asyncio.Queue[str] = asyncio.Queue()
        self._thr = threading.Thread(target=self._reader, daemon=True, name='AsyncStdin-Thread')
        self._thr.start()
        
    def _reader(self):
        try:
            while True:
                line = sys.stdin.readline()
                # _logger.DEBUG(f'stdin读取{line}')
                if not line:        # Ctrl-D / EOF
                    asyncio.run_coroutine_threadsafe(self._q.put(EOF), self._loop)
                    break
                # 非阻塞放入
                asyncio.run_coroutine_threadsafe(self._q.put(line), self._loop)
        except OSError:
            pass                    # 解释器关闭时正常退出
        
    async def readline(self) -> str:
        """可取消的 readline"""
        return await self._q.get()
    
    def close(self):
        # 守护线程无需显式 join；进程退出时自动结束        
        pass


# 进程版本 有个问题，stdin被子进程监听，所有输入都不能直接別父进程监听，包括信号Ctrl + C被子进程监听， 需要根据父进程进行扩展
class AsyncStdinProcess:
    @staticmethod    
    def readline_worker(q_out: multiprocessing.Queue, stdin_fd):
        """子进程：只干一件事——阻塞读 stdin，读到就丢队列"""
        # 在子进程里重新打开 stdin
        # Windows 的 multiprocessing.spawn 会把子进程的 标准句柄 重定向到 NUL（等同于 /dev/null），除非显式传入 stdin=sys.stdin。
        # 在window系统，控制台没有任何输入 一运行，Readline就读到空(EOF), 除非显式传入 stdin=sys.stdin。
        _stdin = open(stdin_fd, 'r', encoding='utf-8', closefd=False)
        
        try:
            # _logger.DEBUG('开始启动Readline')  
            while True:
                line = _stdin.readline()
                # _logger.DEBUG(f'读取到:{line}')
                if not line:  
                    q_out.put(EOF)          # EOF 标记
                    break
                q_out.put(line)
        except KeyboardInterrupt:
            _stdin.close()
            # pass  
                
    def __init__(self, loop: asyncio.AbstractEventLoop = None):                        
        if loop is None:
            loop, _ = getOrCreate_eventloop()
        self._loop:asyncio.AbstractEventLoop = loop        
        self._q = multiprocessing.Queue()             
        self._proc = multiprocessing.Process(target=AsyncStdinProcess.readline_worker, args=(self._q, sys.stdin.fileno()), daemon=True)
        _logger.DEBUG(f'开始创建通道Queue并绑定到子进程{self._q}，启动子进程{self._proc}')
        self._proc.start()
        
    async def readline(self) -> str:
        """异步、可取消、可超时的 readline"""        
        return await self._loop.run_in_executor(None, self._q.get)   # 阻塞的是 Queue.get，可线程取消
    
    def close(self):
        _logger.DEBUG(f'关闭子进程 {self._proc.is_alive()}')
        if self._proc.is_alive():
            self._proc.terminate()  # 立刻把阻塞在 readline 的子进程杀掉
            self._proc.join(timeout=1)


# 可中断 sleep -----------------------------------------------------------
async def sleep(sec: float, stop: asyncio.Event | None = None) -> None:
    """支持外部事件立即中断的 sleep"""
    if stop is None:
        await asyncio.sleep(sec)
    else:
        try:
            await asyncio.wait_for(stop.wait(), timeout=sec)
        except asyncio.TimeoutError:
            pass
        
# 限制并发量的 gather -----------------------------------------------------
async def gather_with_sem(
    coros: typing.Iterable[typing.Awaitable],
    max_concurrent: int = 10,
    *,
    return_exceptions: bool = False,
) -> typing.Any:
    """asyncio.gather 的带并发上限版本"""
    sem = asyncio.Semaphore(max_concurrent)

    async def _wrap(coro: typing.Awaitable) -> typing.Any:
        async with sem:
            return await coro

    return await asyncio.gather(
        *(_wrap(c) for c in coros), return_exceptions=return_exceptions
    )
      
        
#  超时自动取消的 gather ---------------------------------------------------
async def gather_with_timeout(
    coros: typing.Iterable[typing.Awaitable],
    timeout: float,
    *,
    return_exceptions: bool = False,
) -> typing.Any:
    return await asyncio.wait_for(
        asyncio.gather(*coros, return_exceptions=return_exceptions), timeout
    )


#  TCP 端口探活（协程版） -------------------------------------------------
async def tcp_ping(host: str, port: int, timeout: float = 3) -> bool:
    """True=端口通，False=端口不通"""
    fut = asyncio.open_connection(host, port)
    try:
        _, writer = await asyncio.wait_for(fut, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (OSError, asyncio.TimeoutError):
        return False


# 重试装饰器 -------------------------------------------------------------
def retry(
    *,
    attempts: int = 3,
    delay: float = 1,
    backoff: float = 2,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    def decorator(func: typing.Callable) -> typing.Callable:
        async def wrapper(*args, **kwargs):
            nonlocal delay
            for _ in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    await asyncio.sleep(delay)
                    delay *= backoff
                    raise e
        return wrapper

    return decorator


# 后台定时器 --------------------------------------------------------------
def every(
    interval: float,
    *,
    stop: asyncio.Event | None = None,
):
    """异步定时器装饰器，支持外部事件停止"""

    def decorator(func: typing.Callable) -> typing.Callable:
        async def _wrapper():
            while (stop is None) or (not stop.is_set()):
                await func()
                await sleep(interval, stop)

        return _wrapper

    return decorator


# 优雅关闭辅助 -----------------------------------------------------------
def install_stop_signals(stop: asyncio.Event) -> None:
    """Ctrl-C / SIGTERM 一键设置停止事件"""
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())


# 主程入口封装 -----------------------------------------------------------
def run(coro: typing.Awaitable) -> typing.Any:
    """asyncio.run 的简易别名"""
    return asyncio.run(coro)

def getOrCreate_eventloop()->tuple[asyncio.AbstractEventLoop,bool]:
    try:
        _loop = asyncio.get_event_loop()
        return _loop, False
    except RuntimeError:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
        return _loop, True

def is_coroutine_obj(coro)->bool:
    return inspect.iscoroutine(coro)

def is_coroutine_func(func:typing.Callable)->bool:
    return inspect.iscoroutinefunction(func)

def create_coroutine(func:typing.Callable, *args, **kw):
    if not is_coroutine_func(func):
        raise ValueError(f"a coroutine func was expected, got {func!r} not, 需要定义async def")
    
    """接收一个协程工厂函数，返回协程对象并调度"""
    coro = func(*args, **kw)   # 这里才真正产生协程对象    
    # return asyncio.create_task(coro)
    return coro

def run_coroutine_now(coro, loop:asyncio.AbstractEventLoop=None):
    if not is_coroutine_obj(coro):
        raise ValueError(f"a coroutine was expected, got {coro!r}")
    _loop = loop
    if _loop is None:
        _loop, _ = getOrCreate_eventloop()        
    return _loop.create_task(coro)

def run_coroutine_sync(coro, loop:asyncio.AbstractEventLoop=None)->any:
    if not is_coroutine_obj(coro):
        raise ValueError(f"a coroutine was expected, got {coro!r}")
    _loop = loop
    if _loop is None:
        _loop, _ = getOrCreate_eventloop()
        
    return _loop.run_until_complete(coro)
    
# 事件循环里直接调用同步方法(会阻塞事件循环，例如time.sleep)
def run_synctask(func:typing.Callable, *args)->any:
    if not callable(func):
        raise ValueError(f"a callable function was expected, got {func!r}")
    # 直接调用同步方法 - 会阻塞事件循环！
    # return func(*args, **kw)
    
    if is_coroutine_func(func):
        raise ValueError(f"a non coroutine callable function was expected, got {func!r}")
    
    # 更好的方式：使用线程池执行同步方法
    # 在事件循环中
    loop = asyncio.get_event_loop()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     result = await loop.run_in_executor(executor, func, *args)
    #     return result
    return loop.run_in_executor(None, func, *args)

async def await_loop_complete(loop:asyncio.AbstractEventLoop=None,return_exceptions=True,coros:list=None):
    """等当前循环里所有任务（包括后台）结束"""
    if loop is None:
        loop,_ = getOrCreate_eventloop()    
        
    current = asyncio.current_task(loop)          # 自己这条协程
    all_tasks = asyncio.all_tasks(loop)           # 全集
    all_tasks.discard(current)                # 排除自己
    _logger.DEBUG(f'事件循环器{loop}共有{len(all_tasks)}个协程任务在运行中，{all_tasks}')
    if all_tasks:                             # 还有别人
        await asyncio.gather(*all_tasks, return_exceptions=return_exceptions)
        
    if coros:
        if not isinstance(coros, list):
            coros = [coros]
            
        _logger.DEBUG(f'等待执行{len(coros)}个协程任务在运行中，{coros}')
        return await asyncio.gather(*coros, return_exceptions=return_exceptions)
    # # loop = asyncio.get_running_loop()
    # # 当前这一行本身也是任务，要把自己排除
    # all_tasks = asyncio.all_tasks(loop)
    # # all_tasks = [t.result() for t in all_tasks]    
    # if all_tasks:                       # 可能为空
    #     await asyncio.gather(*all_tasks, return_exceptions=return_exceptions)
    
async def cancel_tasks(tasks:set[asyncio.Task]|list[asyncio.Task], return_exceptions=True,coros:list=None):   
    
    if isinstance(tasks, (set, list)):        
        if isinstance(tasks, list):
            tasks = set(tasks)
        
        current = asyncio.current_task()
        _logger.DEBUG(f'开始取消所有指定任务{tasks}[{len(tasks)}]，当前任务{current.get_name()}, 取消后执行{coros}')
        
        tasks.discard(current)
        
        # 1. 先请求取消
        for task in tasks:
            task.cancel()
          
        _logger.DEBUG(f'事件循环器{asyncio.get_event_loop()}共有{len(tasks)}个协程任务在取消中，{tasks}')
        # 2. 等它们真正退出（取消异常会被gather捕获）
        # if coros:            
        #     if not isinstance(coros, list):
        #         coros = [coros]
        #     _logger.DEBUG(f'等待执行{len(coros)}个协程任务在运行中，{coros}')
        #     for coro in coros:
        #         asyncio.get_event_loop().create_task(coro)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=return_exceptions)
        except Exception as e:
            _logger.ERROR(f'OVER {e}', e)
            
        _logger.DEBUG(f'************{coros}')
        # 不能支持asyncio.run(main())，要不事件循环被Cancel掉了
        if coros:            
            if not isinstance(coros, list):
                coros = [coros]
            _logger.DEBUG(f'等待执行{len(coros)}个协程任务在运行中，{coros}')
            return await asyncio.gather(*coros, return_exceptions=return_exceptions)
    else:
        raise ValueError('task必须是list或者set')
        
            
async def cancel_loop_tasks(loop:asyncio.AbstractEventLoop=None,return_exceptions=True,coros:list=None):
    """等当前循环里所有任务（包括后台）取消"""
    
    if loop is None:
        loop,_ = getOrCreate_eventloop()
        
    _logger.DEBUG(f'开始取消{loop}所有可以运行任务，取消后执行{coros}')
    
    # current = asyncio.current_task(loop)          # 自己这条协程
    all_tasks = asyncio.all_tasks(loop)           # 全集
    
    # all_tasks.discard(current)                # 排除自己
    
    # # 1. 先请求取消
    # for task in all_tasks:
    #     task.cancel()
        
    # # 2. 等它们真正退出（取消异常会被gather捕获）
    # await asyncio.gather(*all_tasks, return_exceptions=return_exceptions)        
    
    # if coros:
    #     _logger.DEBUG(f'等待执行{len(coros)}个协程任务在运行中，{coros}')
    #     return await asyncio.gather(*coros, return_exceptions=return_exceptions)
    return await cancel_tasks(all_tasks, return_exceptions, coros)

async def close_loop(loop:asyncio.AbstractEventLoop=None,return_exceptions=True,coros:list=None):
    """等当前循环里所有任务（包括后台）取消"""
    if loop is None:
        loop,_ = getOrCreate_eventloop()    
    rtn = await cancel_loop_tasks(loop, None, coros)
    try:
        loop.stop()
        return rtn
    finally:
        loop.close()

def _add_signal_handler(sig, callback, loop:asyncio.AbstractEventLoop):
    if callback:
        if isWin:
            signal.signal(sig, callback)
        else:
            loop.add_signal_handler(sig, callback)


class GracefulShutdown:
    def __init__(self, loop:asyncio.AbstractEventLoop, signals:list|tuple|signal.Signals=(signal.SIGINT, signal.SIGTERM), callback:Callable=None, *args, **kargs):
        '''
        loop: 主线程的事件循环器
        signals: 监听的信号量
        callback: gracdefully shutdown的释放资源的回调函数，最好是异步
        *args callback的args参数
        **kargs callback的kargs参数
        '''
        self._STOP_EVENT:asyncio.Event = asyncio.Event()
        if callback and not callable(callback):
            raise ValueError(f'callback必须是一个函数，但是得到{callback}')
        
        self._callback = callback
        self._loop = loop        
        self._signals = signals or (signal.SIGINT, signal.SIGTERM)
        self._args = args
        self._kargs = kargs
        self._emited = False
        self._shutdowning = False
        self._shutdown = False
    
    def emit(self):
        if self._emited:
            raise ValueError('优雅关闭器已经emit，不需要重复emit')
        
        def handler(signum, frame):
            signame = signal.Signals(signum).name
            _logger.DEBUG(f"\n>>>收到{signame} {frame}")
            self._loop.call_soon_threadsafe(self._STOP_EVENT.set)
        
        for s in self._signals:    
            signal.signal(s, handler)
            
        self._emited = True
        
    async def _shutdown_gracefully(self):
        # 1. 等待“停止事件”
        await self._STOP_EVENT.wait()
        self._shutdowning = True
        # 2. 进入 graceful shutdown
        if self._callback:
            _logger.DEBUG(">>> 开始启动优雅关闭.....")
            
            if is_coroutine_func(self._callback):
                await self._callback(*self._args, **self._kargs)
            else:
                self._callback(*self._args, **self._kargs)
                
            _logger.DEBUG(">>> 释放所有资源完成")        
        self._shutdown = True
        
    def start_shutdown_gracefully_await(self):
        self._loop.create_task(self._shutdown_gracefully())   
        
    async def wait_event(self):
        return await self._STOP_EVENT.wait()
    
    def shutdown(self):
        self._loop.call_soon_threadsafe(self._STOP_EVENT.set)
    
    def is_shutdowning(self):
        return self._shutdowning
    
    def is_shutdown(self):
        return self._shutdown
        

# 优雅退出事件循环器：Ctrl-C 
# @deprecated(since="1.3.3.2", removed_in="1.3.3.3", replacement="GracefulShutdown")
def add_shutdown_signal_handler(signals:list|tuple|signal.Signals=(signal.SIGINT, signal.SIGTERM), callback:Callable=None, loop:asyncio.AbstractEventLoop=None):
    if callback:
        if not callable(callback):
            raise ValueError('callback必须是一个可调用对象')
        
    if signals is None:
        signals = (signal.SIGINT, signal.SIGTERM)
    
    if isinstance(signals, signal.Signals):
        signals = [signals]
    
    if loop is None:
        loop,_ = getOrCreate_eventloop()    
            
    def shutdown_wrap(_c, _l):
        def _shutdown_handler_win(s:int, f):
            async def _shutdown(_callback):
                if _callback:
                    _logger.DEBUG(f'开始退出回调函数{_callback}')
                    if is_coroutine_func(_callback):
                        await _callback()
                    elif callable(_callback):
                        _callback()
                                                                        
            _l.create_task(_shutdown(_c))
            
        def _shutdown_handler(s:int, f):
            async def _shutdown(_callback):
                if _callback:                            
                    async def wrap_callback(c):
                        _logger.DEBUG(f'开始退出回调函数{c}')                        
                        if is_coroutine_func(_callback):
                            await _callback()
                        elif callable(_callback):
                            _callback()
                
            _l.create_task(_shutdown(_c))
            
        return _shutdown_handler_win if isWin() else _shutdown_handler            
        
    for sig in signals:
        _add_signal_handler(sig, shutdown_wrap(callback, loop), loop)


if __name__ == "__main__":        
    lock = asyncio.Lock()          # 1. 创建锁

    async def critical(idx):
        async with lock:           # 2. 拿锁（拿不到就挂起）
            print(f'[{idx}] 进入临界区')
            await asyncio.sleep(1) # 3. 模拟耗时
            print(f'[{idx}] 离开临界区')

    # import signal
    # # signal.signal(signal.SIGINT, lambda s,f: _logger.DEBUG('退出程序'))
    # # signal.signal(signal.SIGTERM, lambda s,f: _logger.DEBUG('退出程序'))    
    
    async def print_exit():
        _logger.DEBUG('退出程序11111')   
    
    async def main1():        
        # add_shutdown_signal_handler(None, print_exit)        
        await testReadline()
        # await asyncio.gather(*(critical(i) for i in range(5)))
        # await asyncio.sleep(1)
    
    async def testReadline():
        _stdin = AsyncStdin()
        
        while True:
            line = await _stdin.readline()
            if not line:
                _logger.DEBUG('退出')
                break
            else:
                _logger.DEBUG(f'读到：{line.strip()}')
    
    # asyncio.run(main1())
    
    async def test_shutdown(gf:GracefulShutdown, _stdin):        
        gf.start_shutdown_gracefully_await()        
        try:
            while True:
                line = await _stdin.readline()
                if not line:
                    _logger.DEBUG('退出')                
                    break
                else:
                    _logger.DEBUG(f'读到：{line.strip()}')
        except Exception as e:
            _logger.DEBUG(f'错误{e}')
                
        # while True:
        #     await asyncio.sleep(1)
        #     _logger.DEBUG('休眠1秒')
    
    async def shutdown_handler(_stdin):
        # _stdin.close()        
        _logger.DEBUG('退出程序11111')         
        # await cancel_loop_tasks()
        
    def main():            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  
        _stdin = AsyncStdin()
        gf:GracefulShutdown = GracefulShutdown(loop,None,shutdown_handler, _stdin)
        gf.emit()
        
        loop.run_until_complete(test_shutdown(gf,_stdin))
        
    main()
            

