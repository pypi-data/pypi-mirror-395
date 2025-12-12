import re
from typing import Dict, Set, Optional, List
from syunity_core.system.logger import logger
from .models import RBACRole, RBACDepartment, RBACUser, DataScopeType
from .interfaces import IRBACProvider


class RBACEngine:
    """
    RBAC 策略计算引擎
    不包含数据库操作，只负责内存中的权限计算。
    """

    def __init__(self):
        self._provider: Optional[IRBACProvider] = None
        # 缓存
        self._role_map: Dict[str, RBACRole] = {}
        self._dept_map: Dict[str, RBACDepartment] = {}
        self._user_perm_cache: Dict[str, Set[str]] = {}  # user_id -> permissions
        self._is_loaded = False

    def set_provider(self, provider: IRBACProvider):
        """注入数据提供者"""
        self._provider = provider

    def reload(self):
        """
        从 Provider 加载策略并构建缓存
        计算所有角色的权限继承关系（扁平化处理）
        """
        if not self._provider:
            logger.warning("RBAC Engine: No provider set. Engine is empty.")
            return

        logger.info("RBAC Engine: Reloading policies...")

        # 1. 加载基础数据
        raw_roles = {r.code: r for r in self._provider.load_roles()}
        depts = self._provider.load_departments()
        self._dept_map = {d.id: d for d in depts}

        # 2. 计算角色继承 (Flatten Inheritance)
        # 将父角色的权限合并到子角色中，避免运行时递归
        self._role_map = {}
        for r_code, role in raw_roles.items():
            # 复制一份避免修改原始引用
            computed_role = RBACRole(
                code=role.code,
                name=role.name,
                data_scope=role.data_scope,
                parent_roles=role.parent_roles,
                permissions=set(role.permissions)
            )

            # 递归合并父权限
            self._merge_parent_permissions(computed_role, raw_roles)
            self._role_map[r_code] = computed_role

        # 3. 清空用户级缓存
        self._user_perm_cache = {}
        self._is_loaded = True
        logger.info(f"RBAC Engine: Loaded {len(self._role_map)} roles, {len(self._dept_map)} depts.")

    def _merge_parent_permissions(self, role: RBACRole, all_roles_raw: Dict[str, RBACRole], visited=None):
        """递归辅助：合并父级权限"""
        if visited is None: visited = set()
        if role.code in visited: return  # 防止循环继承
        visited.add(role.code)

        for parent_code in role.parent_roles:
            parent = all_roles_raw.get(parent_code)
            if parent:
                role.permissions.update(parent.permissions)
                # 继续向上查找
                self._merge_parent_permissions(parent, all_roles_raw, visited)

    # ============================================
    # 核心 API: 功能权限 (Function Permission)
    # ============================================

    def check_permission(self, user: RBACUser, action: str) -> bool:
        """
        检查用户是否有权执行某动作
        支持通配符: 'device:*' 匹配 'device:read'
        """
        if not self._is_loaded: self.reload()
        if user.is_superuser: return True

        # 1. 获取用户所有权限 (包含继承)
        perms = self._get_user_perms(user)

        # 2. 精确匹配
        if action in perms: return True
        if "*" in perms or "*:*" in perms: return True

        # 3. 前缀通配符匹配
        # 优化: 只有当权限串包含 * 时才进行正则/通配逻辑
        for p in perms:
            if '*' in p:
                # 简单实现: 'device:*' -> startswith 'device:'
                prefix = p.split('*')[0]
                if action.startswith(prefix):
                    return True
        return False

    def _get_user_perms(self, user: RBACUser) -> Set[str]:
        """获取用户最终权限集 (带缓存)"""
        if user.id in self._user_perm_cache:
            return self._user_perm_cache[user.id]

        final_perms = set()
        for role_code in user.roles:
            role = self._role_map.get(role_code)
            if role:
                final_perms.update(role.permissions)

        self._user_perm_cache[user.id] = final_perms
        return final_perms

    # ============================================
    # 核心 API: 数据权限 (Data Scope)
    # ============================================

    def get_data_scope_ids(self, user: RBACUser) -> Optional[List[str]]:
        """
        计算用户的数据权限范围
        Returns:
            None: 代表拥有全部权限 (ALL)
            []: 代表只能看自己 (SELF) 或无权
            ['d1', 'd2']: 代表具体的部门ID列表
        """
        if not self._is_loaded: self.reload()
        if user.is_superuser: return None

        target_dept_ids = set()
        has_all = False
        has_dept_perm = False  # 标记是否拥有任何部门级权限

        for role_code in user.roles:
            role = self._role_map.get(role_code)
            if not role: continue

            if role.data_scope == DataScopeType.ALL:
                has_all = True
                break

            elif role.data_scope == DataScopeType.DEPT_ONLY:
                if user.dept_id:
                    target_dept_ids.add(user.dept_id)
                    has_dept_perm = True

            elif role.data_scope == DataScopeType.DEPT_AND_SUB:
                if user.dept_id and user.dept_id in self._dept_map:
                    base_dept = self._dept_map[user.dept_id]
                    target_dept_ids.add(base_dept.id)
                    # 查找所有子部门 (基于 tree_path)
                    prefix = base_dept.tree_path
                    for d in self._dept_map.values():
                        if d.tree_path.startswith(prefix):
                            target_dept_ids.add(d.id)
                    has_dept_perm = True

            # DataScopeType.SELF 不需要添加 dept_id

        if has_all:
            return None  # 全部权限

        return list(target_dept_ids)


# 导出全局单例，供 import 使用
rbac = RBACEngine()