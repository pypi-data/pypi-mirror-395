import asyncio
import threading
import time
from dataclasses import dataclass
from typing import Optional, List, Callable
from sanic import Sanic, response
from functools import partial

# 假设这是你的日志模块
try:
    from syunity_core.system.logger import logger
except ImportError:
    import logging

    logger = logging.getLogger("HttpServer")
    logging.basicConfig(level=logging.INFO)


# ==========================================
# 配置类
# ==========================================
@dataclass
class HttpServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    access_log: bool = True
    workers: int = 1
    app_name: str = "SyUnityServer"
    cors_enabled: bool = True
    cors_origins: str = "*"


# ==========================================
# 核心封装类
# ==========================================
class HttpServer:
    """
    Sanic HTTP 服务的现代化封装 (Asyncio Loop 模式)
    完全避开 Sanic 内置的信号处理，确保在子线程稳定运行
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[HttpServerConfig] = None):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.config = config or HttpServerConfig()
        self.app = Sanic(self.config.app_name)
        self._setup_config()

        # 运行时状态
        self._server_thread = None
        self._loop = None
        self._server_coroutine = None
        self.is_running = False

        self._initialized = True

    def _setup_config(self):
        """应用基础配置"""
        self.app.config.ACCESS_LOG = self.config.access_log
        self.app.config.CORS_ORIGINS = self.config.cors_origins

        if self.config.cors_enabled:
            self._enable_cors()

        # 注册生命周期钩子
        self.app.register_listener(self._after_server_start, "after_server_start")
        self.app.register_listener(self._before_server_stop, "before_server_stop")

    def _enable_cors(self):
        @self.app.middleware("response")
        async def cors_middleware(request, response):
            if not response: return
            response.headers["Access-Control-Allow-Origin"] = self.config.cors_origins
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

        @self.app.middleware("request")
        async def handle_options(request):
            if request.method == "OPTIONS":
                return response.empty()

    async def _after_server_start(self, app, loop):
        self.is_running = True
        logger.info(f"🚀 HTTP Server started at http://{self.config.host}:{self.config.port}")

    async def _before_server_stop(self, app, loop):
        self.is_running = False
        logger.info("🛑 HTTP Server is stopping...")

    # ==========================================
    # 公共 API
    # ==========================================

    def add_route(self, handler: Callable, uri: str, methods: List[str] = ["GET"], name: str = None):
        self.app.add_route(handler, uri, methods=methods, name=name)
        logger.info(f"Registered route: {methods} {uri}")

    def register_blueprint(self, blueprint, url_prefix: str = None):
        if url_prefix:
            blueprint.url_prefix = url_prefix
        self.app.blueprint(blueprint)
        logger.info(f"Registered blueprint: {blueprint.name} at {url_prefix or '/'}")

    def start(self, blocking: bool = True):
        """启动服务器"""
        if self.is_running:
            logger.warning("Server is already running.")
            return

        if blocking:
            # 主线程阻塞运行：可以直接用 Sanic 的 run，因为主线程支持信号
            # 这里为了统一逻辑，也可以用 loop，但为了 Ctrl+C 有效，使用 run 比较方便
            self.app.run(
                host=self.config.host,
                port=self.config.port,
                debug=self.config.debug,
                access_log=self.config.access_log,
                workers=1,  # Windows 下建议单 worker
                single_process=True
            )
        else:
            # 子线程后台运行：必须使用 asyncio 手动控制
            self._server_thread = threading.Thread(
                target=self._run_async_loop,
                daemon=True,
                name="SanicServerThread"
            )
            self._server_thread.start()
            self._wait_for_start()

    def _run_async_loop(self):
        """在子线程中建立全新的 Event Loop"""
        # 1. 创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop

        # 2. 创建 Server 对象 (使用 low-level API create_server)
        # 这会绕过 Sanic 的信号注册逻辑
        serve_coro = self.app.create_server(
            host=self.config.host,
            port=self.config.port,
            return_asyncio_server=True,
            access_log=self.config.access_log
        )

        # 3. 触发 Sanic 生命周期事件 (before_server_start, etc.)
        # 这一点很重要，否则蓝图可能不生效
        loop.run_until_complete(self.app._startup())

        # 4. 启动 Server
        try:
            self._server_coroutine = loop.run_until_complete(serve_coro)

            # 手动触发 after_start
            loop.run_until_complete(self.app._server_event("after", "start"))

            # 5. 永久运行 Loop
            loop.run_forever()

        except Exception as e:
            logger.error(f"Server loop error: {e}")
        finally:
            loop.close()

    def _wait_for_start(self, timeout=5):
        """轮询等待启动完成"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_running:
                return
            time.sleep(0.1)

    def stop(self):
        """停止服务器"""
        if not self.is_running:
            return

        logger.info("Stopping HTTP Server...")

        if self._loop:
            # 在 loop 线程中执行关闭操作
            async def _stop_coro():
                # 触发停止事件
                await self.app._server_event("before", "stop")

                # 关闭 asyncio server
                if self._server_coroutine:
                    self._server_coroutine.close()
                    await self._server_coroutine.wait_closed()

                await self.app._server_event("after", "stop")

                # 停止 loop
                self._loop.stop()

            # 线程安全地调度关闭任务
            asyncio.run_coroutine_threadsafe(_stop_coro(), self._loop)

    def get_app(self) -> Sanic:
        return self.app


def get_http_server() -> HttpServer:
    return HttpServer()