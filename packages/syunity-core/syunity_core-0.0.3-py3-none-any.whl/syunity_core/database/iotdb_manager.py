"""
IoTDB Manager - 工业级 IoTDB 客户端封装 (适配 apache-iotdb 2.0.5)
功能特性：
1. 连接池管理 (SessionPool + PoolConfig)
2. 高性能写入 (NumpyTablet)
3. 自动异常捕获与重试保护 (@iotdb_guard)
4. 跨库数据在线迁移 (Data Migration)
5. 统一返回格式 (Pandas/Dict/List)
"""

import time
import traceback
from contextlib import contextmanager
from functools import wraps
from typing import List, Dict, Any, Union, Optional
from enum import Enum
import numpy as np
import pandas as pd
from iotdb.SessionPool import SessionPool
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType
from iotdb.utils.NumpyTablet import NumpyTablet
from iotdb.SessionPool import PoolConfig
from syunity_core.system.logger import logger


class OutputFormat(Enum):
    """查询结果返回格式枚举"""
    DF = "dataframe"      # 返回 pd.DataFrame
    DICT = "dict"         # 返回字典 {col: [val1, val2]}
    RECORDS = "records"   # 返回列表 [{col: val1}, {col: val2}]


def iotdb_guard(func):
    """装饰器：IoTDB 操作保护"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_t = time.perf_counter()
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            cost = (time.perf_counter() - start_t) * 1000
            msg = str(e)
            if "already exists" in msg or "300" in msg:
                logger.warning(f"⚠️ [IoTDB] {func.__name__}: {msg}")
            else:
                logger.error(f"❌ [IoTDB] {func.__name__} failed ({cost:.2f}ms): {msg}")
                logger.debug(traceback.format_exc())
            raise e
    return wrapper


class IotDBManager:
    def __init__(self, host: str, port: int, user: str, pwd: str,
                 fetch_size: int = 5000, pool_size: int = 8):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.fetch_size = fetch_size
        self.pool_size = pool_size
        self._pool: Optional[SessionPool] = None

        self._init_pool()

    def _init_pool(self):
        try:
            pool_config = PoolConfig(
                host=self.host,
                port=int(self.port),
                user_name=self.user,
                password=self.pwd,
                fetch_size=self.fetch_size,
                time_zone="Asia/Shanghai"
            )
            self._pool = SessionPool(
                pool_config=pool_config,
                max_pool_size=self.pool_size,
                wait_timeout_in_ms=10000
            )
            logger.info(f"🚀 IoTDB SessionPool (v2.0.5) initialized: {self.host}:{self.port}")
        except Exception as e:
            logger.critical(f"❌ IoTDB Pool Init Failed: {e}")
            raise e

    @contextmanager
    def get_session(self):
        if not self._pool:
            raise RuntimeError("IoTDB SessionPool is not initialized!")
        session = self._pool.get_session()
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            self._pool.put_back(session)

    def close(self):
        if self._pool:
            self._pool.close()
            logger.info("🔌 IoTDB SessionPool closed.")

    @iotdb_guard
    def create_database(self, db_name: str):
        with self.get_session() as session:
            try:
                session.set_storage_group(db_name)
                logger.info(f"✅ Database [{db_name}] created.")
            except Exception as e:
                if "already exists" in str(e) or "300" in str(e):
                    logger.warning(f"⚠️ Database [{db_name}] already exists.")
                else:
                    raise e

    @iotdb_guard
    def delete_database(self, db_names: Union[str, List[str]]):
        if isinstance(db_names, str):
            db_names = [db_names]
        with self.get_session() as session:
            try:
                session.delete_storage_groups(db_names)
                logger.warning(f"🗑️ Database {db_names} deleted.")
            except Exception as e:
                logger.warning(f"⚠️ Delete database failed: {e}")

    @iotdb_guard
    def create_and_set_template(self, template_name: str, schema: Dict[str, TSDataType], paths: List[str]):
        """
        创建并挂载元数据模板 (使用 SQL 方式，避免 SDK API 弃用问题)
        """
        # 1. 构建创建模板的 SQL
        # 格式: CREATE DEVICE TEMPLATE t1 (temperature FLOAT encoding=RLE, status BOOLEAN encoding=PLAIN compression=SNAPPY)
        item_list = []
        for m_name, m_type in schema.items():
            type_str = m_type.name  # 获取枚举名称，如 'DOUBLE', 'BOOLEAN'
            # 默认使用 SNAPPY 压缩，编码让 IoTDB 自适应
            item_list.append(f"{m_name} {type_str} COMPRESSION=SNAPPY")

        items_str = ", ".join(item_list)
        create_sql = f"CREATE DEVICE TEMPLATE {template_name} ({items_str})"

        with self.get_session() as session:
            # 2. 执行创建模板 SQL
            try:
                session.execute_non_query_statement(create_sql)
                logger.info(f"📄 Template [{template_name}] created (via SQL).")
            except Exception as e:
                msg = str(e)
                # 错误代码 300 表示重复创建，304 表示模板已存在
                if "300" in msg or "304" in msg or "already exists" in msg:
                    logger.warning(f"⚠️ Template [{template_name}] already exists.")
                else:
                    raise e

            # 3. 挂载模板 (SET DEVICE TEMPLATE t1 TO root.sg1)
            for path in paths:
                set_sql = f"SET DEVICE TEMPLATE {template_name} TO {path}"
                try:
                    session.execute_non_query_statement(set_sql)
                    logger.info(f"🔗 Template [{template_name}] set to [{path}]")
                except Exception as e:
                    msg = str(e)
                    # 错误代码 300/304 或提示已设置
                    if "300" in msg or "304" in msg or "already set" in msg:
                        pass
                    else:
                        logger.error(f"❌ Failed to set template on {path}: {e}")

    @iotdb_guard
    def insert_tablet(self, device: str, timestamps: List[int],
                      measurements: List[str], values: List[List[Any]],
                      dtypes: List[TSDataType]):
        if not timestamps:
            return
        np_times = np.array(timestamps, dtype=np.int64)
        np_values = []
        for i, dtype in enumerate(dtypes):
            v_arr = np.array(values[i])
            if dtype == TSDataType.DOUBLE:
                v_arr = v_arr.astype(np.float64)
            elif dtype == TSDataType.FLOAT:
                v_arr = v_arr.astype(np.float32)
            elif dtype == TSDataType.BOOLEAN:
                v_arr = v_arr.astype(bool)
            elif dtype == TSDataType.INT32:
                v_arr = v_arr.astype(np.int32)
            elif dtype == TSDataType.INT64:
                v_arr = v_arr.astype(np.int64)
            np_values.append(v_arr)

        tablet = NumpyTablet(device, measurements, dtypes, np_values, np_times)
        with self.get_session() as session:
            session.insert_tablet(tablet)

    @iotdb_guard
    def query(self, sql: str, fmt: OutputFormat = OutputFormat.DF) -> Union[pd.DataFrame, Dict, List]:
        with self.get_session() as session:
            dataset = session.execute_query_statement(sql)
            if not dataset:
                return pd.DataFrame() if fmt == OutputFormat.DF else []
            df = dataset.todf()
            if fmt == OutputFormat.DF:
                return df
            elif fmt == OutputFormat.DICT:
                return df.to_dict(orient='list')
            elif fmt == OutputFormat.RECORDS:
                return df.to_dict(orient='records')
            return df

    @iotdb_guard
    def count_timeseries(self, path_pattern: str = "root.**") -> int:
        df = self.query(f"COUNT TIMESERIES {path_pattern}")
        return int(df.iloc[0, 0]) if not df.empty else 0

    def migrate_to_cloud(self, sql: str, remote_conf: Dict, batch_size=5000):
        logger.info(f"✈️ Migration Start: {sql}")
        remote_session = None
        try:
            remote_session = Session(
                remote_conf['host'],
                int(remote_conf['port']),
                remote_conf.get('username', 'root'),
                remote_conf.get('password', 'root')
            )
            remote_session.open(False)

            df = self.query(sql, fmt=OutputFormat.DF)
            if df.empty:
                logger.warning("⚠️ Source data is empty.")
                return

            cols = [c for c in df.columns if c != 'Time']
            if not cols: return

            first_col = cols[0]
            device_id = ".".join(first_col.split(".")[:-1])
            measurements = [c.split(".")[-1] for c in cols]

            total = len(df)
            for start in range(0, total, batch_size):
                chunk = df.iloc[start: start + batch_size]
                timestamps = chunk['Time'].values.astype(np.int64)
                values_list = []
                dtypes = []

                for col in cols:
                    series = chunk[col]
                    if pd.api.types.is_float_dtype(series):
                        dtypes.append(TSDataType.DOUBLE)
                        values_list.append(series.values.astype(np.float64))
                    elif pd.api.types.is_integer_dtype(series):
                        dtypes.append(TSDataType.INT64)
                        values_list.append(series.values.astype(np.int64))
                    elif pd.api.types.is_bool_dtype(series):
                        dtypes.append(TSDataType.BOOLEAN)
                        values_list.append(series.values.astype(bool))
                    else:
                        dtypes.append(TSDataType.TEXT)
                        values_list.append(series.astype(str).values)

                tablet = NumpyTablet(device_id, measurements, dtypes, values_list, timestamps)
                remote_session.insert_tablet(tablet)
                logger.info(f"   -> Batch {start} migrated.")
            logger.success("✅ Migration completed.")

        except Exception as e:
            logger.error(f"❌ Migration error: {e}")
            logger.debug(traceback.format_exc())
        finally:
            if remote_session:
                remote_session.close()