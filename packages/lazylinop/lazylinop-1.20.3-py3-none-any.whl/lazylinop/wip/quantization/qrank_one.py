from array_api_compat import (
    array_namespace, device,
    is_cupy_array, is_numpy_array, is_torch_array)
from lazylinop.wip.quantization.utils import finfo, promote_types
from lazylinop.wip.quantization import chop
from lazylinop.wip.quantization.algo import _algo5_1_opt_lambda
# from lazylinop import LazyLinOp


def qrank_one(x, y, target):
    r"""
    Find vectors $\hat{x}$ and $\hat{y}$ in the target format such that
    $\hat{x}\hat{y}^T$ is closest to $xy^T$ using Algorithm 5.1
    of reference :ref:`[1] <opt_qrank1>`.

    Args:
        x, y: 1d array
            Column vectors of shape ``(m, 1)`` and ``(n, 1)``
            to be quantized belonging to the same namespace,
            with the same dtype,
            raise an ``Exception`` otherwize.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.

    Returns:
        A tuple ``(xh, yh, rerr)`` where
        ``xh`` is $\hat{x}$ the quantized $x$,
        ``yh`` is $\hat{y}$ the quantized $y$ and
        ``rerr`` the quantization relative error.

        .. Note::

            - The ``dtype`` of ``xh`` and ``yh`` is ``target``.
            - By construction, ``xh`` is not necessarily close to ``x``,
              ``yh`` is not necessarily close to ``y`` but ``xh @ yh.T``
              is close to ``x @ y.T``.
            - If ``target`` is a ``torch.dtype`` and ``x``, ``y``
              are not torch tensors convert ``x`` and ``y``
              before proceeding.
            - If ``x.dtype`` promotes to ``target`` return
              ``(xc, yc, rerr)`` where ``xc`` and ``yc`` are
              ``x`` and ``y`` casted to ``target`` dtype.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.quantization import qrank_one
        >>> from lazylinop.wip.quantization import chop
        >>> m = np.random.randint(2, high=10)
        >>> n = np.random.randint(2, high=10)
        >>> base = 'float64'
        >>> x = np.random.randn(m, 1).astype(base)
        >>> y = np.random.randn(n, 1).astype(base)
        >>> # Quantize using float16.
        >>> target = 'float16'
        >>> xh, yh, rerr = qrank_one(x, y, target)
        >>> xh.shape == x.shape
        True
        >>> yh.shape == y.shape
        True
        >>> xh.dtype == target
        True
        >>> yh.dtype == target
        True
        >>> # RTN strategy for comparison.
        >>> from lazylinop.wip.quantization import chop, finfo
        >>> t = finfo(target).nmant
        >>> n = np.linalg.norm(x @ y.T, ord='fro')
        >>> xr = chop(x, t)
        >>> yr = chop(y, t)
        >>> rtn_rerr = np.linalg.norm(x @ y.T - xr @ yr.T, ord='fro') / n
        >>> # Optimal error versus RTN error.
        >>> bool(rerr <= rtn_rerr)
        True

    .. seealso::
        - :py:func:`lazylinop.wip.quantization.qmonarch`,
        - :py:func:`lazylinop.wip.quantization.qbutterfly`.

    .. _opt_qrank1:

        **References:**

        [1] Rémi Gribonval, Theo Mary, Elisa Riccietti.
        Optimal quantization of rank-one matrices in
        floating-point arithmetic—with applications
        to butterfly factorizations. 2023. hal-04125381
        https://inria.hal.science/hal-04125381v1/document
    """
    xh, yh, opt_rerr, _ = _qrank_one(x, y, target)
    return xh, yh, opt_rerr


