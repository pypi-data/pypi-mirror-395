from typing import Union, List
from sm_bc.crypto.digest import Digest
from sm_bc.crypto.digests.sm3_digest import SM3Digest

class KDF:
    @staticmethod
    def derive_key(digest: Digest, seed: Union[bytes, bytearray, List[int]], key_length: int) -> bytearray:
        """
        SM2 Key Derivation Function (KDF).
        Derives keying material from a shared secret (seed) using a hash function.

        :param digest: The hash function (e.g., SM3Digest) to use.
        :param seed: The shared secret (Z) as bytes.
        :param key_length: The desired length of the keying material in bytes.
        :return: The derived keying material as a bytearray.
        """
        
        digest_size = digest.get_digest_size()
        
        if key_length == 0:
            return bytearray()
            
        counter = 0x00000001 # 32-bit counter
        kdf_output = bytearray(key_length)
        
        for i in range(0, key_length, digest_size):
            digest.reset()
            digest.update_bytes(seed, 0, len(seed))
            
            # Counter as 4 bytes, big-endian
            counter_bytes = counter.to_bytes(4, 'big')
            digest.update_bytes(counter_bytes, 0, 4)
            
            hash_output = bytearray(digest_size)
            digest.do_final(hash_output, 0)
            
            bytes_to_copy = min(digest_size, key_length - i)
            kdf_output[i : i + bytes_to_copy] = hash_output[0 : bytes_to_copy]
            
            counter += 1
            if counter > 0xFFFFFFFF:
                # Counter overflow protection, though unlikely for typical key lengths
                raise OverflowError("KDF counter overflow")
                
        return kdf_output
