"""
Segmented Integer Counter (SIC) mode, also known as CTR mode.

Reference: org.bouncycastle.crypto.modes.SICBlockCipher
           src/crypto/modes/SICBlockCipher.ts (sm-js-bc)
"""

from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.parameters_with_iv import ParametersWithIV
from sm_bc.exceptions import DataLengthException


class SICBlockCipher:
    """
    Counter (CTR) mode implementation, also known as SIC mode.
    
    CTR mode turns a block cipher into a stream cipher by encrypting a counter
    and XORing the result with the plaintext. The counter is incremented for
    each block.
    
    Note: CTR mode uses encryption for both encryption and decryption operations.
    
    Reference: NIST SP 800-38A
    """
    
    def __init__(self, cipher):
        """
        Initialize CTR/SIC mode with a block cipher.
        
        Args:
            cipher: The underlying block cipher
        """
        self.cipher = cipher
        self.block_size = cipher.get_block_size()
        
        self.IV = bytearray(self.block_size)
        self.counter = bytearray(self.block_size)
        self.counter_out = bytearray(self.block_size)
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
        Initialize the cipher.
        
        Note: for_encryption is ignored by CTR mode (always encrypts the counter)
        
        Args:
            for_encryption: Ignored (CTR uses encryption for both directions)
            params: Must be ParametersWithIV containing key and IV
            
        Raises:
            ValueError: If params is not ParametersWithIV or IV has invalid length
        """
        if not isinstance(params, ParametersWithIV):
            raise ValueError('CTR/SIC mode requires ParametersWithIV')
        
        iv_param = params
        self.IV = bytearray(iv_param.get_iv())
        
        if self.block_size < len(self.IV):
            raise ValueError(f'CTR/SIC mode requires IV no greater than: {self.block_size} bytes')
        
        max_counter_size = min(8, self.block_size // 2)
        
        if self.block_size - len(self.IV) > max_counter_size:
            raise ValueError(f'CTR/SIC mode requires IV of at least: {self.block_size - max_counter_size} bytes')
        
        # If None it's an IV change only
        underlying_params = iv_param.get_parameters()
        if underlying_params is not None:
            self.cipher.init(True, underlying_params)
        
        self.reset()
    
    def get_algorithm_name(self) -> str:
        """
        Return the algorithm name and mode.
        
        Returns:
            The name followed by "/SIC" (or "/CTR")
        """
        return self.cipher.get_algorithm_name() + '/SIC'
    
    def get_block_size(self) -> int:
        """
        Return the block size.
        
        Returns:
            The block size in bytes
        """
        return self.cipher.get_block_size()
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int,
                     output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process one block of input.
        
        Args:
            input_data: Input data
            in_off: Offset in input
            output: Output buffer
            out_off: Offset in output
            
        Returns:
            Number of bytes processed
            
        Raises:
            DataLengthException: If buffer too short
        """
        if self.byte_count != 0:
            return self.process_bytes(input_data, in_off, self.block_size, output, out_off)
        
        if in_off + self.block_size > len(input_data):
            raise DataLengthException('input buffer too small')
        
        if out_off + self.block_size > len(output):
            raise DataLengthException('output buffer too short')
        
        # Check counter before using it
        self._check_last_increment()
        
        self.cipher.process_block(self.counter, 0, self.counter_out, 0)
        
        for i in range(self.block_size):
            output[out_off + i] = input_data[in_off + i] ^ self.counter_out[i]
        
        self._increment_counter()
        
        return self.block_size
    
    def process_bytes(self, input_data: Union[bytes, bytearray], in_off: int,
                     length: int, output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process bytes (stream mode).
        
        Args:
            input_data: Input data
            in_off: Offset in input
            length: Number of bytes to process
            output: Output buffer
            out_off: Offset in output
            
        Returns:
            Number of bytes processed
            
        Raises:
            DataLengthException: If buffer too short
        """
        if in_off + length > len(input_data):
            raise DataLengthException('input buffer too small')
        
        if out_off + length > len(output):
            raise DataLengthException('output buffer too short')
        
        for i in range(length):
            if self.byte_count == 0:
                self._check_last_increment()
                self.cipher.process_block(self.counter, 0, self.counter_out, 0)
                next_byte = input_data[in_off + i] ^ self.counter_out[self.byte_count]
                self.byte_count += 1
            else:
                next_byte = input_data[in_off + i] ^ self.counter_out[self.byte_count]
                self.byte_count += 1
                if self.byte_count == len(self.counter):
                    self.byte_count = 0
                    self._increment_counter()
            
            output[out_off + i] = next_byte
        
        return length
    
    def reset(self) -> None:
        """Reset the cipher."""
        for i in range(len(self.counter)):
            self.counter[i] = 0
        self.counter[:len(self.IV)] = self.IV
        self.cipher.reset()
        self.byte_count = 0
    
    def _check_last_increment(self) -> None:
        """Check that counter hasn't wrapped around."""
        # If the IV is the same as the blocksize we assume the user knows what they are doing
        if len(self.IV) < self.block_size:
            if self.counter[len(self.IV) - 1] != self.IV[len(self.IV) - 1]:
                raise ValueError('Counter in CTR/SIC mode out of range')
    
    def _increment_counter(self) -> None:
        """Increment the counter by 1."""
        i = len(self.counter) - 1
        while i >= 0:
            self.counter[i] = (self.counter[i] + 1) & 0xFF
            if self.counter[i] != 0:
                break
            i -= 1
