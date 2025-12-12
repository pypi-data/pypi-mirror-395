from array_api_compat import array_namespace, device
from lazylinop.wip.quantization.utils import finfo


def chop(x, t: int = 24):
    """
    Round matrix elements.

    Args:
        x: array
            ``chop(x, t)`` is the matrix obtained by rounding
            the elements of ``x`` to ``t`` significant binary places.
        t: ``int``, optional
            Number of bits in mantissa.
            Default value is 24, corresponding to IEEE single precision.
            By definition, ``t`` is always lesser than the number of
            bits in mantissa of `x.dtype``.

    Returns:
        An array with rounded elements.
    """

    xp = array_namespace(x)
    if finfo(x.dtype).nmant <= t:
        raise Exception("Number of bits in mantissa of x.dtype must be > t.")

    # Use the representation:
    # x(i,j) = 2^e(i,j) * .d(1)d(2)...d(s) * sign(x(i,j))

    if x.ndim == 1:
        _is1d = True
        x = x.reshape(-1, 1)
    else:
        _is1d = False

    # On the next line `+(x==0)' avoids passing a zero argument to log2,
    # which would cause a warning message to be generated.
    y = xp.abs(x) + (x == 0)
    e = xp.floor(xp.log2(y) + 1)
    # c = xp.round(x * xp.pow(2, t - e)) * xp.pow(2, e - t)
    # It is equivalent to:
    # c = xp.round(x * xp.pow(2, t - e)) / xp.pow(2, t - e)
    # and you avoid to compute two xp.pow(2, ...).
    _pow = xp.pow(2, t - e)
    c = xp.round(x * _pow) / _pow
    # By definition t is always lesser than xp.finfo(x.dtype).nexp.
    _finfo = xp.finfo(x.dtype)
    e_min = -xp.log2(xp.asarray(-_finfo.min))
    e_max = xp.log2(xp.asarray(_finfo.max))
    # Case t > 0, e < 0, (t - e) >= e_max:
    idx = xp.nonzero((t - e) >= e_max)
    if idx[0].shape[0] > 0:
        delta = (t - e[*idx]) - e_max
        p1 = xp.pow(2, delta)
        p2 = xp.pow(2, -e_max)
        c[*idx] = (xp.round((x[*idx] * p1) * p2) / p1) / p2
    # Case t > 0, e > 0, (t - e) <= e_min:
    idx = xp.nonzero((t - e) <= e_min)
    if idx[0].shape[0] > 0:
        delta = (t - e[*idx]) - e_min
        p1 = xp.pow(2, delta)
        p2 = xp.pow(2, -e_min)
        c[*idx] = (xp.round((x[*idx] * p1) * p2) / p1) / p2
    return c.reshape(-1) if _is1d else c
