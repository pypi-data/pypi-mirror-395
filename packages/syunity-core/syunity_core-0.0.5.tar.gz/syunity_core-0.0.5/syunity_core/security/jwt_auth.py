import jwt, datetime
from syunity_core.system.logger import logger


class JWTAuthManager:
    """JWT认证管理：签发与校验 (Access + Refresh)"""
    _inst = None

    def __new__(cls):
        if not cls._inst:
            cls._inst = super().__new__(cls)
            # 默认配置，请通过 cfg() 方法覆盖
            cls._inst.k, cls._inst.alg, cls._inst.exp_m, cls._inst.ref_d = "UNSAFE", "HS256", 60, 7
        return cls._inst

    def cfg(self, key: str, alg="HS256", exp_m=60, ref_d=7):
        """配置密钥与过期时间"""
        self.k, self.alg, self.exp_m, self.ref_d = key, alg, exp_m, ref_d

    def create(self, uid: str, roles: list = None, extra: dict = None) -> dict:
        """生成 Access/Refresh Token 对"""
        now = datetime.datetime.now(datetime.timezone.utc)
        base = {"sub": uid, "iat": now, **(extra or {})}

        # Access Token (含角色，短效)
        acc = jwt.encode(
            {**base, "roles": roles or [], "type": "acc", "exp": now + datetime.timedelta(minutes=self.exp_m)}, self.k,
            self.alg)
        # Refresh Token (仅ID，长效)
        ref = jwt.encode({**base, "type": "ref", "exp": now + datetime.timedelta(days=self.ref_d)}, self.k, self.alg)

        return {"access_token": acc, "refresh_token": ref, "token_type": "bearer"}

    def verify(self, token: str, type_chk: str = None) -> dict:
        """校验并解析 Token，失败返回 None"""
        try:
            load = jwt.decode(token, self.k, algorithms=[self.alg])
            return load if not type_chk or load.get("type") == type_chk else None
        except Exception as e:
            logger.debug(f"JWT Verify Fail: {e}")
            return None

    def refresh(self, ref_token: str) -> str:
        """用 Refresh Token 换新 Access Token"""
        p = self.verify(ref_token, "ref")
        if not p: return None
        # 注意：此处应重新查库获取最新角色，这里简化处理
        now = datetime.datetime.now(datetime.timezone.utc)
        return jwt.encode(
            {"sub": p["sub"], "roles": [], "type": "acc", "exp": now + datetime.timedelta(minutes=self.exp_m),
             "iat": now}, self.k, self.alg)


jwt_manager = JWTAuthManager()