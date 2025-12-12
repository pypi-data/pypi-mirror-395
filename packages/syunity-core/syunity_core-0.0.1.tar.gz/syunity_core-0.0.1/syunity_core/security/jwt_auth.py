import jwt
import datetime
from typing import Dict, Optional, Tuple
from syunity_core.settings import settings
from syunity_core.system.logger import logger


class JWTAuthManager:
    """
    JWT 认证管理器 (单例模式)
    负责 Access Token 和 Refresh Token 的签发与校验
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(JWTAuthManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 防止重复初始化
        if not hasattr(self, '_initialized'):
            self._load_config()
            self._initialized = True

    def _load_config(self):
        """加载 JWT 配置"""
        jwt_conf = getattr(settings.security, 'jwt', None)

        # 默认配置兜底
        self.secret_key = getattr(jwt_conf, 'secret_key', "DEFAULT_UNSAFE_SECRET")
        self.algorithm = getattr(jwt_conf, 'algorithm', "HS256")
        self.access_expire_min = getattr(jwt_conf, 'access_token_expire_minutes', 60)
        self.refresh_expire_days = getattr(jwt_conf, 'refresh_token_expire_days', 7)

        if self.secret_key == "DEFAULT_UNSAFE_SECRET":
            logger.warning("⚠️ JWT is using a default UNSAFE key! Please configure security.jwt.secret_key.")

    def create_tokens(self, user_id: str, roles: list = None, extra_data: dict = None) -> Dict[str, str]:
        """
        登录成功后，同时签发 Access Token 和 Refresh Token
        :param user_id: 用户唯一标识
        :param roles: 用户角色列表 (如 ['admin', 'operator'])
        :param extra_data: 其他需要放入 Token 的非敏感数据
        :return: {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
        """
        if roles is None: roles = []
        if extra_data is None: extra_data = {}

        # 1. 生成 Access Token
        access_payload = {
            "sub": user_id,
            "roles": roles,
            "type": "access",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.access_expire_min),
            "iat": datetime.datetime.utcnow(),  # 签发时间
            **extra_data
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        # 2. 生成 Refresh Token (通常包含较少信息，只用于换取新 token)
        refresh_payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=self.refresh_expire_days),
            "iat": datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_expire_min * 60
        }

    def decode_token(self, token: str) -> Tuple[bool, Optional[dict], str]:
        """
        解析并验证 Token
        :param token: JWT 字符串
        :return: (is_valid, payload_dict, error_message)
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True, payload, "success"

        except jwt.ExpiredSignatureError:
            return False, None, "Token has expired"
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid token: {e}")
            return False, None, "Invalid token"
        except Exception as e:
            logger.error(f"Token decode error: {e}")
            return False, None, f"Decode error: {str(e)}"

    def verify_access_token(self, token: str) -> Optional[dict]:
        """
        校验 Access Token (用于接口鉴权中间件)
        :return: payload if valid, None otherwise
        """
        is_valid, payload, _ = self.decode_token(token)
        if is_valid and payload.get("type") == "access":
            return payload
        return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        使用 Refresh Token 换取新的 Access Token
        :return: New Access Token String or None
        """
        is_valid, payload, _ = self.decode_token(refresh_token)

        # 必须校验 token 类型是 refresh
        if is_valid and payload.get("type") == "refresh":
            user_id = payload["sub"]
            # 这里通常需要查库校验用户是否被封禁，或者 Refresh Token 是否被撤销
            # 为了简化演示，直接签发新的 Access Token
            # 注意：这里我们丢失了原来的 roles 信息，实际生产中建议查库重新获取 roles

            new_access_payload = {
                "sub": user_id,
                "roles": [],  # 建议查库获取
                "type": "access",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.access_expire_min),
                "iat": datetime.datetime.utcnow()
            }
            return jwt.encode(new_access_payload, self.secret_key, algorithm=self.algorithm)

        logger.warning(f"Refresh token validation failed for user: {payload.get('sub', 'unknown')}")
        return None


jwt_manager = JWTAuthManager()