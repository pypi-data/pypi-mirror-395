"""
Cipher Block Chaining (CBC) mode.

Reference: org.bouncycastle.crypto.modes.CBCBlockCipher
           src/crypto/modes/CBCBlockCipher.ts (sm-js-bc)
"""

from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.parameters_with_iv import ParametersWithIV
from sm_bc.exceptions import DataLengthException


class CBCBlockCipher:
    """
    Cipher Block Chaining (CBC) mode implementation.
    
    CBC mode chains blocks together by XORing each plaintext block with the
    previous ciphertext block before encryption. The first block is XORed with
    the initialization vector (IV).
    
    Reference: NIST SP 800-38A
    """
    
    def __init__(self, cipher):
        """
        Initialize CBC mode with a block cipher.
        
        Args:
            cipher: The underlying block cipher (must implement BlockCipher interface)
        """
        self.cipher = cipher
        self.block_size = cipher.get_block_size()
        
        self.IV = bytearray(self.block_size)
        self.cbcV = bytearray(self.block_size)
        self.cbcNextV = bytearray(self.block_size)
        
        self.encrypting = False
    
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
        
        If an IV isn't passed as part of the parameter, the IV will be all zeros.
        
        Args:
            for_encryption: True for encryption, False for decryption
            params: The key and other data required by the cipher
            
        Raises:
            ValueError: If IV length doesn't match block size
        """
        old_encrypting = self.encrypting
        self.encrypting = for_encryption
        
        if isinstance(params, ParametersWithIV):
            iv = params.get_iv()
            
            if len(iv) != self.block_size:
                raise ValueError('initialization vector must be the same length as block size')
            
            self.IV[:] = iv
            params = params.get_parameters()
        else:
            # No IV provided, use all zeros
            for i in range(len(self.IV)):
                self.IV[i] = 0
        
        self.reset()
        
        # If params is None, it's an IV change only (key is to be reused)
        if params is not None:
            self.cipher.init(for_encryption, params)
        elif old_encrypting != for_encryption:
            raise ValueError('cannot change encrypting state without providing key')
    
    def get_algorithm_name(self) -> str:
        """
        Return the algorithm name and mode.
        
        Returns:
            The name of the underlying algorithm followed by "/CBC"
        """
        return self.cipher.get_algorithm_name() + '/CBC'
    
    def get_block_size(self) -> int:
        """
        Return the block size of the underlying cipher.
        
        Returns:
            The block size in bytes
        """
        return self.cipher.get_block_size()
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int,
                     output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process one block of input.
        
        Args:
            input_data: The array containing the input data
            in_off: Offset into the input array where data starts
            output: The array the output data will be copied into
            out_off: The offset into the output array where output will start
            
        Returns:
            The number of bytes processed and produced
            
        Raises:
            DataLengthException: If buffer too short
        """
        if self.encrypting:
            return self._encrypt_block(input_data, in_off, output, out_off)
        else:
            return self._decrypt_block(input_data, in_off, output, out_off)
    
    def reset(self) -> None:
        """Reset the chaining vector back to the IV and reset the underlying cipher."""
        self.cbcV[:] = self.IV
        for i in range(len(self.cbcNextV)):
            self.cbcNextV[i] = 0
        self.cipher.reset()
    
    def _encrypt_block(self, input_data: Union[bytes, bytearray], in_off: int,
                      output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Do the appropriate chaining step for CBC mode encryption.
        
        Args:
            input_data: The array containing the data to be encrypted
            in_off: Offset into the input array where data starts
            output: The array the encrypted data will be copied into
            out_off: The offset into the output array where output will start
            
        Returns:
            The number of bytes processed and produced
            
        Raises:
            DataLengthException: If input buffer too short
        """
        if in_off + self.block_size > len(input_data):
            raise DataLengthException('input buffer too short')
        
        # XOR the cbcV and the input, then encrypt the cbcV
        for i in range(self.block_size):
            self.cbcV[i] ^= input_data[in_off + i]
        
        length = self.cipher.process_block(self.cbcV, 0, output, out_off)
        
        # Copy ciphertext to cbcV
        self.cbcV[:] = output[out_off:out_off + self.block_size]
        
        return length
    
    def _decrypt_block(self, input_data: Union[bytes, bytearray], in_off: int,
                      output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Do the appropriate chaining step for CBC mode decryption.
        
        Args:
            input_data: The array containing the data to be decrypted
            in_off: Offset into the input array where data starts
            output: The array the decrypted data will be copied into
            out_off: The offset into the output array where output will start
            
        Returns:
            The number of bytes processed and produced
            
        Raises:
            DataLengthException: If input buffer too short
        """
        if in_off + self.block_size > len(input_data):
            raise DataLengthException('input buffer too short')
        
        # Save the ciphertext block for next round
        self.cbcNextV[:] = input_data[in_off:in_off + self.block_size]
        
        length = self.cipher.process_block(input_data, in_off, output, out_off)
        
        # XOR the cbcV and the output
        for i in range(self.block_size):
            output[out_off + i] ^= self.cbcV[i]
        
        # Swap the back up buffer into next position
        tmp = self.cbcV
        self.cbcV = self.cbcNextV
        self.cbcNextV = tmp
        
        return length
