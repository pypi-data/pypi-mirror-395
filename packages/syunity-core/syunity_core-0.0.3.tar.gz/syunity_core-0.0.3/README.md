# Syunity Core

[![PyPI version](https://badge.fury.io/py/syunity-core.svg)](https://badge.fury.io/py/syunity-core)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`syunity-core` 是一个高度集成的 Python 核心功能库，旨在简化物联网 (IoT) 及 Web 后端服务的开发。

> ⚠️ **重要提示**: 本项目专为 **Python 3.13** 环境设计，并使用 **paho-mqtt v2.1.0** (MQTT 5.0 协议栈)。

## 核心功能 (13 Modules)

1.  **线程管理**: 统一线程池封装
2.  **MQTT总线**: 基于 paho-mqtt v2.1.0 的发布/订阅封装
3.  **日志管理**: Loguru 集成
4.  **SQLite**: 轻量级数据库管理
5.  **IoTDB**: Apache IoTDB 时序数据库管理
6.  **气象管理**: 气象数据接口封装
7.  **平台管理**: 系统资源监控 (CPU/Mem/Disk)
8.  **日期组件**: 基于 Pendulum 的时间处理
9.  **用户权限**: RBAC 基础模型
10. **加密管理**: AES/RSA/Hash 工具集
11. **配置管理**: YAML/Env 统一加载
12. **JWT登录**: Token 签发与验证
13. **Sanic服务**: 异步 Web 服务脚手架

## 安装

```bash  
pip install syunity-core
```


## 版本更新记录

### v0.0.1  
基于gemini3 pro 生成的代码
准备发布pypi
根据绍兴项目对代码适用性进行验证

### v0.0.2
解决了模块对settings的依赖

### v0.0.3
解决了sqlite_manager self.con问题，后续还是需要对代码足够理解再发布