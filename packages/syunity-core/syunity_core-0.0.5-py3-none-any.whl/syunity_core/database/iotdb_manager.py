import time, traceback, numpy as np, pandas as pd
from contextlib import contextmanager
from iotdb.SessionPool import SessionPool, PoolConfig
from iotdb.utils.IoTDBConstants import TSDataType
from iotdb.utils.NumpyTablet import NumpyTablet
from syunity_core.system.logger import logger

# ================= 配置区域 =================
# IoTDB 类型到 NumPy 类型的映射表，用于 Tablet 高效写入
NP_MAP = {
    TSDataType.DOUBLE: np.float64, TSDataType.FLOAT: np.float32,
    TSDataType.BOOLEAN: bool, TSDataType.INT32: np.int32,
    TSDataType.INT64: np.int64, TSDataType.TEXT: str
}
# 错误白名单：忽略这些非关键异常（如重复创建、路径不存在等）
IGN_ERRS = ["300", "already exist", "507", "Duplicated", "508", "does not exist", "Path"]


def guard(ret=None):
    """
    [装饰器] 全局异常防护盾
    1. 捕获所有方法异常，防止程序崩溃。
    2. 过滤白名单中的错误（如重复创建模板）。
    3. 记录关键错误日志。
    :param ret: 发生异常时的默认返回值
    """

    def dec(f):
        def wrap(self, *a, **k):
            try:
                return f(self, *a, **k)
            except Exception as e:
                # 如果错误信息包含白名单关键词，静默处理
                if any(s in str(e) for s in IGN_ERRS): return ret
                logger.error(f"❌ {f.__name__}: {e}");
                return ret

        return wrap

    return dec


class IotDBManager:
    def __init__(self, host, port, user, pwd, pool_size=8):
        """初始化连接池"""
        logger.info(f"🚀 Init IoTDB: {host}:{port}")
        # 注意：某些版本 SDK 要求 port 必须为字符串
        cfg = PoolConfig(host=host, port=str(port), user_name=user, password=pwd, time_zone="Asia/Shanghai")
        self.pool = SessionPool(pool_config=cfg, max_pool_size=pool_size, wait_timeout_in_ms=10000)

    def close(self):
        """关闭连接池"""
        self.pool.close()

    @contextmanager
    def _sess(self):
        """
        [上下文管理器] 安全获取 Session
        确保每次操作后，无论成功失败，Session 都能归还给连接池。
        """
        s = self.pool.get_session()
        try:
            yield s
        finally:
            self.pool.put_back(s)

    def _val(self, f):
        """
        [关键修复] 安全取值逻辑
        针对 Python SDK 的 Bug：当字段实际为 float 但被误判为 text 时，
        SDK 内部会尝试对 float 调用 decode() 导致崩溃。
        本方法优先直接读取原生 value 属性，绕过 SDK 内部的类型转换。
        """
        v = getattr(f, "value", None)
        # 如果已经是基础类型，直接返回，不要调用 SDK 的 getter
        if isinstance(v, (int, float, bool, str)): return v
        # 如果是 bytes，尝试解码为字符串
        return v.decode() if isinstance(v, bytes) else v

    @guard()
    def execute(self, sql):
        """执行 DDL (非查询语句)"""
        with self._sess() as s: s.execute_non_query_statement(sql)

    @guard(pd.DataFrame())
    def query(self, sql, fmt="df"):
        """
        执行查询并返回 DataFrame
        :param fmt: 返回格式 'df' (DataFrame) | 'dict' (列字典) | 'records' (行列表)
        """
        with self._sess() as s:
            ds = s.execute_query_statement(sql)
            if not ds: return pd.DataFrame() if fmt == "df" else []

            cols, data = ds.get_column_names(), []
            # 标准迭代器遍历，兼容所有 SDK 版本
            while ds.has_next():
                r = ds.next()
                # 使用 _val() 安全提取每个字段的值
                data.append([r.get_timestamp()] + [self._val(f) for f in r.get_fields()])

            ds.close_operation_handle()
            df = pd.DataFrame(data, columns=cols)
            return df if fmt == "df" else df.to_dict('list' if fmt == "dict" else 'records')

    @guard()
    def create_template(self, name, schema, paths=None):
        """创建设备模板并挂载到路径"""
        cols = ", ".join([f"{k} {v.name} COMPRESSION=SNAPPY" for k, v in schema.items()])
        self.execute(f"CREATE DEVICE TEMPLATE {name} ({cols})")
        if paths: [self.execute(f"SET DEVICE TEMPLATE {name} TO {p}") for p in paths]

    @guard()
    def insert_tablet(self, device, times, cols, vals, types):
        """
        [Tablet] 高效批量写入
        必须将 Python list 转换为 NumPy 数组才能被 SDK 识别。
        """
        if not times: return
        # 构造 NumPy 数组列表，字符串类型需指定为 object
        np_vals = [np.array(v, dtype=object if t == TSDataType.TEXT else NP_MAP.get(t)) for v, t in zip(vals, types)]
        with self._sess() as s:
            s.insert_tablet(NumpyTablet(device, cols, types, np_vals, np.array(times, dtype=np.int64)))

    @guard()
    def insert_records(self, devices, times, cols, types, vals):
        """
        [Records] 记录方式写入
        注意：SDK 底层使用 struct.pack，要求传入 Python 原生数值类型 (int/float)。
        严禁在此处将数值转换为字符串 (str)，否则会报 struct error。
        """
        with self._sess() as s: s.insert_records(devices, times, cols, types, vals)

    @guard()
    def migrate(self, sql, remote_conf, batch=5000):
        """数据迁移工具：从当前库查询 -> 写入远程库"""
        df = self.query(sql)
        if df.empty: return

        from iotdb.Session import Session  # 延迟导入，避免未安装时的报错
        rmt = Session(remote_conf['host'], int(remote_conf['port']), remote_conf.get('user', 'root'),
                      remote_conf.get('pwd', 'root'))
        rmt.open(False)

        try:
            # 自动解析 DataFrame 列名为设备路径和测点
            cols = [c for c in df.columns if c != 'Time']
            dev, meas = ".".join(cols[0].split(".")[:-1]), [c.split(".")[-1] for c in cols]

            # 自动推断 Pandas 类型为 IoTDB 类型
            types = [TSDataType.DOUBLE if pd.api.types.is_float_dtype(df[c]) else (
                TSDataType.INT64 if pd.api.types.is_integer_dtype(df[c]) else TSDataType.TEXT) for c in cols]

            # 分批次执行 Tablet 写入
            for i in range(0, len(df), batch):
                chk = df.iloc[i:i + batch]
                vals = [chk[c].values.astype(NP_MAP[t]) for c, t in zip(cols, types)]
                rmt.insert_tablet(NumpyTablet(dev, meas, types, vals, chk['Time'].values.astype(np.int64)))

            logger.info(f"✅ 迁移完成: {len(df)}条")
        finally:
            rmt.close()