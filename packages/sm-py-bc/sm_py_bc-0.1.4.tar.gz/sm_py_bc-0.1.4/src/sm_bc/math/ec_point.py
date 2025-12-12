from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union, List
from sm_bc.math.ec_field_element import ECFieldElement
from sm_bc.util.pack import Pack

if TYPE_CHECKING:
    from sm_bc.math.ec_curve import ECCurve

class ECPoint(ABC):
    def __init__(self, curve: 'ECCurve', x: Optional[ECFieldElement], y: Optional[ECFieldElement], zs: List[ECFieldElement] = None):
        self.curve = curve
        self.x = x
        self.y = y
        self.zs = zs if zs is not None else []
        self.is_infinity = (x is None) or (y is None)

    @abstractmethod
    def add(self, b: 'ECPoint') -> 'ECPoint':
        pass

    @abstractmethod
    def subtract(self, b: 'ECPoint') -> 'ECPoint':
        pass

    @abstractmethod
    def negate(self) -> 'ECPoint':
        pass

    @abstractmethod
    def twice(self) -> 'ECPoint':
        pass

    def multiply(self, k: int) -> 'ECPoint':
        # LTR Double-and-Add
        if self.is_infinity:
            return self
        if k == 0:
            return self.curve.get_infinity()
        if k < 0:
            return self.negate().multiply(-k)
            
        q = self.curve.get_infinity()
        for i in range(k.bit_length() - 1, -1, -1):
            q = q.twice()
            if (k >> i) & 1:
                q = q.add(self)
        return q

    def get_encoded(self, compressed: bool) -> bytes:
        if self.is_infinity:
            return b'\x00'
        
        norm = self.normalize()
        x = norm.x.to_big_integer()
        y = norm.y.to_big_integer()
        
        byte_len = (self.curve.get_field_size() + 7) // 8
        x_bytes = x.to_bytes(byte_len, 'big')
        
        if compressed:
            y_bit = 1 if norm.y.test_bit_zero() else 0
            # 02 or 03
            header = 0x02 | y_bit
            return bytes([header]) + x_bytes
        else:
            y_bytes = y.to_bytes(byte_len, 'big')
            # 04
            return b'\x04' + x_bytes + y_bytes

    def normalize(self) -> 'ECPoint':
        if self.is_infinity:
            return self
            
        # If already affine (Z=1), return self
        # We assume Z is zs[0]
        if not self.zs:
            return self
            
        z = self.zs[0]
        if z.to_big_integer() == 1:
            return self
            
        # Jacobian to Affine
        # x = X / Z^2
        # y = Y / Z^3
        z_inv = z.invert()
        z_inv2 = z_inv.square()
        z_inv3 = z_inv2.multiply(z_inv)
        
        x_aff = self.x.multiply(z_inv2)
        y_aff = self.y.multiply(z_inv3)
        
        return self.curve.create_raw_point(x_aff, y_aff)
    
    def is_valid(self) -> bool:
        if self.is_infinity:
            return True
        
        # Check if point is valid on curve
        # If Jacobian, convert to Affine first or check Jacobian equation
        p = self.normalize()
        
        # y^2 = x^3 + ax + b
        lhs = p.y.square()
        rhs = p.x.square().multiply(p.x).add(self.curve.a.multiply(p.x)).add(self.curve.b)
        return lhs == rhs

    def __eq__(self, other):
        if self is other: return True
        if not isinstance(other, ECPoint): return False
        if self.is_infinity: return other.is_infinity
        if other.is_infinity: return False
        
        p1 = self.normalize()
        p2 = other.normalize()
        return p1.x == p2.x and p1.y == p2.y and self.curve == other.curve
    
    def equals(self, other) -> bool:
        """Check if two points are equal."""
        return self == other

