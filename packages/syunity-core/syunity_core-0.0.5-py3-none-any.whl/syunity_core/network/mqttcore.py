import json
import paho.mqtt.client as mqtt
from syunity_core.system.logger import logger


class MqttCore:
    """MQTT核心组件：负责连接、自动重连、JSON收发及路由分发"""

    def __init__(self, client_id, config=None):
        cfg = config or {}
        self.cli = mqtt.Client(client_id)
        if cfg.get("username"): self.cli.username_pw_set(cfg["username"], cfg["password"])

        self.cli.on_connect = self._on_connect
        self.cli.on_message = self._on_message
        self.cbs = {}  # 路由表 {topic_pattern: callback}

        try:
            self.cli.connect(cfg.get("host", "127.0.0.1"), cfg.get("port", 1883), 60)
            self.cli.loop_start()  # 启动后台线程
        except Exception as e:
            logger.error(f"MQTT启动失败: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        """连接成功后自动重发订阅"""
        if rc == 0:
            logger.info("✅ MQTT连接成功")
            for t in self.cbs: client.subscribe(t)
        else:
            logger.error(f"❌ MQTT连接失败 RC={rc}")

    def _on_message(self, client, userdata, msg):
        """接收消息 -> JSON反序列化 -> 路由匹配"""
        try:
            payload = json.loads(msg.payload)
            # 遍历路由表，支持 # 和 + 通配符匹配
            for pat, func in self.cbs.items():
                if mqtt.topic_matches_sub(pat, msg.topic):
                    func(msg.topic, payload, client._client_id.decode())
        except Exception as e:
            logger.error(f"消息处理异常 [{msg.topic}]: {e}")

    def subscribe(self, topic, callback):
        """订阅主题并绑定回调"""
        self.cbs[topic] = callback
        self.cli.subscribe(topic)
        logger.info(f"📡 订阅: {topic}")

    def publish(self, topic, payload):
        """发布JSON数据"""
        self.cli.publish(topic, json.dumps(payload, ensure_ascii=False))

    def disconnect(self):
        self.cli.loop_stop()
        self.cli.disconnect()
