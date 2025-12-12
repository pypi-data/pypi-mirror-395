from array_api_compat import array_namespace, device
from lazylinop import islazylinop
from lazylinop.basicops import diag
from lazylinop.butterfly import fuse, ksm
from lazylinop.wip.butterfly.fuses import fuses
from lazylinop.wip.quantization.chop import chop
from lazylinop.wip.quantization.utils import finfo


def _map_2d_to_4d(ksv, ix, iy):
    """
    Map 2d rows ``ix`` and columns ``iy`` to 4d indices.

    Args:
        ksv: 4d array
            A 4d array ``ks_values``.
            Map 2d indexing to 4d indexing using
            ``ix = i_a * b * d + i_b * d + i_d`` and
            ``iy = i_a * c * d + i_c * d + i_d``.
        ix: ``list``
            Row indexes.
        iy: ``list``
            Column indexes.
    """
    xp = array_namespace(ksv)
    _device = device(ksv)
    a, b, c, d = ksv.shape
    _ix = xp.asarray(ix, device=_device)
    i_a = _ix // (b * d)
    i_b = (_ix - i_a * b * d) // d
    i_c = (xp.asarray(iy, device=_device) - i_a * c * d) // d
    i_d = _ix - i_a * b * d - i_b * d
    return i_a, i_b, i_c, i_d


def _rtn_strategy(L, t):
    """
    RTN strategy using ``t`` bits in mantissa.

    Args:
        L:
            Apply RTN strategy to ``ks_values`` of ``L``.

    Returns:
        List of 4d arrays that corresponds to
        RTN strategy applied to ``L.ks_values``.
        Of note, dtype is left unchanged.
    """
    p = len(L.ks_values)
    rtn_factors = [None] * p
    xp = array_namespace(L.ks_values[0])
    for i in range(p):
        A, B, C, D = xp.nonzero(L.ks_values[i])
        V = L.ks_values[i][A, B, C, D]
        # Turn ks_values to ksm later on.
        rtn_factors[i] = xp.asarray(L.ks_values[i], copy=True)
        rtn_factors[i][A, B, C, D] = chop(V, t)
    return rtn_factors


def _rerr(L, L_opt, L_rtn):
    """
    Probabilistic estimation of the error.

    Args:
        L:
            Base :py:func:`lazylinop.butterfly.ksm`.
        L_opt:
            :py:func:`lazylinop.butterfly.ksm` with
            quantized ``L.ks_values``.
        L_rtn:
            RTN strategy applied to ``L.ks_values``.
            ``L_rtn = _rtn_strategy(L, t)`` casted into
            target dtype where ``t`` is
            the number of bits in mantissa of target dtype.

    Returns:
        Relative error of quantization and relative error
        of RTN strategy.
    """

    if L_opt.ks_values[0].dtype != L_rtn.ks_values[0].dtype:
        raise Exception("L_opt.ks_values[0].dtype and" +
                        " L_rtn.ks_values[0].dtype must be the same.")
    if array_namespace(L_opt.ks_values[0]) != array_namespace(
            L_rtn.ks_values[0]):
        raise Exception("L_opt.ks_values[0] and L_rtn.ks_values[0]" +
                        " must share the same namespace.")

    n, b = L.shape[1], 128
    base_xp = array_namespace(L.ks_values[0])
    base_dev = L.ks_values[0].device
    xp = array_namespace(L_opt.ks_values[0])
    assert base_xp == xp
    # Base dtype.
    base = L.ks_values[0].dtype
    # Target dtype.
    target = L_opt.ks_values[0].dtype
    # assert base != target
    # Generate batch of random vectors with quantized dtype.
    dev_opt = L_opt.ks_values[0].device
    if 'torch' in str(xp.__package__):
        W_ref = xp.randn(n, b).to(dtype=target, device=dev_opt)
    else:
        W_ref = xp.random.randn(n, b).astype(target)
    W = base_xp.asarray(W_ref, dtype=base, device=base_dev)
    # Compute L @ W and cast to base dtype in L_opt.ks_values namespace.
    W_true = xp.asarray(L @ W, dtype=base, device=dev_opt)
    W_opt = xp.asarray(L_opt @ W_ref, dtype=base)
    W_rtn = xp.asarray(L_rtn @ W_ref, dtype=base, device=dev_opt)
    # Compute relative errors.
    nW = xp.linalg.norm(W_true, ord='fro')
    opt_rerr = xp.linalg.norm(W_true - W_opt, ord='fro') / nW
    rtn_rerr = xp.linalg.norm(W_true - W_rtn, ord='fro') / nW
    return opt_rerr, rtn_rerr


