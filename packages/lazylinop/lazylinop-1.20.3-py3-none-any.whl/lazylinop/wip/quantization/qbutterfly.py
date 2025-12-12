from lazylinop import islazylinop
from lazylinop.butterfly import Chain, ksm
from lazylinop.wip.quantization.algo import (
    _algo7_3_left2right, _algo7_2_pairwise, _rerr)
from lazylinop.wip.quantization.utils import finfo, promote_types
from array_api_compat import (
    array_namespace, is_array_api_obj,
    is_cupy_array, is_numpy_array, is_torch_array)


def qbutterfly(L, target, order: str = 'l2r'):
    r"""
    Optimal quantization of a Butterfly operator ``L`` to a target format
    using Algorithm 7.3 (left-to-right) of reference :ref:`[1] <opt>`
    with ``t = finfo(target).nmant`` bits in mantissa of ``target`` dtype.

    Args:
        L:
            Butterfly operator to be quantized, described either as:

            - a list of $p$ 4d arrays ``ks_values`` of shapes
              compatible with ``lazylinop.butterfly.Chain.square_dyadic()``.
            - or a lazy linear operator ``L`` obtained either with
              :py:func:`lazylinop.butterfly.ksm` or with
              :py:func:`lazylinop.butterfly.ksd` using a square-dyadic chain.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.
        order: ``str``, optional
            Possible choices are `'l2r'` (default) corresponding
            to Algorithm 7.3 or
            `'pairwise'` corresponding to Algorithm 7.2
            of reference :ref:`[1] <opt>`.

    Returns:
        A tuple ``(Lq, rerr)`` where ``Lq`` is of the same nature
        as ``L`` but with ``ks_values`` of dtype ``target``
        and ``rerr`` is the quantization relative error.

        .. Note::

            - The ``dtype`` of ``ks_values`` of ``Lq`` is ``target``.
            - If ``target`` is a ``torch.dtype`` and ``ks_values`` of ``L``
              are not torch tensors convert ``ks_values`` before proceeding.
            - If ``ks_values.dtype`` of ``L`` promotes to ``target`` return
              ``(Lc, rerr)`` where ``Lc`` is ``L`` casted to ``target`` dtype.

    Examples:
        >>> import numpy as np
        >>> from lazylinop import LazyLinOp
        >>> from lazylinop.butterfly import Chain, ksm
        >>> from lazylinop.wip.quantization import qbutterfly
        >>> p = 4
        >>> N = 2 ** p
        >>> # base and target dtype.
        >>> base = 'float64'
        >>> target = 'float16'
        >>> # Square-dyadic chain.
        >>> chain = Chain.square_dyadic((N, N))
        >>> ksp = chain.ks_patterns
        >>> # List of p random 4d arrays compatible with square-dyadic chain.
        >>> ksv = [np.random.randn(*ksp[i]).astype(base) for i in range(p)]
        >>> Lq, rerr = qbutterfly(ksv, target, 'l2r')
        >>> len(Lq) == p
        True
        >>> Lq[0].dtype == target
        True
        >>> # ksm such that len(L.ks_values) == p.
        >>> L = ksm(ksv, backend='xp')
        >>> Lq, rerr = qbutterfly(L, target, 'l2r')
        >>> isinstance(Lq, LazyLinOp)
        True
        >>> len(Lq.ks_values) == p
        True
        >>> Lq.ks_values[0].dtype == target
        True
        >>> # Compute L @ X.
        >>> X = np.random.randn(L.shape[1], 128).astype(base)
        >>> Y = L @ X
        >>> # RTN strategy for comparison.
        >>> from lazylinop.wip.quantization import chop, finfo
        >>> t = finfo(target).nmant
        >>> _ksv = [chop(k, t) for k in ksv]
        >>> Lr = ksm(_ksv, backend='xp')
        >>> Yr = Lr @ X
        >>> n = np.linalg.norm(Y, ord='fro')
        >>> rtn_rerr = np.linalg.norm(Yr - Y, ord='fro') / n
        >>> # Optimal error versus RTN error.
        >>> bool(rerr <= rtn_rerr)
        True

    .. seealso::
        - :py:func:`lazylinop.butterfly.ksm`,
        - :py:func:`lazylinop.butterfly.ksd`,
        - :py:func:`lazylinop.butterfly.Chain`,
        - :py:func:`lazylinop.wip.quantization.finfo`,
        - :py:func:`lazylinop.wip.quantization.qrank_one`,
        - :py:func:`lazylinop.wip.quantization.qmonarch`.

    .. _opt:

        **References:**

        [1] Rémi Gribonval, Theo Mary, Elisa Riccietti.
        Optimal quantization of rank-one matrices in
        floating-point arithmetic—with applications
        to butterfly factorizations. 2023. hal-04125381
        https://inria.hal.science/hal-04125381v1/document
    """
    q, opt_rerr, _ = _qbutterfly(L, target, order)
    return q, opt_rerr


