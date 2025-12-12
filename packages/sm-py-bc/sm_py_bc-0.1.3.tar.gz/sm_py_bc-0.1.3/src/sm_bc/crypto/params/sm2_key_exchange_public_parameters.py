"""
SM2 Key Exchange Public Parameters.

Contains both static and ephemeral public keys for the key agreement protocol.
"""

from ..cipher_parameters import CipherParameters
from .ec_public_key_parameters import ECPublicKeyParameters


class SM2KeyExchangePublicParameters(CipherParameters):
    """
    Public parameters for an SM2 key exchange.
    In this case the ephemeralPublicKey provides the random point used in the algorithm.
    """

    def __init__(
        self,
        static_public_key: ECPublicKeyParameters,
        ephemeral_public_key: ECPublicKeyParameters
    ):
        """
        Create SM2 key exchange public parameters.

        Args:
            static_public_key: The static public key
            ephemeral_public_key: The ephemeral public key

        Raises:
            ValueError: If keys are None or have different domain parameters
        """
        if static_public_key is None:
            raise ValueError("staticPublicKey cannot be None")
        if ephemeral_public_key is None:
            raise ValueError("ephemeralPublicKey cannot be None")
        if not static_public_key.parameters.equals(ephemeral_public_key.parameters):
            raise ValueError("Static and ephemeral public keys have different domain parameters")

        self._static_public_key = static_public_key
        self._ephemeral_public_key = ephemeral_public_key

    def get_static_public_key(self) -> ECPublicKeyParameters:
        """Get the static public key."""
        return self._static_public_key

    def get_ephemeral_public_key(self) -> ECPublicKeyParameters:
        """Get the ephemeral public key."""
        return self._ephemeral_public_key