def _algo7_1(X, Y, target, dochopy: bool):
    """
    Implements Algorithm 7.1.

    Args:
        X, Y: :py:func:`lazylinop.butterfly.ksm`
            ksm with only one ``ks_values``.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.
        dochopy: ``bool``
            - ``True`` if both ``X, Y`` needs to be quantized.
            - ``False`` if only ``X`` needs to be quantized.

    Returns:
        A tuple ``(Xhat, Yhat, lambda, mu)``.
    """

    if not hasattr(X, "ks_values") or not hasattr(Y, "ks_values"):
        raise Exception("X, Y must be lazylinop.butterfly.ksm.")
    if len(X.ks_values) != 1 or len(Y.ks_values) != 1:
        raise Exception("X, Y must have only one ks_values.")

    t = finfo(target).nmant

    # Get namespace, dtype and device.
    xp = array_namespace(X.ks_values[0])
    _dtype = X.ks_values[0].dtype
    _device = device(X.ks_values[0])

    # Turn Xhat and Yhat to ksm later on.
    Xhat = xp.asarray(X.ks_values[0], copy=True)
    Yhat = xp.asarray(Y.ks_values[0], copy=True)
    Xhat[Xhat != 0] = 1
    if dochopy:
        Yhat[Yhat != 0] = 1

    n = X.shape[1]
    ux = xp.zeros((X.shape[1], 1),
                  dtype=_dtype, device=_device)
    uy = xp.zeros((Y.shape[0], 1),
                  dtype=_dtype, device=_device)
    li, mi = [None] * n, [None] * n
    for i in range(n):
        # Extract column i.
        ux[i, 0] = 1
        xd = X @ ux
        ux[i, 0] = 0
        ix = xp.nonzero(xd)[0]
        xs = xd[ix]
        # Extract column i.
        uy[i, 0] = 1
        yd = Y.T @ uy
        uy[i, 0] = 0
        iy = xp.nonzero(yd)[0]
        ys = yd[iy]

        lopt, mopt, _ = _algo5_1_opt_lambda(xs, ys, target, dochopy=dochopy)
        xsq = chop(lopt * xs, t)
        li[i] = lopt
        mi[i] = mopt

        # From 2d xsq to 4d Xhat
        Xhat[_map_2d_to_4d(Xhat, ix, [i])] = xsq.reshape(-1)
        if dochopy:
            ysq = chop(mi[i] * ys, t)
            # From 2d xp.conj(ysq.T) to 4d Yhat
            Yhat[_map_2d_to_4d(Yhat, [i], iy)] = xp.conj(ysq.T).reshape(-1)
    return (
        ksm(Xhat, backend='xp'), ksm(Yhat, backend='xp'), li, mi)


