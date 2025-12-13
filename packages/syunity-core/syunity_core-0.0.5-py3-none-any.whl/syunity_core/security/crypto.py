import os, base64, bcrypt, hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class CryptoManager:
    """核心安全组件：AES加密、Bcrypt哈希、RSA签名、SHA256校验"""
    _inst = None

    def __new__(cls):
        if not cls._inst:
            cls._inst = super().__new__(cls)
            key = os.getenv("SYUNITY_SECURITY_CRYPTO_MASTER_KEY")
            cls._inst.f = Fernet(key.encode() if key else Fernet.generate_key())
        return cls._inst

    # --- AES对称加密 ---
    def encrypt_aes(self, txt: str) -> str:
        try: return self.f.encrypt(txt.encode()).decode() if txt else ""
        except: return ""

    def decrypt_aes(self, txt: str) -> str:
        """解密Base64密文 -> 明文 (修复：解密失败返回空串，不抛异常)"""
        try: return self.f.decrypt(txt.encode()).decode() if txt else ""
        except: return ""  # <--- 这里捕获 InvalidToken 异常

    # --- Bcrypt哈希 ---
    def hash_pwd(self, pwd: str) -> str:
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

    def verify_pwd(self, pwd: str, hashed: str) -> bool:
        try: return bcrypt.checkpw(pwd.encode(), hashed.encode())
        except: return False

    # --- RSA非对称加密 ---
    def gen_rsa_keys(self):
        k = rsa.generate_private_key(65537, 2048)
        return (k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()),
                k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

    def sign(self, data: str, priv_pem: bytes) -> str:
        try:
            k = serialization.load_pem_private_key(priv_pem, None)
            return base64.b64encode(k.sign(data.encode(), padding.PSS(padding.MGF1(hashes.SHA256()), padding.PSS.MAX_LENGTH), hashes.SHA256())).decode()
        except: return ""

    def verify(self, data: str, sig_b64: str, pub_pem: bytes) -> bool:
        try:
            serialization.load_pem_public_key(pub_pem).verify(base64.b64decode(sig_b64), data.encode(), padding.PSS(padding.MGF1(hashes.SHA256()), padding.PSS.MAX_LENGTH), hashes.SHA256())
            return True
        except: return False

    # --- 完整性校验 ---
    def checksum(self, txt: str) -> str:
        return hashlib.sha256(txt.encode()).hexdigest()

crypto_manager = CryptoManager()