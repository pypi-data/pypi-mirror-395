from typing import Union, MutableSequence, List

class Arrays:
    @staticmethod
    def are_equal(a: Union[bytes, bytearray, List[int]], b: Union[bytes, bytearray, List[int]]) -> bool:
        """
        Compare two byte arrays for equality.
        """
        if a is None or b is None:
            return False
        if a is b:
            return True
        return a == b
    
    @staticmethod
    def constant_time_are_equal(a: Union[bytes, bytearray, List[int]], b: Union[bytes, bytearray, List[int]]) -> bool:
        """
        Constant time comparison of two byte arrays.
        """
        if a is None or b is None:
            return False
        if a is b:
            return True
        
        len_a = len(a)
        len_b = len(b)
        
        if len_a != len_b:
            # To be truly constant time we might need to continue comparing, 
            # but typically length mismatch is public knowledge.
            return False
            
        non_equal = 0
        for i in range(len_a):
            non_equal |= (a[i] ^ b[i])
            
        return non_equal == 0

    @staticmethod
    def clone(data: Union[bytes, bytearray, List[int]]) -> Union[bytearray, List[int]]:
        if data is None:
            return None
        return bytearray(data)

    @staticmethod
    def fill(data: MutableSequence[int], value: int) -> None:
        for i in range(len(data)):
            data[i] = value

    @staticmethod
    def concatenate(*arrays: Union[bytes, bytearray]) -> bytearray:
        """
        Concatenate multiple byte arrays.
        
        Args:
            *arrays: Variable number of byte arrays to concatenate
            
        Returns:
            Concatenated byte array
        """
        total_length = sum(len(arr) for arr in arrays)
        result = bytearray(total_length)
        offset = 0
        for arr in arrays:
            result[offset:offset + len(arr)] = arr
            offset += len(arr)
        return result
