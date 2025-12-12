import sys
import logging
from pathlib import Path
from typing import Union
from loguru import logger as _logger

# 导出 logger 对象，方便其他模块直接 import logger 使用
logger = _logger


class InterceptHandler(logging.Handler):
    """
    将标准 logging 库产生的日志拦截并转发给 Loguru。
    这对于捕获 Sanic、Paho-MQTT、SQLAlchemy 等第三方库的日志非常关键。
    """

    def emit(self, record):
        # 获取对应的 Loguru 日志等级
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 查找调用者的堆栈深度，确保日志记录的文件名和行号是正确的
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class LogManager:
    """
    日志管理器：负责初始化配置
    """

    @staticmethod
    def setup(
            service_name: str = "syunity",
            log_dir: Union[str, Path] = "logs",
            level: str = "INFO",
            rotation: str = "10 MB",
            retention: str = "20 days",
            console: bool = True,
            json_format: bool = False
    ):
        """
        配置日志系统

        :param service_name: 服务名称，用于日志文件名
        :param log_dir: 日志存放目录 (默认当前目录下的 logs)
        :param level: 日志等级 (DEBUG, INFO, WARNING, ERROR)
        :param rotation: 切割条件 (例如 "10 MB", "00:00", "1 week")
        :param retention: 保留时间 (例如 "20 days", "1 month")
        :param console: 是否输出到控制台
        :param json_format: 是否以 JSON 格式写入文件 (便于 ELK/Loki 采集)
        """
        # 1. 移除默认的 handler (防止重复)
        logger.remove()

        # 2. 转换路径
        log_path = Path(log_dir)
        if not log_path.exists():
            log_path.mkdir(parents=True, exist_ok=True)

        # 3. 定义日志格式
        # 相比你之前的格式，增加了颜色标记和更清晰的结构
        # 你的旧格式: '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s -%(process)s'
        text_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<magenta>PID:{process}</magenta> - "
            "<level>{message}</level>"
        )

        # 4. 添加控制台输出
        if console:
            logger.add(
                sys.stderr,
                level=level,
                format=text_format,
                enqueue=True,  # 开启异步队列，防止阻塞主线程
                backtrace=True,  # 显示详细的错误堆栈
                diagnose=True  # 显示变量值 (生产环境需谨慎，可能泄露敏感信息，但开发环境极好用)
            )

        # 5. 添加文件输出
        # 注意：Loguru 自动处理了多进程/多线程安全
        log_file = log_path / f"{service_name}.log"

        logger.add(
            str(log_file),
            rotation=rotation,  # 你之前的 maxBytes=10*1024*1024
            retention=retention,  # 你之前的 backupCount=20 (这里用时间更直观，也可以写 "20 files")
            level=level,
            encoding="utf-8",
            enqueue=True,  # 关键！异步写入文件，极大提升高并发下的性能
            compression="zip",  # 额外福利：切割后的历史日志自动压缩，节省磁盘
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}" if not json_format else "{message}",
            serialize=json_format  # 如果为 True，每一行都是 JSON，适合日志采集系统
        )

    @staticmethod
    def intercept_standard_logging(modules: list = None):
        """
        拦截标准库 logging 的日志，全部路由到 Loguru。
        解决了 "使用了 Loguru 但第三方库(如Sanic/Paho)的日志还是打印在控制台乱跑" 的问题。
        """
        if modules is None:
            modules = []

        # 基础拦截
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # 针对特定库拦截 (比如 Sanic, Paho-MQTT)
        for module_name in modules:
            mod_logger = logging.getLogger(module_name)
            mod_logger.handlers = [InterceptHandler()]
            mod_logger.propagate = False


# 为了保持 API 简洁，默认初始化一个配置，但允许用户后续覆盖
# 这样用户 `from syunity_core.system.logger import logger` 直接用也不会报错
if not logger._core.handlers:
    # 默认给一个控制台输出，避免无配置时什么都不显示
    logger.add(sys.stderr, level="INFO")


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
# 在 syunity_core/network/databus.py 中
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