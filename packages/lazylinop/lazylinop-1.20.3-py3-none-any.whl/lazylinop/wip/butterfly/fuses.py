# -*- coding-utf8 -*-
import numpy as np
from lazylinop.butterfly import fuse


def fuses(ts, n_factors: int, strategy: str = 'memory', verbose: bool = True):
    r"""
    Fuse the list ``ts`` of 4D arrays of ``ks_values`` according to
    ``strategy`` argument and return a new list ``t`` of ``ks_values``.
    The resulting list of 4D arrays of ``ks_values`` ``t``
    is of length ``n_factors <= len(ts)`` and satisfies
    ``(ksm(ts[0]) @ ... @ ksm(ts[-1])).toarray() == ksm(t).toarray()``.

    Args:
        ts: ``list`` of 4D arrays
            The dimensions of ``ts[l]`` must satisfy:

            - $\frac{a_lc_l}{a_{l+1}}=\frac{b_{l+1}d_{l+1}}{d_l}$ is an integer
            - $a_lc_ld_l=a_{l+1}b_{l+1}d_{l+1}$
            - $a_l$ divides $a_{l+1}$
            - $d_{l+1}$ divides $d_l$
            otherwize an ``Exception`` is returned.
        n_factors: ``int``
            Number of factors ``n_factors <= n``.
            If ``n_factors = n``, return the square-dyadic decomposition.
            The performance of the algorithm depends on
            the number of factors, the size of the FWHT
            as-well-as the strategy.
            Our experimentation shows that square-dyadic decomposition
            is always the worse choice.
            The best choice is two, three or four factors.
        strategy: ``str``, optional
            It could be:

            - ``balanced`` fuse from left to right and right to left ($n>3$).

              - Case ``n = 6`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5
                - step 1: 01 2 3 45
                - step 2: 012 345
              - Case ``n = 7`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
                - step 3: 0123 456
              - Case ``n = 7`` and ``n_factors = 3``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
            - ``'memory'`` find the two consecutive elements
              that minimize the memory of the resulting fused.
              It is the default value.
            - ``'sparsity'`` find the two consecutive elements that
              minimize the ratio $\frac{1}{ad}$ of the resulting fused.
            - ``'speed'`` find the two consecutive elements that
              minimize the ratio $\frac{bc}{b+c}$ of the resulting fused.
        verbose: ``bool``, optional
            Print fuse steps.
            Default value is ``True``.

    Returns:
        The resulting list ``t`` of ``ks_values`` is a list
        of 4D arrays of length ``n_factors <= len(ts)``.

    .. seealso::
        - :py:func:`lazylinop.butterfly.fuse`,
        - :py:func:`lazylinop.butterfly.ksm`.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly import ksm
        >>> from lazylinop.wip.butterfly.fuses import fuses
        >>> a1, b1, c1, d1 = 2, 2, 2, 4
        >>> a2, b2, c2, d2 = 4, 2, 2, 2
        >>> v1 = np.random.randn(a1, b1, c1, d1)
        >>> v2 = np.random.randn(a2, b2, c2, d2)
        >>> v = fuses([v1, v2], n_factors=1)
               ['0', '1']
        step=0 ['01']
        >>> v[0].shape
        (2, 4, 4, 2)
        >>> L = ksm(v)
        >>> L1 = ksm(v1)
        >>> L2 = ksm(v2)
        >>> x = np.random.randn(L.shape[1])
        >>> np.allclose(L @ x, L1 @ L2 @ x)
        True
    """

    n = len(ts)
    if not isinstance(ts, list):
        raise Exception("ts must be a list.")
    for i in range(n):
        if len(ts[i].shape) != 4:
            raise Exception("Each element of ks must be a 4D array.")
    for i in range(n - 1):
        a1, b1, c1, d1 = ts[i].shape
        a2, b2, c2, d2 = ts[i + 1].shape
        # Valid and chainable?
        if ((a1 * c1) % a2 != 0 or
            (b2 * d2) % d1 != 0 or
            a1 * c1 * d1 != a2 * b2 * d2 or
            a2 % a1 != 0 or
            d1 % d2 != 0):
            raise Exception("Each element of ks must be" +
                            " chainable and valid.")

    if n == n_factors:
        # Nothing to fuse.
        return ts.copy()
    else:
        # Copy the input list.
        _ts = ts.copy()
        m, target = n, n
        if strategy == 'balanced':
            if n <= 3:
                raise Exception("strategy 'balanced' does" +
                                " not work when len(ts) <= 3.")
            # Fuse from left to right and from right to left.
            step = 0
            idx = [str(i) for i in range(n)]
            if verbose:
                print(f"      ", idx)
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    idx[lpos + 1] = idx[lpos] + idx[lpos + 1]
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    idx[rpos - 1] = idx[rpos - 1] + idx[rpos]
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m / 2:
                    lpos, rpos = n_left, m - 1 - n_right
                if verbose:
                    print(f"step={step}", idx[n_left:(n - n_right)])
                step += 1
                if target == n_factors:
                    break
            m, target = n, n
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    _ts[lpos + 1] = fuse(_ts[lpos], _ts[lpos + 1])
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    _ts[rpos - 1] = fuse(_ts[rpos - 1], _ts[rpos])
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m // 2:
                    lpos, rpos = n_left, m - 1 - n_right
                if target == n_factors:
                    break
            return _ts[n_left:(n_left + n_factors)]
        elif strategy in ('memory', 'speed', 'sparsity'):
            step = 0
            idx = [str(i) for i in range(n)]
            if verbose:
                print(f"      ", idx)
            n_fuses = 0
            while True:
                # Build memory list.
                heuristic = np.full(n - n_fuses - 1, 0.0)
                memory = np.full(n - n_fuses - 1, 0)
                sparsity = np.full(n - n_fuses - 1, 0.0)
                for i in range(n - n_fuses - 1):
                    a1, b1, c1, d1 = _ts[i].shape
                    a2, b2, c2, d2 = _ts[i + 1].shape
                    b = (b1 * d1) // d2
                    c = (a2 * c2) // a1
                    memory[i] = a1 * b * c * d2
                    # Because of argmin, compute the inverse.
                    heuristic[i] = 1.0 / ((b + c) / (b * c))
                    sparsity[i] = 1.0 / (a1 * d2)
                # Find argmin.
                if strategy == 'memory':
                    # argmin = np.argmin(memory)
                    tmp = np.where(memory == memory[np.argmin(memory)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                elif strategy == 'speed':
                    # argmin = np.argmin(heuristic)
                    tmp = np.where(
                        heuristic == heuristic[np.argmin(heuristic)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                elif strategy == 'sparsity':
                    # argmin = np.argmin(sparsity)
                    tmp = np.where(
                        sparsity == sparsity[np.argmin(sparsity)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                # Fuse argmin and argmin + 1.
                _ts[argmin] = fuse(_ts[argmin], _ts[argmin + 1])
                idx[argmin] = idx[argmin] + idx[argmin + 1]
                n_fuses += 1
                # Delete argmin + 1.
                _ts.pop(argmin + 1)
                idx.pop(argmin + 1)
                target -= 1
                if verbose:
                    print(f"step={step}", idx)
                step += 1
                if target == n_factors:
                    break
            return _ts
        else:
            raise Exception("strategy must be either 'balanced'," +
                            " 'memory', 'sparsity'" +
                            " or 'speed'.")
