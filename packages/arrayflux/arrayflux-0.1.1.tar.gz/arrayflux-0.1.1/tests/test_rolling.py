from scipy.stats import skew, kurtosis
from arrayflux.core import ArrayFlux
from arrayflux import arrayflux
import pandas as pd
import numpy as np
import pytest


def assert_array_equal(a, b):
    assert np.allclose(a, b, equal_nan=True), f"\nA:\n{a}\nB:\n{b}"


@pytest.mark.parametrize("window", [3, 5, 10])
def test_rolling_basic(window):
    np.random.seed(42)
    data = np.random.randn(50)

    af = arrayflux(data)
    r = af.rolling(window)

    s = pd.Series(data)
    rp = s.rolling(window)

    # mean
    assert_array_equal(r.mean(), rp.mean().to_numpy())

    # std
    assert_array_equal(r.std(), rp.std().to_numpy())

    # var
    assert_array_equal(r.var(), rp.var().to_numpy())

    # min
    assert_array_equal(r.min(), rp.min().to_numpy())

    # max
    assert_array_equal(r.max(), rp.max().to_numpy())

    # median
    assert_array_equal(r.median(), rp.median().to_numpy())

    # sum
    assert_array_equal(r.sum(), rp.sum().to_numpy())

    # quantile
    assert_array_equal(
        r.quantile(0.5),
        rp.quantile(0.5).to_numpy()
    )

    # prod
    assert_array_equal(
        r.prod(),
        rp.apply(np.prod, raw=True).to_numpy()
    )


# Test skew e kurtosis (SciPy required)
def test_skew_kurt():
    np.random.seed(42)
    data = np.random.randn(40)
    window = 5

    af = arrayflux(data)
    r = af.rolling(window)

    s = pd.Series(data)
    rp = s.rolling(window)

    # skew
    pandas_skew = rp.apply(lambda w: skew(w, bias=True), raw=False).to_numpy()
    arrayflux_skew = r.skew()
    assert_array_equal(arrayflux_skew, pandas_skew)

    # kurtosis
    pandas_kurt = rp.apply(
        lambda w: kurtosis(w, bias=False), raw=False
    ).to_numpy()
    arrayflux_kurt = r.kurt(bias=False, fisher=True)
    assert_array_equal(arrayflux_kurt, pandas_kurt)
