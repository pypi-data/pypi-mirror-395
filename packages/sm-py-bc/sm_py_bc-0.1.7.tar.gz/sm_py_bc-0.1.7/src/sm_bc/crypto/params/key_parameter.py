from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters

class KeyParameter(CipherParameters):
    def __init__(self, key: Union[bytes, bytearray, List[int]]):
        self.key = bytearray(key)
        
    def get_key(self) -> bytearray:
        return self.key
