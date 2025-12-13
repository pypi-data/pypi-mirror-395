#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class maternGP(gaussianprocess):
    """Gaussian process with a twice differentiable Matern kernel function."""

    noparams = 2
    description = "(twice differentiable) Matern covariance function"

    @property
    def info(self):
        print("hparam[0] determines the amplitude of variation")
        print("hparam[1] determines the stiffness")
        print("hparam[2] determines the variance of the measurement error")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        xp = np.asarray(xp)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        poly = 1 + 5 * r**2 / 3 / th[1] ** 2 + s5 * r / th[1]
        k = th[0] * e * poly
        jk = np.empty((len(xp), self.noparams))
        jk[:, 0] = e * poly
        jk[:, 1] = 5 * e * th[0] * r**2 * (th[1] + s5 * r) / 3 / th[1] ** 4
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find d/dx of the kernel function."""
        th = np.exp(lth)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        df = 5 * e * th[0] * r * (th[1] + s5 * r) / 3 / th[1] ** 3
        sns = np.ones(np.size(xp))
        sns[x > xp] = -1
        return sns * df, False

    def d1d2covfn(self, x, xp, lth):
        """Find d/dx d/dxp of the kernel function."""
        th = np.exp(lth)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        return (
            5
            * e
            * th[0]
            * (th[1] ** 2 + s5 * th[1] * r - 5 * r**2)
            / 3
            / th[1] ** 4,
            False,
        )

    def d12covfn(self, x, xp, lth):
        """Find d^2/dx^2 of the kernel function."""
        th = np.exp(lth)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        return (
            -5
            * e
            * th[0]
            * (th[1] ** 2 + s5 * th[1] * r - 5 * r**2)
            / 3
            / th[1] ** 4,
            False,
        )

    def d12d2covfn(self, x, xp, lth):
        """Find d^2/dx^2 d/dxp of the kernel function."""
        th = np.exp(lth)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        df = 25 * e * th[0] * r * (3 * th[1] - s5 * r) / 3 / th[1] ** 5
        sns = np.ones(np.size(xp))
        sns[x > xp] = -1
        return sns * df, False

    def d12d22covfn(self, x, xp, lth):
        """Find d^2/dx^2 d^2/dxp^2 of the kernel function."""
        th = np.exp(lth)
        r = np.abs(x - xp)
        s5 = np.sqrt(5)
        e = np.exp(-s5 * r / th[1])
        return (
            25
            * e
            * th[0]
            * (3 * th[1] ** 2 + 5 * r**2 - 5 * s5 * th[1] * r)
            / 3
            / th[1] ** 6,
            False,
        )
