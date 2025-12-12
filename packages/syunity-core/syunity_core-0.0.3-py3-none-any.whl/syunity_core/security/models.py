from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Set, Dict

class DataScopeType(str, Enum):
    """数据权限范围类型"""
    ALL = "all"                  # 所有数据
    CUSTOM = "custom"            # 自定义部门
    DEPT_AND_SUB = "dept_sub"    # 本部门及子部门
    DEPT_ONLY = "dept_only"      # 仅本部门
    SELF = "self"                # 仅本人
    NONE = "none"                # 无权限

@dataclass
class RBACPermission:
    """原子权限定义"""
    code: str          # 例如: 'device:read'
    name: str          # 例如: 'Read Device'

@dataclass
class RBACRole:
    """角色定义"""
    code: str          # 唯一标识，例如: 'admin'
    name: str
    data_scope: DataScopeType = DataScopeType.SELF
    parent_roles: List[str] = field(default_factory=list) # 继承的角色Code列表
    permissions: Set[str] = field(default_factory=set)    # 拥有的权限Code集合

@dataclass
class RBACDepartment:
    """部门定义 (支持树结构)"""
    id: str
    name: str
    parent_id: Optional[str] = None
    tree_path: str = ""  # 物化路径，例如: /root/sub/

@dataclass
class RBACUser:
    """RBAC 用户主体"""
    id: str
    username: str
    dept_id: Optional[str] = None
    roles: List[str] = field(default_factory=list) # 拥有的角色Code列表
    is_superuser: bool = False


""""""