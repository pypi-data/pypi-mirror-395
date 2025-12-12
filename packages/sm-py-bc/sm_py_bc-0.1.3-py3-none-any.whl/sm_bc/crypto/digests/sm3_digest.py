from typing import Union, List, MutableSequence
from sm_bc.crypto.digests.general_digest import GeneralDigest
from sm_bc.util.pack import Pack
from sm_bc.util.memoable import Memoable

class SM3Digest(GeneralDigest):
    DIGEST_LENGTH = 32
    BLOCK_SIZE = 16 # words

    # IV
    IV = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
    ]

    # T constants
    T = [0] * 64
    for i in range(16):
        t = 0x79CC4519
        T[i] = ((t << i) & 0xFFFFFFFF) | (t >> (32 - i))
    for i in range(16, 64):
        n = i % 32
        t = 0x7A879D8A
        T[i] = ((t << n) & 0xFFFFFFFF) | (t >> (32 - n))

    def __init__(self, t: 'SM3Digest' = None):
        self._v = [0] * 8
        self._inwords = [0] * 16
        self._x_off = 0
        self._w = [0] * 68
        super().__init__(t)
        
        if not t:
            self.reset()

    def copy_in(self, t: 'SM3Digest') -> None:
        super().copy_in(t)
        self._v[:] = t._v
        self._inwords[:] = t._inwords
        self._x_off = t._x_off
        # _w is scratch space, no need to copy

    def get_algorithm_name(self) -> str:
        return "SM3"

    def get_digest_size(self) -> int:
        return self.DIGEST_LENGTH

    def do_final(self, output: MutableSequence[int], offset: int) -> int:
        self.finish()
        for i in range(8):
            Pack.int_to_big_endian(self._v[i], output, offset + i * 4)
        self.reset()
        return self.DIGEST_LENGTH

    def reset(self) -> None:
        super().reset()
        self._v[:] = self.IV
        self._x_off = 0
        for i in range(16):
            self._inwords[i] = 0

    def process_word(self, input_: Union[bytes, bytearray, List[int]], offset: int) -> None:
        self._inwords[self._x_off] = Pack.big_endian_to_int(input_, offset)
        self._x_off += 1
        if self._x_off >= 16:
            self.process_block()

    def process_length(self, bit_length: int) -> None:
        if self._x_off > 14:
            self._inwords[self._x_off] = 0
            self._x_off += 1
            self.process_block()
        
        while self._x_off < 14:
            self._inwords[self._x_off] = 0
            self._x_off += 1
        
        # Length is 64-bit, written as two 32-bit words (Big Endian)
        self._inwords[self._x_off] = (bit_length >> 32) & 0xFFFFFFFF
        self._x_off += 1
        self._inwords[self._x_off] = bit_length & 0xFFFFFFFF
        self._x_off += 1

    def process_block(self) -> None:
        W = self._w
        inwords = self._inwords
        V = self._v
        T = self.T

        # 1. Message Expansion
        for j in range(16):
            W[j] = inwords[j]

        for j in range(16, 68):
            wj3 = W[j - 3]
            r15 = ((wj3 << 15) & 0xFFFFFFFF) | (wj3 >> 17)
            wj13 = W[j - 13]
            r7 = ((wj13 << 7) & 0xFFFFFFFF) | (wj13 >> 25)
            
            tmp = W[j - 16] ^ W[j - 9] ^ r15
            p1 = tmp ^ (((tmp << 15) & 0xFFFFFFFF) | (tmp >> 17)) ^ (((tmp << 23) & 0xFFFFFFFF) | (tmp >> 9))
            
            W[j] = p1 ^ r7 ^ W[j - 6]

        A, B, C, D, E, F, G, H = V

        # 2. Compression
        for j in range(64):
            # ROTL(A, 12)
            a12 = ((A << 12) & 0xFFFFFFFF) | (A >> 20)
            
            # SS1
            s1 = (a12 + E + T[j]) & 0xFFFFFFFF
            ss1 = ((s1 << 7) & 0xFFFFFFFF) | (s1 >> 25)
            
            # SS2
            ss2 = ss1 ^ a12
            
            Wj = W[j]
            W1j = Wj ^ W[j + 4]
            
            # TT1, TT2
            if j < 16:
                # FF0, GG0
                ff = A ^ B ^ C
                gg = E ^ F ^ G
            else:
                # FF1, GG1
                ff = (A & B) | (A & C) | (B & C)
                gg = (E & F) | ((~E) & G) & 0xFFFFFFFF # Mask ~E
            
            tt1 = (ff + D + ss2 + W1j) & 0xFFFFFFFF
            tt2 = (gg + H + ss1 + Wj) & 0xFFFFFFFF
            
            D = C
            C = ((B << 9) & 0xFFFFFFFF) | (B >> 23)
            B = A
            A = tt1
            H = G
            G = ((F << 19) & 0xFFFFFFFF) | (F >> 13)
            F = E
            E = tt2 ^ (((tt2 << 9) & 0xFFFFFFFF) | (tt2 >> 23)) ^ (((tt2 << 17) & 0xFFFFFFFF) | (tt2 >> 15)) # P0(tt2)

        # 3. Update V
        V[0] ^= A
        V[1] ^= B
        V[2] ^= C
        V[3] ^= D
        V[4] ^= E
        V[5] ^= F
        V[6] ^= G
        V[7] ^= H
        
        self._x_off = 0

    # Memoable
    def copy(self) -> 'SM3Digest':
        return SM3Digest(self)

    def reset_from_memoable(self, other: Memoable) -> None:
        self.copy_in(other)
    
    def reset_memoable(self, other: Memoable) -> None:
        self.copy_in(other)

