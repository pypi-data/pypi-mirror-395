"""
ECB (Electronic Codebook) 模式实现

警告：ECB 模式不安全，不应在生产环境中使用。
相同的明文块总是加密为相同的密文块，这会泄露信息模式。

此实现仅用于：
- 与旧系统的兼容性
- 测试和教学目的

参考: org.bouncycastle.crypto.modes.ECBBlockCipher
"""

from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.exceptions import DataLengthException


class ECBBlockCipher:
    """ECB模式块密码"""

    def __init__(self, cipher):
        """
        初始化ECB模式
        
        Args:
            cipher: 底层块密码
        """
        self.cipher = cipher
        self.block_size = cipher.get_block_size()

    def get_underlying_cipher(self):
        """返回底层密码"""
        return self.cipher

    def init(self, encrypting: bool, params: CipherParameters) -> None:
        """
        初始化密码
        
        Args:
            encrypting: True表示加密，False表示解密
            params: 密码参数
        """
        self.cipher.init(encrypting, params)

    def get_algorithm_name(self) -> str:
        """返回算法名称"""
        return self.cipher.get_algorithm_name() + '/ECB'

    def get_block_size(self) -> int:
        """返回块大小（字节）"""
        return self.block_size

    def process_block(
        self,
        input_bytes: bytes,
        in_off: int,
        output: bytearray,
        out_off: int
    ) -> int:
        """
        处理一个数据块
        
        Args:
            input_bytes: 输入数据
            in_off: 输入偏移量
            output: 输出缓冲区
            out_off: 输出偏移量
            
        Returns:
            处理的字节数
        """
        if in_off + self.block_size > len(input_bytes):
            raise DataLengthException('input buffer too short')

        if out_off + self.block_size > len(output):
            raise DataLengthException('output buffer too short')

        return self.cipher.process_block(input_bytes, in_off, output, out_off)

    def reset(self) -> None:
        """重置密码到初始状态"""
        self.cipher.reset()
