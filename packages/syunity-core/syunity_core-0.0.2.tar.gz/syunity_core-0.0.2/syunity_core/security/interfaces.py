from abc import ABC, abstractmethod
from typing import List, Optional
from syunity_core.security.models import RBACRole, RBACDepartment, RBACUser

class IRBACProvider(ABC):
    """
    [扩展点] RBAC 数据提供者接口
    上层应用必须实现此接口，将数据库中的数据转换为 RBAC 模型
    """

    @abstractmethod
    def load_roles(self) -> List[RBACRole]:
        """加载系统中所有角色定义"""
        pass

    @abstractmethod
    def load_departments(self) -> List[RBACDepartment]:
        """加载系统中所有部门定义"""
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[RBACUser]:
        """根据ID获取用户详情"""
        pass