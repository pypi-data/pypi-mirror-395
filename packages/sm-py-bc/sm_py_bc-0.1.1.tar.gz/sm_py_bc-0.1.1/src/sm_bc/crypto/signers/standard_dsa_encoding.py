"""
Standard DSA encoding using ASN.1 DER format.

This implementation encodes DSA-style signatures (r, s) using the
standard ASN.1 DER format as defined in various standards including
PKCS#1, X9.62, and others.

The format is:
  SEQUENCE {
    r INTEGER,
    s INTEGER
  }

Based on: org.bouncycastle.crypto.signers.StandardDSAEncoding
"""

from typing import Tuple
from .dsa_encoding import DSAEncoding


class StandardDSAEncoding(DSAEncoding):
    """Standard ASN.1 DER encoding for DSA signatures."""
    
    # Singleton instance
    INSTANCE = None
    
    def __init__(self):
        pass
    
    def encode(self, n: int, r: int, s: int) -> bytes:
        """
        Encode (r, s) signature into ASN.1 DER format.
        
        Args:
            n: Order of the curve
            r: r component of signature
            s: s component of signature
            
        Returns:
            DER-encoded signature
            
        Raises:
            ValueError: If components are out of range
        """
        # Validate inputs
        if r <= 0 or r >= n:
            raise ValueError('r component out of range')
        if s <= 0 or s >= n:
            raise ValueError('s component out of range')
        
        # Encode r as INTEGER
        r_bytes = self._encode_integer(r)
        
        # Encode s as INTEGER
        s_bytes = self._encode_integer(s)
        
        # Calculate total sequence length
        sequence_length = len(r_bytes) + len(s_bytes)
        
        # Build the complete DER encoding: tag (1 byte) + length + content
        length_bytes_count = self._length_bytes_count(sequence_length)
        result = bytearray(1 + length_bytes_count + sequence_length)
        offset = 0
        
        # SEQUENCE tag
        result[offset] = 0x30
        offset += 1
        
        # Encode sequence length
        offset += self._encode_length(result, offset, sequence_length)
        
        # Copy r bytes
        result[offset:offset + len(r_bytes)] = r_bytes
        offset += len(r_bytes)
        
        # Copy s bytes
        result[offset:offset + len(s_bytes)] = s_bytes
        
        return bytes(result)
    
    def decode(self, n: int, encoding: bytes) -> Tuple[int, int]:
        """
        Decode ASN.1 DER signature into (r, s) components.
        
        Args:
            n: Order of the curve
            encoding: DER-encoded signature
            
        Returns:
            Tuple of (r, s)
            
        Raises:
            ValueError: If encoding is invalid
        """
        offset = 0
        
        # Check SEQUENCE tag
        if encoding[offset] != 0x30:
            raise ValueError('Invalid DER encoding: expected SEQUENCE tag')
        offset += 1
        
        # Parse sequence length
        sequence_length, length_bytes = self._parse_length(encoding, offset)
        offset += length_bytes
        
        # Check total length
        if offset + sequence_length != len(encoding):
            raise ValueError('Invalid DER encoding: incorrect sequence length')
        
        # Parse r component
        r, r_length = self._parse_integer(encoding, offset)
        offset += r_length
        
        # Parse s component
        s, s_length = self._parse_integer(encoding, offset)
        offset += s_length
        
        # Check we consumed all bytes
        if offset != len(encoding):
            raise ValueError('Invalid DER encoding: extra bytes')
        
        # Validate ranges
        if r <= 0 or r >= n:
            raise ValueError('Invalid signature: r component out of range')
        if s <= 0 or s >= n:
            raise ValueError('Invalid signature: s component out of range')
        
        return (r, s)
    
    def _encode_integer(self, value: int) -> bytes:
        """
        Encode a positive integer as DER INTEGER.
        
        Args:
            value: Positive integer to encode
            
        Returns:
            DER-encoded INTEGER
            
        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError('Integer must be positive')
        
        # Convert to minimal byte representation
        value_bytes = self._bigint_to_bytes(value)
        
        # Add leading zero if MSB is set (to ensure positive interpretation)
        if (value_bytes[0] & 0x80) != 0:
            value_bytes = b'\x00' + value_bytes
        
        # Build DER INTEGER: tag (1 byte) + length + value bytes
        length_bytes_count = self._length_bytes_count(len(value_bytes))
        result = bytearray(1 + length_bytes_count + len(value_bytes))
        offset = 0
        
        # INTEGER tag
        result[offset] = 0x02
        offset += 1
        
        # Encode length
        offset += self._encode_length(result, offset, len(value_bytes))
        
        # Copy integer bytes
        result[offset:offset + len(value_bytes)] = value_bytes
        
        return bytes(result)
    
    def _parse_integer(self, encoding: bytes, offset: int) -> Tuple[int, int]:
        """
        Parse a DER INTEGER from the encoding.
        
        Args:
            encoding: DER-encoded data
            offset: Starting offset
            
        Returns:
            Tuple of (value, bytes_consumed)
            
        Raises:
            ValueError: If encoding is invalid
        """
        if offset >= len(encoding):
            raise ValueError('Unexpected end of DER encoding')
        
        # Check INTEGER tag
        if encoding[offset] != 0x02:
            raise ValueError('Invalid DER encoding: expected INTEGER tag')
        offset += 1
        
        # Parse length
        length, length_bytes = self._parse_length(encoding, offset)
        offset += length_bytes
        
        if offset + length > len(encoding):
            raise ValueError('Invalid DER encoding: integer extends beyond available data')
        
        # Check for minimal encoding (no unnecessary leading zeros)
        if length > 1 and encoding[offset] == 0x00 and (encoding[offset + 1] & 0x80) == 0:
            raise ValueError('Invalid DER encoding: non-minimal integer')
        
        # Extract integer bytes
        integer_bytes = encoding[offset:offset + length]
        value = self._bytes_to_bigint(integer_bytes)
        
        if value <= 0:
            raise ValueError('Invalid DER encoding: non-positive integer')
        
        return (value, 1 + length_bytes + length)
    
    def _length_bytes_count(self, length: int) -> int:
        """
        Calculate number of bytes needed to encode a length.
        
        Args:
            length: Length value
            
        Returns:
            Number of bytes needed
        """
        if length < 0x80:
            return 1
        else:
            count = 1
            temp = length
            while temp > 0:
                count += 1
                temp = temp >> 8
            return count
    
    def _encode_length(self, buffer: bytearray, offset: int, length: int) -> int:
        """
        Encode length in DER format.
        
        Args:
            buffer: Buffer to write to
            offset: Starting offset
            length: Length value to encode
            
        Returns:
            Number of bytes written
        """
        if length < 0x80:
            # Short form
            buffer[offset] = length
            return 1
        else:
            # Long form
            length_bytes = 0
            temp = length
            while temp > 0:
                length_bytes += 1
                temp = temp >> 8
            
            buffer[offset] = 0x80 | length_bytes
            write_offset = offset + 1
            
            for i in range(length_bytes - 1, -1, -1):
                buffer[write_offset] = (length >> (i * 8)) & 0xFF
                write_offset += 1
            
            return 1 + length_bytes
    
    def _parse_length(self, encoding: bytes, offset: int) -> Tuple[int, int]:
        """
        Parse DER length encoding.
        
        Args:
            encoding: DER-encoded data
            offset: Starting offset
            
        Returns:
            Tuple of (length, bytes_consumed)
            
        Raises:
            ValueError: If encoding is invalid
        """
        if offset >= len(encoding):
            raise ValueError('Unexpected end of DER encoding')
        
        first_byte = encoding[offset]
        
        if (first_byte & 0x80) == 0:
            # Short form
            return (first_byte, 1)
        else:
            # Long form
            length_bytes = first_byte & 0x7F
            
            if length_bytes == 0:
                raise ValueError('Invalid DER encoding: indefinite length not allowed')
            if length_bytes > 4:
                raise ValueError('Invalid DER encoding: length too large')
            if offset + 1 + length_bytes > len(encoding):
                raise ValueError('Invalid DER encoding: length extends beyond available data')
            
            length = 0
            for i in range(length_bytes):
                length = (length << 8) | encoding[offset + 1 + i]
            
            # Check for minimal encoding
            if length < 0x80:
                raise ValueError('Invalid DER encoding: non-minimal length')
            
            return (length, 1 + length_bytes)
    
    def _bigint_to_bytes(self, value: int) -> bytes:
        """
        Convert int to minimal byte array (big-endian).
        
        Args:
            value: Integer value
            
        Returns:
            Byte representation
        """
        if value == 0:
            return b'\x00'
        
        byte_list = []
        while value > 0:
            byte_list.insert(0, value & 0xFF)
            value = value >> 8
        
        return bytes(byte_list)
    
    def _bytes_to_bigint(self, data: bytes) -> int:
        """
        Convert byte array to int (big-endian).
        
        Args:
            data: Byte data
            
        Returns:
            Integer value
        """
        result = 0
        for byte in data:
            result = (result << 8) | byte
        return result


# Create singleton instance
StandardDSAEncoding.INSTANCE = StandardDSAEncoding()