class Fp(ECPoint):
    def __init__(self, curve: 'ECCurve', x: Optional[ECFieldElement], y: Optional[ECFieldElement], zs: List[ECFieldElement] = None):
        super().__init__(curve, x, y, zs)

    def add(self, b: 'ECPoint') -> 'ECPoint':
        if self.is_infinity: return b
        if b.is_infinity: return self
        if self is b: return self.twice()
        
        # Jacobian Addition
        X1, Y1 = self.x, self.y
        Z1 = self.zs[0] if self.zs else self.curve.from_big_integer(1)
        
        X2, Y2 = b.x, b.y
        Z2 = b.zs[0] if b.zs else self.curve.from_big_integer(1)
        
        # Check if Zs are 1 (optimization)
        Z1_is_one = Z1.to_big_integer() == 1
        Z2_is_one = Z2.to_big_integer() == 1
        
        if Z1_is_one:
            U2 = X2
            S2 = Y2
        else:
            Z1_sq = Z1.square()
            U2 = X2.multiply(Z1_sq)
            S2 = Y2.multiply(Z1_sq.multiply(Z1))
            
        if Z2_is_one:
            U1 = X1
            S1 = Y1
        else:
            Z2_sq = Z2.square()
            U1 = X1.multiply(Z2_sq)
            S1 = Y1.multiply(Z2_sq.multiply(Z2))
            
        H = U2.subtract(U1)
        R = S2.subtract(S1)
        
        # If H == 0 (X1 == X2)
        if H.to_big_integer() == 0:
            if R.to_big_integer() == 0:
                # X1=X2, Y1=Y2 -> P = Q -> twice
                return self.twice()
            else:
                # X1=X2, Y1=-Y2 -> P = -Q -> Infinity
                return self.curve.get_infinity()
        
        H_sq = H.square()
        H_cu = H_sq.multiply(H)
        # X3 = R^2 - H^3 - 2*U1*H^2
        #    = R^2 - (H^3 + 2*U1*H^2)
        
        U1_H_sq = U1.multiply(H_sq)
        X3 = R.square().subtract(H_cu).subtract(U1_H_sq.add(U1_H_sq)) # subtract 2*U1*H^2
        
        # Y3 = R(U1H^2 - X3) - S1H^3
        Y3 = R.multiply(U1_H_sq.subtract(X3)).subtract(S1.multiply(H_cu))
        
        # Z3 = H * Z1 * Z2
        if Z1_is_one:
            if Z2_is_one:
                Z3 = H
            else:
                Z3 = H.multiply(Z2)
        else:
            if Z2_is_one:
                Z3 = H.multiply(Z1)
            else:
                Z3 = H.multiply(Z1).multiply(Z2)
                
        return Fp(self.curve, X3, Y3, [Z3])

    def twice(self) -> 'ECPoint':
        if self.is_infinity: return self
        
        X1, Y1 = self.x, self.y
        Z1 = self.zs[0] if self.zs else self.curve.from_big_integer(1)
        
        if Y1.to_big_integer() == 0:
            return self.curve.get_infinity()
            
        # Jacobian Doubling
        # M = 3X1^2 + aZ1^4
        # if Z1=1, M = 3X1^2 + a
        
        X1_sq = X1.square()
        
        if Z1.to_big_integer() == 1:
            M = X1_sq.add(X1_sq).add(X1_sq).add(self.curve.a) # 3X1^2 + a
        else:
            Z1_sq = Z1.square()
            Z1_4 = Z1_sq.square()
            # aZ1^4
            # Note: a might be negative? handled by Fp.
            M = X1_sq.add(X1_sq).add(X1_sq).add(self.curve.a.multiply(Z1_4))
            
        Y1_sq = Y1.square()
        S = X1.multiply(Y1_sq).multiply(self.curve.from_big_integer(4)) # 4XY^2
        T = Y1_sq.square().multiply(self.curve.from_big_integer(8)) # 8Y^4
        
        X3 = M.square().subtract(S.add(S)) # M^2 - 2S
        
        # Y3 = M(S - X3) - T
        Y3 = M.multiply(S.subtract(X3)).subtract(T)
        
        # Z3 = 2Y1Z1
        Z3 = Y1.multiply(Z1).multiply(self.curve.from_big_integer(2))
        
        return Fp(self.curve, X3, Y3, [Z3])

    def subtract(self, b: 'ECPoint') -> 'ECPoint':
        if b.is_infinity: return self
        return self.add(b.negate())

    def negate(self) -> 'ECPoint':
        if self.is_infinity: return self
        return Fp(self.curve, self.x, self.y.negate(), self.zs)