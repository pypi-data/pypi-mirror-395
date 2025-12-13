import base64
import logging
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

logger = logging.getLogger("SecretUtil")


class SecretUtil:
    """加密工具类，支持AES-CBC加密解密"""
    
    def __init__(self, secret_key=None):
        """
        初始化加密工具
        
        Args:
            secret_key: 加密密钥，如果为None则从环境变量获取
        """
        self.secret_key = secret_key or self._get_default_key()
        # 确保密钥长度为16, 24, 或32字节
        if len(self.secret_key) not in [16, 24, 32]:
            raise ValueError("密钥长度必须为16, 24或32字节")
    
    def _get_default_key(self):
        """获取默认密钥"""
        key = os.getenv('PLUGIN_SECRET_KEY')
        if not key:
            # 生成默认密钥（仅用于开发环境）
            key = "default_secret_key_32bytes!!"
            logger.warning("使用默认密钥，生产环境请设置PLUGIN_SECRET_KEY环境变量")
        return key.encode('utf-8') if isinstance(key, str) else key
    
    def set_key(self, new_key):
        """设置新的加密密钥"""
        if len(new_key) not in [16, 24, 32]:
            raise ValueError("密钥长度必须为16, 24或32字节")
        self.secret_key = new_key.encode('utf-8') if isinstance(new_key, str) else new_key
    
    def encrypt_data(self, plain_data):
        """
        加密数据
        
        Args:
            plain_data: 原始数据（字符串或可序列化对象）
            
        Returns:
            str: 加密后的Base64编码数据，失败返回None
        """
        try:
            # 如果数据不是字符串，先转换为JSON字符串
            if not isinstance(plain_data, str):
                import json
                plain_data = json.dumps(plain_data, ensure_ascii=False)
            
            # 生成随机IV
            iv = os.urandom(16)
            
            # 创建AES加密器
            cipher = AES.new(self.secret_key, AES.MODE_CBC, iv)
            
            # 对数据进行填充并加密
            padded_data = pad(plain_data.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            
            # 将IV和加密数据合并，并进行Base64编码
            combined = iv + encrypted
            return base64.b64encode(combined).decode('utf-8')
            
        except Exception as e:
            logger.error(f"数据加密失败: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        """
        解密数据
        
        Args:
            encrypted_data: 加密的Base64编码数据
            
        Returns:
            str: 解密后的数据，失败返回None
        """
        try:
            # 解码Base64数据
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # 提取IV和实际加密数据
            iv = encrypted_bytes[:16]
            ciphertext = encrypted_bytes[16:]
            
            # 创建AES解密器
            cipher = AES.new(self.secret_key, AES.MODE_CBC, iv)
            
            # 解密并去除填充
            decrypted = cipher.decrypt(ciphertext)
            unpadded = unpad(decrypted, AES.block_size)
            
            # 返回解密后的字符串
            return unpadded.decode('utf-8')
            
        except Exception as e:
            logger.error(f"数据解密失败: {e}")
            return None
