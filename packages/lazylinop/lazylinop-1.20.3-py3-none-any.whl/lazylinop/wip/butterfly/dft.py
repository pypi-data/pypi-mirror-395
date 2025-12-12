from numpy import log2
from lazylinop.butterfly import ksm
from lazylinop.butterfly.ksm import _multiple_ksm
from lazylinop.basicops import bitrev
from lazylinop.butterfly.dft import _dft_square_dyadic_ks_values
from lazylinop.wip.butterfly.fuses import fuses


def dft_helper(N: int, n_factors: int, backend: str = 'numpy',
               strategy: str = 'memory', dtype: str = 'complex64',
               device = 'cpu'):
    r"""
    Return a :class:`LazyLinOp` `L` corresponding to
    the Discrete-Fourier-Transform (DFT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    Args:
        N: ``int``
            DFT of size $N$. $N$ must be a power of two.
        n_factors: ``int``
            Number of factors ``n_factors <= n``.
            If ``n_factors = n``, return the square-dyadic decomposition.
            The performance of the algorithm depends on
            the number of factors, the size of the DFT
            as-well-as the strategy.
            Our experimentation shows that square-dyadic decomposition
            is always the worse choice.
            The best choice is two, three or four factors.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        strategy: ``str``, optional
            See :py:func:`lazylinop.wip.butterfly.fuses.fuses`
            for more details.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Benchmark of our DFT implementation is
    (we use default hyper-parameters here):

    .. image:: _static/default_dft_batch_size512_complex64.svg

    Returns:
        :class:`LazyLinOp` `L` corresponding to the DFT.

    .. seealso::
        - :py:func:`lazylinop.butterfly.fuse`,
        - :py:func:`lazylinop.wip.butterfly.fuses.fuses`.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    p = int(log2(N))
    if n_factors > p or n_factors < 1:
        raise Exception("n_factors must be positive and less or"
                        + " equal to int(np.log2(N)).")
    if 'complex' not in str(dtype):
        raise Exception("dtype must be either complex.")

    # FIXME
    params = None
    # if n_factors == ...:
    #     params = None
    # elif n_factors == ...:
    #     params = None
    # else:
    #     params = None

    ks_values = _dft_square_dyadic_ks_values(
        N, dtype=dtype, device=device)
    ksv = fuses(ks_values, n_factors, strategy)

    if backend in ('cupy', 'numpy', 'pytorch', 'scipy', 'xp'):
        L = ksm(ksv, backend=backend) @ bitrev(2 ** p)
    else:
        L = _multiple_ksm(ksv, backend=backend,
                          params=params, perm=True)
    L.ks_values = ksv
    return L
