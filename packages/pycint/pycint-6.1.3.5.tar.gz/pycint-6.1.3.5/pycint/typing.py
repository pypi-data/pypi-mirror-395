from typing import Callable, TypeAlias, no_type_check

try:
    from typing import type_check_only
except ImportError:

    def type_check_only(cls):
        return cls


import numpy as np

# Complex type for _Complex in C
Complex: TypeAlias = complex

# Callback function types
CallbackFunc: TypeAlias = Callable[..., int]
VoidCallbackFunc: TypeAlias = Callable[..., None]


@type_check_only
class CData:
    """Base class for cffi C-compatible data structures.

    This is an abstract base class that serves as the foundation for all C-compatible
    data types in the chc2c package. It represents memory structures that are passed
    between Python and C code via cffi.
    """


@type_check_only
class Ptr[T](CData):
    """Generic pointer type that supports arithmetic operations (+, -, []).

    A typed pointer type that wraps cffi pointers, enabling safe memory access and
    pointer arithmetic in Python. The generic type T represents the type of data
    being pointed to. Supports addition/subtraction of integers (pointer arithmetic)
    and index access to elements in the memory block.

    Type parameters:
        T: The type of the elements being pointed to.

    Example:
        ptr: Ptr[float64] = ...  # Pointer to float64 values
        val = ptr[0]  # Access first element
        next_ptr = ptr + 1  # Move pointer to next element

    """

    @no_type_check
    def __add__(self, rhs: int) -> "Ptr": ...

    @no_type_check
    def __radd__(self, lhs: int) -> "Ptr": ...

    @no_type_check
    def __sub__(self, rhs: int) -> "Ptr": ...

    @no_type_check
    def __getitem__(self, index: int) -> T: ...


@type_check_only
class CArray[T](Ptr[T]):
    """Array type derived from Ptr, with length information.

    An extension of Ptr that represents an array with known length. This type provides
    a Pythonic interface to C arrays by implementing the __len__ method, making it
    compatible with Python's len() function.

    Type parameters:
        T: The type of the elements in the array.

    Note:
        The actual length information is typically stored in the C data structure
        and made available through the managing class (e.g., Atoms, Shells).

    """

    @no_type_check
    def __len__(self) -> int: ...


type CallbackFunc = Callable[..., int]
type VoidCallbackFunc = Callable[..., None]


@type_check_only
class PairData(CData):
    """Corresponds to C PairData struct."""

    rij: CArray[float]  # double rij[3]
    eij: float
    cceij: float


@type_check_only
class CINTOpt(CData):
    """Corresponds to C CINTOpt struct."""

    index_xyz_array: Ptr[Ptr[int]]  # int **index_xyz_array
    non0ctr: Ptr[Ptr[int]]  # int **non0ctr
    sortedidx: Ptr[Ptr[int]]  # int **sortedidx
    nbas: int
    log_max_coeff: Ptr[Ptr[float]]  # double **log_max_coeff
    pairdata: Ptr[Ptr[PairData]]  # PairData **pairdata


@type_check_only
class CINTEnvVars(CData):
    """Corresponds to C CINTEnvVars struct."""

    atm: Ptr[int]  # int *atm
    bas: Ptr[int]  # int *bas
    env: Ptr[float]  # double *env
    shls: Ptr[int]  # int *shls
    natm: int
    nbas: int

    i_l: int
    j_l: int
    k_l: int
    l_l: int
    nfi: int  # number of cartesian components
    nfj: int

    # union for nfk/grids_offset
    nfk: int
    grids_offset: int

    # union for nfl/ngrids
    nfl: int
    ngrids: int

    nf: int  # = nfi*nfj*nfk*nfl
    rys_order: int  # = nrys_roots for regular ERIs. can be nrys_roots/2 for SR ERIs
    x_ctr: CArray[int]  # int x_ctr[4]

    gbits: int
    ncomp_e1: int  # = 1 if spin free, = 4 when spin included
    ncomp_e2: int  # corresponds to POSX,POSY,POSZ,POS1, see cint.h
    ncomp_tensor: int  # e.g. = 3 for gradients

    # values may diff based on the g0_2d4d algorithm
    li_ceil: int  # power of x, == i_l if nabla is involved, otherwise == i_l
    lj_ceil: int
    lk_ceil: int
    ll_ceil: int
    g_stride_i: int  # nrys_roots * shift of (i++,k,l,j)
    g_stride_k: int  # nrys_roots * shift of (i,k++,l,j)
    g_stride_l: int  # nrys_roots * shift of (i,k,l++,j)
    g_stride_j: int  # nrys_roots * shift of (i,k,l,j++)
    nrys_roots: int
    g_size: int  # ref to cint2e.c g = malloc(sizeof(double)*g_size)

    g2d_ijmax: int
    g2d_klmax: int
    common_factor: float
    expcutoff: float
    rirj: CArray[float]  # double rirj[3]
    rkrl: CArray[float]  # double rkrl[3]
    rx_in_rijrx: Ptr[float]  # double *rx_in_rijrx
    rx_in_rklrx: Ptr[float]  # double *rx_in_rklrx

    ri: Ptr[float]  # double *ri
    rj: Ptr[float]  # double *rj
    rk: Ptr[float]  # double *rk

    # union for rl/grids
    rl: Ptr[float]  # double *rl (in int2e or int3c2e)
    grids: Ptr[float]  # double *grids (in int1e_grids)

    f_g0_2e: CallbackFunc  # int (*f_g0_2e)()
    f_g0_2d4d: VoidCallbackFunc  # void (*f_g0_2d4d)()
    f_gout: VoidCallbackFunc  # void (*f_gout)()
    opt: Ptr[CINTOpt]  # CINTOpt *opt

    # values are assigned during calculation
    idx: Ptr[int]  # int *idx
    ai: CArray[float]  # double ai[1]
    aj: CArray[float]  # double aj[1]
    ak: CArray[float]  # double ak[1]
    al: CArray[float]  # double al[1]
    fac: CArray[float]  # double fac[1]
    rij: CArray[float]  # double rij[3]
    rkl: CArray[float]  # double rkl[3]


