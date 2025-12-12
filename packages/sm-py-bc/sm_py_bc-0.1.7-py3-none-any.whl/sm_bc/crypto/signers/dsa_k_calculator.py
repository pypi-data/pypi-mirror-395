from typing import Protocol
from sm_bc.util.secure_random import SecureRandom

class DSAKCalculator(Protocol):
    def is_deterministic(self) -> bool:
        ...

    def init(self, n: int, random: SecureRandom) -> None:
        ...

    def next_k(self) -> int:
        ...

class RandomDSAKCalculator(DSAKCalculator):
    def __init__(self):
        self.n = 0
        self.random = None

    def is_deterministic(self) -> bool:
        return False

    def init(self, n: int, random: SecureRandom) -> None:
        self.n = n
        self.random = random

    def next_k(self) -> int:
        # Simple random generation mod n, ensuring k < n
        q_bit_length = self.n.bit_length()
        
        while True:
            # Generate bytes
            # Note: if n is small, this might be inefficient, but for ECC n is large
            byte_len = (q_bit_length + 7) // 8
            k_bytes = self.random.generate_seed(byte_len)
            k = int.from_bytes(k_bytes, 'big')
            
            if k > 0 and k < self.n:
                return k
