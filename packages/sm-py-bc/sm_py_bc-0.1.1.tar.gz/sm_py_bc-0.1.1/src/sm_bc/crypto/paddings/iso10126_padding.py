"""
ISO 10126 Padding implementation.

ISO 10126 padding fills with random bytes, except the last byte
which contains the padding length.

Reference: Withdrawn ISO/IEC 10116:2006 (now deprecated but still in use)
"""

from typing import Union
import secrets


class ISO10126Padding:
    """
    ISO 10126 Padding scheme.
    
    Pads data with random bytes, with the last byte indicating padding length.
    This provides some security through randomness but is now deprecated in
    favor of PKCS#7.
    
    Format:
    - Fill with random bytes
    - Last byte contains padding length (1-255)
    
    Example for 3-byte padding: [random, random, 0x03]
    
    Note: This standard was withdrawn in 2007 but is still used in some systems.
    """
    
    def __init__(self):
        """Initialize ISO 10126 Padding."""
        pass
    
    def add_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Add ISO 10126 padding to data.
        
        Args:
            data: The data to pad
            block_size: The block size in bytes
            
        Returns:
            Padded data
            
        Raises:
            ValueError: If block_size is invalid
        """
        if block_size < 1 or block_size > 255:
            raise ValueError(f'Invalid block size: {block_size}')
        
        # Calculate padding length
        padding_length = block_size - (len(data) % block_size)
        
        # Create padded data
        padded = bytearray(data)
        
        # Add random bytes (except last byte)
        if padding_length > 1:
            padded.extend(secrets.token_bytes(padding_length - 1))
        
        # Last byte is padding length
        padded.append(padding_length)
        
        return padded
    
    def remove_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Remove ISO 10126 padding from data.
        
        Args:
            data: The padded data
            block_size: The block size in bytes
            
        Returns:
            Unpadded data
            
        Raises:
            ValueError: If padding is invalid or block_size is invalid
        """
        if block_size < 1 or block_size > 255:
            raise ValueError(f'Invalid block size: {block_size}')
        
        if len(data) == 0:
            raise ValueError('Cannot remove padding from empty data')
        
        if len(data) % block_size != 0:
            raise ValueError('Data length is not a multiple of block size')
        
        # Get padding length from last byte
        padding_length = data[-1]
        
        # Validate padding length
        if padding_length < 1 or padding_length > block_size:
            raise ValueError(f'Invalid padding length: {padding_length}')
        
        if len(data) < padding_length:
            raise ValueError('Padding length exceeds data length')
        
        # Remove padding
        return bytearray(data[:-padding_length])
    
    def get_padded_length(self, data_length: int, block_size: int) -> int:
        """
        Calculate the length after padding.
        
        Args:
            data_length: The original data length
            block_size: The block size in bytes
            
        Returns:
            Length after padding
        """
        padding_length = block_size - (data_length % block_size)
        return data_length + padding_length
