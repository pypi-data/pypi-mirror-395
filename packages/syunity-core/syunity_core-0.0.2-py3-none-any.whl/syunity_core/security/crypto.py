import base64
import os
import bcrypt
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from syunity_core.system.logger import logger


class CryptoManager:
    """
    [系统安全核心]
    负责：AES对称加密、Bcrypt密码哈希、RSA数字签名、文件完整性校验
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CryptoManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 防止重复初始化
        if not hasattr(self, '_initialized'):
            self._init_keys()
            self._initialized = True

    def _init_keys(self):
        """
        初始化密钥。
        在实际生产中，这里应该从 os.environ 获取 Master Key。
        为了测试方便，如果环境变量没有，我们自动生成一个。
        """
        env_key = os.getenv("SYUNITY_SECURITY_CRYPTO_MASTER_KEY")

        if env_key:
            try:
                self._fernet_key = env_key.encode('utf-8') if isinstance(env_key, str) else env_key
                self._fernet = Fernet(self._fernet_key)
                logger.info("🔒 CryptoManager initialized with provided Master Key.")
            except Exception as e:
                logger.critical(f"❌ Invalid Master Key provided: {e}")
                raise e
        else:
            logger.warning("⚠️ No Master Key found in ENV. Generating a temporary one (Data loss on restart!).")
            self._fernet_key = Fernet.generate_key()
            self._fernet = Fernet(self._fernet_key)

    # ==========================================
    # 1. 对称加密 (AES-Fernet) - 用于配置文件、敏感数据
    # ==========================================
    def encrypt_aes(self, plain_text: str) -> str:
        """加密字符串 -> 返回 Base64 密文"""
        if not plain_text: return ""
        try:
            cipher_bytes = self._fernet.encrypt(plain_text.encode('utf-8'))
            return cipher_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"AES Encrypt error: {e}")
            return ""

    def decrypt_aes(self, cipher_text: str) -> str:
        """解密字符串 -> 返回明文"""
        if not cipher_text: return ""
        try:
            plain_bytes = self._fernet.decrypt(cipher_text.encode('utf-8'))
            return plain_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"AES Decrypt error: {e}")
            return ""

    # ==========================================
    # 2. 密码哈希 (Bcrypt) - 用于用户登录
    # ==========================================
    def hash_password(self, plain_password: str, rounds: int = 12) -> str:
        """生成带盐哈希"""
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """校验密码"""
        try:
            # bcrypt.checkpw 需要 bytes
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    # ==========================================
    # 3. 非对称加密 (RSA) - 用于数字签名/License
    # ==========================================
    def generate_rsa_key_pair(self):
        """(工具方法) 生成一对公私钥 PEM 格式，仅用于测试或初始配置"""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return priv_pem, pub_pem

    def sign_data(self, data: str, private_key_pem: bytes) -> str:
        """使用私钥签名 -> 返回 Base64 签名串"""
        try:
            private_key = serialization.load_pem_private_key(private_key_pem, password=None)
            signature = private_key.sign(
                data.encode('utf-8'),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            logger.error(f"RSA Sign failed: {e}")
            return ""

    def verify_signature(self, data: str, signature_b64: str, public_key_pem: bytes) -> bool:
        """使用公钥验签 -> 返回 True/False"""
        try:
            public_key = serialization.load_pem_public_key(public_key_pem)
            signature = base64.b64decode(signature_b64)
            public_key.verify(
                signature,
                data.encode('utf-8'),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            logger.warning(f"RSA Verify failed: {e}")
            return False

    # ==========================================
    # 4. 完整性校验 (Hash) - 用于文件/报文
    # ==========================================
    def get_string_checksum(self, content: str) -> str:
        """计算字符串 SHA256"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


# 导出单例
crypto_manager = CryptoManager()