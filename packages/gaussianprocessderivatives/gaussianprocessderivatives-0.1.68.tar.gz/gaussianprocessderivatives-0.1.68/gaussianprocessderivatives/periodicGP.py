#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class periodicGP(gaussianprocess):
    """Gaussian process with a periodic kernel function."""

    noparams = 3
    description = "periodic covariance function"

    @property
    def info(self):
        print("hparam[0] determines the amplitude of variation")
        print("hparam[1] determines the stiffness")
        print("hparam[2] determines the period")
        print("hparam[3] determines the variance of the measurement error")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        xp = np.asarray(xp)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        k = th[0] * pr
        jk = np.empty((len(xp), self.noparams))
        jk[:, 0] = pr
        jk[:, 1] = -2 * pr * th[0] * np.sin((x - xp) / th[2]) ** 2
        jk[:, 2] = (
            2
            * pr
            * th[0]
            * th[1]
            * (x - xp)
            * np.sin(2 * (x - xp) / th[2])
            / th[2] ** 2
        )
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find d/dx of the kernel function."""
        th = np.exp(lth)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        return (
            -2 * pr * th[0] * th[1] * np.sin(2 * (x - xp) / th[2]) / th[2],
            False,
        )

    def d1d2covfn(self, x, xp, lth):
        """Find d/dx d/xp of the kernel function."""
        th = np.exp(lth)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        return (
            2
            * pr
            * th[0]
            * th[1]
            / th[2] ** 2
            * (
                2 * np.cos(2 * (x - xp) / th[2])
                + th[1] * (-1 + np.cos(4 * (x - xp) / th[2]))
            ),
            False,
        )

    def d12covfn(self, x, xp, lth):
        """Find d^2/dx^2 of the kernel function."""
        th = np.exp(lth)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        return (
            -2
            * pr
            * th[0]
            * th[1]
            / th[2] ** 2
            * (
                2 * np.cos(2 * (x - xp) / th[2])
                + th[1] * (-1 + np.cos(4 * (x - xp) / th[2]))
            ),
            False,
        )

    def d12d2covfn(self, x, xp, lth):
        """Find d^2/dx^2 d/dxp of the covariance function."""
        th = np.exp(lth)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        return (
            -4
            * pr
            * th[0]
            * th[1]
            / th[2] ** 3
            * (
                2
                - th[1] ** 2
                + 6 * th[1] * np.cos(2 * (x - xp) / th[2])
                + th[1] ** 2 * np.cos(4 * (x - xp) / th[2])
            )
            * np.sin(2 * (x - xp) / th[2]),
            False,
        )

    def d12d22covfn(self, x, xp, lth):
        """Find d^2/dx^2 d^2/dxp^2 of the covariance function."""
        th = np.exp(lth)
        pr = np.exp(-2 * th[1] * np.sin((x - xp) / th[2]) ** 2)
        return (
            2
            * pr
            * th[0]
            * th[1]
            / th[2] ** 4
            * (
                (8 - 12 * th[1] ** 2) * np.cos(2 * (x - xp) / th[2])
                + th[1]
                * (
                    -4
                    + 3 * th[1] ** 2
                    - 4 * (-7 + th[1] ** 2) * np.cos(4 * (x - xp) / th[2])
                    + 12 * th[1] * np.cos(6 * (x - xp) / th[2])
                    + th[1] ** 2 * np.cos(8 * (x - xp) / th[2])
                )
            ),
            False,
        )
