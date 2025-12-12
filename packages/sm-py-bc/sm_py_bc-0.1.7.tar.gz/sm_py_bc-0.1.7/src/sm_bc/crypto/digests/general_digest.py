from typing import Union, List, MutableSequence
from sm_bc.crypto.extended_digest import ExtendedDigest
from sm_bc.util.memoable import Memoable
from sm_bc.util.pack import Pack

class GeneralDigest(ExtendedDigest, Memoable):
    """
    Base class for MD4-family digests.
    """
    BYTE_LENGTH = 64

    def __init__(self, t: 'GeneralDigest' = None):
        self._x_buf = bytearray(4)
        self._x_buf_off = 0
        self._byte_count = 0
        if t:
            self.copy_in(t)

    def copy_in(self, t: 'GeneralDigest') -> None:
        self._x_buf[:] = t._x_buf
        self._x_buf_off = t._x_buf_off
        self._byte_count = t._byte_count

    def update(self, input_: int) -> None:
        self._x_buf[self._x_buf_off] = input_
        self._x_buf_off += 1
        if self._x_buf_off == 4:
            self.process_word(self._x_buf, 0)
            self._x_buf_off = 0
        self._byte_count += 1

    def update_bytes(self, input_: Union[bytes, bytearray, List[int]], offset: int, length: int) -> None:
        # Determine the limit
        limit = offset + length
        limit = max(offset, limit) # ensure no negative length implies weirdness

        # If we have buffered bytes, fill the buffer first
        while self._x_buf_off != 0 and offset < limit:
            self.update(input_[offset])
            offset += 1
        
        # Process full 4-byte words directly
        while offset <= (limit - 4):
            self.process_word(input_, offset)
            offset += 4
            self._byte_count += 4
        
        # Buffer remaining bytes
        while offset < limit:
            self.update(input_[offset])
            offset += 1

    def finish(self) -> None:
        bit_length = self._byte_count << 3
        self.update(128)
        while self._x_buf_off != 0:
            self.update(0)
        
        self.process_length(bit_length)
        self.process_block()

    def reset(self) -> None:
        self._byte_count = 0
        self._x_buf_off = 0
        for i in range(4):
            self._x_buf[i] = 0

    def get_byte_length(self) -> int:
        return 64

    def process_word(self, input_: Union[bytes, bytearray, List[int]], offset: int) -> None:
        raise NotImplementedError

    def process_length(self, bit_length: int) -> None:
        raise NotImplementedError

    def process_block(self) -> None:
        raise NotImplementedError
