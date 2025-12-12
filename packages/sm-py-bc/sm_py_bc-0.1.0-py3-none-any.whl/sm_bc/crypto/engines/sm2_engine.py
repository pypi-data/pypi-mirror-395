"""
SM2 public key encryption engine.

Based on:
- https://tools.ietf.org/html/draft-shen-sm2-ecdsa-02
- org.bouncycastle.crypto.engines.SM2Engine
- src/crypto/engines/SM2Engine.ts (sm-js-bc)

Implements SM2 encryption/decryption with two modes:
- C1C2C3: Ciphertext format is C1||C2||C3 (default)
- C1C3C2: Ciphertext format is C1||C3||C2

Where:
- C1: Elliptic curve point (ephemeral public key)
- C2: Encrypted message
- C3: Hash value for integrity check
"""

from enum import Enum
from typing import Optional, Union
from sm_bc.crypto.digests.sm3_digest import SM3Digest
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.ec_key_parameters import ECKeyParameters
from sm_bc.crypto.params.ec_private_key_parameters import ECPrivateKeyParameters
from sm_bc.crypto.params.ec_public_key_parameters import ECPublicKeyParameters
from sm_bc.crypto.params.parameters_with_random import ParametersWithRandom
from sm_bc.crypto.params.ec_domain_parameters import ECDomainParameters
from sm_bc.math.ec_point import ECPoint
from sm_bc.math.ec_multiplier import AbstractECMultiplier
from sm_bc.util.secure_random import SecureRandom
from sm_bc.util.arrays import Arrays
from sm_bc.util.big_integers import BigIntegers
from sm_bc.exceptions import DataLengthException, InvalidCipherTextException


class SM2Mode(Enum):
    """SM2 ciphertext encoding modes."""
    C1C2C3 = 'C1C2C3'
    C1C3C2 = 'C1C3C2'


class FixedPointCombMultiplier(AbstractECMultiplier):
    """Multiplier using fixed-point comb method (placeholder, falls back to simple multiply)."""
    
    def multiply_positive(self, p: ECPoint, k: int) -> ECPoint:
        # For now, use simple multiplication
        # TODO: Implement actual fixed-point comb multiplication for performance
        return p.multiply(k)


