"""
SM2 Key Exchange protocol implementation.

Based on https://tools.ietf.org/html/draft-shen-sm2-ecdsa-02

Implements the SM2 key agreement protocol allowing two parties to establish
a shared secret key over an insecure communication channel.
"""

import math
from typing import Optional, List

from ..digest import Digest
from ..digests.sm3_digest import SM3Digest
from ..cipher_parameters import CipherParameters
from ..params.parameters_with_id import ParametersWithID
from ..params.sm2_key_exchange_private_parameters import SM2KeyExchangePrivateParameters
from ..params.sm2_key_exchange_public_parameters import SM2KeyExchangePublicParameters
from ..params.ec_private_key_parameters import ECPrivateKeyParameters
from ..params.ec_domain_parameters import ECDomainParameters
from ...math.ec_point import ECPoint
from ...math.ec_field_element import ECFieldElement
from ...math.ec_algorithms import ECAlgorithms
from ...util.arrays import Arrays
from ...util.pack import Pack


class SM2KeyExchange:
    """
    SM2 Key Exchange implementation.

    This class implements the SM2 key agreement protocol that allows two parties
    (initiator and responder) to establish a shared secret key.
    """

    def __init__(self, digest: Optional[Digest] = None):
        """
        Constructor.

        Args:
            digest: Optional digest to use (defaults to SM3)
        """
        self.digest = digest if digest is not None else SM3Digest()
        self.user_id = bytes()
        self.static_key: Optional[ECPrivateKeyParameters] = None
        self.static_pub_point: Optional[ECPoint] = None
        self.ephemeral_pub_point: Optional[ECPoint] = None
        self.ec_params: Optional[ECDomainParameters] = None
        self.w: Optional[int] = None
        self.ephemeral_key: Optional[ECPrivateKeyParameters] = None
        self.initiator: Optional[bool] = None

    def init(self, priv_param: CipherParameters) -> None:
        """
        Initialize the key exchange with private parameters.

        Args:
            priv_param: Private parameters for key exchange
        """
        if isinstance(priv_param, ParametersWithID):
            base_param = priv_param.get_parameters()
            self.user_id = priv_param.get_id()
        else:
            base_param = priv_param
            self.user_id = bytes()

        if not isinstance(base_param, SM2KeyExchangePrivateParameters):
            raise ValueError("Expected SM2KeyExchangePrivateParameters")

        self.initiator = base_param.is_initiator()
        self.static_key = base_param.get_static_private_key()
        self.ephemeral_key = base_param.get_ephemeral_private_key()
        self.ec_params = self.static_key.parameters
        self.static_pub_point = base_param.get_static_public_point()
        self.ephemeral_pub_point = base_param.get_ephemeral_public_point()

        # Calculate w = floor((field_size - 1) / 2)
        self.w = (self.ec_params.curve.get_field_size() - 1) // 2

    def calculate_key(self, k_len: int, pub_param: CipherParameters) -> bytes:
        """
        Calculate the shared key.

        Args:
            k_len: Length of the key to generate (in bits)
            pub_param: Public parameters from the other party

        Returns:
            The generated shared key
        """
        if k_len <= 0:
            raise ValueError("Key length must be positive")

        if isinstance(pub_param, ParametersWithID):
            other_pub = pub_param.get_parameters()
            other_user_id = pub_param.get_id()
        else:
            other_pub = pub_param
            other_user_id = bytes()

        if not isinstance(other_pub, SM2KeyExchangePublicParameters):
            raise ValueError("Expected SM2KeyExchangePublicParameters")

        za = self._get_z(self.digest, self.user_id, self.static_pub_point)
        zb = self._get_z(self.digest, other_user_id, other_pub.get_static_public_key().q)

        u = self._calculate_u(other_pub)

        if self.initiator:
            rv = self._kdf(u, za, zb, k_len)
        else:
            rv = self._kdf(u, zb, za, k_len)

        return rv

    def calculate_key_with_confirmation(
        self,
        k_len: int,
        confirmation_tag: Optional[bytes],
        pub_param: CipherParameters
    ) -> List[bytes]:
        """
        Calculate key with confirmation tags.

        Args:
            k_len: Length of the key to generate (in bits)
            confirmation_tag: Confirmation tag from the other party (for initiator)
            pub_param: Public parameters from the other party

        Returns:
            Array containing [key, confirmationTag1, confirmationTag2]
        """
        if k_len <= 0:
            raise ValueError("Key length must be positive")

        if isinstance(pub_param, ParametersWithID):
            other_pub = pub_param.get_parameters()
            other_user_id = pub_param.get_id()
        else:
            other_pub = pub_param
            other_user_id = bytes()

        if not isinstance(other_pub, SM2KeyExchangePublicParameters):
            raise ValueError("Expected SM2KeyExchangePublicParameters")

        if self.initiator and confirmation_tag is None:
            raise ValueError("If initiating, confirmationTag must be set")

        za = self._get_z(self.digest, self.user_id, self.static_pub_point)
        zb = self._get_z(self.digest, other_user_id, other_pub.get_static_public_key().q)

        u = self._calculate_u(other_pub)

        if self.initiator:
            rv = self._kdf(u, za, zb, k_len)

            inner = self._calculate_inner_hash(
                self.digest,
                u,
                za,
                zb,
                self.ephemeral_pub_point,
                other_pub.get_ephemeral_public_key().q
            )

            s1 = self._s1(self.digest, u, inner)

            if not Arrays.constant_time_are_equal(s1, confirmation_tag):
                raise ValueError("Confirmation tag mismatch")

            return [rv, self._s2(self.digest, u, inner)]
        else:
            rv = self._kdf(u, zb, za, k_len)

            inner = self._calculate_inner_hash(
                self.digest,
                u,
                zb,
                za,
                other_pub.get_ephemeral_public_key().q,
                self.ephemeral_pub_point
            )

            return [rv, self._s1(self.digest, u, inner), self._s2(self.digest, u, inner)]

    def _calculate_u(self, other_pub: SM2KeyExchangePublicParameters) -> ECPoint:
        """Calculate the U point for key derivation."""
        params = self.static_key.parameters

        p1 = ECAlgorithms.clean_point(params.curve, other_pub.get_static_public_key().q)
        p2 = ECAlgorithms.clean_point(params.curve, other_pub.get_ephemeral_public_key().q)

        x1 = self._reduce(self.ephemeral_pub_point.normalize().x.to_big_integer())
        x2 = self._reduce(p2.normalize().x.to_big_integer())
        t_a = self.static_key.d + (x1 * self.ephemeral_key.d)
        k1 = (self.ec_params.h * t_a) % self.ec_params.n
        k2 = (k1 * x2) % self.ec_params.n

        return ECAlgorithms.sum_of_two_multiplies(p1, k1, p2, k2).normalize()

    def _kdf(self, u: ECPoint, za: bytes, zb: bytes, klen: int) -> bytes:
        """Key Derivation Function (KDF) implementation."""
        digest_size = self.digest.get_digest_size()
        buf = bytearray(max(4, digest_size))
        rv = bytearray(math.ceil(klen / 8))
        off = 0

        # Memoable support not implemented yet - simpler version
        ct = 0

        while off < len(rv):
            normalized_u = u.normalize()
            self._add_field_element(self.digest, normalized_u.x)
            self._add_field_element(self.digest, normalized_u.y)
            self.digest.update_bytes(za, 0, len(za))
            self.digest.update_bytes(zb, 0, len(zb))

            ct += 1
            Pack.int_to_big_endian(ct, buf, 0)
            self.digest.update_bytes(buf, 0, 4)
            self.digest.do_final(buf, 0)

            copy_len = min(digest_size, len(rv) - off)
            rv[off:off + copy_len] = buf[0:copy_len]
            off += copy_len

        return bytes(rv)

    def _reduce(self, x: int) -> int:
        """Reduce function: x1~ = 2^w + (x1 AND (2^w - 1))"""
        mask = (1 << self.w) - 1
        return (x & mask) | (1 << self.w)

    def _s1(self, digest: Digest, u: ECPoint, inner: bytes) -> bytes:
        """Calculate S1 confirmation tag."""
        digest.update(0x02)
        normalized_u = u.normalize()
        self._add_field_element(digest, normalized_u.y)
        digest.update_bytes(inner, 0, len(inner))
        return self._digest_do_final()

    def _calculate_inner_hash(
        self,
        digest: Digest,
        u: ECPoint,
        za: bytes,
        zb: bytes,
        p1: ECPoint,
        p2: ECPoint
    ) -> bytes:
        """Calculate inner hash for confirmation."""
        normalized_u = u.normalize()
        normalized_p1 = p1.normalize()
        normalized_p2 = p2.normalize()
        self._add_field_element(digest, normalized_u.x)
        digest.update_bytes(za, 0, len(za))
        digest.update_bytes(zb, 0, len(zb))
        self._add_field_element(digest, normalized_p1.x)
        self._add_field_element(digest, normalized_p1.y)
        self._add_field_element(digest, normalized_p2.x)
        self._add_field_element(digest, normalized_p2.y)
        return self._digest_do_final()

    def _s2(self, digest: Digest, u: ECPoint, inner: bytes) -> bytes:
        """Calculate S2 confirmation tag."""
        digest.update(0x03)
        normalized_u = u.normalize()
        self._add_field_element(digest, normalized_u.y)
        digest.update_bytes(inner, 0, len(inner))
        return self._digest_do_final()

    def _get_z(self, digest: Digest, user_id: bytes, pub_point: ECPoint) -> bytes:
        """Calculate Z value (user identification hash)."""
        self._add_user_id(digest, user_id)

        self._add_field_element(digest, self.ec_params.curve.a)
        self._add_field_element(digest, self.ec_params.curve.b)
        self._add_field_element(digest, self.ec_params.g.x)
        self._add_field_element(digest, self.ec_params.g.y)
        normalized_pub_point = pub_point.normalize()
        self._add_field_element(digest, normalized_pub_point.x)
        self._add_field_element(digest, normalized_pub_point.y)

        return self._digest_do_final()

    def _add_user_id(self, digest: Digest, user_id: bytes) -> None:
        """Add user ID to digest with length prefix."""
        length = len(user_id) * 8  # Length in bits
        digest.update(length >> 8)
        digest.update(length & 0xFF)
        digest.update_bytes(user_id, 0, len(user_id))

    def _add_field_element(self, digest: Digest, v: ECFieldElement) -> None:
        """Add field element to digest."""
        p = v.get_encoded()
        digest.update_bytes(p, 0, len(p))

    def _digest_do_final(self) -> bytes:
        """Finalize digest and return result."""
        result = bytearray(self.digest.get_digest_size())
        self.digest.do_final(result, 0)
        return bytes(result)
