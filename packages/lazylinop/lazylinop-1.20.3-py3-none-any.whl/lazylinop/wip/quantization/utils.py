from array_api_compat import array_namespace


def promote_types(t1, t2):
    """
    Promote to the type in which both ``t1`` and ``t2``
    may be safely cast.

    Args:
        t1, t2: NumPy/CuPy or torch dtype
            ``t1`` and ``t2`` are two dtypes.

    Returns:
        If the two types share the same namespace and
        ``t1`` and ``t2`` are not ``torch.float8_*`` return
        the promoted type, otherwise return ``None``.

    Examples:
        >>> import numpy as np
        >>> t1 = np.dtype('float16')
        >>> t2 = np.dtype('float64')
        >>> promote_types(t1, t2) == t2
        True
        >>> import torch
        >>> t1 = torch.float16
        >>> t2 = torch.bfloat16
        >>> promote_types(t1, t2) == torch.float32
        True
        >>> t1 = torch.float32
        >>> t2 = torch.bfloat16
        >>> promote_types(t1, t2) == t1
        True
        >>> t1 = torch.float8_e4m3fn
        >>> t2 = torch.float32
        >>> promote_types(t1, t2) is None
        True

    .. seealso::

        - `NumPy promote <https://numpy.org/doc/stable/reference/
          generated/numpy.promote_types.html>`_,
        - `PyTorch promote <https://docs.pytorch.org/docs/stable/
          generated/torch.promote_types.html>`_.
    """

    # Infer namespace.
    if 'torch' in str(t1) and 'torch' in str(t2):
        import array_api_compat.torch as xp
    elif 'torch' not in str(t1) and 'torch' not in str(t2):
        import array_api_compat.numpy as xp
    else:
        return None

    try:
        return xp.promote_types(t1, t2)
    except RuntimeError:
        # RuntimeError: Promotion for Float8 Types is not supported,
        # attempted to promote Float8_e5m2(e4m3fn) and Float
        if 'torch.float8_e' in str(t1) and 'torch.float8_e' in str(t2):
            return None


class _info():

    def __init__(self, dtype, nexp=None, nmant=None):

        # Infer array namespace.
        import array_api_compat.torch as xp
        if isinstance(dtype, xp.dtype):
            _is_torch = True
        else:
            import array_api_compat.numpy as xp
            _is_torch = False

        _f = xp.finfo(dtype)

        # Copy attribute value.
        for a in dir(_f):
            if a.startswith('__'):
                continue
            self.__setattr__(a, _f.__getattribute__(a))

        # If dtype is a torch.dtype add nmant and nexp attributes.
        if _is_torch:
            self.nexp = nexp
            self.nmant = nmant

        del _f

    def __repr__(self):
        msg = ""
        for a in dir(self):
            if a.startswith('_'):
                continue
            msg = msg + f"{a}={self.__getattribute__(a)}\n"
        return msg


def finfo(dtype):
    """
    Get info about the numerical properties of ``dtype``.
    ``dtype`` is a floating point type.
    If ``dtype`` is a ``torch.dtype`` add ``nmant`` and
    ``nexp`` attributes.

    Args:
        dtype:
            Get info about this dtype.

    Returns:
        An object that stores the numerical properties
        of ``dtype``.

    Examples:
        >>> import torch
        >>> from lazylinop.wip.quantization import finfo
        >>> f = finfo(torch.bfloat16)
        >>> f.nmant
        7

    .. seealso::
        - `NumPy finfo <https://numpy.org/doc/stable/reference/
          generated/numpy.finfo.html>`_,
        - `PyTorch finfo <https://docs.pytorch.org/docs/
          stable/type_info.html>`_.
    """
    # AttributeError: 'torch.finfo' object has no attribute 'nmant'
    import array_api_compat.torch as xp
    if isinstance(dtype, xp.dtype):
        try:
            x = xp.asarray([1.0, 1.0], dtype=dtype).numpy()
            f = _info(x.dtype)
        except TypeError:
            if str(dtype) == 'torch.float8_e4m3fn':
                f = _info(dtype, 4, 3)
            elif str(dtype) == 'torch.float8_e5m2':
                f = _info(dtype, 5, 2)
            elif str(dtype) == 'torch.bfloat16':
                f = _info(dtype, 8, 7)
    else:
        f = _info(dtype)
    return f
