import time
import json
import threading
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Callable, Optional, Any, List, Union, Set
from contextlib import contextmanager
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion, MQTTProtocolVersion
from syunity_core.security.rbac import rbac
from syunity_core.security.models import RBACUser
from syunity_core.system.logger import logger   
    

# ==========================================
# 配置与数据结构
# ==========================================

@dataclass
class MqttConfig:
    """MQTT 代理配置数据类"""
    host: str
    port: int = 1883
    client_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    keepalive: int = 60
    clean_session: bool = False  # 注意：MQTT v5 中该参数行为有所不同
    connection_timeout: int = 10
    reconnect_delay_min: int = 1
    reconnect_delay_max: int = 120
    protocol: MQTTProtocolVersion = MQTTProtocolVersion.MQTTv311


class ConnectionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()


# 全局注册表
_mqtt_clients: Dict[str, 'MqttCore'] = {}
_thread_lock = threading.RLock()  # 使用可重入锁 (RLock) 更安全


# ==========================================
# 核心类
# ==========================================

class MqttCore:
    """
    基于 Paho MQTT v2.x 的现代化线程安全客户端封装
    支持上下文管理、自动重连、MQTT 5.0 属性兼容
    """

    def __init__(self, client_id: str, broker_config: Union[Dict, MqttConfig], auto_connect: bool = True):
        self.client_id = client_id

        # 兼容字典配置传入，自动转换为 dataclass
        if isinstance(broker_config, dict):
            # 过滤掉不属于 dataclass 的多余字段，防止报错
            valid_keys = MqttConfig.__annotations__.keys()
            filtered_config = {k: v for k, v in broker_config.items() if k in valid_keys}
            # 处理 client_id 默认值
            if 'client_id' not in filtered_config:
                filtered_config['client_id'] = f"mqtt_{client_id}"
            self.config = MqttConfig(**filtered_config)
        else:
            self.config = broker_config

        self.state = ConnectionState.DISCONNECTED
        self.client: Optional[mqtt.Client] = None

        # 数据存储
        self._subscriptions: Set[str] = set()
        self._topic_callbacks: Dict[str, List[Callable]] = {}
        self._pending_messages: List[Dict] = []

        # 同步控制
        self._connection_event = threading.Event()
        self._stop_event = threading.Event()

        # 注册实例
        with _thread_lock:
            _mqtt_clients[client_id] = self

        if auto_connect:
            self.connect()

    def __enter__(self):
        """支持 'with MqttCore(...) as client:' 语法"""
        if not self.is_connected():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> bool:
        """初始化并连接 (非阻塞启动，阻塞等待结果)"""
        if self.state != ConnectionState.DISCONNECTED:
            logger.warning(f"Client {self.client_id} is already {self.state.name}")
            return True

        try:
            self.state = ConnectionState.CONNECTING
            self._connection_event.clear()
            self._stop_event.clear()

            # Paho v2.x 初始化：必须指定 CallbackAPIVersion
            self.client = mqtt.Client(
                callback_api_version=CallbackAPIVersion.VERSION2,
                client_id=self.config.client_id,
                protocol=self.config.protocol
            )

            # MQTT v311 clean_session 设置 / MQTT v5 clean_start
            # Paho 内部会自动根据协议版本处理 clean_session 参数
            if self.config.protocol == MQTTProtocolVersion.MQTTv311:
                self.client.clean_session = self.config.clean_session

            # 认证配置
            if self.config.username and self.config.password:
                self.client.username_pw_set(self.config.username, self.config.password)

            # 利用 Paho 内置的高级重连机制，替代手写的重连线程
            self.client.reconnect_delay_set(
                min_delay=self.config.reconnect_delay_min,
                max_delay=self.config.reconnect_delay_max
            )

            # 绑定回调
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message
            self.client.on_subscribe = self._on_subscribe
            self.client.on_publish = self._on_publish

            logger.info(f"Connecting {self.client_id} to {self.config.host}:{self.config.port}")

            # 建立连接
            self.client.connect(
                host=self.config.host,
                port=self.config.port,
                keepalive=self.config.keepalive
            )

            # 启动后台网络线程 (Paho 自身管理线程)
            self.client.loop_start()

            # 等待连接结果
            if not self._connection_event.wait(self.config.connection_timeout):
                logger.error(f"Connection timeout for {self.client_id}")
                self.disconnect()  # 清理资源
                return False

            return self.state == ConnectionState.CONNECTED

        except Exception as e:
            logger.error(f"Fatal connection error for {self.client_id}: {e}")
            self.state = ConnectionState.DISCONNECTED
            return False

    def disconnect(self):
        """优雅断开连接"""
        with _thread_lock:
            if self.client_id in _mqtt_clients:
                del _mqtt_clients[self.client_id]

        self._stop_event.set()
        if self.client:
            # 停止网络循环
            self.client.loop_stop()
            if self.is_connected():
                self.client.disconnect()
            self.client = None

        self.state = ConnectionState.DISCONNECTED
        logger.info(f"Client {self.client_id} disconnected and disposed")

    # ==========================================
    # Paho v2 回调函数 (签名变更)
    # ==========================================

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        """
        Paho v2 连接回调
        reason_code: 也就是旧版的 rc，但现在是一个对象，0 仍代表成功
        properties: MQTT v5 属性
        """
        if reason_code.is_failure:
            logger.error(f"Connection failed for {self.client_id}: {reason_code}")
            self.state = ConnectionState.DISCONNECTED
            self._connection_event.set()  # 解锁等待，但状态为失败
            return

        self.state = ConnectionState.CONNECTED
        logger.info(f"Client {self.client_id} connected (Reason: {reason_code})")

        self._connection_event.set()

        # 恢复订阅
        # 注意：在 Paho 中，如果 clean_session=False，服务器会记住订阅，不需要重新订阅
        # 但为了保险起见或 clean_session=True，通常重新发送订阅
        with _thread_lock:
            for topic in self._subscriptions:
                self._safe_subscribe(topic)

        # 处理离线期间积压的消息
        self._flush_pending_messages()

    def _on_disconnect(self, client, userdata, flags, reason_code, properties=None):
        """Paho v2 断开回调"""
        self.state = ConnectionState.DISCONNECTED

        # reason_code 0 (Success) 表示调用了 disconnect() 主动断开
        # 其他值表示意外断开，loop_start 会自动触发 reconnect_delay_set 设定的重连
        if reason_code.value != 0:
            logger.warning(f"Unexpected disconnection {self.client_id}: {reason_code}. Auto-reconnecting...")
        else:
            logger.info(f"Client {self.client_id} disconnected normally")

    def _on_message(self, client, userdata, msg):
        """消息路由：集成 RBAC 权限检查 (修正版)"""
        try:
            topic = msg.topic
            # 尝试解析 Payload
            try:
                payload_str = msg.payload.decode('utf-8')
                data = json.loads(payload_str)
            except (UnicodeDecodeError, json.JSONDecodeError):
                data = msg.payload if isinstance(msg.payload, bytes) else msg.payload

            # =================================================
            # RBAC 权限拦截核心逻辑
            # =================================================
            # 必须确保 rbac 模块已导入，且 payload 是字典包含 user_id
            if isinstance(data, dict) and "user_id" in data and rbac:
                user_id = data["user_id"]
                required_perm = self._get_permission_for_topic(topic)

                if required_perm:
                    # --- [修正点开始] ---
                    # 错误原因：rbac.get_provider() 方法不存在
                    # 修正方案：直接访问 rbac.provider 属性，并增加判空保护

                    current_provider = getattr(rbac, 'provider', None)

                    if not current_provider:
                        logger.error("RBAC: Provider not initialized/loaded in engine. Blocking request.")
                        return  # 拦截：安全起见，鉴权组件未就绪时拒绝所有敏感操作

                    # 从 Provider 获取用户对象
                    user = current_provider.get_user(user_id)
                    # --- [修正点结束] ---

                    if not user:
                        logger.warning(f"RBAC: Unknown user '{user_id}' for topic {topic}")
                        return  # 拦截：用户不存在

                    if not rbac.check_permission(user, required_perm):
                        logger.warning(f"RBAC: User '{user_id}' denied. Needs '{required_perm}' on {topic}")
                        return  # 拦截：权限不足

                    logger.info(f"RBAC: User '{user_id}' granted '{required_perm}' on {topic}")

            # =================================================
            # 原有路由逻辑 (Paho 2.x 匹配)
            # =================================================
            matched_callbacks = set()

            with _thread_lock:
                # 浅拷贝防止迭代时修改
                registered_patterns = list(self._topic_callbacks.keys())

            for pattern in registered_patterns:
                # 使用 Paho 自带的高级匹配 (支持 + 和 #)
                if mqtt.topic_matches_sub(pattern, topic):
                    callbacks = self._topic_callbacks.get(pattern, [])
                    matched_callbacks.update(callbacks)

            if not matched_callbacks:
                logger.debug(f"No handler for topic: {topic}")
                return

            for callback in matched_callbacks:
                try:
                    callback(topic, data, self.client_id)
                except Exception as e:
                    logger.error(f"Error inside callback {callback.__name__}: {e}")

        except Exception as e:
            # 打印完整的堆栈信息以便调试
            import traceback
            logger.error(f"Message handling crash: {e}")
            logger.error(traceback.format_exc())

    def _get_permission_for_topic(self, topic: str) -> Optional[str]:
        """
        定义 Topic 到 RBAC 权限的映射规则
        实际项目中这里应该读取配置文件或数据库
        """
        if topic.startswith("secure/admin"):
            return "*:*"  # 需要超管权限
        if topic.startswith("secure/write"):
            return "file:write"
        if topic.startswith("secure/read"):
            return "file:read"
        return None  # 其他 topic 不鉴权

    def _on_subscribe(self, client, userdata, mid, reason_code_list, properties=None):
        """Paho v2 订阅回调：reason_code_list 包含每个 topic 的结果"""
        # reason_code_list[0].is_failure
        logger.debug(f"Subscribed {self.client_id} mid={mid}, codes={reason_code_list}")

    def _on_publish(self, client, userdata, mid, reason_code=None, properties=None):
        logger.debug(f"Published {self.client_id} mid={mid}")

    # ==========================================
    # 业务逻辑
    # ==========================================

    def subscribe(self, topic: str, qos: int = 0, callback: Optional[Callable] = None) -> bool:
        """统一的订阅入口"""
        with _thread_lock:
            if callback:
                if topic not in self._topic_callbacks:
                    self._topic_callbacks[topic] = []
                if callback not in self._topic_callbacks[topic]:
                    self._topic_callbacks[topic].append(callback)

            return self._safe_subscribe(topic, qos)

    def unsubscribe(self, topic: str, callback: Optional[Callable] = None):
        """取消订阅或移除回调"""
        with _thread_lock:
            if topic in self._topic_callbacks:
                if callback:
                    # 仅移除特定回调
                    self._topic_callbacks[topic] = [cb for cb in self._topic_callbacks[topic] if cb != callback]
                    if not self._topic_callbacks[topic]:
                        del self._topic_callbacks[topic]
                else:
                    # 移除所有
                    del self._topic_callbacks[topic]

            # 如果该 topic 没有任何回调了，且也不在纯订阅列表中，可以在这里选择取消 MQTT 层的订阅
            # 但为了简单，通常保持 MQTT 连接层的订阅，只在本地不再路由
            self._subscriptions.discard(topic)
            if self.is_connected():
                try:
                    self.client.unsubscribe(topic)
                    logger.info(f"Unsubscribed {self.client_id} from {topic}")
                except Exception as e:
                    logger.error(f"Unsubscribe error: {e}")

    def publish(self, topic: str, payload: Any, qos: int = 0, retain: bool = False) -> bool:
        """发布消息"""
        # 序列化
        if isinstance(payload, (dict, list)):
            try:
                final_payload = json.dumps(payload)
            except TypeError:
                final_payload = str(payload)
        else:
            final_payload = payload

        # 如果未连接，加入队列
        if not self.is_connected():
            logger.info(f"Buffering message for {topic} (Offline)")
            with _thread_lock:
                self._pending_messages.append({
                    "topic": topic, "payload": final_payload, "qos": qos, "retain": retain
                })
            return True

        return self._do_publish(topic, final_payload, qos, retain)

    def _do_publish(self, topic, payload, qos, retain) -> bool:
        try:
            info = self.client.publish(topic, payload, qos, retain)
            # info.rc 在 v2 中也是 ReasonCode，但 publish 返回的是 MQTTMessageInfo，保留了 rc 属性用于向后兼容
            if info.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"Publish failed rc={info.rc}")
                return False
            return True
        except Exception as e:
            logger.error(f"Publish exception: {e}")
            return False

    def _safe_subscribe(self, topic: str, qos: int = 0) -> bool:
        """内部订阅逻辑"""
        self._subscriptions.add(topic)
        if self.is_connected():
            try:
                self.client.subscribe(topic, qos)
                logger.info(f"Sent subscribe request for {topic}")
                return True
            except Exception as e:
                logger.error(f"Subscribe exception: {e}")
                return False
        return True

    def _flush_pending_messages(self):
        """发送离线队列"""
        with _thread_lock:
            if not self._pending_messages:
                return
            msgs = self._pending_messages[:]
            self._pending_messages.clear()

        logger.info(f"Flushing {len(msgs)} pending messages")
        for m in msgs:
            self._do_publish(m["topic"], m["payload"], m["qos"], m["retain"])

    def is_connected(self) -> bool:
        return self.state == ConnectionState.CONNECTED and self.client is not None


# ==========================================
# 模块级辅助函数
# ==========================================

def get_mqtt_client(client_id: str) -> Optional[MqttCore]:
    with _thread_lock:
        return _mqtt_clients.get(client_id)


def publish_to_all(topic: str, payload: Any, qos: int = 0, retain: bool = False) -> Dict[str, bool]:
    """向所有实例广播"""
    with _thread_lock:
        # 创建浅拷贝防止迭代时字典变更
        targets = list(_mqtt_clients.values())

    return {c.client_id: c.publish(topic, payload, qos, retain) for c in targets}


def disconnect_all():
    with _thread_lock:
        targets = list(_mqtt_clients.values())

    for client in targets:
        client.disconnect()