
from typing import Union, Callable, Iterable, Tuple, TypeVar, Sized, Sequence

angle = float
T = TypeVar('T')

def any(f: Callable, lst: Iterable) -> bool:
    for i in lst:
        if f(i):
            return True
    return False

def sign(n: Union[int, float]) -> int:
    if n == 0:
        return 0
    return int(n / abs(n))