@type_check_only
class Cint:
    # Length and counting functions
    @no_type_check
    @staticmethod
    def CINTlen_cart(l: int) -> int: ...
    @no_type_check
    @staticmethod
    def CINTlen_spinor(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgtos_cart(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgtos_spheric(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgtos_spinor(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgto_cart(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgto_spheric(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTcgto_spinor(bas_id: int, bas: Ptr[int]) -> int: ...
    @no_type_check
    @staticmethod
    def CINTtot_pgto_spheric(bas: Ptr[int], nbas: int) -> int: ...
    @no_type_check
    @staticmethod
    def CINTtot_pgto_spinor(bas: Ptr[int], nbas: int) -> int: ...
    @no_type_check
    @staticmethod
    def CINTtot_cgto_cart(bas: Ptr[int], nbas: int) -> int: ...
    @no_type_check
    @staticmethod
    def CINTtot_cgto_spheric(bas: Ptr[int], nbas: int) -> int: ...
    @no_type_check
    @staticmethod
    def CINTtot_cgto_spinor(bas: Ptr[int], nbas: int) -> int: ...

    # Offset functions
    @staticmethod
    def CINTshells_cart_offset(
        ao_loc: CArray[int], bas: Ptr[int], nbas: int
    ) -> None: ...
    @staticmethod
    def CINTshells_spheric_offset(
        ao_loc: CArray[int], bas: Ptr[int], nbas: int
    ) -> None: ...
    @staticmethod
    def CINTshells_spinor_offset(
        ao_loc: CArray[int], bas: Ptr[int], nbas: int
    ) -> None: ...

    # Transformation functions
    @no_type_check
    @staticmethod
    def CINTc2s_bra_sph(
        sph: Ptr[float], nket: int, cart: Ptr[float], l: int
    ) -> Ptr[float]: ...
    @no_type_check
    @staticmethod
    def CINTc2s_ket_sph(
        sph: Ptr[float], nket: int, cart: Ptr[float], l: int
    ) -> Ptr[float]: ...
    @no_type_check
    @staticmethod
    def CINTc2s_ket_sph1(
        sph: Ptr[float], cart: Ptr[float], lds: int, ldc: int, l: int
    ) -> Ptr[float]: ...

    # Normalization function
    @no_type_check
    @staticmethod
    def CINTgto_norm(n: int, a: float) -> float: ...

    # Optimizer management functions
    @staticmethod
    def CINTinit_2e_optimizer(
        opt: Ptr[Ptr[CINTOpt]],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
    ) -> None: ...
    @staticmethod
    def CINTinit_optimizer(
        opt: Ptr[Ptr[CINTOpt]],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
    ) -> None: ...
    @staticmethod
    def CINTdel_2e_optimizer(opt: Ptr[Ptr[CINTOpt]]) -> None: ...
    @staticmethod
    def CINTdel_optimizer(opt: Ptr[Ptr[CINTOpt]]) -> None: ...

    # Two-electron integral functions
    @no_type_check
    @staticmethod
    def cint2e_cart(
        opijkl: Ptr[float],
        shls: Ptr[int],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
        opt: Ptr[CINTOpt],
    ) -> int: ...
    @staticmethod
    def cint2e_cart_optimizer(
        opt: Ptr[Ptr[CINTOpt]],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
    ) -> None: ...
    @no_type_check
    @staticmethod
    def cint2e_sph(
        opijkl: Ptr[float],
        shls: Ptr[int],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
        opt: Ptr[CINTOpt],
    ) -> int: ...
    @staticmethod
    def cint2e_sph_optimizer(
        opt: Ptr[Ptr[CINTOpt]],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
    ) -> None: ...
    @no_type_check
    @staticmethod
    def cint2e(
        opijkl: Ptr[float],
        shls: Ptr[int],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
        opt: Ptr[CINTOpt],
    ) -> int: ...
    @staticmethod
    def cint2e_optimizer(
        opt: Ptr[Ptr[CINTOpt]],
        atm: Ptr[int],
        natm: int,
        bas: Ptr[int],
        nbas: int,
        env: Ptr[float],
    ) -> None: ...

    # Spinor transformation functions
    @staticmethod
    def CINTc2s_ket_spinor_sf1(
        gspa: Ptr[np.complex128],
        gspb: Ptr[np.complex128],
        gcart: Ptr[float],
        lds: int,
        ldc: int,
        nctr: int,
        l: int,
        kappa: int,
    ) -> None: ...
    @staticmethod
    def CINTc2s_iket_spinor_sf1(
        gspa: Ptr[np.complex128],
        gspb: Ptr[np.complex128],
        gcart: Ptr[float],
        lds: int,
        ldc: int,
        nctr: int,
        l: int,
        kappa: int,
    ) -> None: ...
    @staticmethod
    def CINTc2s_ket_spinor_si1(
        gspa: Ptr[np.complex128],
        gspb: Ptr[np.complex128],
        gcart: Ptr[float],
        lds: int,
        ldc: int,
        nctr: int,
        l: int,
        kappa: int,
    ) -> None: ...
    @staticmethod
    def CINTc2s_iket_spinor_si1(
        gspa: Ptr[np.complex128],
        gspb: Ptr[np.complex128],
        gcart: Ptr[float],
        lds: int,
        ldc: int,
        nctr: int,
        l: int,
        kappa: int,
    ) -> None: ...
