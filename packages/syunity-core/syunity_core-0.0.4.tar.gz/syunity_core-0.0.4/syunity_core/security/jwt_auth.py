import jwt
import datetime
from typing import Dict, Optional, Tuple, List, Any

# 保持 logger 引用，用于记录错误
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

    def __init__(self,
                 secret_key: str = "DEFAULT_UNSAFE_SECRET",
                 algorithm: str = "HS256",
                 access_expire_min: int = 60,
                 refresh_expire_days: int = 7):
        """
        初始化管理器
        注意：在生产环境中，建议初始化后调用 configure() 方法注入安全的密钥和配置
        """
        # 防止单例重复初始化
        if not hasattr(self, '_initialized'):
            self.secret_key = secret_key
            self.algorithm = algorithm
            self.access_expire_min = access_expire_min
            self.refresh_expire_days = refresh_expire_days

            if self.secret_key == "DEFAULT_UNSAFE_SECRET":
                logger.warning(
                    "⚠️ JWT manager initialized with DEFAULT KEY. Please call .configure() with a secure key!")

            self._initialized = True

    def configure(self, secret_key: str, algorithm: str = "HS256",
                  access_expire_min: int = 60, refresh_expire_days: int = 7):
        """
        外部配置入口：用于在应用启动时注入真实配置
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_expire_min = access_expire_min
        self.refresh_expire_days = refresh_expire_days
        logger.info(f"✅ JWT Manager configured (Algo: {algorithm}, Access: {access_expire_min}m)")

    def create_tokens(self, user_id: str, roles: List[str] = None, extra_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        登录成功后，同时签发 Access Token 和 Refresh Token
        :param user_id: 用户唯一标识
        :param roles: 用户角色列表 (如 ['admin', 'operator'])
        :param extra_data: 其他需要放入 Token 的非敏感数据
        :return: {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
        """
        if roles is None: roles = []
        if extra_data is None: extra_data = {}

        now = datetime.datetime.now(datetime.timezone.utc)

        # 1. 生成 Access Token
        access_payload = {
            "sub": user_id,
            "roles": roles,
            "type": "access",
            "exp": now + datetime.timedelta(minutes=self.access_expire_min),
            "iat": now,
            **extra_data
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        # 2. 生成 Refresh Token (通常包含较少信息，只用于换取新 token)
        refresh_payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": now + datetime.timedelta(days=self.refresh_expire_days),
            "iat": now
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
            now = datetime.datetime.now(datetime.timezone.utc)

            # 注意：这里为了演示直接签发。生产环境中，建议在此处：
            # 1. 查库校验用户状态（是否被封禁）
            # 2. 重新获取用户最新的 roles 列表

            new_access_payload = {
                "sub": user_id,
                "roles": [],  # 建议从数据库重新获取
                "type": "access",
                "exp": now + datetime.timedelta(minutes=self.access_expire_min),
                "iat": now
            }
            return jwt.encode(new_access_payload, self.secret_key, algorithm=self.algorithm)

        logger.warning(f"Refresh token validation failed for token payload: {payload}")
        return None


# 创建全局实例 (使用默认不安全配置，请务必在启动时调用 configure)
jwt_manager = JWTAuthManager()