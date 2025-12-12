import numpy as np
from numpy.typing import NDArray

from pycint._cint import ffi
from pycint.typing import Ptr

DTYPE_MAPS: dict[str, str] = {
    "float64": "double",
    "float32": "float",
    "uint64": "size_t",
    "complex128": "double _Complex",
    "int32": "int",
}


def as_ptr[T: np.generic](arr: NDArray[T]) -> Ptr[T]:
    """Get cffi pointer from NDArray."""
    if arr.flags.f_contiguous:
        arr = arr.T
    elif arr.flags.c_contiguous:
        pass
    else:
        msg = "Array is not contiguous."
        raise ValueError(msg)
    return ffi.from_buffer(f"{DTYPE_MAPS[arr.dtype.name]} *", arr)
