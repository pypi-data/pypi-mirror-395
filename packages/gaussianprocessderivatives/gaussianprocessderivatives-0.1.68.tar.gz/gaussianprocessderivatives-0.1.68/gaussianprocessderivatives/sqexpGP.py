#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class sqexpGP(gaussianprocess):
    """Gaussian process with a squared exponential kernel function."""

    noparams = 2
    description = "squared exponential Gaussian process"

    @property
    def info(self):
        print("hparam[0] determines the amplitude of variation")
        print("hparam[1] determines the flexibility")
        print("hparam[2] determines the variance of the measurement error")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        xp = np.array(xp)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        k = th[0] * e
        jk = np.empty((len(xp), self.noparams))
        jk[:, 0] = e * th[0]
        jk[:, 1] = -th[0] * th[1] * e / 2.0 * (x - xp) ** 2
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find d/dx of the kernel function."""
        th = np.exp(lth)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        return -e * th[0] * th[1] * (x - xp), False

    def d1d2covfn(self, x, xp, lth):
        """Find d/dx d/dxp of the kernel function."""
        th = np.exp(lth)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        return -e * th[0] * th[1] * (-1 + th[1] * (x - xp) ** 2), False

    def d12covfn(self, x, xp, lth):
        """Find d^2/dx^2 of the kernel function."""
        th = np.exp(lth)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        return e * th[0] * th[1] * (-1 + th[1] * (x - xp) ** 2), False

    def d12d2covfn(self, x, xp, lth):
        """Find d^2/dx^2 d/dxp of the kernel function."""
        th = np.exp(lth)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        return (
            e * th[0] * th[1] ** 2 * (-3 + th[1] * (x - xp) ** 2) * (x - xp),
            False,
        )

    def d12d22covfn(self, x, xp, lth):
        """Find d^2/dx^2 d^2/dxp^2 of the kernel function."""
        th = np.exp(lth)
        e = np.exp(-th[1] / 2.0 * (x - xp) ** 2)
        return (
            e
            * th[0]
            * th[1] ** 2
            * (3 - 6 * th[1] * (x - xp) ** 2 + th[1] ** 2 * (x - xp) ** 4),
            False,
        )