def _algo7_3_left2right(L, target):
    r"""
    Given $p$ butterfly factors $L=B_1,\cdots,B_p$ quantizes them with
    ``t`` bits using Algorithm 7.1 and Algorithm 7.3 (left-to-right heuristic).

    Args:
        L: :py:func:`lazylinop.butterfly.ksm`
            Butterfly factors $L=B_1,\cdots,B_p$.
            Length of ``L.ks_values`` is $p$.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.

    Returns:
        A tuple (list of 4d quantized arrays,
        list of 4d RTN strategy arrays).
    """

    if not islazylinop(L):
        raise Exception("L must be a LazyLinOp.")

    t = finfo(target).nmant

    # Get namespace, dtype and device.
    xp = array_namespace(L.ks_values[0])
    _dtype = L.ks_values[0].dtype
    _device = device(L.ks_values[0])
    p = len(L.ks_values)

    # Turn q_factors[k] to ksm later on.
    Bhat = [None] * p

    # Left to right strategy.
    X = ksm(L.ks_values[0], backend='xp')
    # Fuse consecutive factors to increase performance
    # and because _algo7_1 expects len(X.ks_values) == 1.
    Y = ksm(fuses([L.ks_values[f] for f in range(1, p)],
                  n_factors=1, strategy='memory', verbose=False),
            backend='xp')
    for k in range(p - 2):

        # Quantize XY.
        Bhat[k], _, li, mi = _algo7_1(X, Y, target, False)

        # Fuse diag(mi) (1, 1, 1, d) with L.ks_values[k + 1].
        # Of note, _algo7_1 expects len(X.ks_values) == 1.
        mi = xp.asarray(
            mi, dtype=_dtype, device=_device).reshape(1, 1, 1, -1)
        X = ksm(fuse(mi, L.ks_values[k + 1]), backend='xp')
        # Fuse consecutive factors to increase performance.
        Y = ksm(fuses([L.ks_values[f] for f in range(k + 2, p)],
                      n_factors=1, strategy='memory', verbose=False),
                backend='xp')

    # Quantize XY.
    Bhat[p - 2], Bhat[p - 1], li, mi = _algo7_1(X, Y, target, True)

    # Turn ks_values to ksm later on.
    q_factors = [None] * p
    for i in range(p):
        q_factors[i] = xp.asarray(Bhat[i].ks_values[0], copy=True)

    # RTN strategy for comparison.
    rtn_factors = _rtn_strategy(L, t)

    return q_factors, rtn_factors


