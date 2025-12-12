import sqlite3
import os
from typing import List, Dict, Union
from contextlib import contextmanager
from pypinyin import lazy_pinyin
from syunity_core.system.logger import logger


class SqliteManager:
    def __init__(self, db_path: str, debug_mode: bool = False, reset_db: bool = False):
        """
        初始化 SQLite 管理器
        :param db_path: 数据库绝对路径
        :param debug_mode: 调试模式
        :param reset_db: 是否重置数据库
        """
        self.db_path = db_path
        self.debug_mode = debug_mode

        # ✅ 修复点 1：必须先定义 conn 属性，防止后面调用 _reset_database 时报错
        self.conn = None
        self.conn_params = {"timeout": 10, "check_same_thread": False}

        # 1. 确保目录
        self._ensure_db_dir()

        # 2. 重置逻辑 (现在调用它时，self.conn 已经是 None 了，不会报错)
        if self.debug_mode and reset_db:
            self._reset_database()

        # 3. 建立连接
        self._init_connection()

    def _ensure_db_dir(self):
        dirname = os.path.dirname(self.db_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

    def _reset_database(self):
        if os.path.exists(self.db_path):
            try:
                # 这里会访问 self.conn，所以 __init__ 里必须先定义它
                if self.conn:
                    self.conn.close()

                os.remove(self.db_path)
                logger.warning(f"⚠️ Database reset: {self.db_path}")
            except Exception as e:
                logger.error(f"Reset failed: {e}")

    def _init_connection(self):
        try:
            # 如果之前没定义 conn_params，这里也会报错，所以建议把 conn_params 也提到上面
            self.conn = sqlite3.connect(self.db_path, **self.conn_params)
            self.conn.row_factory = sqlite3.Row
            self.conn.create_collation("PINYIN", self._pinyin_sort)
            logger.info(f"Connected to SQLite: {self.db_path}")
        except Exception as e:
            logger.critical(f"Connection failed: {e}")
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
        if not self.conn: self._init_connection()
        cursor = self.conn.cursor()
        try:
            yield cursor
            if commit: self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"SQL Error: {e}")
            raise e
        finally:
            cursor.close()

    # --- CRUD 接口 (保持不变) ---
    def execute(self, sql: str, params: tuple = (), commit=True) -> int:
        with self._cursor(commit=commit) as cur:
            cur.execute(sql, params)
            return cur.lastrowid

    def create_table(self, table: str, columns: Dict[str, str], constraints: List[str] = None):
        cols = []
        has_pk = any("PRIMARY KEY" in v.upper() for v in columns.values())
        if "id" not in columns and not has_pk:
            cols.append("id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL")
        for k, v in columns.items():
            cols.append(f"{k} {v}")
        if constraints:
            cols.extend(constraints)
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(cols)})"
        self.execute(sql)

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

    def find(self, table: str, where: Dict = None) -> List[Dict]:
        w_sql = ""
        w_vals = ()
        if where:
            clauses = [f"{k}=?" for k in where.keys()]
            w_sql = f"WHERE {' AND '.join(clauses)}"
            w_vals = tuple(where.values())

        sql = f"SELECT * FROM {table} {w_sql}"
        with self._cursor() as cur:
            cur.execute(sql, w_vals)
            return [dict(row) for row in cur.fetchall()]

    def close(self):
        if self.conn: self.conn.close()