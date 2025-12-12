from typing import Optional
# 假设这三个文件在同一目录下，如果是不同目录请调整 import 路径
from .sqlite_manager import SqliteManager
from .iotdb_manager import IotDBManager


class DBProxy:
    """
    统一数据库代理。
    支持关系型数据库 (SQLite) 和时序数据库 (IoTDB)。
    """

    def __init__(self):
        self._sqlite: Optional[SqliteManager] = None
        self._iotdb: Optional[IotDBManager] = None

    # --- SQLite 部分 ---
    def init_sqlite(self, db_path: str, debug_mode: bool = False, reset_db: bool = False):
        """初始化 SQLite"""
        if self._sqlite is not None: return
        self._sqlite = SqliteManager(db_path, debug_mode, reset_db)

    @property
    def sqlite(self) -> SqliteManager:
        """获取 SQLite 实例"""
        if self._sqlite is None:
            raise RuntimeError("❌ SQLite not initialized! Call db.init_sqlite(...) first.")
        return self._sqlite

    # --- IoTDB 部分 ---
    def init_iotdb(self, host: str, port: int, user: str, pwd: str, **kwargs):
        """
        初始化 IoTDB
        :param kwargs: 透传给 IotDBManager 的参数 (例如 pool_size, fetch_size)
        """
        # 如果已初始化且未关闭，直接返回
        if self._iotdb is not None:
            return

        self._iotdb = IotDBManager(host, port, user, pwd, **kwargs)

    @property
    def iotdb(self) -> IotDBManager:
        """获取 IoTDB 实例"""
        if self._iotdb is None:
            raise RuntimeError("❌ IoTDB not initialized! Call db.init_iotdb(...) first.")
        return self._iotdb

    # --- 生命周期管理 (新增核心修改) ---
    def close(self):
        """
        显式关闭所有连接并重置状态。
        在测试脚本结束或系统退出时调用，确保下次 init 能创建新连接。
        """
        if self._sqlite:
            # 如果 SqliteManager 有 close 方法建议调用
            # self._sqlite.close()
            self._sqlite = None

        if self._iotdb:
            try:
                self._iotdb.close()
            except Exception:
                pass
            self._iotdb = None  # 【关键】重置为 None

    # --- 兼容旧代码的魔法方法 ---
    def __getattr__(self, name):
        # 默认转发给 SQLite，保持之前的兼容性
        if self._sqlite:
            return getattr(self._sqlite, name)
        raise AttributeError(f"'DBProxy' object has no attribute '{name}'")


# 全局单例
db = DBProxy()