class SM2Engine:
    """
    SM2 encryption/decryption engine.
    
    Reference: SM2Engine.ts (TypeScript implementation)
    """
    
    # Alias for compatibility
    Mode = SM2Mode
    
    def __init__(self, digest: Optional[SM3Digest] = None, mode: SM2Mode = SM2Mode.C1C2C3):
        """
        Initialize SM2Engine.
        
        Args:
            digest: Hash function to use (defaults to SM3)
            mode: Ciphertext encoding mode (C1C2C3 or C1C3C2)
        """
        self.digest = digest if digest is not None else SM3Digest()
        self.mode = mode
        
        self.for_encryption: bool = False
        self.ec_key: Optional[ECKeyParameters] = None
        self.ec_params: Optional[ECDomainParameters] = None
        self.curve_length: int = 0
        self.random: Optional[SecureRandom] = None
    
    def init(self, for_encryption: bool, param: CipherParameters) -> None:
        """
        Initialize engine for encryption or decryption.
        
        Args:
            for_encryption: True for encryption, False for decryption
            param: For encryption: ParametersWithRandom containing ECPublicKeyParameters
                   For decryption: ECPrivateKeyParameters
        """
        self.for_encryption = for_encryption
        
        if for_encryption:
            r_param = param
            if isinstance(r_param, ParametersWithRandom):
                self.ec_key = r_param.parameters
                self.random = r_param.random
            else:
                self.ec_key = param
                self.random = SecureRandom()
            
            self.ec_params = self.ec_key.parameters
            
            # Verify [h]Q is not at infinity
            ec_pub_key = self.ec_key
            s = ec_pub_key.q.multiply(self.ec_params.h)
            if s.is_infinity:
                raise ValueError('invalid key: [h]Q at infinity')
        else:
            self.ec_key = param
            self.ec_params = self.ec_key.parameters
        
        self.curve_length = (self.ec_params.curve.get_field_size() + 7) // 8
    
    def process_block(self, input_data: Union[bytes, bytearray], in_off: int, in_len: int) -> bytearray:
        """
        Process a block of data (encrypt or decrypt).
        
        Args:
            input_data: Input data
            in_off: Offset in input
            in_len: Length of data to process
            
        Returns:
            Processed data
            
        Raises:
            DataLengthException: If input buffer is too short
        """
        if in_off + in_len > len(input_data) or in_len == 0:
            raise DataLengthException('input buffer too short')
        
        if self.for_encryption:
            return self._encrypt(input_data, in_off, in_len)
        else:
            return self._decrypt(input_data, in_off, in_len)
    
    def get_output_size(self, input_len: int) -> int:
        """Get output size for given input length."""
        return (1 + 2 * self.curve_length) + input_len + self.digest.get_digest_size()
    
    def create_base_point_multiplier(self) -> AbstractECMultiplier:
        """Create multiplier for base point operations."""
        return FixedPointCombMultiplier()
    
    def _encrypt(self, input_data: Union[bytes, bytearray], in_off: int, in_len: int) -> bytearray:
        """Encrypt plaintext."""
        c2 = bytearray(in_len)
        c2[:] = input_data[in_off:in_off + in_len]
        
        multiplier = self.create_base_point_multiplier()
        
        while True:
            # Generate random k
            k = self._next_k()
            
            # C1 = [k]G
            c1_p = multiplier.multiply(self.ec_params.g, k).normalize()
            c1 = c1_p.get_encoded(False)
            
            # [k]PB
            k_pb = self.ec_key.q.multiply(k).normalize()
            
            # C2 = M ⊕ KDF(x2||y2, klen)
            self._kdf(self.digest, k_pb, c2)
            
            # Check if encryption failed (KDF returned all zeros)
            if not self._not_encrypted(c2, input_data, in_off):
                break
        
        # C3 = Hash(x2||M||y2)
        c3 = bytearray(self.digest.get_digest_size())
        self._add_field_element(self.digest, k_pb.x)
        self.digest.update_bytes(input_data, in_off, in_len)
        self._add_field_element(self.digest, k_pb.y)
        self.digest.do_final(c3, 0)
        
        # Return C1||C2||C3 or C1||C3||C2
        if self.mode == SM2Mode.C1C3C2:
            return Arrays.concatenate(c1, c3, c2)
        else:
            return Arrays.concatenate(c1, c2, c3)
    
    def _decrypt(self, input_data: Union[bytes, bytearray], in_off: int, in_len: int) -> bytearray:
        """Decrypt ciphertext."""
        # Extract C1
        c1 = bytearray(self.curve_length * 2 + 1)
        c1[:] = input_data[in_off:in_off + len(c1)]
        
        c1_p_initial = self.ec_params.curve.decode_point(bytes(c1))
        
        # Verify [h]C1 is not at infinity
        s = c1_p_initial.multiply(self.ec_params.h)
        if s.is_infinity:
            raise InvalidCipherTextException('[h]C1 at infinity')
        
        # Compute [d]C1
        c1_p = c1_p_initial.multiply(self.ec_key.d).normalize()
        
        digest_size = self.digest.get_digest_size()
        c2 = bytearray(in_len - len(c1) - digest_size)
        
        # Extract C2 based on mode
        if self.mode == SM2Mode.C1C3C2:
            c2[:] = input_data[in_off + len(c1) + digest_size:in_off + in_len]
        else:
            c2[:] = input_data[in_off + len(c1):in_off + len(c1) + len(c2)]
        
        # M = C2 ⊕ KDF(x2||y2, klen)
        self._kdf(self.digest, c1_p, c2)
        
        # Compute C3' = Hash(x2||M||y2)
        c3 = bytearray(digest_size)
        self._add_field_element(self.digest, c1_p.x)
        self.digest.update_bytes(c2, 0, len(c2))
        self._add_field_element(self.digest, c1_p.y)
        self.digest.do_final(c3, 0)
        
        # Verify C3' === C3 (constant-time comparison)
        check = 0
        if self.mode == SM2Mode.C1C3C2:
            for i in range(len(c3)):
                check |= c3[i] ^ input_data[in_off + len(c1) + i]
        else:
            for i in range(len(c3)):
                check |= c3[i] ^ input_data[in_off + len(c1) + len(c2) + i]
        
        # Clear sensitive data
        Arrays.fill(c1, 0)
        Arrays.fill(c3, 0)
        
        if check != 0:
            Arrays.fill(c2, 0)
            raise InvalidCipherTextException('invalid cipher text')
        
        return c2
    
    def _not_encrypted(self, enc_data: bytearray, input_data: Union[bytes, bytearray], in_off: int) -> bool:
        """Check if encryption failed (KDF returned all zeros)."""
        for i in range(len(enc_data)):
            if enc_data[i] != input_data[in_off + i]:
                return False
        return True
    
    def _kdf(self, digest: SM3Digest, c1: ECPoint, enc_data: bytearray) -> None:
        """
        Key Derivation Function using SM3.
        
        Derives key material and XORs it with enc_data in place.
        """
        digest_size = digest.get_digest_size()
        buf = bytearray(max(4, digest_size))
        off = 0
        
        # Optimize with Memoable if available
        memo = None
        copy = None
        
        if hasattr(digest, 'copy') and callable(getattr(digest, 'copy')):
            self._add_field_element(digest, c1.x)
            self._add_field_element(digest, c1.y)
            memo = digest
            copy = memo.copy()
        
        ct = 0
        
        while off < len(enc_data):
            if memo and copy:
                memo.reset_from_memoable(copy)
            else:
                self._add_field_element(digest, c1.x)
                self._add_field_element(digest, c1.y)
            
            # Add counter (big-endian)
            ct += 1
            buf[0] = (ct >> 24) & 0xff
            buf[1] = (ct >> 16) & 0xff
            buf[2] = (ct >> 8) & 0xff
            buf[3] = ct & 0xff
            
            digest.update_bytes(buf, 0, 4)
            digest.do_final(buf, 0)
            
            xor_len = min(digest_size, len(enc_data) - off)
            for i in range(xor_len):
                enc_data[off + i] ^= buf[i]
            off += xor_len
    
    def _next_k(self) -> int:
        """Generate random k in range [1, n-1]."""
        n = self.ec_params.n
        bit_length = BigIntegers.bit_length(n)
        
        while True:
            k = BigIntegers.create_random_big_integer(bit_length, self.random)
            if k != 0 and k < n:
                return k
    
    def _add_field_element(self, digest: SM3Digest, v) -> None:
        """Add field element to digest."""
        p = BigIntegers.as_unsigned_byte_array(self.curve_length, v.to_big_integer())
        digest.update_bytes(p, 0, len(p))
