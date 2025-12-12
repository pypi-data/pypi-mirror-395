from __future__ import annotations

from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import skew, kurtosis
from arrayflux.core import ArrayFlux
import numpy as np


class Rolling:
    """Rolling window operations for ArrayFlux."""

    def __init__(
        self,
        parent: ArrayFlux,
        window: int
    ) -> None:
        self.parent = parent
        self.window = window
        self.windows = sliding_window_view(parent, window)

    def _pad(self, arr: np.ndarray) -> ArrayFlux:
        """Pad the result with NaN to match original length."""
        missing = self.window - 1
        padded = np.concatenate([np.full(missing, np.nan), arr])
        return ArrayFlux(padded)

    def mean(self) -> ArrayFlux:
        """Rolling mean (ddof=0 always)."""
        return self._pad(np.mean(self.windows, axis=1))

    def std(self, ddof: int = 1) -> ArrayFlux:
        """Rolling standard deviation."""
        core = np.std(self.windows, axis=1, ddof=ddof)
        return self._pad(core)

    def var(self, ddof: int = 1) -> ArrayFlux:
        """Rolling variance."""
        core = np.var(self.windows, axis=1, ddof=ddof)
        return self._pad(core)

    def min(self) -> ArrayFlux:
        """Rolling minimum."""
        return self._pad(np.min(self.windows, axis=1))

    def max(self) -> ArrayFlux:
        """Rolling maximum."""
        return self._pad(np.max(self.windows, axis=1))

    def median(self) -> ArrayFlux:
        """Rolling median."""
        return self._pad(np.median(self.windows, axis=1))

    def sum(self) -> ArrayFlux:
        """Rolling sum."""
        return self._pad(np.sum(self.windows, axis=1))

    def quantile(self, q: float) -> ArrayFlux:
        """Rolling quantile."""
        core = np.quantile(self.windows, q=q, axis=1)
        return self._pad(core)

    def prod(self) -> ArrayFlux:
        """Rolling product."""
        return self._pad(np.prod(self.windows, axis=1))

    def skew(self, bias: bool = True) -> ArrayFlux:
        """Rolling skewness."""
        core = skew(self.windows, axis=1, bias=bias)
        return self._pad(core)

    def kurt(
        self,
        bias: bool = False,
        fisher: bool = False
    ) -> ArrayFlux:
        """
        Rolling kurtosis.
        Parameters match SciPy:
        - bias=False, fisher=False, identical to pandas rolling apply(kurtosis)
        """
        core = kurtosis(
            self.windows,
            axis=1,
            bias=bias,
            fisher=fisher
        )
        return self._pad(core)

    def cov(self, other: ArrayFlux, ddof: int = 0) -> ArrayFlux:
        """
        Rolling covariance.
        ddof = 0, pandas behavior
        ddof = 1, unbiased estimator
        """
        if len(other) != len(self.parent):
            raise ValueError("Series must have same length.")

        win_other = sliding_window_view(other, self.window)
        x = self.windows
        y = win_other

        mean_x = np.mean(x, axis=1)
        mean_y = np.mean(y, axis=1)

        num = np.sum(
            (x - mean_x[:, None]) * (y - mean_y[:, None]),
            axis=1
        )

        denom = self.window - ddof
        core = num / denom

        return self._pad(core)

    def corr(self, other: ArrayFlux, ddof: int = 0) -> ArrayFlux:
        """
        Rolling correlation.
        pandas rolling corr uses ddof=0.
        """
        cov = self.cov(other, ddof=ddof)
        std_x = self.std(ddof=ddof)
        std_y = other.rolling(self.window).std(ddof=ddof)
        return cov / (std_x * std_y)
