from syunity_core.system.logger import logger


class DBProxy:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBProxy, cls).__new__(cls)
            cls._instance._sqlite = None
            cls._instance._iotdb = None
        return cls._instance

    def init_sqlite(self, db_path: str, debug: bool = False, reset: bool = False):
        """初始化 SQLite"""
        try:
            from .sqlite_manager import SqliteManager
            self._sqlite = SqliteManager(db_path, debug, reset)
        except ImportError as e:
            logger.critical(f"❌ SQLite 模块加载失败: {e}")
            raise

    def init_iotdb(self, host: str, port: int, user: str, pwd: str, pool_size: int = 8):
        """初始化 IoTDB - 增加详细调试信息"""
        logger.info("⚙️ 正在加载 IotDBManager 模块...")
        try:
            from .iotdb_manager import IotDBManager
        except ImportError as e:
            logger.critical(f"❌ 无法导入 IotDBManager (请检查是否安装 apache-iotdb): {e}")
            raise e

        logger.info(f"⚙️ 正在实例化 IotDBManager ({host}:{port})...")
        try:
            # 强制覆盖旧实例
            if self._iotdb:
                self._iotdb.close()

            self._iotdb = IotDBManager(host, port, user, pwd, pool_size)
            logger.info("✅ IotDBManager 实例化成功并已挂载到 DBProxy")
        except Exception as e:
            logger.critical(f"❌ IotDBManager 初始化崩溃: {e}")
            self._iotdb = None  # 确保失败时置空
            raise e

    @property
    def sqlite(self):
        if self._sqlite is None:
            raise RuntimeError("❌ SQLite not initialized! Call db.init_sqlite(...) first.")
        return self._sqlite

    @property
    def iotdb(self):
        if self._iotdb is None:
            # 这里的报错说明 init_iotdb 没有成功运行，或者运行失败被吞了
            raise RuntimeError("❌ IoTDB not initialized! Call db.init_iotdb(...) first.")
        return self._iotdb

    def close(self):
        """关闭所有连接"""
        if self._sqlite:
            try:
                self._sqlite.close()
            except:
                pass
            self._sqlite = None
            logger.info("SQLite 连接已释放")

        if self._iotdb:
            try:
                self._iotdb.close()
            except:
                pass
            self._iotdb = None
            logger.info("IoTDB 连接已释放")


# 单例导出
db = DBProxy()