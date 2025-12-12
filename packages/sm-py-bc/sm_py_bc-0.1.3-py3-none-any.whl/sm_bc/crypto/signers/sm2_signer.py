from typing import Union, List, Optional
from sm_bc.crypto.digest import Digest
from sm_bc.crypto.digests.sm3_digest import SM3Digest
from sm_bc.crypto.signers.dsa_encoding import DSAEncoding, StandardDSAEncoding
from sm_bc.crypto.signers.dsa_k_calculator import DSAKCalculator, RandomDSAKCalculator
from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.crypto.params.ec_key_parameters import ECKeyParameters
from sm_bc.crypto.params.ec_private_key_parameters import ECPrivateKeyParameters
from sm_bc.crypto.params.ec_public_key_parameters import ECPublicKeyParameters
from sm_bc.crypto.params.parameters_with_id import ParametersWithID
from sm_bc.crypto.params.parameters_with_random import ParametersWithRandom
from sm_bc.math.ec_multiplier import SimpleMultiplier, ECMultiplier
from sm_bc.math.ec_point import ECPoint
from sm_bc.util.secure_random import SecureRandom

class SM2Signer:
    def __init__(self, digest: Digest = None, encoding: DSAEncoding = None, k_calculator: DSAKCalculator = None):
        self.digest = digest if digest else SM3Digest()
        self.encoding = encoding if encoding else StandardDSAEncoding()
        self.k_calculator = k_calculator if k_calculator else RandomDSAKCalculator()
        
        self.ec_params = None
        self.pub_key_point: Optional[ECPoint] = None
        self.ec_key: Optional[ECKeyParameters] = None
        self.z: bytes = b''
    
    def get_algorithm_name(self) -> str:
        """Return the algorithm name."""
        return 'SM2'
    
    def init(self, for_signing: bool, param: CipherParameters) -> None:
        self.for_signing = for_signing
        
        base_param = param
        user_id = b"1234567812345678"
        
        if isinstance(base_param, ParametersWithID):
            user_id = base_param.id
            base_param = base_param.parameters
            
        if for_signing:
            if isinstance(base_param, ParametersWithRandom):
                r_param = base_param
                base_param = r_param.parameters
                self.k_calculator.init(base_param.parameters.n, r_param.random)
            else:
                self.k_calculator.init(base_param.parameters.n, SecureRandom())
                
            if not isinstance(base_param, ECPrivateKeyParameters):
                raise ValueError("ECPrivateKeyParameters required for signing")
            self.ec_key = base_param
        else:
             if not isinstance(base_param, ECPublicKeyParameters):
                raise ValueError("ECPublicKeyParameters required for verification")
             self.ec_key = base_param
             
        self.ec_params = self.ec_key.parameters
        
        # Calculate Z
        # We need public key point for Z. 
        # If signing, we derive it from d * G ? No, usually we need public key for Z calculation even when signing?
        # The standard says Z uses User's Public Key.
        # So if we only have private key, we must calculate public key point: P = d * G.
        
        if for_signing:
            self.pub_key_point = self.ec_params.g.multiply(self.ec_key.d).normalize()
        else:
            self.pub_key_point = self.ec_key.q.normalize()
            
        self.z = self.get_z(user_id)
        
        self.digest.reset()
        self.digest.update_bytes(self.z, 0, len(self.z))

    def update(self, b: int) -> None:
        self.digest.update(b)

    def update_bytes(self, b: Union[bytes, bytearray, List[int]], off: int, len_: int) -> None:
        self.digest.update_bytes(b, off, len_)

    def generate_signature(self) -> bytes:
        if not self.for_signing:
            raise ValueError("Not initialized for signing")
            
        n = self.ec_params.n
        e_hash = bytearray(self.digest.get_digest_size())
        self.digest.do_final(e_hash, 0)
        
        e = int.from_bytes(e_hash, 'big')
        d = self.ec_key.d
        
        multiplier = self.create_base_point_multiplier()
        
        while True:
            k = self.k_calculator.next_k()
            
            # (x1, y1) = k * G
            p1 = multiplier.multiply(self.ec_params.g, k).normalize()
            x1 = p1.x.to_big_integer()
            
            r = (e + x1) % n
            if r == 0 or (r + k) == n:
                continue
                
            # s = (1 + d)^-1 * (k - r * d)
            d_plus_1 = (1 + d) % n
            d_plus_1_inv = pow(d_plus_1, -1, n)
            
            s = (d_plus_1_inv * (k - r * d)) % n
            
            if s == 0:
                continue
                
            return self.encoding.encode(n, r, s)

    def verify_signature(self, signature: bytes) -> bool:
        if self.for_signing:
            raise ValueError("Not initialized for verification")
            
        n = self.ec_params.n
        try:
            r, s = self.encoding.decode(n, signature)
        except Exception:
            return False
            
        if r < 1 or r >= n or s < 1 or s >= n:
            return False
            
        e_hash = bytearray(self.digest.get_digest_size())
        self.digest.do_final(e_hash, 0)
        e = int.from_bytes(e_hash, 'big')
        
        t = (r + s) % n
        if t == 0:
            return False
            
        # (x1, y1) = s*G + t*P
        # P is pub_key_point
        p1 = self.ec_params.g.multiply(s).add(self.pub_key_point.multiply(t)).normalize()
        
        if p1.is_infinity:
            return False
            
        x1 = p1.x.to_big_integer()
        expected_r = (e + x1) % n
        
        return expected_r == r

    def reset(self) -> None:
        self.digest.reset()
        if self.z:
            self.digest.update_bytes(self.z, 0, len(self.z))

    def get_z(self, user_id: bytes) -> bytes:
        digest = SM3Digest()
        
        # entl * 8 (bits)
        length = len(user_id) * 8
        digest.update(length >> 8 & 0xFF)
        digest.update(length & 0xFF)
        
        digest.update_bytes(user_id, 0, len(user_id))
        
        self.add_field_element(digest, self.ec_params.curve.a)
        self.add_field_element(digest, self.ec_params.curve.b)
        self.add_field_element(digest, self.ec_params.g.x)
        self.add_field_element(digest, self.ec_params.g.y)
        self.add_field_element(digest, self.pub_key_point.x)
        self.add_field_element(digest, self.pub_key_point.y)
        
        output = bytearray(digest.get_digest_size())
        digest.do_final(output, 0)
        return output

    def add_field_element(self, digest: Digest, v) -> None:
        val = v.to_big_integer()
        size = (self.ec_params.curve.get_field_size() + 7) // 8
        digest.update_bytes(val.to_bytes(size, 'big'), 0, size)
        
    def create_base_point_multiplier(self) -> ECMultiplier:
        return SimpleMultiplier()
