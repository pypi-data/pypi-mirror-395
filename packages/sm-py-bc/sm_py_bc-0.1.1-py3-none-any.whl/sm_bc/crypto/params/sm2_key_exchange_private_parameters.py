"""
SM2 Key Exchange Private Parameters.

Contains both static and ephemeral private keys along with their
corresponding public points for the key agreement protocol.
"""

from ..cipher_parameters import CipherParameters
from .ec_private_key_parameters import ECPrivateKeyParameters
from ...math.ec_point import ECPoint
from ...math.ec_multiplier import FixedPointCombMultiplier


class SM2KeyExchangePrivateParameters(CipherParameters):
    """
    Private parameters for an SM2 key exchange.
    The ephemeralPrivateKey is used to calculate the random point used in the algorithm.
    """

    def __init__(
        self,
        initiator: bool,
        static_private_key: ECPrivateKeyParameters,
        ephemeral_private_key: ECPrivateKeyParameters
    ):
        """
        Create SM2 key exchange private parameters.

        Args:
            initiator: Whether this party is the initiator of the key exchange
            static_private_key: The static private key
            ephemeral_private_key: The ephemeral private key

        Raises:
            ValueError: If keys are None or have different domain parameters
        """
        if static_private_key is None:
            raise ValueError("staticPrivateKey cannot be None")
        if ephemeral_private_key is None:
            raise ValueError("ephemeralPrivateKey cannot be None")

        parameters = static_private_key.parameters
        if not parameters.equals(ephemeral_private_key.parameters):
            raise ValueError("Static and ephemeral private keys have different domain parameters")

        m = FixedPointCombMultiplier()

        self._initiator = initiator
        self._static_private_key = static_private_key
        self._static_public_point = m.multiply(parameters.g, static_private_key.d).normalize()
        self._ephemeral_private_key = ephemeral_private_key
        self._ephemeral_public_point = m.multiply(parameters.g, ephemeral_private_key.d).normalize()

    def is_initiator(self) -> bool:
        """Check if this party is the initiator."""
        return self._initiator

    def get_static_private_key(self) -> ECPrivateKeyParameters:
        """Get the static private key."""
        return self._static_private_key

    def get_static_public_point(self) -> ECPoint:
        """Get the computed static public point."""
        return self._static_public_point

    def get_ephemeral_private_key(self) -> ECPrivateKeyParameters:
        """Get the ephemeral private key."""
        return self._ephemeral_private_key

    def get_ephemeral_public_point(self) -> ECPoint:
        """Get the computed ephemeral public point."""
        return self._ephemeral_public_point
