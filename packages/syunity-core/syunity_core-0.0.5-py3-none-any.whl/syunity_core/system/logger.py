import sys, logging
from pathlib import Path
from typing import Union
from loguru import logger as _logger

logger = _logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__: frame, depth = frame.f_back, depth + 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class LogManager:
    @staticmethod
    def setup(service_name: str = "syunity", log_dir: Union[str, Path] = "logs", level: str = "INFO",
              rotation: str = "10 MB", retention: str = "20 days", console: bool = True, json_format: bool = False):
        logger.remove()
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> | <magenta>PID:{process}</magenta> - <level>{message}</level>"

        if console:
            logger.add(sys.stderr, level=level, format=fmt, enqueue=True, backtrace=True, diagnose=True)

        logger.add(str(log_path / f"{service_name}.log"), rotation=rotation, retention=retention, level=level,
                   encoding="utf-8", enqueue=True, compression="zip", serialize=json_format,
                   format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}" if not json_format else "{message}")

    @staticmethod
    def intercept_standard_logging(modules: list = None):
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        for mod in (modules or []):
            l = logging.getLogger(mod)
            l.handlers = [InterceptHandler()]
            l.propagate = False


if not logger._core.handlers: logger.add(sys.stderr, level="INFO")


"""

这个新版方案强在哪里？
解耦 (Decoupling):

不再依赖 setting.py。所有的配置（路径、大小、名字）都通过 setup 函数的参数传递。
用户使用时，可以在他的 main.py 里决定日志存哪里，而不是被库写死。
拦截能力 (Interception):

增加了 InterceptHandler 类。
这是核心库设计的关键。当你以后集成了 Sanic 或者 Paho-MQTT，它们内部用的是 logging.getLogger('sanic')。如果不拦截，你的控制台会有两种格式的日志混杂。使用了这个类，所有的日志统一由 Loguru 管理，格式整齐划一。
性能 (Performance):

enqueue=True: 你的旧代码在写文件时是同步的，I/O 慢会卡住主线程。新代码使用后台队列写入，不阻塞业务逻辑，这对高并发 Web 服务（Sanic）和高频 MQTT 消息处理至关重要。
功能增强:

compression="zip": 历史日志自动压缩，节省服务器空间。
backtrace=True: 报错时能看到变量的值，而不只是行号。
rotation="10 MB" / retention="20 days": 语义更清晰。
如何在工程中使用？
场景 1：作为库的开发者（在 syunity-core 内部使用）

python
# 在 syunity_core/network/mqttcore.py 中
from syunity_core.system.logger import logger

class MqttBus:
    def connect(self):
        try:
            # ... 连接逻辑
            logger.info("MQTT Connected successfully.")
        except Exception as e:
            logger.exception("MQTT Connection failed") # 自动打印漂亮的堆栈
场景 2：作为用户（安装了你的包后使用）

用户在他的项目入口文件（例如 main.py）中初始化一次即可：

python
from syunity_core.system.logger import LogManager, logger
from syunity_core.web.sanic_server import create_app

# 1. 初始化配置 (指定他的项目名和路径)
LogManager.setup(
    service_name="my_iot_project", 
    log_dir="./my_logs", 
    level="DEBUG",
    rotation="50 MB"
)

# 2. 拦截第三方库日志 (可选，但推荐)
LogManager.intercept_standard_logging(["sanic", "paho.mqtt.client"])

# 3. 开始使用
logger.info("项目启动...")

"""