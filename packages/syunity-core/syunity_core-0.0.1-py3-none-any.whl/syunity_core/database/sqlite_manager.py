import sqlite3
import os
from typing import List, Dict, Union, Tuple
from contextlib import contextmanager
from pypinyin import lazy_pinyin

# 1. 引入配置
# 假设 setting.py 在 syunity_core 根目录下，或者根据你的实际路径调整 import
from syunity_core.settings import settings

# 2. 引入你定义好的 logger 对象
# 注意：这里只引入 logger 对象用于打印，不要在这里引入 LogManager 进行 setup
from syunity_core.system.logger import logger


class SqliteManager:
    def __init__(self, db_name: str = None):
        """
        初始化 SQLite 管理器
        :param db_name: 数据库名称（不含后缀），默认为当前项目名
        """
        # 1. 确定数据库名称
        if not db_name:
            self.db_name = f"{settings.system.project_name}_{settings.system.env}"
        else:
            self.db_name = db_name

        # 2. 构建完整路径
        self.db_path = os.path.join(
            settings.system.root_path, "db", "sqlite", f"{self.db_name}.db"
        )

        # 3. 确保目录存在
        self._ensure_db_dir()

        # 4. 自动重置逻辑 (仅在 dev 环境且 debug_mode 为 True 时生效)
        if settings.system.debug_mode and self._should_reset():
            self._reset_database()

        # 5. 连接参数
        self.conn_params = {"timeout": 10, "check_same_thread": False}
        self.conn = None
        self._init_connection()

    def _ensure_db_dir(self):
        """确保数据库目录存在"""
        dirname = os.path.dirname(self.db_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

    def _should_reset(self) -> bool:
        """判断是否配置了重置数据库"""
        # 读取配置中的 reset_db 字段，默认为 False
        return getattr(settings.system, "reset_db", False)

    def _reset_database(self):
        """删除现有数据库文件"""
        if os.path.exists(self.db_path):
            try:
                if self.conn:
                    self.conn.close()
                os.remove(self.db_path)
                # 【修改点】使用 logger 记录警告
                logger.warning(f"⚠️ Database reset: {self.db_path} has been removed based on configuration.")
            except Exception as e:
                logger.error(f"Failed to reset database: {e}")

    def _init_connection(self):
        """初始化连接"""
        try:
            self.conn = sqlite3.connect(self.db_path, **self.conn_params)
            self.conn.row_factory = sqlite3.Row
            self.conn.create_collation("PINYIN", self._pinyin_sort)

            # 【修改点】记录连接信息
            logger.info(f"Connected to SQLite DB: {self.db_path}")
        except Exception as e:
            # 【修改点】使用 critical 记录严重错误，exception=True 会自动打印堆栈
            logger.critical(f"Failed to connect to database {self.db_path}: {e}")
            raise e

    @staticmethod
    def _pinyin_sort(s1, s2):
        p = lazy_pinyin(str(s1))
        q = lazy_pinyin(str(s2))
        if p > q: return 1
        if p < q: return -1
        return 0

    @contextmanager
    def _cursor(self, commit=False):
        if not self.conn:
            self._init_connection()

        cursor = self.conn.cursor()
        try:
            yield cursor
            if commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            # 【修改点】记录 SQL 执行错误
            logger.error(f"SQL Execution Error: {e}")
            raise e
        finally:
            cursor.close()

    # --- CRUD 接口 (逻辑不变，仅需确认日志调用) ---

    def execute(self, sql: str, params: tuple = (), commit=True) -> int:
        with self._cursor(commit=commit) as cur:
            cur.execute(sql, params)
            # 开发调试时可取消注释下面这行
            # logger.debug(f"SQL: {sql} | Params: {params}")
            return cur.lastrowid

    def create_table(self, table: str, columns: Dict[str, str], constraints: List[str] = None):
        """
        创建表
        :param table: 表名
        :param columns: 字段定义
               例如: {"username": "TEXT UNIQUE", "age": "INTEGER", "email": "TEXT"}
        :param constraints: 表级约束列表 (用于组合唯一键、外键等)
               例如: ["UNIQUE(username)", "UNIQUE(dept_id, emp_code)", "FOREIGN KEY(dept_id) REFERENCES department(id)"]
        """
        cols = []

        # 1. 处理字段定义
        # 如果字段定义里没有主键，且字典里也没有 id 字段，自动添加 id
        has_pk = any("PRIMARY KEY" in v.upper() for v in columns.values())
        if "id" not in columns and not has_pk:
            cols.append("id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL")

        for k, v in columns.items():
            cols.append(f"{k} {v}")

        # 2. 处理表级约束 (组合唯一、外键等)
        if constraints:
            cols.extend(constraints)

        # 3. 拼接 SQL
        column_defs = ", ".join(cols)
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({column_defs})"

        self.execute(sql)
        logger.debug(f"Table ensured: {table}")

    def save(self, table: str, data: Union[Dict, List[Dict]], replace=False) -> int:
        if not data: return 0
        items = data if isinstance(data, list) else [data]
        if not items: return 0

        keys = list(items[0].keys())
        placeholders = ",".join(["?"] * len(keys))
        cols = ",".join(keys)
        action = "INSERT OR REPLACE" if replace else "INSERT"

        sql = f"{action} INTO {table} ({cols}) VALUES ({placeholders})"
        params = [tuple(item.get(k) for k in keys) for item in items]

        with self._cursor(commit=True) as cur:
            if len(items) > 1:
                cur.executemany(sql, params)
                count = cur.rowcount
            else:
                cur.execute(sql, params[0])
                count = cur.lastrowid
            return count

    def update(self, table: str, data: Dict, where: Dict):
        sets = [f"{k}=?" for k in data.keys()]
        w_sql, w_vals = self._build_where(where)
        sql = f"UPDATE {table} SET {','.join(sets)} {w_sql}"
        self.execute(sql, tuple(data.values()) + w_vals)

    def delete(self, table: str, where: Dict):
        w_sql, w_vals = self._build_where(where)
        sql = f"DELETE FROM {table} {w_sql}"
        self.execute(sql, w_vals)

    def find(self, table: str, where: Dict = None, page: int = None, size: int = 10, order_by: str = "id ASC") -> Union[
        List[Dict], Tuple[List[Dict], int]]:
        w_sql, w_vals = self._build_where(where)
        base_sql = f"SELECT * FROM {table} {w_sql} ORDER BY {order_by}"

        with self._cursor() as cur:
            if page:
                offset = (page - 1) * size
                limit_sql = f"{base_sql} LIMIT ? OFFSET ?"
                cur.execute(limit_sql, w_vals + (size, offset))
                rows = [dict(row) for row in cur.fetchall()]

                count_sql = f"SELECT COUNT(*) FROM {table} {w_sql}"
                cur.execute(count_sql, w_vals)
                total = cur.fetchone()[0]
                return rows, total
            else:
                cur.execute(base_sql, w_vals)
                return [dict(row) for row in cur.fetchall()]

    def find_one(self, table: str, where: Dict = None) -> Union[Dict, None]:
        res = self.find(table, where, page=1, size=1)
        rows = res[0]
        return rows[0] if rows else None

    def _build_where(self, where: Dict) -> Tuple[str, Tuple]:
        if not where: return "", ()
        clauses = []
        vals = []
        for k, v in where.items():
            if isinstance(v, (list, tuple)) and len(v) == 2 and isinstance(v[0], (int, float)) and isinstance(v[1],
                                                                                                              (int,
                                                                                                               float)):
                clauses.append(f"{k} BETWEEN ? AND ?")
                vals.extend(v)
            elif isinstance(v, list):
                if not v: continue
                p = ",".join(["?"] * len(v))
                clauses.append(f"{k} IN ({p})")
                vals.extend(v)
            elif isinstance(v, str) and ("%" in v):
                clauses.append(f"{k} LIKE ?")
                vals.append(v)
            else:
                clauses.append(f"{k} = ?")
                vals.append(v)
        return f"WHERE {' AND '.join(clauses)}", tuple(vals)

    def close(self):
        if self.conn:
            self.conn.close()


# --- 实例化单例 ---
# 注意：这里实例化时会打印日志
# 如果 main.py 还没运行 LogManager.setup()，日志会默认输出到 stderr (loguru 默认行为)
# 当 main.py 运行 setup() 后，后续日志会按配置写入文件
db = SqliteManager()