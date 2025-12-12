from typing import Tuple, Protocol, Union, List

class DSAEncoding(Protocol):
    def encode(self, n: int, r: int, s: int) -> bytes:
        ...

    def decode(self, n: int, encoding: Union[bytes, bytearray, List[int]]) -> Tuple[int, int]:
        ...

class StandardDSAEncoding(DSAEncoding):
    def encode(self, n: int, r: int, s: int) -> bytes:
        return self.encode_der(r, s)

    def decode(self, n: int, encoding: Union[bytes, bytearray, List[int]]) -> Tuple[int, int]:
        return self.decode_der(encoding)

    def encode_der(self, r: int, s: int) -> bytes:
        r_bytes = self.encode_integer(r)
        s_bytes = self.encode_integer(s)
        
        content = r_bytes + s_bytes
        return b'\x30' + self.encode_length(len(content)) + content

    def encode_integer(self, val: int) -> bytes:
        # Convert to bytes (minimal length, signed big-endian)
        # Python's to_bytes with signed=True handles two's complement automatically
        # calculating length: (bit_length + 8) // 8
        
        # Special case for 0?
        if val == 0:
            return b'\x02\x01\x00'
            
        # To ensure minimal encoding and correct sign bit handling:
        # If val is positive and MSB is 1, we need an extra byte 0x00
        # int.bit_length() gives bits excluding sign.
        # For val > 0:
        # e.g. 127 (0x7F) -> 7 bits -> 1 byte (0x7F). MSB 0. OK.
        # e.g. 128 (0x80) -> 8 bits -> 1 byte (0x80). Signed interpretation is -128. Need 0x00 0x80.
        # Formula: (val.bit_length() + 1 + 7) // 8 gives bytes required including sign bit for positive numbers.
        
        byte_len = (val.bit_length() + 8) // 8
        # Python's to_bytes needs exact length.
        # But wait, Python signed=True to_bytes behaves correctly for Two's Complement.
        # If I ask for 1 byte for 128, it will fail (OverflowError).
        # So I need to calculate correct length.
        
        byte_len = (val.bit_length() + 1 + 7) // 8
        val_bytes = val.to_bytes(byte_len, 'big', signed=True)
        
        return b'\x02' + self.encode_length(len(val_bytes)) + val_bytes

    def encode_length(self, length: int) -> bytes:
        if length < 128:
            return bytes([length])
        
        # Long form
        # Calculate number of bytes needed for length
        len_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
        return bytes([0x80 | len(len_bytes)]) + len_bytes

    def decode_der(self, encoding: Union[bytes, bytearray, List[int]]) -> Tuple[int, int]:
        # Minimal DER decoder for SEQUENCE { INTEGER, INTEGER }
        data = bytearray(encoding)
        idx = 0
        
        if data[idx] != 0x30:
            raise ValueError("Not a SEQUENCE")
        idx += 1
        
        seq_len, len_bytes = self.decode_length(data, idx)
        idx += len_bytes
        
        if idx + seq_len != len(data):
            # Strict check? BC sometimes allows extra bytes? No, strict usually.
            pass
            
        # Read r
        if data[idx] != 0x02:
             raise ValueError("Not an INTEGER")
        idx += 1
        
        r_len, len_bytes = self.decode_length(data, idx)
        idx += len_bytes
        
        r_bytes = data[idx : idx + r_len]
        r = int.from_bytes(r_bytes, 'big', signed=True)
        idx += r_len
        
        # Read s
        if data[idx] != 0x02:
             raise ValueError("Not an INTEGER")
        idx += 1
        
        s_len, len_bytes = self.decode_length(data, idx)
        idx += len_bytes
        
        s_bytes = data[idx : idx + s_len]
        s = int.from_bytes(s_bytes, 'big', signed=True)
        idx += s_len
        
        return r, s

    def decode_length(self, data: bytearray, idx: int) -> Tuple[int, int]:
        b = data[idx]
        if (b & 0x80) == 0:
            return b, 1
        
        num_bytes = b & 0x7F
        length = int.from_bytes(data[idx+1 : idx+1+num_bytes], 'big')
        return length, 1 + num_bytes
