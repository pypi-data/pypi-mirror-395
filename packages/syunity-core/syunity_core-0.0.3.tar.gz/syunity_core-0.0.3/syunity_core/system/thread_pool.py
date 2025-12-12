"""
    在 Python 现代工程（特别是涉及 Web、IoT、数据库混合的场景）中，“主流且先进” 的线程管理方式已经不再是简单地随处写 threading.Thread(target=...).start()。

    现代做法的核心理念是 “集中托管 (Centralized Management)” 和 “优雅退出 (Graceful Shutdown)”。

    你需要一个 线程管理器 (ThreadManager)，它应该具备以下核心功能：

    异常隔离：某个线程（如 MQTT 消费）崩了，不能让主进程挂掉，且必须记录详细堆栈日志。
    生命周期管理：统一启动、统一停止。
    信号处理：捕获 Ctrl+C (SIGINT) 或 kill (SIGTERM)，通知所有子线程安全结束（而不是直接杀掉导致数据损坏）。
    状态监测：随时可以知道哪些线程还在活，哪些挂了。
    停止机制：向死循环的线程（如 while True）发送停止信号。

"""

import threading
import signal
import time
import inspect
import traceback
from typing import Dict, Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor, Future
from syunity_core.system.logger import logger


class ServiceThread(threading.Thread):
    """
    封装后的服务线程类
    """

    def __init__(self, name: str, target: Callable, args: tuple = (), kwargs: dict = None, daemon: bool = False):
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.args = args
        self.kwargs = kwargs or {}
        self._stop_event = threading.Event()
        self._is_running = False

    def stop(self):
        """发出停止信号"""
        self._stop_event.set()

    def stopped(self) -> bool:
        """检查是否收到停止信号"""
        return self._stop_event.is_set()

    def run(self):
        self._is_running = True
        logger.info(f"🔄 [Thread: {self.name}] Started")
        try:
            # 智能参数注入: 如果目标函数需要 stop_event，则自动注入
            sig = inspect.signature(self.target)
            if 'stop_event' in sig.parameters:
                self.kwargs['stop_event'] = self._stop_event

            self.target(*self.args, **self.kwargs)

        except Exception as e:
            logger.critical(f"❌ [Thread: {self.name}] Crashed: {e}")
            logger.exception(e)
        finally:
            self._is_running = False
            logger.info(f"⏹ [Thread: {self.name}] Stopped")


class ThreadManager:
    """
    全局线程管理器 (单例模式)
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        self.services: Dict[str, ServiceThread] = {}
        # 线程池：用于短任务
        self.executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="Worker")
        self.shutting_down = False

        # 注册信号
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def register(self, name: str, target: Callable, args: tuple = (), kwargs: dict = None, daemon: bool = False):
        """注册并启动长驻服务"""
        if name in self.services and self.services[name].is_alive():
            logger.warning(f"⚠️ Service [{name}] is already running.")
            return

        t = ServiceThread(name, target, args, kwargs, daemon)
        self.services[name] = t
        t.start()
        logger.debug(f"✅ Service [{name}] registered and started.")

    def restart_service(self, name: str):
        """重启某个服务 (如果挂了或者需要重置)"""
        if name not in self.services:
            logger.error(f"❌ Cannot restart unknown service: {name}")
            return

        old_thread = self.services[name]
        logger.warning(f"🔄 Restarting service [{name}]...")

        # 1. 先停止旧的
        if old_thread.is_alive():
            old_thread.stop()
            old_thread.join(timeout=3.0)

        # 2. 创建新的 (复用旧参数)
        self.register(
            name=name,
            target=old_thread.target,
            args=old_thread.args,
            kwargs=old_thread.kwargs,
            daemon=old_thread.daemon
        )

    def submit_task(self, func: Callable, *args, success_cb: Callable = None, error_cb: Callable = None, **kwargs):
        """
        提交临时任务
        :param func: 目标函数
        :param success_cb: 成功回调 func(result)
        :param error_cb: 失败回调 func(exception)
        """
        if self.shutting_down:
            logger.warning("⚠️ System shutting down, task rejected.")
            return

        future = self.executor.submit(func, *args, **kwargs)

        # 使用闭包处理回调
        def _callback(fut: Future):
            try:
                result = fut.result()
                if success_cb:
                    success_cb(result)
            except Exception as e:
                logger.error(f"❌ Async task failed: {e}")
                logger.exception(e)  # 打印完整堆栈以便调试
                if error_cb:
                    error_cb(e)

        future.add_done_callback(_callback)

    def get_status(self):
        status = {}
        for name, t in self.services.items():
            status[name] = "Running" if t.is_alive() else "Stopped"
        return status

    def stop_all(self):
        self.shutting_down = True
        logger.warning("🛑 Stopping all services...")

        for name, t in self.services.items():
            if t.is_alive():
                t.stop()

        self.executor.shutdown(wait=False)

        for name, t in self.services.items():
            if t.is_alive():
                t.join(timeout=1.0)

        logger.success("👋 All services stopped.")

    def _signal_handler(self, signum, frame):
        sig_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"
        logger.warning(f"📥 Received signal: {sig_name}. Shutdown initiated.")
        self.stop_all()
        import sys
        sys.exit(0)


# 导出单例
tm = ThreadManager()
