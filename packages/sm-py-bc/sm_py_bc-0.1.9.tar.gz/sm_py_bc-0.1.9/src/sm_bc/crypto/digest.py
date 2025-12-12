from typing import Protocol, Union, List, MutableSequence

class Digest(Protocol):
    """
    Base interface for message digests.
    """
    def get_algorithm_name(self) -> str:
        """Return the name of the algorithm the digest implements."""
        ...

    def get_digest_size(self) -> int:
        """Return the size in bytes of the digest produced by this message digest."""
        ...

    def update(self, input_: int) -> None:
        """Update the digest with a single byte."""
        ...

    def update_bytes(self, input_: Union[bytes, bytearray, List[int]], offset: int, length: int) -> None:
        """Update the digest with a block of bytes."""
        ...

    def do_final(self, output: MutableSequence[int], offset: int) -> int:
        """
        Close the digest, producing the final digest value.
        The do_final call leaves the digest reset.
        """
        ...

    def reset(self) -> None:
        """Reset the digest back to its initial state."""
        ...
