"""
ISO 7816-4 Padding implementation.

Reference: org.bouncycastle.crypto.paddings.ISO7816d4Padding
"""

from typing import Union


class ISO7816d4Padding:
    """
    ISO 7816-4 padding - pads with 0x80 followed by zero bytes.
    
    Reference: org.bouncycastle.crypto.paddings.ISO7816d4Padding
    """
    
    def __init__(self):
        """Initialize ISO 7816-4 Padding."""
        pass
    
    def add_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Add ISO 7816-4 padding to data.
        
        Args:
            data: The data to pad
            block_size: The block size in bytes
            
        Returns:
            Padded data
            
        Raises:
            ValueError: If block_size is invalid
        """
        if block_size < 1:
            raise ValueError(f'Invalid block size: {block_size}')
        
        # Calculate padding length
        padding_length = block_size - (len(data) % block_size)
        
        # Create padded data
        padded = bytearray(data)
        
        # Add mandatory 0x80 byte
        padded.append(0x80)
        
        # Fill rest with zeros
        for _ in range(padding_length - 1):
            padded.append(0x00)
        
        return padded
    
    def remove_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Remove ISO 7816-4 padding from data.
        
        Args:
            data: The padded data
            block_size: The block size in bytes
            
        Returns:
            Unpadded data
            
        Raises:
            ValueError: If padding is invalid or block_size is invalid
        """
        if block_size < 1:
            raise ValueError(f'Invalid block size: {block_size}')
        
        if len(data) == 0:
            raise ValueError('Cannot remove padding from empty data')
        
        if len(data) % block_size != 0:
            raise ValueError('Data length is not a multiple of block size')
        
        # Find the 0x80 marker byte (search from end)
        marker_pos = -1
        for i in range(len(data) - 1, -1, -1):
            if data[i] == 0x80:
                marker_pos = i
                break
            elif data[i] != 0x00:
                raise ValueError('Invalid padding: non-zero byte in padding area')
        
        if marker_pos == -1:
            raise ValueError('Invalid padding: no 0x80 byte found')
        
        # Remove padding
        return bytearray(data[:marker_pos])
    
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
