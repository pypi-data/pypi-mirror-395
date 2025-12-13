import os
from typing import Callable, Optional, List, Any, Dict
from syunity_core.system.logger import logger
from syunity_core.system.thread_pool import tm
from syunity_core.security.rbac import rbac, RBACUser

# 定义验证器函数类型: 接收 token str, 返回 claims dict 或 None
TokenValidator = Callable[[str], Optional[Dict[str, Any]]]


class DataBus:
    """
    通用数据总线 (DataBus)
    功能：MQTT 消息分发、RBAC 鉴权、参数校验、线程池隔离
    """

    def __init__(self, mqtt_core, token_validator: TokenValidator, dev_mode: bool = False):
        """
        :param mqtt_core: MQTT 通信核心实例
        :param token_validator: 外部注入的 Token 校验函数
        :param dev_mode: 是否开启开发模式。开启后，缺失 Token 的请求将自动获得超管权限。
        """
        self.mqtt = mqtt_core
        self.validator = token_validator

        # 允许通过参数或环境变量开启 (环境变量优先级更高)
        self.dev_mode = dev_mode or (os.getenv("SYUNITY_DEV_MODE") == "true")

        if self.dev_mode:
            logger.warning("⚠️ DataBus 运行在 [开发模式] - 鉴权检查已放宽！")

        # 确保 RBAC 策略已加载
        if not rbac._is_loaded:
            try:
                rbac.reload()
            except Exception as e:
                logger.warning(f"RBAC Provider not ready or failed to load: {e}")

    def subscribe(self, topic: str, permission: str = None, required_keys: List[str] = None):
        """
        [装饰器模式] 注册 Topic 路由 (适用于代码硬编码场景)
        :param topic: MQTT Topic
        :param permission: 权限标识，建议使用 Perms.XXX 常量
        :param required_keys: Payload 必须包含的字段
        """

        def decorator(func: Callable):
            self.register_route(topic, func, permission, required_keys)
            return func

        return decorator

    def register_route(self, topic: str, func: Callable, permission: str = None, required_keys: List[str] = None):
        """
        [普通方法模式] 注册 Topic 路由 (适用于 YAML 配置驱动场景)
        :param topic: MQTT Topic
        :param func: 业务回调函数对象
        :param permission: 权限标识
        :param required_keys: Payload 必须包含的字段
        """

        # 定义实际的 MQTT 回调入口 (闭包捕获了配置参数)
        def _entry_point(recv_topic, payload, client_id):
            # 将具体的鉴权和执行逻辑丢给线程池，避免阻塞 MQTT 接收线程
            tm.submit_task(
                self._middleware,
                func, permission, required_keys, recv_topic, payload, client_id,
                error_cb=lambda e: logger.error(f"❌ Bus Execution Error [{recv_topic}]: {e}")
            )

        # 调用底层 MQTT Core 进行实际订阅
        self.mqtt.subscribe(topic, _entry_point)

    def _middleware(self, func, perm, req_keys, topic, payload, client_id):
        """
        安全中间件：参数校验 -> Token解析 -> 权限判定 -> 业务执行
        """
        try:
            # 1. 参数完整性校验 (Fail Fast)
            if req_keys:
                missing = [k for k in req_keys if k not in payload]
                if missing:
                    logger.warning(f"⚠️ [Data] {topic} 拒绝: 缺少参数 {missing}")
                    return

            # 2. 鉴权流程
            current_user = None

            # --- 2.1 绿色通道 (Dev Mode) ---
            # 开发模式下，如果没带 token，直接伪造一个超级管理员
            if self.dev_mode and perm and "token" not in payload:
                current_user = RBACUser(
                    id="dev_root",
                    username="Dev_God",
                    is_superuser=True,  # 超管无视 RBAC 检查
                    roles=["admin"]
                )
                payload["_user"] = current_user
                logger.info(f"🟢 [DevMode] 自动授予 {topic} 超级权限")

            # --- 2.2 正常鉴权 (Production Mode) ---
            elif perm:
                token = payload.get("token")
                if not token:
                    logger.warning(f"⛔ [Auth] {topic} 拒绝: Payload 缺失 'token'")
                    return

                # 调用验证器
                claims = self.validator(token)
                if not claims:
                    logger.warning(f"⛔ [Auth] {topic} 拒绝: Token 验证失败或过期")
                    return

                # 构建用户上下文
                current_user = RBACUser(
                    id=claims.get("sub"),
                    username=claims.get("name", "unknown"),
                    roles=claims.get("roles", []),
                    dept_id=claims.get("dept_id"),
                    is_superuser=claims.get("is_superuser", False)
                )

                # RBAC 检查
                if not rbac.check_permission(current_user, perm):
                    logger.warning(f"⛔ [RBAC] 用户 [{current_user.username}] 无权访问 [{topic}] (需权限: {perm})")
                    return

                # 鉴权通过，注入上下文
                payload["_user"] = current_user
                logger.debug(f"🔓 [Access] {current_user.username} -> {topic}")

            # 3. 执行业务逻辑
            func(topic, payload, client_id)

        except Exception as e:
            logger.error(f"❌ Middleware Exception [{topic}]: {e}", exc_info=True)