def _algo7_2_pairwise(L, target):
    r"""
    Given $p$ butterfly factors $B_1,\cdots,B_p$ quantizes them with
    ``t`` bits using Algorithm 7.1 and Algorithm 7.2 (pairwise heuristic).

    Args:
        L: :py:func:`lazylinop.butterfly.ksm`
            Length of ``L.ks_values`` is $p$
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.

    Returns:
        A tuple (list of 4d quantized arrays,
        list of 4d RTN strategy arrays).
    """

    if not islazylinop(L):
        raise Exception("L must be a LazyLinOp.")

    t = finfo(target).nmant

    # Get namespace, dtype and device.
    xp = array_namespace(L.ks_values[0])
    _dtype = L.ks_values[0].dtype
    _device = device(L.ks_values[0])
    p = len(L.ks_values)
    for k in range(1, p):
        _dtype = xp.promote_types(
            _dtype, L.ks_values[k].dtype)

    # Turn Bhat[k] to ksm later on.
    Bhat = [None] * (p - p % 2)

    # Pairwise strategy.
    for k in range(p // 2):
        k1 = 2 * k
        k2 = 2 * k + 1
        X = ksm(L.ks_values[k1], backend='xp')
        Y = ksm(L.ks_values[k2], backend='xp')
        # Quantize B_{2k}B_{2k+1}.
        Bhat[k1], Bhat[k2], _, _ = _algo7_1(X, Y, target, True)

    # Return ks_values as 4d arrays.
    q_factors = [None] * p
    # p is odd.
    if p % 2 == 1:
        q_factors[p - 1] = xp.asarray(L.ks_values[p - 1], copy=True)
        i_a, i_b, i_c, i_d = xp.nonzero(q_factors[p - 1])
        q_factors[p - 1][i_a, i_b, i_c, i_d] = chop(
            q_factors[p - 1][i_a, i_b, i_c, i_d], t)

    # Turn ks_values to ksm later on.
    for i in range(p - p % 2):
        q_factors[i] = xp.asarray(Bhat[i].ks_values[0], copy=True)

    # RTN strategy for comparison.
    rtn_factors = _rtn_strategy(L, t)

    return q_factors, rtn_factors


def _algo5_1_opt_lambda(x, y, target, *, dochopy: bool = True):
    r"""
    Algorithm 5.1, version optimized for time for large-scale butterflies.

    Args:
        x, y: 1d array
            Vectors to be quantized.
        target: NumPy/CuPy or torch dtype
            Target dtype of the quantization.
        dochopy: ``bool``, optional
            - ``True`` if both ``x, y`` needs to be quantized.
            - ``False`` if just ``x`` needs to be quantized.

    Returns:
        ``l1opt`` optimal lambda, such that
        $\hat{x}=chop(l1opt*x,t)$ and $\hat{y}=chop(mu(\hat{x})*y,t)$.
    """

    # FIXME
    assert x.ndim == 2
    assert y.ndim == 2

    xp = array_namespace(x)
    _dtype = x.dtype
    _device = device(x)
    if _device != device(y):
        raise Exception("x and y must be on the same device.")
    if x.ndim == 2 and x.shape[1] != 1:
        raise Exception("x must be 1d array.")
    if y.ndim == 2 and y.shape[1] != 1:
        raise Exception("y must be 1d array.")

    x12 = xp.abs(x) / xp.pow(2, xp.floor(xp.log2(xp.abs(x))))

    # Generate breakpoints.
    t = finfo(target).nmant
    m = xp.asarray(
        list(range(2 ** (t - 1), 2 ** t)), dtype=x12.dtype, device=_device)
    li = xp.asarray([1], dtype=x12.dtype)
    for i in range(x.shape[0]):
        for e in range(1, 2 + 1):
            nextl = (m + 0.5) * 2 ** (e - t) / x12[i]
            li = xp.concat((li, nextl[
                xp.logical_and(nextl < 2, nextl > 1)]))

    # Sort breakpoints.
    li = xp.sort(xp.asarray(li))

    # Find the optimum.
    lmid = xp.asarray(
        (li[:(-1)] + li[1:]) / 2, device=_device).reshape(-1, 1)
    nl = lmid.shape[0]
    lopt, mopt, opt_rerr = None, None, xp.inf
    xy = x @ y.T
    nxy = xp.linalg.norm(xy, ord="fro")
    # Compute error per batch instead of using a simple loop.
    batch = 128
    while nl % batch != 0:
        batch -= 1
    for i in range(nl // batch):
        lx = x @ lmid[(i * batch):((i + 1) * batch)].T
        xh = chop(lx, t)
        mu = (x.T @ xh) / xp.linalg.norm(xh, axis=0) ** 2
        # Compute hat(x) and hat(y).
        xh = xp.asarray(xh, dtype=target, device=_device)
        # FIXME: dochopy if ty != inf.
        yh = xp.asarray(chop(y @ mu, t) if dochopy else y @ mu,
                        dtype=target, device=_device)
        # Compute C_{x,y}(hat{x},hat{y})=||xy^T-hat{x}hat{y}^T||^2.
        # Use direct computation to avoid artifial zero in C_{x,y} that
        # arise when using expanded expression from :ref:`[1] <opt_qrank1>`
        # especially for lower precision.
        if 'float8_e5m2' in str(target) or 'float8_e4m3fn' in str(target):
            # RuntimeError: "bmm" not implemented for 'Float8_e5m2'
            for j in range(batch):
                u = xh[:, j].reshape(-1, 1)
                v = yh[:, j].reshape(1, -1)
                rerr = xp.linalg.norm(
                    xy - xp.asarray(u @ v, dtype=xy.dtype), ord="fro") / nxy
                if rerr < opt_rerr:
                    opt_rerr = rerr
                    lopt = lmid[i * batch + j, 0]
                    mopt = mu[0, j]
        else:
            bxh = xh.T.reshape(batch, xh.shape[0], 1)
            byh = yh.T.reshape(batch, 1, yh.shape[0])
            diff = xy - xp.asarray(bxh @ byh, dtype=xy.dtype)
            rerr = xp.linalg.norm(diff, axis=(1, 2), ord="fro") / nxy
            idx = xp.argmin(rerr)
            assert batch == rerr.shape[0]
            if rerr[idx] < opt_rerr:
                opt_rerr = rerr[idx]
                lopt = lmid[i * batch + idx, 0]
                mopt = mu[0, idx]

    return lopt, mopt, opt_rerr
