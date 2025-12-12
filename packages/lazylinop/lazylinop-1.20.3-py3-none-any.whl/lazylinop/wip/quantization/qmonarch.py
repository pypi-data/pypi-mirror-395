from lazylinop import islazylinop
from lazylinop.butterfly import Chain, ksm
from lazylinop.wip.quantization.algo import _algo7_2_pairwise, _rerr
from lazylinop.wip.quantization.utils import finfo, promote_types
from array_api_compat import (
    array_namespace, is_array_api_obj,
    is_cupy_array, is_numpy_array, is_torch_array)


def qmonarch(L, target):
    r"""
    Optimal quantization of a Monarch operator ``L`` to a target format
    using Algorithm 7.2 (pairwise) of reference :ref:`[1] <opt_qmonarch>`
    with ``t = finfo(target).nmant`` bits in mantissa of ``target`` dtype.

    Args:
        L:
            Monarch operator to be quantized, described either as:

            - a list of two 4d arrays ``ks_values`` of shapes
              compatible with ``lazylinop.butterfly.Chain.monarch()``.
            - or a lazy linear operator ``L`` obtained either with
              :py:func:`lazylinop.butterfly.ksm` or with
              :py:func:`lazylinop.butterfly.ksd` using a Monarch chain.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.

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
        >>> from lazylinop.wip.quantization import qmonarch
        >>> M, N = 4, 10
        >>> # base and target dtype.
        >>> base = 'float64'
        >>> target = 'float16'
        >>> chain = Chain.monarch((M, N))
        >>> ksp = chain.ks_patterns
        >>> # List of two random 4d arrays compatible with the Monarch chain.
        >>> ksv = [np.random.randn(*ksp[i]).astype(base) for i in range(2)]
        >>> Lq, rerr = qmonarch(ksv, target)
        >>> isinstance(Lq, list)
        True
        >>> len(Lq) == 2
        True
        >>> Lq[0].dtype == target
        True
        >>> # ksm such that len(L.ks_values) == 2.
        >>> L = ksm(ksv, backend='xp')
        >>> Lq, rerr = qmonarch(L, target)
        >>> isinstance(Lq, LazyLinOp)
        True
        >>> len(Lq.ks_values) == 2
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
        - :py:func:`lazylinop.wip.quantization.qbutterfly`.

    .. _opt_qmonarch:

        **References:**

        [1] Rémi Gribonval, Theo Mary, Elisa Riccietti.
        Optimal quantization of rank-one matrices in
        floating-point arithmetic—with applications
        to butterfly factorizations. 2023. hal-04125381
        https://inria.hal.science/hal-04125381v1/document
    """
    q, opt_rerr, _ = _qmonarch(L, target)
    return q, opt_rerr


def _qmonarch(L, target):

    if not isinstance(L, list) and not islazylinop(L):
        raise Exception("L must be a list of two 4d arrays or a ksm.")

    # Infer array_namespace, dtype and device from L.
    if islazylinop(L):
        p = len(L.ks_values)
        if p != 2:
            raise Exception("len(L.ks_values) must be equal to 2.")
        xp = array_namespace(L.ks_values[0])
        dtype = L.ks_values[0].dtype
        device = L.ks_values[0].device
        if xp != array_namespace(L.ks_values[1]):
            raise Exception("Each element of the list L must" +
                            " have the same array namespace.")
        if dtype != L.ks_values[1].dtype:
            raise Exception("Each ks_values must" +
                            " have the same dtype.")
        if device != L.ks_values[1].device:
            raise Exception("Each ks_vaues must" +
                            " have the same device.")
        patterns = [L.ks_values[0].shape, L.ks_values[1].shape]
    elif isinstance(L, list) and is_array_api_obj(L[0]):
        p = len(L)
        if p != 2:
            raise Exception("len(L) must be equal to 2.")
        xp = array_namespace(L[0])
        dtype = L[0].dtype
        device = L[0].device
        patterns = [L[0].shape, L[1].shape]
        for i in range(2):
            if not is_array_api_obj(L[i]):
                raise Exception("Each element of the list L" +
                                " must be a 4d array.")
        if xp != array_namespace(L[1]):
            raise Exception("Each element of the list L must" +
                            " have the same array namespace.")
        if dtype != L[1].dtype:
            raise Exception("Each element of the list L must" +
                            " have the same dtype.")
        if device != L[1].device:
            raise Exception("Each element of the list L must" +
                            " have the same device.")
    # Check that the patterns correspond to a Monarch chain.
    _, _p, _q, _ = patterns[0]
    a, b, _, d = patterns[0]
    M = a * b * d
    a, _, c, d = patterns[1]
    N = a * c * d
    chain = Chain.monarch((M, N), _p, _q)
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
                    L.ks_values[i]).to(device=device) for i in range(2)]
            elif is_cupy_array(L.ks_values[0]):
                # CuPy array.
                import array_api_compat.cupy as _xp
                device = f"cuda:{device.id}"
                _ksv = [xp.from_numpy(
                    _xp.asnumpy(
                        L.ks_values[i])).to(device=device) for i in range(2)]
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
                _L = [xp.from_numpy(L[i]).to(device=device) for i in range(2)]
            elif is_cupy_array(L[0]):
                # CuPy array.
                import array_api_compat.cupy as _xp
                device = f"cuda:{device.id}"
                _L = [xp.from_numpy(
                    _xp.asnumpy(L[i])).to(device=device) for i in range(2)]
        else:
            _L = L
        # Update dtype and device.
        dtype = _L[0].dtype
        device = _L[0].device

    # Number of bits in the mantissa in target.
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
            Wc = W0.to(dtype=target, device=device)
        else:
            W0 = xp.random.randn(n, 128).astype(dtype)
            Wc = W0.astype(target)
        W0 = L0 @ W0
        Wc = Lc @ Wc
        nY = xp.linalg.norm(W0, ord='fro')
        cast_rerr = xp.linalg.norm(W0 - Wc, ord='fro') / nY
        return (Lc if islazylinop(_L) else kc, cast_rerr, None)

    # Quantize.
    _L = _L if islazylinop(_L) else ksm(_L, backend="xp")
    q_factors, rtn_factors = _algo7_2_pairwise(_L, target)

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