def _qrank_one(x, y, target):

    xp = array_namespace(x)
    if xp != array_namespace(y):
        raise Exception("x and y must have the" +
                        " same array namespace.")

    _dtype = x.dtype
    if _dtype != y.dtype:
        raise Exception("x and y must have the same dtype.")

    _device = device(x)
    if _device != device(y):
        raise Exception("x and y must have the same device.")

    if x.ndim != 2 or (x.ndim == 2 and x.shape[1]) != 1 or (
            y.ndim != 2 or (y.ndim == 2 and y.shape[1] != 1)):
        raise Exception("x and y must be column vectors.")

    # x and y are NumPy/CuPy arrays and target dtype is torch.
    # Convert x and y to torch tensors.
    if not is_torch_array(x) and 'torch' in str(target):
        # Update array namespace.
        import array_api_compat.torch as xp
        # FIXME: xp.asarray(...) raises an error:
        # RuntimeError: could not retrieve buffer from object
        if is_numpy_array(x):
            # NumPy array.
            _device = 'cpu'
            _x = xp.from_numpy(x).to(device=_device)
            _y = xp.from_numpy(y).to(device=_device)
        elif is_cupy_array(x):
            # CuPy array.
            import array_api_compat.cupy as _xp
            _device = f"cuda:{_device.id}"
            _x = xp.from_numpy(_xp.asnumpy(x)).to(device=_device)
            _y = xp.from_numpy(_xp.asnumpy(y)).to(device=_device)
    else:
        _x = x
        _y = y
    # Update dtype and device.
    _dtype = _x.dtype
    _device = _x.device

    # Number of bits in the mantissa of target.
    t = finfo(target).nmant

    xy = _x @ _y.T
    nxy = xp.linalg.norm(xy, ord="fro")

    _promote = promote_types(target, _dtype)
    if t >= finfo(_dtype).nmant:  # or _promote == _dtype:
        # If target >= _dtype return a casted copy of x and y.
        from warnings import warn
        warn("target >= dtype return a casted copy of x and y.")
        _xc = xp.asarray(_x, dtype=target, copy=True)
        _yc = xp.asarray(_y, dtype=target, copy=True)
        rerr = xp.linalg.norm(
            xy - _xc @ _yc.T, ord='fro') / nxy
        return (_xc, _yc, rerr, None)

    # Compute hat(x) and hat(y).
    lopt, mopt, opt_rerr = _algo5_1_opt_lambda(
        _x, _y, target, dochopy=True)
    xh = xp.asarray(chop(lopt * _x, t), device=_device, dtype=target)
    # FIXME: dochopy if ty != inf.
    yh = xp.asarray(chop(mopt * _y, t), device=_device, dtype=target)

    # RTN strategy for comparison.
    xr = xp.asarray(chop(_x, t), dtype=target)
    yr = xp.asarray(chop(_y, t), dtype=target)
    rtn_rerr = xp.linalg.norm(
        xy - xp.asarray(xr @ yr.T, dtype=xy.dtype), ord="fro") / nxy

    return xh, yh, opt_rerr, rtn_rerr


# def _lazy_rank_one(u, v):
#     r"""Return a :py:class:`.LazyLinOp` ``L`` corresponding
#     to the product $\left(uv^T\right)x$ of a batch of vectors $x$
#     with a rank one matrix $uv^T$.

#     Args:
#         u, v: 1d arrays.
#             Column vectors of shape ``(m, 1)`` and ``(n, 1)``.
#             Raise an ``Exception`` if array namespaces differ.

#     Returns:
#         A :py:class:`.LazyLinOp` of shape ``(m, n)``.
#     """

#     xp = array_namespace(u)
#     if xp != array_namespace(v):
#         raise Exception("u and v array namespaces must be the same.")

#     if u.ndim != 2 or (u.ndim == 2 and u.shape[1] != 1):
#         raise Exception("u must be a column vector.")
#     if v.ndim != 2 or (v.ndim == 2 and v.shape[1] != 1):
#         raise Exception("v must be a column vector.")

#     def _matmat(u, v, x):
#         # Compute u @ v.T @ x
#         # From left to right:
#         # (m, 1) @ (1, n) @ (n, b)
#         #          (m, n) @ (n, b)
#         # op: m * n + m * n * b
#         # From right to left:
#         # (m, 1) @ (1, n) @ (n, b)
#         # (m, 1) @ (1, b)
#         # op: n * b + m * b
#         m = u.shape[0]
#         n = v.shape[0]
#         b = x.shape[1]
#         l2r = m * n + m * n * b
#         r2l = n * b + m * b
#         if l2r < r2l:
#             _tmp = u @ v.T
#             return _tmp @ x
#         else:
#             _tmp = v.T @ x
#             return u @ _tmp

#     # rmatmat corresponds to (u @ v.T).H @ y
#     #                        conj(v) @ u.H @ y
#     #                        conj(v) @ conj(u).T @ y.
#     L = LazyLinOp(
#         shape=(u.shape[0], v.shape[0]),
#         matmat=lambda x: _matmat(u, v, x),
#         rmatmat=lambda x: _matmat(xp.conj(v), xp.conj(u), x))
#     if 'torch' in str(xp.__package__):
#         L.u = u.clone()
#         L.v = v.clone()
#     else:
#         L.u = xp.copy(u)
#         L.v = xp.copy(v)
#     return L
