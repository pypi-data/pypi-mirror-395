from typing import Union, List, Dict, Any, Optional
from enum import Enum
import pendulum

TZ = "Asia/Shanghai"


class TimeFormat(Enum):
    DEFAULT, ISO8601 = "YYYY-MM-DD HH:mm:ss", "YYYY-MM-DDTHH:mm:ss.SSSSSSZ"
    DATE_ONLY, TIME_ONLY, COMPACT = "YYYY-MM-DD", "HH:mm:ss", "YYYYMMDDHHmmss"
    CN_DEFAULT, CN_DATE = "YYYY年MM月DD日 HH:mm:ss", "YYYY年MM月DD日"


class TimeScale(Enum):
    SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR = "second", "minute", "hour", "day", "week", "month", "quarter", "year"


class DateUtils:
    @staticmethod
    def _p(v):
        if isinstance(v, pendulum.DateTime): return v.in_tz(TZ)
        if isinstance(v, (int, float)): return pendulum.from_timestamp(v / 1000 if v > 9e10 else v, tz=TZ)
        return pendulum.parse(str(v), tz=TZ)

    @staticmethod
    def _t(d: pendulum.DateTime) -> int:
        return int(d.timestamp() * 1000)

    @staticmethod
    def _ret(d_list: List[pendulum.DateTime], fmt) -> List[Union[int, str]]:
        """内部通用返回处理：fmt为None返int，否则返str"""
        if fmt is None: return [DateUtils._t(d) for d in d_list]
        f = fmt.value if isinstance(fmt, Enum) else fmt
        return [d.format(f) for d in d_list]

    @staticmethod
    def now_ts() -> int:
        return DateUtils._t(pendulum.now(TZ))

    @staticmethod
    def str_to_ts13(s: str) -> int:
        return DateUtils._t(DateUtils._p(s))

    @staticmethod
    def format(obj: Union[int, str, List, Dict], fmt: Union[TimeFormat, str] = TimeFormat.DEFAULT) -> Any:
        if isinstance(obj, list): return [DateUtils.format(i, fmt) for i in obj]
        if isinstance(obj, dict): return {DateUtils.format(k, fmt): v for k, v in obj.items()}
        f = fmt.value if isinstance(fmt, Enum) else fmt
        return DateUtils._p(obj).format(f)

    @staticmethod
    def humanize(ts: int, locale='zh') -> str:
        return (pendulum.set_locale(locale) or DateUtils._p(ts)).diff_for_humans()

    @staticmethod
    def get_range(ts: int, sc: TimeScale, fmt=None) -> List[Union[int, str]]:
        st = DateUtils._p(ts).start_of(sc.value)
        # 利用 _ret 统一处理返回类型
        return DateUtils._ret([st, st.add(**{f"{sc.value}s": 1})], fmt)

    @staticmethod
    def shift(ts: int, n: int, unit: TimeScale) -> int:
        return DateUtils._t(DateUtils._p(ts).add(**{f"{unit.value}s": n}))

    @staticmethod
    def shift_series(s: List[int], n: int, unit: TimeScale, fmt=None) -> List[Union[int, str]]:
        # 先计算出平移后的 DateTime 对象列表
        d_list = [DateUtils._p(t).add(**{f"{unit.value}s": n}) for t in s]
        return DateUtils._ret(d_list, fmt)

    @staticmethod
    def generate_series(start, end, val: int, unit: TimeScale, fmt=None) -> List[Union[int, str]]:
        s, e = DateUtils._p(start), DateUtils._p(end)
        # 获取 interval 生成的 DateTime 列表 (左闭右开)
        d_list = list(pendulum.interval(s, e.subtract(microseconds=1)).range(f"{unit.value}s", val))
        return DateUtils._ret(d_list, fmt)


date_utils = DateUtils