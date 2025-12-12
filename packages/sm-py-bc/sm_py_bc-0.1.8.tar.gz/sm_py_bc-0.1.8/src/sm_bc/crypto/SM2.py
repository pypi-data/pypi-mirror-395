"""
SM2 curve and domain parameters.

Based on GM/T 0003-2012 and GMNamedCurves.java
"""

from sm_bc.math.ec_curve import Fp as ECCurveFp
from sm_bc.math.ec_point import ECPoint
from sm_bc.crypto.params.ec_domain_parameters import ECDomainParameters
from sm_bc.util.secure_random import SecureRandom
from sm_bc.crypto.engines.sm2_engine import SM2Engine
from sm_bc.crypto.signers.sm2_signer import SM2Signer
from sm_bc.crypto.params.ec_public_key_parameters import ECPublicKeyParameters
from sm_bc.crypto.params.ec_private_key_parameters import ECPrivateKeyParameters
from sm_bc.crypto.params.parameters_with_random import ParametersWithRandom


class SM2:
    """SM2 elliptic curve parameters (SM2P256V1)."""
    
    # Prime p
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    
    # Curve coefficient a
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    
    # Curve coefficient b
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    
    # Base point order n
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    
    # Cofactor h
    h = 1
    
    _domain_params = None
    
    @classmethod
    def get_parameters(cls) -> ECDomainParameters:
        """Get SM2 domain parameters."""
        if cls._domain_params is None:
            # Create curve
            curve = ECCurveFp(cls.p, cls.a, cls.b, cls.n, cls.h)
            
            # Create base point G
            G = curve.create_point(cls.Gx, cls.Gy)
            
            # Create domain parameters
            cls._domain_params = ECDomainParameters(curve, G, cls.n, cls.h, None)
        
        return cls._domain_params
    
    @classmethod
    def get_curve(cls) -> ECCurveFp:
        """Get curve."""
        return cls.get_parameters().curve
    
    @classmethod
    def get_G(cls) -> ECPoint:
        """Get base point G."""
        return cls.get_parameters().g
    
    @classmethod
    def get_n(cls) -> int:
        """Get order n."""
        return cls.n
    
    @classmethod
    def get_h(cls) -> int:
        """Get cofactor h."""
        return cls.h
    
    # Base point G coordinates
    Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    
    @classmethod
    def validate_public_key(cls, Q: ECPoint) -> bool:
        """Validate public key point."""
        if Q.is_infinity:
            return False
        
        if not Q.is_valid():
            return False
        
        # Check [n]Q = O
        nQ = Q.multiply(cls.n)
        if not nQ.is_infinity:
            return False
        
        return True
    
    @classmethod
    def validate_private_key(cls, d: int) -> bool:
        """Validate private key."""
        return 0 < d < cls.n
    
    @classmethod
    def generate_key_pair(cls) -> dict:
        """
        Generate SM2 key pair.
        
        Returns:
            Dictionary containing private key (int) and public key coordinates {x, y}
        """
        random = SecureRandom()
        
        # Generate random private key d where 1 <= d < n
        while True:
            seed = random.generate_seed(32)  # 256 bits / 8 = 32 bytes
            d = int.from_bytes(seed, 'big')
            if 0 < d < cls.n:
                break
        
        # Calculate public key Q = [d]G
        G = cls.get_G()
        Q = G.multiply(d)
        
        if Q.is_infinity or not cls.validate_public_key(Q):
            raise ValueError('Generated invalid public key')
        
        affine_Q = Q.normalize()
        
        return {
            'private_key': d,
            'public_key': {
                'x': affine_Q.x.to_big_integer(),
                'y': affine_Q.y.to_big_integer()
            }
        }
    
    @classmethod
    def encrypt(cls, message: bytes | str, public_key: dict | int, public_key_y: int = None) -> bytes:
        """
        Encrypt plaintext using SM2 public key.
        
        Args:
            message: Message to encrypt (string or bytes)
            public_key: Public key object with x and y coordinates, or separate x coordinate
            public_key_y: Public key Y coordinate (if first parameter is not a dict)
        
        Returns:
            Encrypted ciphertext as bytes
        """
        # Convert string to bytes if needed
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
        
        # Handle different parameter formats
        if isinstance(public_key, dict):
            public_key_x = public_key['x']
            public_key_y_value = public_key['y']
        elif isinstance(public_key, int) and isinstance(public_key_y, int):
            public_key_x = public_key
            public_key_y_value = public_key_y
        else:
            raise ValueError('Invalid public key format. Expected dict with x,y properties or separate x,y int values')
        
        # Create public key parameters
        curve = cls.get_curve()
        Q = curve.create_point(public_key_x, public_key_y_value)
        domain_params = cls.get_parameters()
        pub_key = ECPublicKeyParameters(Q, domain_params)
        
        # Create engine and initialize for encryption
        engine = SM2Engine()
        engine.init(True, ParametersWithRandom(pub_key, SecureRandom()))
        
        # Encrypt
        return engine.process_block(message_bytes, 0, len(message_bytes))
    
    @classmethod
    def decrypt(cls, ciphertext: bytes, private_key: int) -> bytes:
        """
        Decrypt ciphertext using SM2 private key.
        
        Args:
            ciphertext: Ciphertext to decrypt
            private_key: Private key
        
        Returns:
            Decrypted plaintext as bytes
        """
        # Create private key parameters
        domain_params = cls.get_parameters()
        priv_key = ECPrivateKeyParameters(private_key, domain_params)
        
        # Create engine and initialize for decryption
        engine = SM2Engine()
        engine.init(False, priv_key)
        
        # Decrypt
        return engine.process_block(ciphertext, 0, len(ciphertext))
    
    @classmethod
    def sign(cls, message: bytes | str, private_key: int) -> bytes:
        """
        Sign a message using SM2 private key.
        
        Args:
            message: Message to sign (string or bytes)
            private_key: Private key for signing
        
        Returns:
            Signature as bytes
        """
        # Convert string to bytes if needed
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
        
        # Create private key parameters
        domain_params = cls.get_parameters()
        priv_key = ECPrivateKeyParameters(private_key, domain_params)
        
        # Create signer and initialize for signing
        signer = SM2Signer()
        signer.init(True, ParametersWithRandom(priv_key, SecureRandom()))
        
        # Update signer with message data
        signer.update_bytes(message_bytes, 0, len(message_bytes))
        
        # Generate signature
        return signer.generate_signature()
    
    @classmethod
    def verify(cls, message: bytes | str, signature: bytes, 
               public_key: dict | int, public_key_y: int = None) -> bool:
        """
        Verify a signature using SM2 public key.
        
        Args:
            message: Original message (string or bytes)
            signature: Signature to verify
            public_key: Public key object with x and y coordinates, or separate x coordinate
            public_key_y: Public key Y coordinate (if first parameter is not a dict)
        
        Returns:
            True if signature is valid, False otherwise
        """
        # Convert string to bytes if needed
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
        
        # Handle different parameter formats
        if isinstance(public_key, dict):
            public_key_x = public_key['x']
            public_key_y_value = public_key['y']
        elif isinstance(public_key, int) and isinstance(public_key_y, int):
            public_key_x = public_key
            public_key_y_value = public_key_y
        else:
            raise ValueError('Invalid public key format. Expected dict with x,y properties or separate x,y int values')
        
        # Create public key parameters
        curve = cls.get_curve()
        Q = curve.create_point(public_key_x, public_key_y_value)
        domain_params = cls.get_parameters()
        pub_key = ECPublicKeyParameters(Q, domain_params)
        
        # Create signer and initialize for verification
        signer = SM2Signer()
        signer.init(False, pub_key)
        
        # Update signer with message data
        signer.update_bytes(message_bytes, 0, len(message_bytes))
        
        # Verify the signature
        return signer.verify_signature(signature)
