"""
    config/
    ├── default.yaml       # 通用配置（API地址、Topic结构、请求头）
    ├── dev.yaml           # 开发环境（127.0.0.1、调试模式）
    └── prod.yaml          # 生产环境（真实IP、关闭调试）
    .env                   # 密钥（AES Key, JWT Key, 数据库密码）
    setting.py             # 代码定义

    逻辑内聚：你原本分散在 JSON 里的 @project 替换逻辑，现在被封装在 settings 类的方法里 (get_mqtt_client_id)。业务代码调用时不需要再关心怎么拼接字符串。
    结构清晰：
        settings.mqtt_topics.get('user') 比原来的 json['Toris']['USER'] 更直观，且如果项目名改了，代码不用变，只要改 yaml。
    安全分离：jwt_key 和 aes_key 从代码/配置文件中移出，推荐使用 .env 管理。
    扩展性：如果新增一个 test 环境，只需要复制一份 dev.yaml 改名为 test.yaml 并修改里面的 IP 即可。

    代码中的 Import	     需要安装的 pip 包名	说明
    import yaml	PyYAML	注意：包名是 PyYAML，不是 yaml。
    from deepmerge ...	deepmerge	用于深度合并字典（基础配置 + 环境配置）。
    from pydantic ...	pydantic	核心数据校验库（建议使用 v2.x 版本）。
    from pydantic_settings ...	pydantic-settings	Pydantic v2 之后，Settings 模块被独立出来了。

"""

import os
import platform
import time
from pathlib import Path
from typing import Dict, Optional
import yaml
from deepmerge import always_merger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).resolve().parent
CONFIG_DIR = ROOT_PATH / "config"


# --- 子模型定义 ---

class SecurityConfig(BaseModel):
    jwt_key: str = "default_jwt_key"  # 建议通过环境变量 SECURITY_JWT_KEY 覆盖
    aes_key: str = "default_aes_key"  # 建议通过环境变量 SECURITY_AES_KEY 覆盖


class WeatherConfig(BaseModel):
    api_key: Optional[str] = Field(default=None, alias="key")  # 对应 yaml 中的 key 或 环境变量 WEATHER_API_KEY
    user_agent: str
    endpoints: Dict[str, str]


class IotdbConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 6667
    username: str = "root"
    password: str = "root"


class MqttConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 1883
    # 模板字符串
    username_template: str = "syunity_user"
    password: Optional[str] = None

    keepalive: int = 60
    min_delay: int = 1
    max_delay: int = 2000


class SystemConfig(BaseModel):
    project_name: str = "Toris"
    env: str = "dev"
    debug_mode: bool = True
    auto_start: bool = True
    log_level: str = "INFO"
    client_id_template: str = "client-id-default"
    root_path: Path = Field(default=None)


# --- 主配置类 ---

class Settings(BaseSettings):
    system: SystemConfig = SystemConfig()
    security: SecurityConfig = SecurityConfig()
    mqtt: MqttConfig = MqttConfig()
    iotdb: IotdbConfig = IotdbConfig()
    weather: WeatherConfig

    # 专门存放 Topic 映射
    mqtt_topics: Dict[str, str] = {}

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='_',  # 允许 IOTDB_PASSWORD 覆盖 iotdb.password
        extra='ignore'
    )

    @classmethod
    def load_config(cls):
        env_name = os.getenv("SYUNITY_ENV", "dev")
        print(f"🔵 Environment: {env_name}")

        yaml_files = [
            CONFIG_DIR / "default.yaml",
            CONFIG_DIR / f"{env_name}.yaml"
        ]

        combined_config = {}
        for file_path in yaml_files:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = yaml.safe_load(f) or {}
                    always_merger.merge(combined_config, file_data)

        # 注入环境名称
        if "system" not in combined_config: combined_config["system"] = {}
        combined_config["system"]["env"] = env_name

        combined_config["system"]["root_path"] = ROOT_PATH

        return cls(**combined_config)

    # --- 辅助逻辑：动态解析占位符 ---
    # 对应原来的 "@project", "@pcname" 等逻辑
    def get_mqtt_client_id(self, ukey="default") -> str:
        tpl = self.system.client_id_template
        return self._replace_placeholders(tpl, ukey)

    def get_mqtt_username(self) -> str:
        tpl = self.mqtt.username_template
        return self._replace_placeholders(tpl)

    def _replace_placeholders(self, text: str, ukey="") -> str:
        """统一处理 @project, @pcname, @timestamp 等替换逻辑"""
        pc_name = platform.node()
        timestamp = str(int(time.time()))

        text = text.replace("@project", self.system.project_name)
        text = text.replace("@pcname", pc_name)
        text = text.replace("@timestamp", timestamp)
        text = text.replace("@ukey", ukey)
        # 密码如果需要拼接入字符串(虽然不推荐)，也可以在这里处理
        return text


# --- 导出 ---
settings = Settings.load_config()

if __name__ == '__main__':
    # 测试打印
    print(f"Current Project: {settings.system.project_name}")
    print(f"Debug Mode: {settings.system.debug_mode}")
    print(f"IoTDB Connect: {settings.iotdb.host}:{settings.iotdb.port}")

    # 测试动态生成逻辑
    print(f"Generated MQTT ClientID: {settings.get_mqtt_client_id('device01')}")
    print(f"Generated MQTT Username: {settings.get_mqtt_username()}")

    # 测试 Topic 获取
    print(f"User Service Topic: {settings.mqtt_topics.get('user')}")

    # 测试密钥 (来自 .env)
    print(f"Weather API Key: {settings.weather.api_key}")

    print(settings.system.root_path)