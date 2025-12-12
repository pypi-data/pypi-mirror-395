from typing import Protocol
from sm_bc.crypto.digest import Digest

class ExtendedDigest(Digest, Protocol):
    """
    Extended interface for message digests that provide access to the internal byte length.
    """
    def get_byte_length(self) -> int:
        """Return the size in bytes of the internal buffer of this digest."""
        ...