def _qbutterfly(L, target, order: str = 'l2r'):

    if not isinstance(L, list) and not islazylinop(L):
        raise Exception("L must be a list of 4d arrays or a ksm.")

    # Infer array_namespace, dtype and device from L.
    if islazylinop(L):
        p = len(L.ks_values)
        if p < 2:
            raise Exception("len(L.ks_values) must be >= 2.")
        xp = array_namespace(L.ks_values[0])
        dtype = L.ks_values[0].dtype
        device = L.ks_values[0].device
        for i in range(1, p):
            if xp != array_namespace(L.ks_values[i]):
                raise Exception("Each ks_values must" +
                                " have the same array namespace.")
            if dtype != L.ks_values[i].dtype:
                raise Exception("Each ks_values must" +
                                " have the same dtype.")
            if device != L.ks_values[i].device:
                raise Exception("Each ks_values must" +
                                " have the same device.")
        # Shape.
        M, N = L.shape
    elif isinstance(L, list):
        p = len(L)
        if p < 2:
            raise Exception("len(L) must be >= 2.")
        xp = array_namespace(L[0])
        dtype = L[0].dtype
        device = L[0].device
        for i in range(p):
            if not is_array_api_obj(L[i]):
                raise Exception("Each element of the list L" +
                                " must be a 4d array.")
            if xp != array_namespace(L[i]):
                raise Exception("Each element of the list L must" +
                                " have the same array namespace.")
            if dtype != L[i].dtype:
                raise Exception("Each element of the list L must" +
                                " have the same dtype.")
            if device != L[i].device:
                raise Exception("Each element of the list L must" +
                                " have the same device.")
        # Shape.
        a, b, _, d = L[0].shape
        M = a * b * d
        a, _, c, d = L[-1].shape
        N = a * c * d
    # Check that the shapes correspond to square-dyadic chain.
    chain = Chain.square_dyadic((M, N))
    for i in range(chain.n_patterns):
        shape = (L.ks_values[i] if islazylinop(L) else L[i]).shape
        if shape != chain.ks_patterns[i]:
            raise Exception(
                "Shapes of L must correspond to a square-dyadic chain.")

    # L is NumPy/CuPy arrays and target dtype is torch.
    # Convert L to torch tensors?
    if islazylinop(L):
        if not is_torch_array(L.ks_values[0]) and 'torch' in str(target):
            # Update array namespace.
            import array_api_compat.torch as xp
            # FIXME: xp.asarray(...) raises an error:
            # RuntimeError: could not retrieve buffer from object
            if is_numpy_array(L.ks_values[0]):
                # NumPy array.
                device = 'cpu'
                _ksv = [xp.from_numpy(
                    L.ks_values[i]).to(device=device) for i in range(p)]
            elif is_cupy_array(L.ks_values[0]):
                # CuPy array.
                import array_api_compat.cupy as _xp
                device = f"cuda:{device.id}"
                _ksv = [xp.from_numpy(
                    _xp.asnumpy(
                        L.ks_values[i])).to(device=device) for i in range(p)]
            _L = ksm(_ksv, backend='xp')
        else:
            _L = L
        # Update dtype and device.
        dtype = _L.ks_values[0].dtype
        device = _L.ks_values[0].device
    elif is_array_api_obj(L[0]):
        if not is_torch_array(L[0]) and 'torch' in str(target):
            # Update array namespace.
            import array_api_compat.torch as xp
            # FIXME: xp.asarray(...) raises an error:
            # RuntimeError: could not retrieve buffer from object
            if is_numpy_array(L[0]):
                # NumPy array.
                device = 'cpu'
                _L = [xp.from_numpy(L[i]).to(device=device) for i in range(p)]
            elif is_cupy_array(L[0]):
                # CuPy array.
                import array_api_compat.cupy as _xp
                device = f"cuda:{device.id}"
                _L = [xp.from_numpy(
                    _xp.asnumpy(L[i])).to(device=device) for i in range(p)]
        else:
            _L = L
        # Update dtype and device.
        dtype = _L[0].dtype
        device = _L[0].device

    # Number of bits in the mantissa of target.
    t = finfo(target).nmant

    _promote = promote_types(target, dtype)
    if t >= finfo(dtype).nmant:  # or _promote == dtype:
        # If target >= dtype return a casted copy of L.
        from warnings import warn
        warn("target >= dtype return a casted copy of L.")
        # Cast ks_values.
        if isinstance(_L, list):
            L0 = ksm(_L, backend='xp')
            kc = [xp.asarray(k, dtype=target, copy=True) for k in _L]
        elif islazylinop(_L):
            L0 = _L
            kc = [xp.asarray(
                k, dtype=target, copy=True) for k in _L.ks_values]
        # Cast LazyLinOp.
        Lc = ksm(kc, backend='xp')
        n = Lc.shape[1]
        if 'torch' in str(xp.__package__):
            W0 = xp.randn(n, 128).to(dtype=dtype, device=device)
        else:
            W0 = xp.random.randn(n, 128).astype(dtype)
        W0 = L0 @ W0
        Wc = Lc @ xp.asarray(W0, dtype=target)
        nY = xp.linalg.norm(W0, ord='fro')
        cast_rerr = xp.linalg.norm(W0 - Wc, ord='fro') / nY
        return (Lc if islazylinop(_L) else kc, cast_rerr, None)

    # Quantize.
    _L = _L if islazylinop(_L) else ksm(_L, backend="xp")
    if order == 'l2r':
        q_factors, rtn_factors = _algo7_3_left2right(_L, target)
    elif order == 'pairwise':
        q_factors, rtn_factors = _algo7_2_pairwise(_L, target)
    else:
        raise NotImplementedError("order is either 'l2r' or 'pairwise'.")

    # Return ks_values such that ks_values[i].dtype == target.
    q_factors = [
        xp.asarray(i, dtype=target, device=device) for i in q_factors]
    rtn_factors = [
        xp.asarray(i, dtype=target, device=device) for i in rtn_factors]

    # Probabilistic estimation of the error.
    opt_rerr, rtn_rerr = _rerr(
        _L, ksm(q_factors, backend='xp'), ksm(rtn_factors, backend='xp'))

    if isinstance(L, list):
        return (q_factors, opt_rerr, rtn_rerr)
    elif islazylinop(L):
        return (ksm(q_factors, backend='xp'), opt_rerr, rtn_rerr)
