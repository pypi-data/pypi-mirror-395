"""
带填充的缓冲块密码

此类包装一个BlockCipher并应用填充，使其能够处理任意长度的数据。

参考: org.bouncycastle.crypto.paddings.PaddedBufferedBlockCipher
"""

from typing import Any
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.exceptions.data_length_exception import DataLengthException
from sm_bc.exceptions.invalid_cipher_text_exception import InvalidCipherTextException


class PaddedBufferedBlockCipher:
    """带填充的缓冲块密码"""
    
    def __init__(self, cipher: Any, padding: Any):
        """
        构造函数
        
        Args:
            cipher: 底层块密码
            padding: 填充方案
        """
        self.cipher = cipher
        self.padding = padding
        self.buf = bytearray(cipher.get_block_size())
        self.buf_off = 0
        self.for_encryption = False
    
    def get_underlying_cipher(self) -> Any:
        """获取底层密码"""
        return self.cipher
    
    def init(self, encrypting: bool, params: CipherParameters) -> None:
        """
        初始化密码
        
        Args:
            encrypting: True 表示加密，False 表示解密
            params: 密码参数
        """
        self.for_encryption = encrypting
        self.reset()
        self.cipher.init(encrypting, params)
    
    def get_block_size(self) -> int:
        """返回块大小"""
        return self.cipher.get_block_size()
    
    def get_output_size(self, length: int) -> int:
        """
        获取输出大小
        
        Args:
            length: 输入长度
            
        Returns:
            输出将需要的字节数
        """
        total = length + self.buf_off
        left_over = total % len(self.buf)
        
        if left_over == 0:
            if self.for_encryption:
                return total + len(self.buf)
            return total
        
        return total - left_over + len(self.buf)
    
    def get_update_output_size(self, length: int) -> int:
        """
        获取可更新输出大小
        
        Args:
            length: 输入长度
            
        Returns:
            更新时将产生的字节数
        """
        total = length + self.buf_off
        left_over = total % len(self.buf)
        return total - left_over
    
    def process_byte(self, input_byte: int, output: bytearray, out_off: int) -> int:
        """
        处理一个字节
        
        Args:
            input_byte: 输入字节
            output: 输出缓冲区
            out_off: 输出偏移量
            
        Returns:
            写入输出的字节数
        """
        result_len = 0
        
        self.buf[self.buf_off] = input_byte
        self.buf_off += 1
        
        if self.buf_off == len(self.buf):
            result_len = self.cipher.process_block(self.buf, 0, output, out_off)
            self.buf_off = 0
        
        return result_len
    
    def process_bytes(
        self,
        input_data: bytes,
        in_off: int,
        length: int,
        output: bytearray,
        out_off: int
    ) -> int:
        """
        处理字节数组
        
        Args:
            input_data: 输入数据
            in_off: 输入偏移量
            length: 要处理的字节数
            output: 输出缓冲区
            out_off: 输出偏移量
            
        Returns:
            写入输出的字节数
        """
        if length < 0:
            raise ValueError('Cannot have a negative input length')
        
        block_size = self.get_block_size()
        gap_len = len(self.buf) - self.buf_off
        
        if length > gap_len:
            self.buf[self.buf_off:self.buf_off + gap_len] = input_data[in_off:in_off + gap_len]
            
            result_len = self.cipher.process_block(self.buf, 0, output, out_off)
            
            self.buf_off = 0
            length -= gap_len
            in_off += gap_len
            
            while length > len(self.buf):
                result_len += self.cipher.process_block(input_data, in_off, output, out_off + result_len)
                
                length -= block_size
                in_off += block_size
            
            self.buf[self.buf_off:self.buf_off + length] = input_data[in_off:in_off + length]
            
            self.buf_off += length
            
            return result_len
        else:
            self.buf[self.buf_off:self.buf_off + length] = input_data[in_off:in_off + length]
            
            self.buf_off += length
            
            return 0
    
    def do_final(self, output: bytearray, out_off: int) -> int:
        """
        完成处理
        
        Args:
            output: 输出缓冲区
            out_off: 输出偏移量
            
        Returns:
            写入输出的字节数
        """
        block_size = self.cipher.get_block_size()
        result_len = 0
        
        if self.for_encryption:
            if self.buf_off == block_size:
                if out_off + 2 * block_size > len(output):
                    self.reset()
                    raise DataLengthException('output buffer too short')
                
                result_len = self.cipher.process_block(self.buf, 0, output, out_off)
                self.buf_off = 0
            
            self.padding.add_padding(self.buf, self.buf_off)
            
            result_len += self.cipher.process_block(self.buf, 0, output, out_off + result_len)
            
            self.reset()
        else:
            if self.buf_off == block_size:
                result_len = self.cipher.process_block(self.buf, 0, self.buf, 0)
                self.buf_off = 0
            else:
                self.reset()
                raise DataLengthException('last block incomplete in decryption')
            
            try:
                count = self.padding.pad_count(self.buf)
                
                result_len -= count
                
                output[out_off:out_off + result_len] = self.buf[0:result_len]
            except Exception as e:
                self.reset()
                if isinstance(e, (DataLengthException, InvalidCipherTextException)):
                    raise
                raise InvalidCipherTextException(str(e))
            finally:
                self.reset()
        
        return result_len
    
    def reset(self) -> None:
        """重置密码到初始状态"""
        for i in range(len(self.buf)):
            self.buf[i] = 0
        self.buf_off = 0
        
        self.cipher.reset()
