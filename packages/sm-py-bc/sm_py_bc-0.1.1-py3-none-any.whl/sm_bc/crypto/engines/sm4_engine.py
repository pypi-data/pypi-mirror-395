"""
SM4 Block Cipher - 128-bit block cipher with 128-bit key.

Based on:
- GB/T 32907-2016 (Chinese national standard)
- https://eprint.iacr.org/2008/329.pdf
- org.bouncycastle.crypto.engines.SM4Engine
- src/crypto/engines/SM4Engine.ts (sm-js-bc)

SM4 is a 128-bit block cipher using 32 rounds of Feistel structure.
"""

from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.key_parameter import KeyParameter
from sm_bc.exceptions import DataLengthException
from sm_bc.util.pack import Pack


class SM4Engine:
    """
    SM4 block cipher implementation.
    
    Reference: GB/T 32907-2016
    """
    
    BLOCK_SIZE = 16
    
    # S-box for nonlinear transformation
    Sbox = bytes([
        0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
        0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
        0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
        0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
        0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
        0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
        0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
        0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
        0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
        0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
        0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
        0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
        0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
        0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
        0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
    ])
    
    # System parameter CK for key expansion
    CK = [
        0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
        0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
        0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
        0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
        0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
        0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
        0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
        0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279
    ]
    
    # System parameter FK for key expansion
    FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
    
    def __init__(self):
        """Initialize SM4Engine."""
        self.X = [0] * 4  # State registers
        self.rk = None  # Round keys
    
    def init(self, for_encryption: bool, params: CipherParameters) -> None:
        """
        Initialize the cipher.
        
        Args:
            for_encryption: True for encryption, False for decryption
            params: KeyParameter containing the 128-bit key
            
        Raises:
            ValueError: If params is not KeyParameter or key length is invalid
        """
        if not isinstance(params, KeyParameter):
            raise ValueError(f'invalid parameter passed to SM4 init - {type(params).__name__}')
        
        key = params.get_key()
        if len(key) != 16:
            raise ValueError('SM4 requires a 128 bit key')
        
        self.rk = self._expand_key(for_encryption, key)
    
    def get_algorithm_name(self) -> str:
        """Return the algorithm name."""
        return 'SM4'
    
    def get_block_size(self) -> int:
        """Return the block size (16 bytes)."""
        return SM4Engine.BLOCK_SIZE
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int,
                     output: Union[bytearray, List[int]], out_off: int) -> int:
        """
        Process one block of data.
        
        Args:
            input_data: Input data
            in_off: Offset in input
            output: Output buffer
            out_off: Offset in output
            
        Returns:
            Number of bytes processed (16)
            
        Raises:
            ValueError: If not initialized
            DataLengthException: If buffer too short
        """
        if self.rk is None:
            raise ValueError('SM4 not initialised')
        
        if in_off + SM4Engine.BLOCK_SIZE > len(input_data):
            raise DataLengthException('input buffer too short')
        
        if out_off + SM4Engine.BLOCK_SIZE > len(output):
            raise DataLengthException('output buffer too short')
        
        # Read input (big-endian)
        self.X[0] = Pack.big_endian_to_int(input_data, in_off)
        self.X[1] = Pack.big_endian_to_int(input_data, in_off + 4)
        self.X[2] = Pack.big_endian_to_int(input_data, in_off + 8)
        self.X[3] = Pack.big_endian_to_int(input_data, in_off + 12)
        
        # 32 rounds iteration
        for i in range(0, 32, 4):
            self.X[0] = self._F0(self.X, self.rk[i])
            self.X[1] = self._F1(self.X, self.rk[i + 1])
            self.X[2] = self._F2(self.X, self.rk[i + 2])
            self.X[3] = self._F3(self.X, self.rk[i + 3])
        
        # Reverse output (big-endian)
        Pack.int_to_big_endian(self.X[3], output, out_off)
        Pack.int_to_big_endian(self.X[2], output, out_off + 4)
        Pack.int_to_big_endian(self.X[1], output, out_off + 8)
        Pack.int_to_big_endian(self.X[0], output, out_off + 12)
        
        return SM4Engine.BLOCK_SIZE
    
    def reset(self) -> None:
        """Reset the cipher."""
        # No internal state to reset beyond rk
        pass
    
    def _rotate_left(self, x: int, bits: int) -> int:
        """
        Circular left shift.
        
        Args:
            x: Value to shift
            bits: Number of bits to shift
            
        Returns:
            Shifted value (32-bit)
        """
        x = x & 0xFFFFFFFF
        return ((x << bits) | (x >> (32 - bits))) & 0xFFFFFFFF
    
    def _tau(self, A: int) -> int:
        """
        Nonlinear transformation τ (tau) - S-box substitution.
        
        Args:
            A: Input value
            
        Returns:
            Transformed value
        """
        b0 = (SM4Engine.Sbox[(A >> 24) & 0xff] & 0xff) << 24
        b1 = (SM4Engine.Sbox[(A >> 16) & 0xff] & 0xff) << 16
        b2 = (SM4Engine.Sbox[(A >> 8) & 0xff] & 0xff) << 8
        b3 = SM4Engine.Sbox[A & 0xff] & 0xff
        
        return (b0 | b1 | b2 | b3) & 0xFFFFFFFF
    
    def _L_ap(self, B: int) -> int:
        """
        Linear transformation L' (for key expansion).
        
        Args:
            B: Input value
            
        Returns:
            Transformed value
        """
        return (B ^ self._rotate_left(B, 13) ^ self._rotate_left(B, 23)) & 0xFFFFFFFF
    
    def _T_ap(self, Z: int) -> int:
        """
        Composite permutation T' (for key expansion).
        T'(Z) = L'(τ(Z))
        
        Args:
            Z: Input value
            
        Returns:
            Transformed value
        """
        return self._L_ap(self._tau(Z))
    
    def _expand_key(self, for_encryption: bool, key: bytes) -> List[int]:
        """
        Key expansion algorithm.
        
        Args:
            for_encryption: True for encryption, False for decryption
            key: 128-bit key
            
        Returns:
            32 round keys
        """
        rk = [0] * 32
        MK = [0] * 4
        
        # Read master key MK (big-endian)
        MK[0] = Pack.big_endian_to_int(key, 0)
        MK[1] = Pack.big_endian_to_int(key, 4)
        MK[2] = Pack.big_endian_to_int(key, 8)
        MK[3] = Pack.big_endian_to_int(key, 12)
        
        # Initialize K
        K = [0] * 4
        K[0] = (MK[0] ^ SM4Engine.FK[0]) & 0xFFFFFFFF
        K[1] = (MK[1] ^ SM4Engine.FK[1]) & 0xFFFFFFFF
        K[2] = (MK[2] ^ SM4Engine.FK[2]) & 0xFFFFFFFF
        K[3] = (MK[3] ^ SM4Engine.FK[3]) & 0xFFFFFFFF
        
        if for_encryption:
            # Encryption: forward generate round keys
            rk[0] = (K[0] ^ self._T_ap((K[1] ^ K[2] ^ K[3] ^ SM4Engine.CK[0]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[1] = (K[1] ^ self._T_ap((K[2] ^ K[3] ^ rk[0] ^ SM4Engine.CK[1]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[2] = (K[2] ^ self._T_ap((K[3] ^ rk[0] ^ rk[1] ^ SM4Engine.CK[2]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[3] = (K[3] ^ self._T_ap((rk[0] ^ rk[1] ^ rk[2] ^ SM4Engine.CK[3]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            
            for i in range(4, 32):
                rk[i] = (rk[i - 4] ^ self._T_ap((rk[i - 3] ^ rk[i - 2] ^ rk[i - 1] ^ SM4Engine.CK[i]) & 0xFFFFFFFF)) & 0xFFFFFFFF
        else:
            # Decryption: reverse generate round keys
            rk[31] = (K[0] ^ self._T_ap((K[1] ^ K[2] ^ K[3] ^ SM4Engine.CK[0]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[30] = (K[1] ^ self._T_ap((K[2] ^ K[3] ^ rk[31] ^ SM4Engine.CK[1]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[29] = (K[2] ^ self._T_ap((K[3] ^ rk[31] ^ rk[30] ^ SM4Engine.CK[2]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            rk[28] = (K[3] ^ self._T_ap((rk[31] ^ rk[30] ^ rk[29] ^ SM4Engine.CK[3]) & 0xFFFFFFFF)) & 0xFFFFFFFF
            
            for i in range(27, -1, -1):
                rk[i] = (rk[i + 4] ^ self._T_ap((rk[i + 3] ^ rk[i + 2] ^ rk[i + 1] ^ SM4Engine.CK[31 - i]) & 0xFFFFFFFF)) & 0xFFFFFFFF
        
        return rk
    
    def _L(self, B: int) -> int:
        """
        Linear transformation L (for encryption round function).
        
        Args:
            B: Input value
            
        Returns:
            Transformed value
        """
        return (B ^
                self._rotate_left(B, 2) ^
                self._rotate_left(B, 10) ^
                self._rotate_left(B, 18) ^
                self._rotate_left(B, 24)) & 0xFFFFFFFF
    
    def _T(self, Z: int) -> int:
        """
        Composite permutation T (for encryption round function).
        T(Z) = L(τ(Z))
        
        Args:
            Z: Input value
            
        Returns:
            Transformed value
        """
        return self._L(self._tau(Z))
    
    def _F0(self, X: List[int], rk: int) -> int:
        """
        Round function F0.
        
        Args:
            X: State array
            rk: Round key
            
        Returns:
            New X[0]
        """
        return (X[0] ^ self._T((X[1] ^ X[2] ^ X[3] ^ rk) & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    def _F1(self, X: List[int], rk: int) -> int:
        """
        Round function F1.
        
        Args:
            X: State array
            rk: Round key
            
        Returns:
            New X[1]
        """
        return (X[1] ^ self._T((X[2] ^ X[3] ^ X[0] ^ rk) & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    def _F2(self, X: List[int], rk: int) -> int:
        """
        Round function F2.
        
        Args:
            X: State array
            rk: Round key
            
        Returns:
            New X[2]
        """
        return (X[2] ^ self._T((X[3] ^ X[0] ^ X[1] ^ rk) & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    def _F3(self, X: List[int], rk: int) -> int:
        """
        Round function F3.
        
        Args:
            X: State array
            rk: Round key
            
        Returns:
            New X[3]
        """
        return (X[3] ^ self._T((X[0] ^ X[1] ^ X[2] ^ rk) & 0xFFFFFFFF)) & 0xFFFFFFFF
