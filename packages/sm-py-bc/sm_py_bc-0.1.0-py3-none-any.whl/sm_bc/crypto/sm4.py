"""
SM4 高级 API - 提供便捷的加密/解密接口

SM4 是一个 128 位分组密码算法，使用 128 位密钥

标准: GB/T 32907-2016

Example:
    >>> from sm_bc.crypto.sm4 import SM4
    >>> 
    >>> # 生成密钥
    >>> key = SM4.generate_key()
    >>> 
    >>> # 加密数据（ECB模式）
    >>> plaintext = b'Hello, SM4!'
    >>> ciphertext = SM4.encrypt(plaintext, key)
    >>> 
    >>> # 解密数据
    >>> decrypted = SM4.decrypt(ciphertext, key)
    >>> assert decrypted == plaintext
"""

import os
from .engines.sm4_engine import SM4Engine
from .params.key_parameter import KeyParameter


class SM4:
    """SM4 高级API"""
    
    KEY_SIZE = 16  # 128位 = 16字节
    BLOCK_SIZE = 16  # 128位 = 16字节

    @staticmethod
    def generate_key() -> bytes:
        """
        生成随机的 SM4 密钥（128位）
        
        Returns:
            16字节的随机密钥
        """
        return os.urandom(SM4.KEY_SIZE)

    @staticmethod
    def encrypt(plaintext: bytes, key: bytes) -> bytes:
        """
        加密数据（ECB模式，PKCS7填充）
        
        注意：ECB模式不安全，仅用于演示和兼容性测试。
        生产环境请使用 CBC、CTR 或 GCM 模式。
        
        Args:
            plaintext: 明文数据
            key: 128位密钥
            
        Returns:
            密文数据（包含填充）
            
        Raises:
            ValueError: 如果密钥长度不是16字节
        """
        if len(key) != SM4.KEY_SIZE:
            raise ValueError('SM4 requires a 128 bit (16 byte) key')

        # 应用 PKCS7 填充
        padded_data = SM4._pkcs7_padding(plaintext, SM4.BLOCK_SIZE)

        # 创建引擎并初始化
        engine = SM4Engine()
        engine.init(True, KeyParameter(key))

        # 加密所有块
        ciphertext = bytearray(len(padded_data))
        for i in range(0, len(padded_data), SM4.BLOCK_SIZE):
            engine.process_block(padded_data, i, ciphertext, i)

        return bytes(ciphertext)

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes) -> bytes:
        """
        解密数据（ECB模式，PKCS7填充）
        
        Args:
            ciphertext: 密文数据
            key: 128位密钥
            
        Returns:
            明文数据（已移除填充）
            
        Raises:
            ValueError: 如果密钥长度不是16字节或密文长度不是块大小的倍数
        """
        if len(key) != SM4.KEY_SIZE:
            raise ValueError('SM4 requires a 128 bit (16 byte) key')

        if len(ciphertext) % SM4.BLOCK_SIZE != 0:
            raise ValueError('Ciphertext length must be a multiple of block size (16 bytes)')

        # 创建引擎并初始化
        engine = SM4Engine()
        engine.init(False, KeyParameter(key))

        # 解密所有块
        padded_data = bytearray(len(ciphertext))
        for i in range(0, len(ciphertext), SM4.BLOCK_SIZE):
            engine.process_block(ciphertext, i, padded_data, i)

        # 移除 PKCS7 填充
        return SM4._pkcs7_unpadding(bytes(padded_data))

    @staticmethod
    def encrypt_block(block: bytes, key: bytes) -> bytes:
        """
        加密单个块（无填充）
        
        适用于需要直接控制加密过程的场景。
        输入数据必须正好是 16 字节。
        
        Args:
            block: 16字节的数据块
            key: 128位密钥
            
        Returns:
            16字节的加密块
            
        Raises:
            ValueError: 如果块大小不是16字节或密钥长度不是16字节
        """
        if len(block) != SM4.BLOCK_SIZE:
            raise ValueError('Block must be exactly 16 bytes')

        if len(key) != SM4.KEY_SIZE:
            raise ValueError('SM4 requires a 128 bit (16 byte) key')

        engine = SM4Engine()
        engine.init(True, KeyParameter(key))

        output = bytearray(SM4.BLOCK_SIZE)
        engine.process_block(block, 0, output, 0)

        return bytes(output)

    @staticmethod
    def decrypt_block(block: bytes, key: bytes) -> bytes:
        """
        解密单个块（无填充）
        
        Args:
            block: 16字节的加密块
            key: 128位密钥
            
        Returns:
            16字节的明文块
            
        Raises:
            ValueError: 如果块大小不是16字节或密钥长度不是16字节
        """
        if len(block) != SM4.BLOCK_SIZE:
            raise ValueError('Block must be exactly 16 bytes')

        if len(key) != SM4.KEY_SIZE:
            raise ValueError('SM4 requires a 128 bit (16 byte) key')

        engine = SM4Engine()
        engine.init(False, KeyParameter(key))

        output = bytearray(SM4.BLOCK_SIZE)
        engine.process_block(block, 0, output, 0)

        return bytes(output)

    @staticmethod
    def _pkcs7_padding(data: bytes, block_size: int) -> bytes:
        """
        PKCS7 填充
        
        Args:
            data: 原始数据
            block_size: 块大小
            
        Returns:
            填充后的数据
        """
        padding_length = block_size - (len(data) % block_size)
        padded_data = bytearray(data)
        
        # 填充字节的值等于填充长度
        padded_data.extend([padding_length] * padding_length)
        
        return bytes(padded_data)

    @staticmethod
    def _pkcs7_unpadding(data: bytes) -> bytes:
        """
        移除 PKCS7 填充
        
        Args:
            data: 填充后的数据
            
        Returns:
            原始数据
            
        Raises:
            ValueError: 如果填充无效
        """
        if len(data) == 0:
            raise ValueError('Cannot unpad empty data')

        padding_length = data[-1]

        # 验证填充
        if padding_length < 1 or padding_length > SM4.BLOCK_SIZE:
            raise ValueError('Invalid padding')

        # 检查所有填充字节是否正确
        for i in range(len(data) - padding_length, len(data)):
            if data[i] != padding_length:
                raise ValueError('Invalid padding')

        return data[:len(data) - padding_length]
