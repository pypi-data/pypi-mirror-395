"""
Cipher Feedback (CFB) mode.

Reference: org.bouncycastle.crypto.modes.CFBBlockCipher
           src/crypto/modes/CFBBlockCipher.ts (sm-js-bc)
"""

from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.parameters_with_iv import ParametersWithIV
from sm_bc.exceptions import DataLengthException


class CFBBlockCipher:
    """
    Cipher Feedback (CFB) mode implementation.
    
    In CFB mode, the previous ciphertext block is encrypted and XORed with
    the plaintext to produce the ciphertext. This makes CFB a self-synchronizing
    stream cipher.
    
    Key characteristics:
    - Converts block cipher into stream cipher
    - Self-synchronizing (recovers from bit errors)
    - Encryption of previous ciphertext provides keystream
    - Different encrypt/decrypt logic
    
    Reference: NIST SP 800-38A
    """
    
    def __init__(self, cipher, bit_block_size: int):
        """
        Create a CFB mode cipher.
        
        Args:
            cipher: The block cipher to use as the basis of the feedback mode
            bit_block_size: The block size in bits (must be multiple of 8,
                          between 8 and cipher block size * 8)
        
        Raises:
            ValueError: If bit_block_size is invalid
        """
        cipher_block_size = cipher.get_block_size()
        
        if (bit_block_size > cipher_block_size * 8 or 
            bit_block_size < 8 or 
            bit_block_size % 8 != 0):
            raise ValueError(f'CFB{bit_block_size} not supported')
        
        self.cipher = cipher
        self.cipher_block_size = cipher_block_size
        self.block_size = bit_block_size // 8
        
        self.IV = bytearray(cipher_block_size)
        self.cfb_v = bytearray(cipher_block_size)  # Feedback register
        self.cfb_out_v = bytearray(cipher_block_size)  # Encrypted output
        self.in_buf = bytearray(self.block_size)  # Input buffer
        
        self.encrypting = False
        self.byte_count = 0
    
    def get_underlying_cipher(self):
        """
        Return the underlying block cipher.
        
        Returns:
            The underlying block cipher
        """
        return self.cipher
    
    def init(self, for_encryption: bool, params: CipherParameters) -> None:
        """
        Initialize the cipher and possibly the IV.
        
        Args:
            for_encryption: True for encryption, False for decryption
            params: The key and other data required by the cipher
        """
        self.encrypting = for_encryption
        
        if isinstance(params, ParametersWithIV):
            iv_param = params
            iv = iv_param.get_iv()
            
            if len(iv) < len(self.IV):
                # Prepend the supplied IV with zeros (per FIPS PUB 81)
                for i in range(len(self.IV) - len(iv)):
                    self.IV[i] = 0
                self.IV[len(self.IV) - len(iv):] = iv
            else:
                self.IV[:] = iv[:len(self.IV)]
            
            self.reset()
            
            # If None, it's an IV change only
            underlying_params = iv_param.get_parameters()
            if underlying_params is not None:
                # CFB always encrypts, even in decryption mode
                self.cipher.init(True, underlying_params)
        else:
            self.reset()
            
            # If it's not None, key is to be reused
            if params is not None:
                # CFB always encrypts
                self.cipher.init(True, params)
    
    def get_algorithm_name(self) -> str:
        """
        Return the algorithm name and mode.
        
        Returns:
            The name of the underlying algorithm followed by "/CFB" and block size
        """
        return f'{self.cipher.get_algorithm_name()}/CFB{self.block_size * 8}'
    
    def get_block_size(self) -> int:
        """
        Return the block size we are operating at.
        
        Returns:
            The block size in bytes
        """
        return self.block_size
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int,
                     output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process one block of input.
        
        Args:
            input_data: The input buffer
            in_off: Offset into the input array where data starts
            output: The output buffer
            out_off: Offset into the output array where result will be written
            
        Returns:
            The number of bytes processed
        """
        self.process_bytes(input_data, in_off, self.block_size, output, out_off)
        return self.block_size
    
    def process_bytes(self, input_data: Union[bytes, bytearray], in_off: int,
                     length: int, output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process bytes in CFB mode.
        
        Args:
            input_data: The input data
            in_off: Offset into the input array
            length: Number of bytes to process
            output: The output buffer
            out_off: Offset into the output array
            
        Returns:
            The number of bytes processed
            
        Raises:
            DataLengthException: If buffer too short
        """
        if in_off + length > len(input_data):
            raise DataLengthException('input buffer too small')
        
        if out_off + length > len(output):
            raise DataLengthException('output buffer too short')
        
        for i in range(length):
            if self.encrypting:
                output[out_off + i] = self._encrypt_byte(input_data[in_off + i])
            else:
                output[out_off + i] = self._decrypt_byte(input_data[in_off + i])
        
        return length
    
    def reset(self) -> None:
        """Reset the chaining vector back to the IV and reset the underlying cipher."""
        self.cfb_v[:] = self.IV
        for i in range(len(self.in_buf)):
            self.in_buf[i] = 0
        self.byte_count = 0
        self.cipher.reset()
    
    def get_current_iv(self) -> bytearray:
        """
        Return the current state of the initialization vector.
        
        Returns:
            Copy of current IV
        """
        return bytearray(self.cfb_v)
    
    def _encrypt_byte(self, input_byte: int) -> int:
        """
        Encrypt a single byte.
        
        Args:
            input_byte: The byte to encrypt
            
        Returns:
            The encrypted byte
        """
        if self.byte_count == 0:
            self.cipher.process_block(self.cfb_v, 0, self.cfb_out_v, 0)
        
        rv = self.cfb_out_v[self.byte_count] ^ input_byte
        self.in_buf[self.byte_count] = rv
        self.byte_count += 1
        
        if self.byte_count == self.block_size:
            self.byte_count = 0
            
            # Shift cfb_v left by block_size bytes
            self.cfb_v[:len(self.cfb_v) - self.block_size] = \
                self.cfb_v[self.block_size:]
            # Copy in_buf to the end of cfb_v
            self.cfb_v[len(self.cfb_v) - self.block_size:] = self.in_buf
        
        return rv
    
    def _decrypt_byte(self, input_byte: int) -> int:
        """
        Decrypt a single byte.
        
        Args:
            input_byte: The byte to decrypt
            
        Returns:
            The decrypted byte
        """
        if self.byte_count == 0:
            self.cipher.process_block(self.cfb_v, 0, self.cfb_out_v, 0)
        
        self.in_buf[self.byte_count] = input_byte
        rv = self.cfb_out_v[self.byte_count] ^ input_byte
        self.byte_count += 1
        
        if self.byte_count == self.block_size:
            self.byte_count = 0
            
            # Shift cfb_v left by block_size bytes
            self.cfb_v[:len(self.cfb_v) - self.block_size] = \
                self.cfb_v[self.block_size:]
            # Copy in_buf to the end of cfb_v
            self.cfb_v[len(self.cfb_v) - self.block_size:] = self.in_buf
        
        return rv
