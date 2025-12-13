import threading
from abc import ABC, abstractmethod
from typing import List, Optional, Set, Dict
from dataclasses import dataclass, field
from enum import Enum


# ================= 1. 常量与配置 (Constants) =================

class Perms:
    """系统权限标识常量表"""
    # A. 平台服务 (Domain: sys)
    SYS_ENTITY_READ = "sys:entity:read"  # 实体查询
    SYS_USER_WRITE = "sys:user:write"  # 用户管理
    SYS_AUTH_EXEC = "sys:auth:exec"  # 认证操作
    SYS_DATA_MANAGE = "sys:data:manage"  # 数据迁移/文件管理
    SYS_META_READ = "sys:meta:read"  # 元数据获取
    SYS_WEATHER_READ = "sys:weather:read"  # 气象数据

    # B. 母线负荷预测 (Domain: biz/predict)
    PREDICT_READ = "biz:predict:read"  # 查看预测结果/出力
    PREDICT_EXEC = "biz:predict:exec"  # 执行预测(D+1/中长期/回测)
    PREDICT_CORRECT = "biz:predict:correct"  # 写入智能修正

    # C. 主变重过载 (Domain: biz/trans)
    TRANS_READ = "biz:trans:read"  # 综合分析/溯因

    # D. 经济调度 (Domain: biz/dispatch)
    DISPATCH_READ = "biz:dispatch:read"  # 评估结果
    DISPATCH_EXEC = "biz:dispatch:exec"  # 策略生成

    # E. 指标分析 (Domain: biz/analysis)
    ANALYSIS_CALC = "biz:analysis:calc"  # 指标计算
    ANALYSIS_READ = "biz:analysis:read"  # 统计查询/对比


# ================= 2. 模型定义 (Models) =================

class DataScopeType(str, Enum):
    ALL = "all"  # 全部数据 (返回 None)
    CUSTOM = "custom"  # 自定义部门 (返回指定 IDs)
    DEPT_AND_SUB = "dept_sub"  # 本部门及子部门
    DEPT_ONLY = "dept_only"  # 仅本部门
    SELF = "self"  # 仅本人 (返回 [])
    NONE = "none"  # 无权限


@dataclass
class RBACRole:
    code: str
    name: str
    data_scope: DataScopeType = DataScopeType.SELF
    parent_roles: List[str] = field(default_factory=list)  # 父角色Code
    permissions: Set[str] = field(default_factory=set)  # 权限Code集合
    custom_dept_ids: List[str] = field(default_factory=list)  # 自定义范围时的部门ID


@dataclass
class RBACDepartment:
    id: str
    name: str
    parent_id: Optional[str] = None
    tree_path: str = ""  # 树路径，如 /root/dev/


@dataclass
class RBACUser:
    id: str
    username: str
    dept_id: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    is_superuser: bool = False


# ================= 3. 接口定义 (Interface) =================

class IRBACProvider(ABC):
    """数据提供者接口，解耦数据库层"""

    @abstractmethod
    def load_roles(self) -> List[RBACRole]: pass

    @abstractmethod
    def load_departments(self) -> List[RBACDepartment]: pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[RBACUser]: pass


# ================= 4. 核心引擎 (Engine) =================

class RBACEngine:
    """RBAC 策略引擎 (单例/线程安全)"""
    _instance = None

    def __new__(cls):
        if not cls._instance: cls._instance = super().__new__(cls); cls._instance._init()
        return cls._instance

    def _init(self):
        self._provider: Optional[IRBACProvider] = None
        self._lock = threading.RLock()
        self._is_loaded = False
        self._role_map: Dict[str, RBACRole] = {}
        self._dept_map: Dict[str, RBACDepartment] = {}
        self._user_perm_cache: Dict[str, Set[str]] = {}

    def set_provider(self, provider: IRBACProvider):
        self._provider = provider

    def reload(self):
        """加载数据并计算继承关系"""
        if not self._provider: return
        with self._lock:
            # 1. 加载并索引数据
            raw_roles = {r.code: r for r in self._provider.load_roles()}
            self._dept_map = {d.id: d for d in self._provider.load_departments()}

            # 2. 扁平化角色继承 (避免运行时递归)
            self._role_map = {}
            for code, r in raw_roles.items():
                new_r = RBACRole(r.code, r.name, r.data_scope, r.parent_roles, set(r.permissions), r.custom_dept_ids)
                self._merge(new_r, raw_roles)
                self._role_map[code] = new_r

            self._user_perm_cache.clear()
            self._is_loaded = True

    def _merge(self, role: RBACRole, all_roles: Dict[str, RBACRole], visited=None):
        """递归合并父级权限"""
        if visited is None: visited = set()
        if role.code in visited: return
        visited.add(role.code)
        for p_code in role.parent_roles:
            if parent := all_roles.get(p_code):
                role.permissions.update(parent.permissions)
                self._merge(parent, all_roles, visited)

    def check_permission(self, user: RBACUser, action: str) -> bool:
        """鉴权：支持精确匹配和前缀通配符(user:*)"""
        if not self._is_loaded: self.reload()
        if user.is_superuser: return True

        with self._lock:
            perms = self._get_perms(user)
            if action in perms or "*" in perms: return True
            # 优化：仅当包含*时才进行前缀检查
            return any(p.endswith('*') and action.startswith(p[:-1]) for p in perms)

    def get_data_scope_ids(self, user: RBACUser) -> Optional[List[str]]:
        """计算数据范围: None=全部, []=仅自己, [ids]=特定部门"""
        if not self._is_loaded: self.reload()
        if user.is_superuser: return None

        target, has_all = set(), False
        with self._lock:
            for r_code in user.roles:
                if not (role := self._role_map.get(r_code)): continue
                if role.data_scope == DataScopeType.ALL:
                    has_all = True;
                    break
                elif role.data_scope == DataScopeType.CUSTOM:
                    target.update(role.custom_dept_ids)
                elif role.data_scope == DataScopeType.DEPT_ONLY and user.dept_id:
                    target.add(user.dept_id)
                elif role.data_scope == DataScopeType.DEPT_AND_SUB and user.dept_id:
                    if base := self._dept_map.get(user.dept_id):
                        target.add(base.id)
                        target.update(d.id for d in self._dept_map.values() if d.tree_path.startswith(base.tree_path))
        return None if has_all else list(target)

    def _get_perms(self, user: RBACUser) -> Set[str]:
        if user.id in self._user_perm_cache: return self._user_perm_cache[user.id]
        perms = set()
        for code in user.roles:
            if role := self._role_map.get(code): perms.update(role.permissions)
        self._user_perm_cache[user.id] = perms
        return perms


rbac = RBACEngine()