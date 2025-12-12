from abc import ABC, abstractmethod
from typing import Optional

class ECFieldElement(ABC):
    @abstractmethod
    def to_big_integer(self) -> int:
        pass

    @abstractmethod
    def get_field_size(self) -> int:
        pass

    @abstractmethod
    def add(self, b: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def add_one(self) -> 'ECFieldElement':
        pass

    @abstractmethod
    def subtract(self, b: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def multiply(self, b: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def divide(self, b: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def negate(self) -> 'ECFieldElement':
        pass

    @abstractmethod
    def square(self) -> 'ECFieldElement':
        pass

    @abstractmethod
    def invert(self) -> 'ECFieldElement':
        pass

    @abstractmethod
    def sqrt(self) -> Optional['ECFieldElement']:
        pass

    @abstractmethod
    def multiply_minus_product(self, b: 'ECFieldElement', x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def multiply_plus_product(self, b: 'ECFieldElement', x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def square_minus_product(self, x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def square_plus_product(self, x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        pass

    @abstractmethod
    def test_bit_zero(self) -> bool:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ECFieldElement):
            return False
        return self.to_big_integer() == other.to_big_integer() and self.get_field_size() == other.get_field_size()

    def __str__(self) -> str:
        return hex(self.to_big_integer())[2:].upper()


class Fp(ECFieldElement):
    def __init__(self, q: int, x: int):
        self.q = q
        self.x = x % q

    def to_big_integer(self) -> int:
        return self.x

    def get_field_size(self) -> int:
        return self.q.bit_length()

    def add(self, b: 'ECFieldElement') -> 'ECFieldElement':
        return Fp(self.q, self.x + b.to_big_integer())

    def add_one(self) -> 'ECFieldElement':
        return Fp(self.q, self.x + 1)

    def subtract(self, b: 'ECFieldElement') -> 'ECFieldElement':
        return Fp(self.q, self.x - b.to_big_integer())

    def multiply(self, b: 'ECFieldElement') -> 'ECFieldElement':
        return Fp(self.q, self.x * b.to_big_integer())

    def divide(self, b: 'ECFieldElement') -> 'ECFieldElement':
        return Fp(self.q, self.x * pow(b.to_big_integer(), -1, self.q))

    def negate(self) -> 'ECFieldElement':
        return Fp(self.q, -self.x)

    def square(self) -> 'ECFieldElement':
        return Fp(self.q, self.x * self.x)

    def invert(self) -> 'ECFieldElement':
        return Fp(self.q, pow(self.x, -1, self.q))

    def sqrt(self) -> Optional['ECFieldElement']:
        # Simple check for p % 4 == 3
        if (self.q & 3) == 3:
            # x ^ ((p+1)/4)
            z = pow(self.x, (self.q + 1) >> 2, self.q)
            if (z * z) % self.q == self.x:
                return Fp(self.q, z)
            return None
        
        # Tonelli-Shanks for general case (p % 4 == 1)
        # First check if x is a quadratic residue
        if pow(self.x, (self.q - 1) // 2, self.q) != 1:
            return None

        s = 0
        t = self.q - 1
        while (t & 1) == 0:
            t >>= 1
            s += 1
        
        if s == 1:
            z = pow(self.x, (self.q + 1) >> 2, self.q)
            return Fp(self.q, z) if (z * z) % self.q == self.x else None

        # Find a non-residue z
        z = 1
        while pow(z, (self.q - 1) // 2, self.q) != self.q - 1:
            z += 1
        
        c = pow(z, t, self.q)
        r = pow(self.x, (t + 1) // 2, self.q)
        t = pow(self.x, t, self.q)
        m = s

        while True:
            if t == 1:
                return Fp(self.q, r)
            
            i = 0
            zz = t
            found = False
            for i in range(1, m):
                zz = (zz * zz) % self.q
                if zz == 1:
                    found = True
                    break
            
            if not found:
                return None
                
            b = c
            for _ in range(m - i - 1):
                b = (b * b) % self.q
            
            r = (r * b) % self.q
            c = (b * b) % self.q
            t = (t * c) % self.q
            m = i
    
    def get_encoded(self) -> bytes:
        """Encode field element as bytes (big-endian)."""
        byte_len = (self.q.bit_length() + 7) // 8
        return self.x.to_bytes(byte_len, 'big')

    def multiply_minus_product(self, b: 'ECFieldElement', x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        ax = self.x
        bx = b.to_big_integer()
        xx = x.to_big_integer()
        yx = y.to_big_integer()
        return Fp(self.q, ax * bx - xx * yx)

    def multiply_plus_product(self, b: 'ECFieldElement', x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        ax = self.x
        bx = b.to_big_integer()
        xx = x.to_big_integer()
        yx = y.to_big_integer()
        return Fp(self.q, ax * bx + xx * yx)

    def square_minus_product(self, x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        ax = self.x
        xx = x.to_big_integer()
        yx = y.to_big_integer()
        return Fp(self.q, ax * ax - xx * yx)

    def square_plus_product(self, x: 'ECFieldElement', y: 'ECFieldElement') -> 'ECFieldElement':
        ax = self.x
        xx = x.to_big_integer()
        yx = y.to_big_integer()
        return Fp(self.q, ax * ax + xx * yx)

    def test_bit_zero(self) -> bool:
        return (self.x & 1) == 1
