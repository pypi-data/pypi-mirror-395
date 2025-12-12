"""
High-level cipher interface for easy encryption/decryption.

This module provides convenient wrapper classes that combine block ciphers,
cipher modes, and padding schemes into easy-to-use interfaces.
"""

from typing import Union, Optional
from .engines.sm4_engine import SM4Engine
from .modes import CBCBlockCipher, SICBlockCipher, OFBBlockCipher, CFBBlockCipher
from .paddings import PKCS7Padding, ISO7816d4Padding, ZeroBytePadding, ISO10126Padding
from .params.key_parameter import KeyParameter
from .params.parameters_with_iv import ParametersWithIV


class SM4Cipher:
    """
    High-level SM4 cipher interface.
    
    Provides convenient methods for encrypting and decrypting data with SM4
    using various cipher modes and padding schemes.
    
    Example:
        # CBC mode with PKCS#7 padding
        cipher = SM4Cipher(mode='CBC', padding='PKCS7')
        cipher.init(True, key, iv)
        ciphertext = cipher.encrypt(plaintext)
        
        cipher.init(False, key, iv)
        plaintext = cipher.decrypt(ciphertext)
    """
    
    MODES = {
        'ECB': ('direct', None),  # Direct SM4Engine
        'CBC': ('block', CBCBlockCipher),
        'CTR': ('stream', SICBlockCipher),
        'OFB': ('stream_bitblock', OFBBlockCipher),
        'CFB': ('stream_bitblock', CFBBlockCipher),
    }
    
    PADDINGS = {
        'PKCS7': PKCS7Padding,
        'ISO7816-4': ISO7816d4Padding,
        'ISO10126': ISO10126Padding,
        'ZERO': ZeroBytePadding,
        'NONE': None,
    }
    
    def __init__(self, mode: str = 'CBC', padding: str = 'PKCS7'):
        """
        Initialize SM4 cipher.
        
        Args:
            mode: Cipher mode ('ECB', 'CBC', 'CTR', 'OFB', 'CFB')
            padding: Padding scheme ('PKCS7', 'ISO7816-4', 'ISO10126', 'ZERO', 'NONE')
        
        Raises:
            ValueError: If mode or padding is invalid
        """
        if mode.upper() not in self.MODES:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {list(self.MODES.keys())}")
        
        if padding.upper() not in self.PADDINGS:
            raise ValueError(f"Invalid padding: {padding}. Must be one of {list(self.PADDINGS.keys())}")
        
        self.mode_name = mode.upper()
        self.padding_name = padding.upper()
        
        # Create base engine
        base_engine = SM4Engine()
        
        # Get mode configuration
        mode_type, mode_class = self.MODES[self.mode_name]
        
        # Wrap with mode if needed
        if mode_type == 'direct':
            self.engine = base_engine
            self.is_stream = False
        elif mode_type == 'block':
            self.engine = mode_class(base_engine)
            self.is_stream = False
        elif mode_type == 'stream':
            self.engine = mode_class(base_engine)
            self.is_stream = True
        elif mode_type == 'stream_bitblock':
            # OFB and CFB need bit_block_size parameter (128 bits = 16 bytes)
            self.engine = mode_class(base_engine, 128)
            self.is_stream = True
        
        # Create padding if needed
        if self.PADDINGS[self.padding_name] is not None:
            self.padding = self.PADDINGS[self.padding_name]()
        else:
            self.padding = None
        
        self.block_size = 16  # SM4 block size
        self.initialized = False
        self.encrypting = False
    
    def init(self, encrypting: bool, key: Union[bytes, bytearray], 
             iv: Optional[Union[bytes, bytearray]] = None):
        """
        Initialize the cipher for encryption or decryption.
        
        Args:
            encrypting: True for encryption, False for decryption
            key: 16-byte encryption key
            iv: Initialization vector (required for CBC, OFB, CFB, CTR modes)
        
        Raises:
            ValueError: If key length is invalid or IV is missing when required
        """
        if len(key) != 16:
            raise ValueError(f"Invalid key length: {len(key)}. SM4 requires 16 bytes.")
        
        self.encrypting = encrypting
        
        # Check if IV is required
        if self.mode_name in ['CBC', 'CTR', 'OFB', 'CFB']:
            if iv is None:
                raise ValueError(f"IV is required for {self.mode_name} mode")
            if len(iv) != 16:
                raise ValueError(f"Invalid IV length: {len(iv)}. Must be 16 bytes.")
            params = ParametersWithIV(KeyParameter(key), iv)
        else:
            params = KeyParameter(key)
        
        self.engine.init(encrypting, params)
        self.initialized = True
    
    def encrypt(self, plaintext: Union[bytes, bytearray]) -> bytearray:
        """
        Encrypt plaintext.
        
        Args:
            plaintext: Data to encrypt
        
        Returns:
            Encrypted data (ciphertext)
        
        Raises:
            RuntimeError: If cipher is not initialized or initialized for decryption
        """
        if not self.initialized:
            raise RuntimeError("Cipher not initialized. Call init() first.")
        
        if not self.encrypting:
            raise RuntimeError("Cipher initialized for decryption, not encryption")
        
        # For stream ciphers, no padding needed
        if self.is_stream:
            data = bytearray(plaintext)
            output = bytearray(len(data))
            if hasattr(self.engine, 'process_bytes'):
                self.engine.process_bytes(data, 0, len(data), output, 0)
            else:
                # Fallback for stream ciphers without process_bytes
                for i in range(0, len(data), self.block_size):
                    self.engine.process_block(data, i, output, i)
            return output
        
        # For block ciphers, handle padding
        if self.padding is not None:
            data = self.padding.add_padding(plaintext, self.block_size)
        else:
            data = bytearray(plaintext)
            # Check block alignment
            if len(data) % self.block_size != 0:
                raise ValueError(f"Data length must be multiple of {self.block_size} when padding is disabled")
        
        # Encrypt
        output = bytearray(len(data))
        for i in range(0, len(data), self.block_size):
            self.engine.process_block(data, i, output, i)
        
        return output
    
    def decrypt(self, ciphertext: Union[bytes, bytearray]) -> bytearray:
        """
        Decrypt ciphertext.
        
        Args:
            ciphertext: Data to decrypt
        
        Returns:
            Decrypted data (plaintext)
        
        Raises:
            RuntimeError: If cipher is not initialized or initialized for encryption
            ValueError: If ciphertext length is invalid
        """
        if not self.initialized:
            raise RuntimeError("Cipher not initialized. Call init() first.")
        
        if self.encrypting:
            raise RuntimeError("Cipher initialized for encryption, not decryption")
        
        # For stream ciphers, no padding to remove
        if self.is_stream:
            output = bytearray(len(ciphertext))
            if hasattr(self.engine, 'process_bytes'):
                self.engine.process_bytes(ciphertext, 0, len(ciphertext), output, 0)
            else:
                # Fallback for stream ciphers without process_bytes
                for i in range(0, len(ciphertext), self.block_size):
                    self.engine.process_block(ciphertext, i, output, i)
            return output
        
        # For block ciphers, check alignment
        if len(ciphertext) % self.block_size != 0:
            raise ValueError(f"Ciphertext length must be multiple of {self.block_size}")
        
        # Decrypt
        output = bytearray(len(ciphertext))
        for i in range(0, len(ciphertext), self.block_size):
            self.engine.process_block(ciphertext, i, output, i)
        
        # Remove padding if needed
        if self.padding is not None and hasattr(self.padding, 'remove_padding'):
            output = self.padding.remove_padding(output, self.block_size)
        
        return output
    
    def reset(self):
        """Reset the cipher to initial state."""
        if hasattr(self.engine, 'reset'):
            self.engine.reset()
        self.initialized = False
    
    def get_algorithm_name(self) -> str:
        """Get the algorithm name."""
        return f"SM4/{self.mode_name}/{self.padding_name if self.padding_name != 'NONE' else 'NoPadding'}"


def create_sm4_cipher(mode: str = 'CBC', padding: str = 'PKCS7') -> SM4Cipher:
    """
    Factory function to create SM4 cipher.
    
    Args:
        mode: Cipher mode ('ECB', 'CBC', 'CTR', 'OFB', 'CFB')
        padding: Padding scheme ('PKCS7', 'ISO7816-4', 'ISO10126', 'ZERO', 'NONE')
    
    Returns:
        Configured SM4Cipher instance
    
    Example:
        cipher = create_sm4_cipher('CBC', 'PKCS7')
        cipher.init(True, key, iv)
        ciphertext = cipher.encrypt(plaintext)
    """
    return SM4Cipher(mode=mode, padding=padding)
