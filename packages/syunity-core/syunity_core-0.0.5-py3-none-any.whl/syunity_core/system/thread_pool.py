import threading, signal, inspect, sys
from concurrent.futures import ThreadPoolExecutor
from syunity_core.system.logger import logger

class ServiceThread(threading.Thread):
    """封装的服务线程，支持参数自动注入和优雅停止"""
    def __init__(self, name: str, target, args=(), kwargs=None, daemon=False):
        super().__init__(name=name, daemon=daemon)
        self.target, self.args, self.kwargs = target, args, kwargs or {}
        self._stop_event, self._is_running = threading.Event(), False

    def stop(self): self._stop_event.set()
    def stopped(self) -> bool: return self._stop_event.is_set()

    def run(self):
        self._is_running = True
        logger.info(f"🔄 [Thread: {self.name}] Started")
        try:
            # 如果目标函数有 stop_event 参数，自动注入
            if 'stop_event' in inspect.signature(self.target).parameters: self.kwargs['stop_event'] = self._stop_event
            self.target(*self.args, **self.kwargs)
        except Exception as e: logger.critical(f"❌ [Thread: {self.name}] Crashed: {e}"); logger.exception(e)
        finally: self._is_running = False; logger.info(f"⏹ [Thread: {self.name}] Stopped")

class ThreadManager:
    """全局线程管理器(单例)"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance: cls._instance = super(ThreadManager, cls).__new__(cls); cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        self.services, self.shutting_down = {}, False
        self.executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="Worker")
        for s in (signal.SIGINT, signal.SIGTERM): signal.signal(s, self._signal_handler)

    def register(self, name: str, target, args=(), kwargs=None, daemon=False):
        """注册并启动长驻服务"""
        if name in self.services and self.services[name].is_alive(): return logger.warning(f"⚠️ Service [{name}] running.")
        t = ServiceThread(name, target, args, kwargs, daemon)
        self.services[name] = t; t.start(); logger.debug(f"✅ Service [{name}] registered.")

    def restart_service(self, name: str):
        """重启指定服务"""
        if name not in self.services: return logger.error(f"❌ Unknown service: {name}")
        old = self.services[name]; logger.warning(f"🔄 Restarting [{name}]...")
        if old.is_alive(): old.stop(); old.join(3.0)
        self.register(name, old.target, old.args, old.kwargs, old.daemon)

    def submit_task(self, func, *args, success_cb=None, error_cb=None, **kwargs):
        """提交临时任务到线程池"""
        if self.shutting_down: return logger.warning("⚠️ System shutting down, task rejected.")
        def _cb(fut):
            try: (success_cb(fut.result()) if success_cb else None)
            except Exception as e: logger.error(f"❌ Task failed: {e}"); logger.exception(e); (error_cb(e) if error_cb else None)
        self.executor.submit(func, *args, **kwargs).add_done_callback(_cb)

    def get_status(self): return {n: "Running" if t.is_alive() else "Stopped" for n, t in self.services.items()}

    def stop_all(self):
        """停止所有服务和线程池"""
        self.shutting_down = True; logger.warning("🛑 Stopping all services...")
        for t in self.services.values(): t.stop() if t.is_alive() else None
        self.executor.shutdown(wait=False)
        for t in self.services.values(): t.join(1.0) if t.is_alive() else None
        logger.success("👋 All services stopped.")

    def _signal_handler(self, signum, frame):
        logger.warning(f"📥 Signal {signum}. Shutdown."); self.stop_all(); sys.exit(0)

tm = ThreadManager()