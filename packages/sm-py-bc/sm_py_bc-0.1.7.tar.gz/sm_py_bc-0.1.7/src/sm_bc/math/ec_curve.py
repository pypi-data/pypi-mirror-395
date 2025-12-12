from abc import ABC, abstractmethod
from typing import Optional, Union, List
from sm_bc.math.ec_field_element import ECFieldElement, Fp
import sm_bc.math.ec_point as ec_point # Circular import handling

class ECCurve(ABC):
    def __init__(self, field_size: int):
        self.field_size = field_size
        self.a: Optional[ECFieldElement] = None
        self.b: Optional[ECFieldElement] = None
        self.order = None
        self.cofactor = None
        self.coord_system = 0 # AFFINE default

    @abstractmethod
    def get_field_size(self) -> int:
        pass

    @abstractmethod
    def from_big_integer(self, x: int) -> ECFieldElement:
        pass

    @abstractmethod
    def create_point(self, x: int, y: int) -> 'ec_point.ECPoint':
        pass

    @abstractmethod
    def get_infinity(self) -> 'ec_point.ECPoint':
        pass
    
    def validate_point(self, x: int, y: int) -> 'ec_point.ECPoint':
        p = self.create_point(x, y)
        if not p.is_valid():
            raise ValueError("Point not on curve")
        return p

    def decode_point(self, encoded: Union[bytes, bytearray, List[int]]) -> 'ec_point.ECPoint':
        p = None
        expected_length = (self.field_size + 7) // 8

        type_ = encoded[0]
        
        if type_ == 0x00:
            return self.get_infinity()
            
        if type_ == 0x02 or type_ == 0x03:
            # Compressed
            if len(encoded) != (expected_length + 1):
                raise ValueError("Incorrect length for compressed encoding")
            
            y_tilde = type_ & 1
            x_bytes = encoded[1:]
            # Convert x_bytes to int
            x_val = int.from_bytes(x_bytes, 'big')
            x = self.from_big_integer(x_val)
            
            # Solve for y: y^2 = x^3 + ax + b
            # alpha = x^3 + ax + b
            alpha = x.multiply(x).add(self.a).multiply(x).add(self.b)
            beta = alpha.sqrt()
            
            if beta is None:
                raise ValueError("Invalid point compression")
            
            bit0 = 1 if beta.test_bit_zero() else 0
            
            if bit0 != y_tilde:
                beta = beta.negate()
                
            p = self.create_raw_point(x, beta)
            
        elif type_ == 0x04 or type_ == 0x06 or type_ == 0x07:
            # Uncompressed (04) or Hybrid (06/07)
            if len(encoded) != (2 * expected_length + 1):
                raise ValueError("Incorrect length for uncompressed/hybrid encoding")
            
            x_bytes = encoded[1:expected_length+1]
            y_bytes = encoded[expected_length+1:]
            
            x = self.from_big_integer(int.from_bytes(x_bytes, 'big'))
            y = self.from_big_integer(int.from_bytes(y_bytes, 'big'))
            
            p = self.create_raw_point(x, y)
        else:
             raise ValueError("Invalid point encoding " + str(type_))
             
        return p

    @abstractmethod
    def create_raw_point(self, x: ECFieldElement, y: ECFieldElement) -> 'ec_point.ECPoint':
        pass

    def __eq__(self, other):
        if self is other: return True
        if not isinstance(other, ECCurve): return False
        return self.field_size == other.field_size and self.a == other.a and self.b == other.b


class Fp(ECCurve):
    def __init__(self, q: int, a: int, b: int, order: int = None, cofactor: int = None):
        super().__init__(q.bit_length())
        self.q = q
        self.a = self.from_big_integer(a)
        self.b = self.from_big_integer(b)
        self.order = order
        self.cofactor = cofactor
        self._infinity = ec_point.Fp(self, None, None)

    def get_field_size(self) -> int:
        return self.q.bit_length()

    def from_big_integer(self, x: int) -> ECFieldElement:
        return Fp.FpElement(self.q, x)

    def create_point(self, x: int, y: int) -> 'ec_point.ECPoint':
        return self.create_raw_point(self.from_big_integer(x), self.from_big_integer(y))

    def create_raw_point(self, x: ECFieldElement, y: ECFieldElement) -> 'ec_point.ECPoint':
        return ec_point.Fp(self, x, y)

    def get_infinity(self) -> 'ec_point.ECPoint':
        return self._infinity
    
    def equals(self, other) -> bool:
        """Check if two curves are equal."""
        if not isinstance(other, Fp):
            return False
        return (self.q == other.q and 
                (self.a.equals(other.a) if hasattr(self.a, 'equals') else self.a == other.a) and
                (self.b.equals(other.b) if hasattr(self.b, 'equals') else self.b == other.b))
    
    # Alias the element class for internal use
    from sm_bc.math.ec_field_element import Fp as FpElement
