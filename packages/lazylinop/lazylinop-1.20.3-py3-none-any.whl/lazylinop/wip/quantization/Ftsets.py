import json


def gen_float(t: int, emax: int, *, include_subn=None):
    """
    Generates a floating point number system with ``t`` bits
    of precision and ``(1-emax, emax)`` exponent range
    include subnormals by default
    """

    if include_subn is None:
        _include_subn = 0
    else:
        _include_subn = include_subn
    if include_subn:
        m = range(1, 2**t - 1 + 1)
    else:
        m = range(2 ** (t - 1), 2**t - 1 + 1)
    emin = 1 - emax
    F = []
    for e in range(emin, emax + 1):
        F.append(m * 2 ** (e - t))
    F.append(2**emax)
    return F


def gen_set_of_FP_products(F):
    """
    generate set of xy where x, y are in ``F``.
    """
    S = []
    for i in F:
        for j in F:
            S.append(i * j)
    # Remove duplicates.
    S = np.unique(np.asarray(S))
    return S.tolist()


# Generates elements of Ft, FtFt, F2t
emax = 2
for t in range(2, 17 + 1):
    F = gen_float(t, emax)
    Ft[t] = F(F >= 1 and F <= 2)
    if t <= 11:
        F = gen_float(t, emax)
        F = gen_set_of_FP_products(F)
        FtFt[t] = F(F >= 1 and F <= 2)
        F = gen_float(2 * t, emax)
        F2t[t] = F(F >= 1 and F <= 2)

data = {"Ft": Ft, "FtFt": FtFt, "F2t": F2t}
with open("Ftsets.json", "w") as out_file:
    json.dump(data, out_file, indent=1)
