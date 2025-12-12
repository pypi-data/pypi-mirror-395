"""
Implements Galois/Counter Mode (GCM) as detailed in NIST Special Publication 800-38D.

GCM is an AEAD (Authenticated Encryption with Associated Data) mode that provides:
- Confidentiality (encryption)
- Authenticity (authentication tag)
- Optional additional authenticated data (AAD) - data that is authenticated but not encrypted
"""
from sm_bc.crypto.params.key_parameter import KeyParameter
from src.crypto.params.AEADParameters import AEADParameters
from sm_bc.crypto.params.parameters_with_iv import ParametersWithIV
from src.crypto.modes.gcm_util import GCMUtil
from sm_bc.util.pack import Pack


class GCMBlockCipher:
    """
    Galois/Counter Mode (GCM) implementation.
    
    Key features:
    - Based on CTR mode for encryption
    - Uses Galois field multiplication for authentication
    - Produces an authentication tag to verify integrity
    - Supports variable-length nonces (12 bytes recommended)
    - Supports variable-length authentication tags (96-128 bits recommended)
    """
    
    BLOCK_SIZE = 16
    
    def __init__(self, cipher):
        """
        Create a GCM mode cipher.
        
        Args:
            cipher: The block cipher (must have 16-byte block size and implement
                   get_block_size, init, process_block, reset, get_algorithm_name methods)
        """
        if cipher.get_block_size() != self.BLOCK_SIZE:
            raise ValueError(f"cipher required with a block size of {self.BLOCK_SIZE}")
        
        self.cipher = cipher
        
        # Initialization state
        self.for_encryption = False
        self.initialised = False
        self.mac_size = 16
        self.nonce = None
        self.associated_text = None
        
        # GCM state
        self.H = bytearray(self.BLOCK_SIZE)  # Hash subkey
        self.J0 = bytearray(self.BLOCK_SIZE)  # Initial counter block
        self.counter = bytearray(self.BLOCK_SIZE)  # Current counter
        self.S = bytearray(self.BLOCK_SIZE)  # Authentication state
        self.S_at = bytearray(self.BLOCK_SIZE)  # AAD authentication state
        
        # Buffering
        self.buf_block = bytearray(self.BLOCK_SIZE)
        self.buf_off = 0
        self.total_length = 0
        
        # AAD processing
        self.at_block = bytearray(self.BLOCK_SIZE)
        self.at_block_pos = 0
        self.at_length = 0
        
        # Final state
        self.mac_block = None
        self.ciphertext_buffer = bytearray()
        self.ciphertext_buffer_length = 0
    
    def get_underlying_cipher(self):
        """Get the underlying cipher"""
        return self.cipher
    
    def get_algorithm_name(self) -> str:
        """Get the algorithm name"""
        return f"{self.cipher.get_algorithm_name()}/GCM"
    
    def get_block_size(self) -> int:
        """Get the block size (always 16 bytes for GCM)"""
        return self.BLOCK_SIZE
    
    def init(self, for_encryption: bool, params) -> None:
        """
        Initialize the cipher.
        
        Args:
            for_encryption: True for encryption, false for decryption
            params: AEADParameters or ParametersWithIV
        """
        self.for_encryption = for_encryption
        self.mac_block = None
        self.initialised = True
        
        if isinstance(params, AEADParameters):
            new_nonce = params.get_nonce()
            self.associated_text = params.get_associated_text()
            
            mac_size_bits = params.get_mac_size()
            if mac_size_bits < 32 or mac_size_bits > 128 or mac_size_bits % 8 != 0:
                raise ValueError(f"Invalid value for MAC size: {mac_size_bits}")
            
            self.mac_size = mac_size_bits // 8
            key_param = params.get_key()
        elif isinstance(params, ParametersWithIV):
            new_nonce = params.get_iv()
            self.associated_text = None
            self.mac_size = 16
            key_param = params.get_parameters()
        else:
            raise ValueError("invalid parameters passed to GCM")
        
        buf_length = self.BLOCK_SIZE if for_encryption else self.BLOCK_SIZE + self.mac_size
        self.buf_block = bytearray(buf_length)
        
        if not new_nonce or len(new_nonce) < 1:
            raise ValueError("IV must be at least 1 byte")
        
        self.nonce = new_nonce
        
        # Initialize cipher and compute H = E(K, 0)
        self.cipher.init(True, key_param)
        self.H = bytearray(self.BLOCK_SIZE)
        self.cipher.process_block(self.H, 0, self.H, 0)
        
        # Compute J0 from nonce
        self.J0 = bytearray(self.BLOCK_SIZE)
        if len(new_nonce) == 12:
            # Standard case: 96-bit nonce
            self.J0[:12] = new_nonce
            self.J0[15] = 0x01
        else:
            # Non-standard: hash the nonce
            self._g_hash(self.J0, new_nonce)
            len_block = bytearray(16)
            Pack.long_to_big_endian(len(new_nonce) * 8, len_block, 8)
            self._g_hash_block(self.J0, bytes(len_block))
        
        # Initialize state
        self.S = bytearray(self.BLOCK_SIZE)
        self.S_at = bytearray(self.BLOCK_SIZE)
        self.at_block = bytearray(self.BLOCK_SIZE)
        self.at_block_pos = 0
        self.at_length = 0
        self.counter = bytearray(self.J0)
        self.buf_off = 0
        self.total_length = 0
        
        # Process AAD if provided
        if self.associated_text:
            self.process_aad_bytes(self.associated_text, 0, len(self.associated_text))
    
    def process_aad_bytes(self, aad: bytes, offset: int, length: int) -> None:
        """Process additional authenticated data (AAD)"""
        self._check_status()
        
        in_off = offset
        remaining = length
        
        # Fill partial block
        if self.at_block_pos > 0:
            available = self.BLOCK_SIZE - self.at_block_pos
            if remaining < available:
                self.at_block[self.at_block_pos:self.at_block_pos + remaining] = aad[in_off:in_off + remaining]
                self.at_block_pos += remaining
                return
            
            self.at_block[self.at_block_pos:self.BLOCK_SIZE] = aad[in_off:in_off + available]
            self._g_hash_block(self.S_at, bytes(self.at_block))
            self.at_length += self.BLOCK_SIZE
            in_off += available
            remaining -= available
            self.at_block_pos = 0
        
        # Process complete blocks
        while remaining >= self.BLOCK_SIZE:
            self._g_hash_block(self.S_at, aad[in_off:in_off + self.BLOCK_SIZE])
            self.at_length += self.BLOCK_SIZE
            in_off += self.BLOCK_SIZE
            remaining -= self.BLOCK_SIZE
        
        # Buffer remaining bytes
        if remaining > 0:
            self.at_block[:remaining] = aad[in_off:in_off + remaining]
            self.at_block_pos = remaining
    
    def process_block(self, input_bytes: bytes, in_off: int, output: bytearray, out_off: int) -> int:
        """Process a block of data (not supported for GCM)"""
        raise ValueError("processBlock not supported for GCM mode (use processBytes and doFinal)")
    
    def process_bytes(self, input_bytes: bytes, in_off: int, length: int, 
                     output: bytearray, out_off: int) -> int:
        """Process bytes of data"""
        self._check_status()
        
        if in_off + length > len(input_bytes):
            raise ValueError("Input buffer too short")
        
        if self.for_encryption:
            # Encryption mode: process blocks immediately
            return self._encrypt_bytes(input_bytes, in_off, length, output, out_off)
        else:
            # Decryption mode: buffer all data for MAC verification in doFinal
            new_length = self.ciphertext_buffer_length + length
            if new_length > len(self.ciphertext_buffer):
                new_buffer = bytearray(max(new_length, len(self.ciphertext_buffer) * 2))
                new_buffer[:self.ciphertext_buffer_length] = self.ciphertext_buffer[:self.ciphertext_buffer_length]
                self.ciphertext_buffer = new_buffer
            
            self.ciphertext_buffer[self.ciphertext_buffer_length:new_length] = input_bytes[in_off:in_off + length]
            self.ciphertext_buffer_length += length
            
            return 0  # No output until doFinal verifies MAC
    
    def do_final(self, output: bytearray, out_off: int) -> int:
        """Complete processing and generate/verify authentication tag"""
        self._check_status()
        
        if self.for_encryption:
            return self._encrypt_do_final(output, out_off)
        else:
            return self._decrypt_do_final(output, out_off)
    
    def reset(self) -> None:
        """Reset the cipher to initial state"""
        self.S = bytearray(self.BLOCK_SIZE)
        self.S_at = bytearray(self.BLOCK_SIZE)
        self.at_block = bytearray(self.BLOCK_SIZE)
        self.at_block_pos = 0
        self.at_length = 0
        
        if self.J0:
            self.counter = bytearray(self.J0)
        
        self.buf_off = 0
        self.total_length = 0
        self.mac_block = None
        self.ciphertext_buffer_length = 0
        
        if self.associated_text:
            self.process_aad_bytes(self.associated_text, 0, len(self.associated_text))
        
        self.cipher.reset()
    
    def get_mac(self) -> bytes:
        """Get the authentication tag (MAC)"""
        if not self.mac_block:
            return bytes(self.mac_size)
        return bytes(self.mac_block)
    
    def get_output_size(self, length: int) -> int:
        """Get the output size for the given input length"""
        total_data = length + self.buf_off
        
        if self.for_encryption:
            return total_data + self.mac_size
        
        return 0 if total_data < self.mac_size else total_data - self.mac_size
    
    # Private helper methods
    
    def _check_status(self) -> None:
        """Check if cipher is initialized"""
        if not self.initialised:
            raise ValueError("GCM cipher not initialised")
    
    def _encrypt_bytes(self, input_bytes: bytes, in_off: int, length: int,
                      output: bytearray, out_off: int) -> int:
        """Encrypt bytes"""
        processed = 0
        
        for i in range(length):
            self.buf_block[self.buf_off] = input_bytes[in_off + i]
            self.buf_off += 1
            
            if self.buf_off == self.BLOCK_SIZE:
                self._encrypt_block(self.buf_block, output, out_off + processed)
                processed += self.BLOCK_SIZE
                self.buf_off = 0
        
        return processed
    
    def _encrypt_block(self, block: bytearray, output: bytearray, out_off: int) -> None:
        """Encrypt a block"""
        # Initialize cipher state if this is the first block
        if self.total_length == 0:
            self._init_cipher()
        
        # Increment counter
        GCMUtil.increment(self.counter)
        
        # Encrypt counter
        counter_block = bytearray(self.BLOCK_SIZE)
        self.cipher.process_block(bytes(self.counter), 0, counter_block, 0)
        
        # XOR with plaintext
        ciphertext = bytearray(self.BLOCK_SIZE)
        for i in range(self.BLOCK_SIZE):
            ciphertext[i] = block[i] ^ counter_block[i]
        
        # Update authentication hash with ciphertext
        self._g_hash_block(self.S, bytes(ciphertext))
        self.total_length += self.BLOCK_SIZE
        
        # Output ciphertext
        output[out_off:out_off + self.BLOCK_SIZE] = ciphertext
    
    def _encrypt_do_final(self, output: bytearray, out_off: int) -> int:
        """Finalize encryption"""
        # Initialize cipher state if not done yet
        if self.total_length == 0:
            self._init_cipher()
        
        result_len = 0
        
        # Process any remaining bytes
        if self.buf_off > 0:
            # Increment counter
            GCMUtil.increment(self.counter)
            
            # Encrypt counter
            counter_block = bytearray(self.BLOCK_SIZE)
            self.cipher.process_block(bytes(self.counter), 0, counter_block, 0)
            
            # XOR with plaintext (partial block)
            ciphertext = bytearray(self.buf_off)
            for i in range(self.buf_off):
                ciphertext[i] = self.buf_block[i] ^ counter_block[i]
            
            # Update authentication hash (pad to block size)
            padded_ciphertext = bytearray(self.BLOCK_SIZE)
            padded_ciphertext[:self.buf_off] = ciphertext
            self._g_hash_block(self.S, bytes(padded_ciphertext))
            self.total_length += self.buf_off
            
            # Output ciphertext
            output[out_off:out_off + self.buf_off] = ciphertext
            result_len = self.buf_off
        
        # Hash the lengths
        len_block = bytearray(self.BLOCK_SIZE)
        Pack.long_to_big_endian(self.at_length * 8, len_block, 0)
        Pack.long_to_big_endian(self.total_length * 8, len_block, 8)
        self._g_hash_block(self.S, bytes(len_block))
        
        # Compute tag: T = GCTR_K(J0, S)
        tag = bytearray(self.BLOCK_SIZE)
        self.cipher.process_block(bytes(self.J0), 0, tag, 0)
        GCMUtil.xor(tag, bytes(self.S))
        
        # Output tag (truncated to mac_size)
        self.mac_block = bytes(tag[:self.mac_size])
        output[out_off + result_len:out_off + result_len + self.mac_size] = self.mac_block
        
        result_len += self.mac_size
        self.reset()
        
        return result_len
    
    def _init_cipher(self) -> None:
        """Initialize cipher state"""
        # Finalize AAD processing
        if self.at_block_pos > 0:
            self._g_hash_block(self.S_at, bytes(self.at_block))
            self.at_length += self.at_block_pos
        
        # Initialize S with AAD hash
        if self.at_length > 0:
            self.S[:] = self.S_at
    
    def _decrypt_do_final(self, output: bytearray, out_off: int) -> int:
        """Finalize decryption"""
        if self.ciphertext_buffer_length < self.mac_size:
            raise ValueError("data too short")
        
        # Initialize cipher state if not done yet
        if self.total_length == 0:
            self._init_cipher()
        
        # ciphertext_buffer contains all ciphertext + MAC
        data_len = self.ciphertext_buffer_length - self.mac_size
        ciphertext = self.ciphertext_buffer[:self.ciphertext_buffer_length]
        
        # First, hash all ciphertext blocks for MAC computation
        pos = 0
        while pos + self.BLOCK_SIZE <= data_len:
            block = bytes(ciphertext[pos:pos + self.BLOCK_SIZE])
            self._g_hash_block(self.S, block)
            self.total_length += self.BLOCK_SIZE
            pos += self.BLOCK_SIZE
        
        # Hash any remaining partial block
        if pos < data_len:
            padded_block = bytearray(self.BLOCK_SIZE)
            padded_block[:data_len - pos] = ciphertext[pos:data_len]
            self._g_hash_block(self.S, bytes(padded_block))
            self.total_length += data_len - pos
        
        # Extract the received MAC/tag from the buffer
        received_tag = bytes(ciphertext[data_len:self.ciphertext_buffer_length])
        
        # Hash the lengths
        len_block = bytearray(self.BLOCK_SIZE)
        Pack.long_to_big_endian(self.at_length * 8, len_block, 0)
        Pack.long_to_big_endian(self.total_length * 8, len_block, 8)
        self._g_hash_block(self.S, bytes(len_block))
        
        # Compute expected tag
        expected_tag = bytearray(self.BLOCK_SIZE)
        self.cipher.process_block(bytes(self.J0), 0, expected_tag, 0)
        GCMUtil.xor(expected_tag, bytes(self.S))
        
        # Verify tag (constant-time comparison)
        tag_match = True
        for i in range(self.mac_size):
            if expected_tag[i] != received_tag[i]:
                tag_match = False
        
        if not tag_match:
            raise ValueError("mac check in GCM failed")
        
        # MAC verified! Now decrypt all data
        pos = 0
        while pos + self.BLOCK_SIZE <= data_len:
            GCMUtil.increment(self.counter)
            counter_block = bytearray(self.BLOCK_SIZE)
            self.cipher.process_block(bytes(self.counter), 0, counter_block, 0)
            
            for i in range(self.BLOCK_SIZE):
                output[out_off + pos + i] = ciphertext[pos + i] ^ counter_block[i]
            pos += self.BLOCK_SIZE
        
        # Decrypt any remaining partial block
        if pos < data_len:
            GCMUtil.increment(self.counter)
            counter_block = bytearray(self.BLOCK_SIZE)
            self.cipher.process_block(bytes(self.counter), 0, counter_block, 0)
            
            for i in range(data_len - pos):
                output[out_off + pos + i] = ciphertext[pos + i] ^ counter_block[i]
        
        self.mac_block = received_tag
        
        self.reset()
        return data_len
    
    def _g_hash_block(self, Y: bytearray, X: bytes) -> None:
        """GHASH function: multiply and XOR in Galois field"""
        GCMUtil.xor(Y, X)
        result = GCMUtil.multiply(bytes(Y), bytes(self.H))
        Y[:] = result
    
    def _g_hash(self, Y: bytearray, data: bytes) -> None:
        """GHASH over multiple blocks"""
        pos = 0
        while pos + self.BLOCK_SIZE <= len(data):
            self._g_hash_block(Y, data[pos:pos + self.BLOCK_SIZE])
            pos += self.BLOCK_SIZE
        
        if pos < len(data):
            padded_block = bytearray(self.BLOCK_SIZE)
            padded_block[:len(data) - pos] = data[pos:]
            self._g_hash_block(Y, bytes(padded_block))
