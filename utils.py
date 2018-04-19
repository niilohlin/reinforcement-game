
from typing import Union

def sign(n: Union[int, float]) -> int:
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0
