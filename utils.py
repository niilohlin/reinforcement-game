
from typing import Union

angle = float

def sign(n: Union[int, float]) -> int:
    if n == 0:
        return 0
    return int(n / abs(n))
