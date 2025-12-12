"""
Output Feedback (OFB) mode.

Reference: org.bouncycastle.crypto.modes.OFBBlockCipher
           src/crypto/modes/OFBBlockCipher.ts (sm-js-bc)
"""

from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.parameters_with_iv import ParametersWithIV
from sm_bc.exceptions import DataLengthException


class OFBBlockCipher:
    """
    Output Feedback (OFB) mode implementation.
    
    In OFB mode, the block cipher encrypts the previous output to produce
    the next keystream block. The keystream is then XORed with the plaintext.
    
    Key characteristics:
    - Encryption and decryption are identical operations (XOR with keystream)
    - Converts block cipher into stream cipher
    - Does not propagate errors
    - Feedback is from encrypted output, not ciphertext
    
    Reference: NIST SP 800-38A
    """
    
    def __init__(self, cipher, bit_block_size: int):
        """
        Create an OFB mode cipher.
        
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
            raise ValueError(f'OFB{bit_block_size} not supported')
        
        self.cipher = cipher
        self.block_size = bit_block_size // 8
        
        self.IV = bytearray(cipher_block_size)
        self.ofb_v = bytearray(cipher_block_size)  # Output feedback register
        self.ofb_out_v = bytearray(cipher_block_size)  # Encrypted output
        
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
        
        Note: for_encryption is ignored for OFB mode since encryption
        and decryption are identical operations.
        
        Args:
            for_encryption: Ignored (OFB encryption and decryption are identical)
            params: The parameters (should be ParametersWithIV for first init)
        """
        if isinstance(params, ParametersWithIV):
            iv_param = params
            iv = iv_param.get_iv()
            
            if len(iv) < len(self.IV):
                # Prepend the supplied IV with zeros (per FIPS PUB 81)
                for i in range(len(self.IV)):
                    self.IV[i] = 0
                self.IV[len(self.IV) - len(iv):] = iv
            else:
                self.IV[:] = iv[:len(self.IV)]
            
            self.reset()
            
            # If None, it's an IV change only
            underlying_params = iv_param.get_parameters()
            if underlying_params is not None:
                # OFB always encrypts the feedback register, regardless of mode
                self.cipher.init(True, underlying_params)
        else:
            self.reset()
            
            # If it's not None, key is to be reused
            if params is not None:
                # OFB always encrypts the feedback register
                self.cipher.init(True, params)
    
    def get_algorithm_name(self) -> str:
        """
        Get the algorithm name.
        
        Returns:
            The name of the underlying algorithm followed by "/OFB" and block size
        """
        return f'{self.cipher.get_algorithm_name()}/OFB{self.block_size * 8}'
    
    def get_block_size(self) -> int:
        """
        Get the block size in bytes.
        
        Returns:
            The block size in bytes
        """
        return self.block_size
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int,
                     output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process a block of input.
        
        Args:
            input_data: The input buffer
            in_off: The offset into input where data starts
            output: The output buffer
            out_off: The offset into output where result will be written
            
        Returns:
            The number of bytes processed
        """
        self.process_bytes(input_data, in_off, self.block_size, output, out_off)
        return self.block_size
    
    def process_bytes(self, input_data: Union[bytes, bytearray], in_off: int,
                     length: int, output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process a stream of bytes.
        
        Args:
            input_data: The input buffer
            in_off: The offset into input where data starts
            length: The number of bytes to process
            output: The output buffer
            out_off: The offset into output where result will be written
            
        Returns:
            The number of bytes processed
            
        Raises:
            DataLengthException: If buffer too short
        """
        if in_off + length > len(input_data):
            raise DataLengthException('input buffer too short')
        
        if out_off + length > len(output):
            raise DataLengthException('output buffer too short')
        
        for i in range(length):
            output[out_off + i] = self._calculate_byte(input_data[in_off + i])
        
        return length
    
    def reset(self) -> None:
        """Reset the feedback register back to the IV and reset the underlying cipher."""
        self.ofb_v[:] = self.IV
        self.byte_count = 0
        self.cipher.reset()
    
    def get_current_iv(self) -> bytearray:
        """
        Get the current IV/output feedback register state.
        
        Returns:
            A copy of the current output feedback register
        """
        return bytearray(self.ofb_v)
    
    def _calculate_byte(self, input_byte: int) -> int:
        """
        Calculate a single output byte.
        
        Args:
            input_byte: The input byte
            
        Returns:
            The output byte (XOR of input with keystream)
        """
        # Generate new keystream block if needed
        if self.byte_count == 0:
            self.cipher.process_block(self.ofb_v, 0, self.ofb_out_v, 0)
        
        # XOR input with keystream
        output_byte = self.ofb_out_v[self.byte_count] ^ input_byte
        self.byte_count += 1
        
        # Update feedback register when block is complete
        if self.byte_count == self.block_size:
            self.byte_count = 0
            
            # Shift ofb_v left by block_size bytes
            self.ofb_v[:len(self.ofb_v) - self.block_size] = \
                self.ofb_v[self.block_size:]
            
            # Append the encrypted output to feedback register
            self.ofb_v[len(self.ofb_v) - self.block_size:] = \
                self.ofb_out_v[:self.block_size]
        
        return output_byte
