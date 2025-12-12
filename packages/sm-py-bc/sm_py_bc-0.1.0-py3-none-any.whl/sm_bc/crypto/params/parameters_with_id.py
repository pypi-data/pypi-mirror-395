from typing import Union, List
from sm_bc.crypto.cipher_parameters import CipherParameters

class ParametersWithID(CipherParameters):
    def __init__(self, parameters: CipherParameters, id_bytes: Union[bytes, bytearray, List[int]]):
        self.parameters = parameters
        self.id = id_bytes
    
    def get_parameters(self) -> CipherParameters:
        """Get the wrapped parameters."""
        return self.parameters
    
    def get_id(self) -> bytes:
        """Get the ID bytes."""
        if isinstance(self.id, bytes):
            return self.id
        return bytes(self.id)
