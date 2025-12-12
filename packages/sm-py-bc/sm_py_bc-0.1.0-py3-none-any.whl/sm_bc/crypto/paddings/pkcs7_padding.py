"""
PKCS#7 padding implementation.

Reference: org.bouncycastle.crypto.paddings.PKCS7Padding
"""

from typing import Union


class PKCS7Padding:
    """
    PKCS#7 padding - pads with the number of padding bytes.
    
    Reference: org.bouncycastle.crypto.paddings.PKCS7Padding
    """
    
    def __init__(self):
        """Initialize PKCS7 Padding."""
        pass
    
    def add_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Add PKCS7 padding to data.
        
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
        
        # Add padding bytes (all set to padding_length)
        padded.extend(bytes([padding_length] * padding_length))
        
        return padded
    
    def remove_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Remove PKCS7 padding from data.
        
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
        
        # Verify all padding bytes are correct
        for i in range(1, padding_length + 1):
            if data[-i] != padding_length:
                raise ValueError('Invalid padding bytes')
        
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
