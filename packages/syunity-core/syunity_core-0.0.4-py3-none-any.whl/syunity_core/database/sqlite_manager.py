import sqlite3, os, time
from contextlib import contextmanager
from pypinyin import lazy_pinyin
from syunity_core.system.logger import logger
from pathlib import Path

class SqliteManager:
    def __init__(self, db_path: str, debug: bool = False, reset: bool = False):
        self.db_path, self.conn = db_path, None  # 初始化路径和连接对象占位
        os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None # 确保目录存在
        if debug and reset and os.path.exists(db_path): # 调试模式下重置数据库，注意debug模式会重置数据库
            os.remove(db_path); logger.warning(f"已重置: {db_path}") # 删除旧库
        self.conn = sqlite3.connect(db_path, timeout=10, check_same_thread=False) # 建立连接
        self.conn.row_factory = sqlite3.Row # 设置结果以字典形式访问
        self.conn.create_collation("PINYIN", lambda s1, s2: (lazy_pinyin(str(s1))>lazy_pinyin(str(s2))) - (lazy_pinyin(str(s1))<lazy_pinyin(str(s2)))) # 注册拼音排序lambda简化版
        logger.info(f"数据库已连接: {db_path}")

    @contextmanager # 上下文管理器装饰器
    def _cursor(self, commit=False): # 获取游标的辅助方法
        cursor = self.conn.cursor() # 创建游标
        try: yield cursor; self.conn.commit() if commit else None # 产出游标，根据标志提交事务
        except Exception as e: self.conn.rollback(); logger.error(f"SQL错误: {e}"); raise # 出错回滚并记录
        finally: cursor.close() # 确保游标关闭

    def execute(self, sql: str, params=(), commit=True):
        cursor = self.conn.cursor() # 注意：这里不使用 _cursor 上下文，因为要返回 cursor 给外部用
        try:
            cursor.execute(sql, params)
            if commit: self.conn.commit()
            return cursor
        except Exception as e:
            cursor.close()
            self.conn.rollback()
            logger.error(f"SQL执行失败: {e}")
            raise e

    def create_table(self, table: str, cols: dict, cons: list = None): # 建表
        defs = [f"{k} {v}" for k, v in cols.items()] # 生成列定义
        if not any("PRIMARY KEY" in v.upper() for v in cols.values()) and "id" not in cols: defs.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT") # 自动补ID
        self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(defs + (cons or []))})") # 执行建表SQL

    def save(self, table: str, data, replace=False): # 插入或更新数据
        items = data if isinstance(data, list) else [data] # 统一转为列表处理
        if not items: return 0 # 空数据直接返回
        keys, q = list(items[0].keys()), ",".join(["?"]*len(items[0])) # 获取字段名和问号占位符
        sql = f"INSERT {'OR REPLACE ' if replace else ''}INTO {table} ({','.join(keys)}) VALUES ({q})" # 拼接SQL
        with self._cursor(True) as cur: cur.executemany(sql, [tuple(i[k] for k in keys) for i in items]); return cur.rowcount or cur.lastrowid # 执行并返回影响行数

    def find(self, table: str, where: dict = None): # 查询数据
        sql, vals = f"SELECT * FROM {table}", () # 初始化SQL
        if where: sql, vals = f"{sql} WHERE {' AND '.join([f'{k}=?' for k in where])}", tuple(where.values()) # 拼接WHERE条件
        with self._cursor() as cur: cur.execute(sql, vals); return [dict(row) for row in cur.fetchall()] # 执行并转为字典列表返回

    def close(self): self.conn.close() if self.conn else None # 关闭连接


    def backup(self, bk_dir: str, retention: int=7) -> str:
        if not self.conn: return ""
        try:
            d = Path(bk_dir); d.mkdir(parents=True, exist_ok=True)
            bk_file = d / f"{self.path.stem}_bk_{time.strftime('%Y%m%d_%H%M%S')}.db"
            with sqlite3.connect(str(bk_file)) as bk_db: self.conn.backup(bk_db)
            if retention > 0: [f.unlink() for f in sorted(d.glob(f"{self.path.stem}_bk_*.db"))[:-retention] if retention < len(list(d.glob(f"{self.path.stem}_bk_*.db")))] # 一行流清理逻辑：按文件名排序（时间顺序），保留最后N个，其他的删掉
            logger.info(f"备份成功: {bk_file}"); return str(bk_file)
        except Exception as e: logger.error(f"备份失败: {e}"); return ""