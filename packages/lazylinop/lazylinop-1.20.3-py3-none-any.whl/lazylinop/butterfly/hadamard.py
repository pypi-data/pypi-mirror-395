import numpy as np
from lazylinop.butterfly.ksm import ksm, _multiple_ksm
try:
    import torch
except ModuleNotFoundError:
    torch = None
try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None
import array_api_compat


def _hadamard_square_dyadic_ks_values(N: int,
                                      dtype: str = 'float64',
                                      device = 'cpu'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``H @ P.T`` matrix decomposition into
    ``n = int(np.log2(N))`` factors, where ``H`` is the Hadamard
    matrix and ``P`` the bit-reversal permutation matrix.
    The size $N=2^n$ of the Hadamard matrix must be a power of $2$.

    We can draw the square-dyadic decomposition for $N=16$:

    .. image:: _static/square_dyadic.svg

    Args:
        N: ``int``
            FWHT of size $N=2^n$.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.
        device: optional
            Send ``ks_values`` to device ``device``.
            The default value is ``'cpu'``.

    Returns:
        List of 4d arrays corresponding to ``ks_values``.
        Infer the namespace (see
        `array-api-compat <https://data-apis.org/array-api-compat/>`_
        for more details)
        of ``ks_values`` from ``dtype`` and ``device`` arguments.
        By default, namespace of ``ks_values`` is ``numpy``
        and dtype is ``'float64'``.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly.hadamard import _hadamard_square_dyadic_ks_values
        >>> from lazylinop.butterfly import ksm
        >>> from lazylinop.signal import fwht
        >>> N = 2 ** 5
        >>> ks_values = _hadamard_square_dyadic_ks_values(N)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values)
        >>> np.allclose(fwht(N) @ x, (L @ x) / np.sqrt(N))
        True

    .. _dec:

        **References:**

        [1] Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
        Dao T, Gu A, Eichhorn M, Rudra A, Re C.
        Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    norm = 1.0  # / np.sqrt(2.0)
    p = int(np.log2(N))
    # Infer the namespace from dtype and device.
    if torch is not None and isinstance(dtype, torch.dtype):
        import array_api_compat.torch as xp
    elif cp is not None and not 'cpu' in str(device):
        import array_api_compat.cupy as xp
    else:
        xp = np
    # Build ks_values.
    ks_values = [None] * p
    for n in range(p):
        if n == (p - 1):
            h2 = norm * xp.asarray([[1, 1], [1, -1]], dtype=dtype,
                                   device=device)
            a = N // 2
            b, c = 2, 2
            d = 1
            ks_values[n] = xp.empty((a, b, c, d), dtype=dtype,
                                    device=device)
            for i in range(a):
                ks_values[n][i, :, :, 0] = h2
        else:
            s = N // 2 ** (p - n)
            t = N // 2 ** (n + 1)
            a = s
            b, c = 2, 2
            d = t
            ks_values[n] = xp.empty((a, b, c, d), dtype=dtype,
                                    device=device)
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Loop over the a blocks.
            for i in range(a):
                for u in range(t):
                    for v in range(4):
                        if v == 0:
                            # Identity.
                            sub_col = u
                            sub_row = u
                            tmp = norm
                        elif v == 1:
                            # Identity.
                            sub_col = u + t
                            sub_row = u
                            tmp = norm
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + t
                            tmp = norm
                        else:
                            # -Identity.
                            sub_col = u + t
                            sub_row = u + t
                            tmp = -norm
                        j = sub_row // d
                        k = sub_col // d
                        ks_values[n][i, j, k, sub_col - k * d] = tmp
    return ks_values


