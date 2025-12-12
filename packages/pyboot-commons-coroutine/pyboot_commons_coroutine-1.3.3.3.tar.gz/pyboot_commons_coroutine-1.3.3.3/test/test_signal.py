import asyncio
import signal
import os
from pyboot.commons.coroutine.tools import cancel_loop_tasks

async def main():
    # 1. 主线程事件循环
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()

    def _handler(signum, frame):
        signame = signal.Signals(signum).name
        print(f"\n收到 {signame}，准备优雅退出…")        
        loop.call_soon_threadsafe(stop.set)   # 保证线程安全

    # 2. 注册两种信号
    signal.signal(signal.SIGINT, _handler)
    if os.name != "nt":               # Windows 没有 SIGTERM，忽略也不报错
        signal.signal(signal.SIGTERM, _handler)

    # 3. 业务协程
    async def job(n):
        try:
            while True:
                print(f"job{n} running")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print(f"job{n} cancelled")
            raise

    tasks = [asyncio.create_task(job(i)) for i in range(2)]

    # 4. 等待退出信号
    await stop.wait()

    # 5. 取消并等待收尾
    await cancel_loop_tasks()
    
    # for t in tasks:
    #     t.cancel()
    # await asyncio.gather(*tasks, return_exceptions=True)
    print("全部任务已取消，进程退出")

if __name__ == "__main__":
    asyncio.run(main())