def fwht(N: int, backend: str = 'numpy', dtype: str = 'float64',
         device = 'cpu'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Fast-Walsh-Hadamard-Transform (FWHT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is orthogonal and *symmetric* and
    the inverse WHT operator is ``L.T = L``.

    The number of factors $n$ of the square-dyadic decomposition
    is given by $n=\log_2\left(N\right)$

    Infer the namespace (see
    `array-api-compat <https://data-apis.org/array-api-compat/>`_
    for more details)
    of ``L.ks_values`` from ``dtype`` and ``device`` arguments.
    By default, namespace of ``L.ks_values`` is ``numpy``
    and dtype is ``'float64'``.

    Args:
        N: ``int``
            Size of the FWHT. $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.
        device: optional
            The device of Hadamard matrix elements.
            The default value is ``'cpu'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the FWHT.
        ``L`` is equivalent to ``hadamard(N, backend, dtype) / sqrt(N)``.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly import fwht as bfwht
        >>> from lazylinop.signal import fwht as sfwht
        >>> N = 2 ** 5
        >>> x = np.random.randn(N).astype('float64')
        >>> y = bfwht(N) @ x
        >>> z = sfwht(N) @ x
        >>> np.allclose(y, z)
        True

    .. seealso::

        :py:func:`hadamard`
    """
    return hadamard(N, backend, dtype, device) / np.sqrt(N)


def hadamard(N: int, backend: str = 'numpy', dtype: str = 'float64',
             device = 'cpu'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Hadamard matrix.

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is not orthogonal and its inverse is ``L.T / N``.
    ``L`` is *symmetric*.

    The number of factors $n$ of the square-dyadic decomposition
    is given by $n=\log_2\left(N\right)$.

    Infer the namespace (see
    `array-api-compat <https://data-apis.org/array-api-compat/>`_
    for more details)
    of ``L.ks_values`` from ``dtype`` and ``device`` arguments.
    By default, namespace of ``L.ks_values`` is ``numpy``
    and dtype is ``'float64'``.

    Args:
        N: ``int``
            Size of the Hadamard matrix.
            $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.
        device: optional
            The device of Hadamard matrix elements.
            The default value is ``'cpu'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the
        Hadamard matrix.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.butterfly import hadamard
        >>> N = 2 ** 5
        >>> x = np.random.randn(N).astype('float64')
        >>> y = hadamard(N) @ x
        >>> z = sp.linalg.hadamard(N) @ x
        >>> np.allclose(y, z)
        True

    .. seealso::

        - `Wikipedia <https://en.wikipedia.org/wiki/Hadamard_matrix>`_,
        - :py:func:`fwht`.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")

    ks_values = _hadamard_square_dyadic_ks_values(N, dtype=dtype,
                                                  device=device)
    if backend in ('numpy', 'cupy', 'pytorch', 'xp'):
        return ksm(ks_values, backend='xp')
    elif backend in ('cupyx', 'scipy'):
        return ksm(ks_values, backend=backend)
    else:
        # FIXME: params=None.
        return _multiple_ksm(ks_values, backend=backend,
                             params=None, perm=False)


def _fwht_helper(N: int, n_factors: int, backend: str = 'numpy',
                 strategy: str = 'memory', dtype: str = 'float64',
                 device = 'cpu'):
    r"""
    Return a :class:`LazyLinOp` `L` corresponding to
    the Fast-Walsh-Hadamard-Transform (FWHT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is orthogonal and *symmetric* and
    the inverse WHT operator is ``L.T = L``.

    Infer the namespace (see
    `array-api-compat <https://data-apis.org/array-api-compat/>`_
    for more details)
    of ``L.ks_values`` from ``dtype`` and ``device`` arguments.
    By default, namespace of ``L.ks_values`` is ``numpy``
    and dtype is ``'float64'``.

    Args:
        N: ``int``
            FWHT of size $N$. $N$ must be a power of two.
        n_factors: ``int``
            Number of factors ``n_factors <= n``.
            If ``n_factors = n``, return the square-dyadic decomposition.
            The performance of the algorithm depends on
            the number of factors, the size of the FWHT
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
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.
        device: optional
            The device of Hadamard matrix elements.
            The default value is ``'cpu'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the FWHT.

    .. seealso::
        - :py:func:`lazylinop.butterfly.fuse`,
        - :py:func:`lazylinop.wip.butterfly.fuses.fuses`.
    """
    from lazylinop.wip.butterfly.fuses import fuses
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    p = int(np.log2(N))
    if n_factors > p or n_factors < 1:
        raise ValueError("n_factors must be positive and less or"
                         + " equal to int(np.log2(N)).")

    # FIXME
    params = None
    # if n_factors == ...:
    #     params = None
    # elif n_factors == ...:
    #     params = None
    # else:
    #     params = None

    ks_values = _hadamard_square_dyadic_ks_values(
        N, dtype=dtype, device=device)
    ksv = fuses(ks_values, n_factors, strategy)

    if backend in ('numpy', 'cupy', 'pytorch', 'xp'):
        H = ksm(ksv, backend='xp')
    elif backend in ('cupyx', 'scipy'):
        H = ksm(ksv, backend=backend)
    else:
        H = _multiple_ksm(ksv, backend=backend,
                          params=params, perm=False)
    H.ks_values = ksv
    return H / np.sqrt(N)
