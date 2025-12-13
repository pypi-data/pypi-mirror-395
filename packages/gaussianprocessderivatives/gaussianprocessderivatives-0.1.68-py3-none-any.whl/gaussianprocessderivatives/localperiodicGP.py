#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class localperiodicGP(gaussianprocess):
    """Gaussian process with a locally periodic covariance function."""

    noparams = 4
    description = "locally periodic covariance function"

    @property
    def info(self):
        print("hparam[0] determines the amplitude of variation")
        print("hparam[1] determines the stiffness")
        print("hparam[2] determines the period")
        print("hparam[3] determines the local length scale")
        print("hparam[4] determines the variance of the measurement error")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        xp = np.asarray(xp)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        k = th[0] * lpr
        jk = np.empty((len(xp), self.noparams))
        jk[:, 0] = lpr
        jk[:, 1] = -2 * lpr * th[0] * np.sin((x - xp) / th[2]) ** 2
        jk[:, 2] = (
            2
            / th[2] ** 2
            * lpr
            * th[0]
            * th[1]
            * (x - xp)
            * np.sin(2 * (x - xp) / th[2])
        )
        jk[:, 3] = -lpr * th[0] * (x - xp) ** 2 / 2
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find d/dx of the covariance function."""
        th = np.exp(lth)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        return (
            lpr
            * th[0]
            * (
                th[3] * (-x + xp)
                - (2 * th[1] * np.sin((2 * (x - xp)) / th[2])) / th[2]
            ),
            False,
        )

    def d1d2covfn(self, x, xp, lth):
        """Find d/dx d/xp of the covariance function."""
        th = np.exp(lth)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        return (
            lpr
            * th[0]
            * (
                (
                    -2 * th[1] ** 2
                    + th[2] ** 2 * th[3]
                    - th[2] ** 2 * th[3] ** 2 * x**2
                    + 2 * th[2] ** 2 * th[3] ** 2 * x * xp
                    - th[2] ** 2 * th[3] ** 2 * xp**2
                    + 4 * th[1] * np.cos((2 * (x - xp)) / th[2])
                    + 2 * th[1] ** 2 * np.cos((4 * (x - xp)) / th[2])
                    - 4
                    * th[1]
                    * th[2]
                    * th[3]
                    * x
                    * np.sin((2 * (x - xp)) / th[2])
                    + 4
                    * th[1]
                    * th[2]
                    * th[3]
                    * xp
                    * np.sin((2 * (x - xp)) / th[2])
                )
                / th[2] ** 2
            ),
            False,
        )

    def d12covfn(self, x, xp, lth):
        """Find d^2/dx^2 of the covariance function."""
        th = np.exp(lth)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        return (
            lpr
            * th[0]
            * (
                2 * th[1] ** 2
                - th[2] ** 2 * th[3]
                + th[2] ** 2 * th[3] ** 2 * x**2
                - 2 * th[2] ** 2 * th[3] ** 2 * x * xp
                + th[2] ** 2 * th[3] ** 2 * xp**2
                - 4 * th[1] * np.cos((2 * (x - xp)) / th[2])
                - 2 * th[1] ** 2 * np.cos((4 * (x - xp)) / th[2])
                + 4
                * th[1]
                * th[2]
                * th[3]
                * x
                * np.sin((2 * (x - xp)) / th[2])
                - 4
                * th[1]
                * th[2]
                * th[3]
                * xp
                * np.sin((2 * (x - xp)) / th[2])
            )
            / th[2] ** 2,
            False,
        )

    def d12d2covfn(self, x, xp, lth):
        """Find d^2/dx^2 d/dxp of the covariance function."""
        th = np.exp(lth)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        return (
            -lpr
            * th[0]
            * (
                (
                    -6 * th[1] ** 2 * th[2] * th[3] * x
                    + 3 * th[2] ** 3 * th[3] ** 2 * x
                    - th[2] ** 3 * th[3] ** 3 * x**3
                    + 6 * th[1] ** 2 * th[2] * th[3] * xp
                    - 3 * th[2] ** 3 * th[3] ** 2 * xp
                    + 3 * th[2] ** 3 * th[3] ** 3 * x**2 * xp
                    - 3 * th[2] ** 3 * th[3] ** 3 * x * xp**2
                    + th[2] ** 3 * th[3] ** 3 * xp**3
                    + 12
                    * th[1]
                    * th[2]
                    * th[3]
                    * (x - xp)
                    * np.cos((2 * (x - xp)) / th[2])
                    + 6
                    * th[1] ** 2
                    * th[2]
                    * th[3]
                    * (x - xp)
                    * np.cos((4 * (x - xp)) / th[2])
                    + 8 * th[1] * np.sin((2 * (x - xp)) / th[2])
                    - 6 * th[1] ** 3 * np.sin((2 * (x - xp)) / th[2])
                    + 6
                    * th[1]
                    * th[2] ** 2
                    * th[3]
                    * np.sin((2 * (x - xp)) / th[2])
                    - 6
                    * th[1]
                    * th[2] ** 2
                    * th[3] ** 2
                    * x**2
                    * np.sin((2 * (x - xp)) / th[2])
                    + 12
                    * th[1]
                    * th[2] ** 2
                    * th[3] ** 2
                    * x
                    * xp
                    * np.sin((2 * (x - xp)) / th[2])
                    - 6
                    * th[1]
                    * th[2] ** 2
                    * th[3] ** 2
                    * xp**2
                    * np.sin((2 * (x - xp)) / th[2])
                    + 12 * th[1] ** 2 * np.sin((4 * (x - xp)) / th[2])
                    + 2 * th[1] ** 3 * np.sin((6 * (x - xp)) / th[2])
                )
                / th[2] ** 3
            ),
            False,
        )

    def d12d22covfn(self, x, xp, lth):
        """Find d^2/dx^2 d^2/dxp^2 of the covariance function."""
        th = np.exp(lth)
        lpr = np.exp(
            -2 * th[1] * np.sin((x - xp) / th[2]) ** 2
            - (x - xp) ** 2 * th[3] / 2
        )
        return (
            lpr
            * th[0]
            * (
                -8 * th[1] ** 2
                + 6 * th[1] ** 4
                - 12 * th[1] ** 2 * th[2] ** 2 * th[3]
                + 3 * th[2] ** 4 * th[3] ** 2
                + 12 * th[1] ** 2 * th[2] ** 2 * th[3] ** 2 * x**2
                - 6 * th[2] ** 4 * th[3] ** 3 * x**2
                + th[2] ** 4 * th[3] ** 4 * x**4
                - 24 * th[1] ** 2 * th[2] ** 2 * th[3] ** 2 * x * xp
                + 12 * th[2] ** 4 * th[3] ** 3 * x * xp
                - 4 * th[2] ** 4 * th[3] ** 4 * x**3 * xp
                + 12 * th[1] ** 2 * th[2] ** 2 * th[3] ** 2 * xp**2
                - 6 * th[2] ** 4 * th[3] ** 3 * xp**2
                + 6 * th[2] ** 4 * th[3] ** 4 * x**2 * xp**2
                - 4 * th[2] ** 4 * th[3] ** 4 * x * xp**3
                + th[2] ** 4 * th[3] ** 4 * xp**4
                - 8
                * th[1]
                * (
                    -2
                    + 3 * th[1] ** 2
                    + 3 * th[2] ** 2 * th[3] * (-1 + th[3] * (x - xp) ** 2)
                )
                * np.cos((2 * (x - xp)) / th[2])
                - 4
                * th[1] ** 2
                * (
                    -14
                    + 2 * th[1] ** 2
                    + 3 * th[2] ** 2 * th[3] * (-1 + th[3] * (x - xp) ** 2)
                )
                * np.cos((4 * (x - xp)) / th[2])
                + 24 * th[1] ** 3 * np.cos((6 * (x - xp)) / th[2])
                + 2 * th[1] ** 4 * np.cos((8 * (x - xp)) / th[2])
                - 32
                * th[1]
                * th[2]
                * th[3]
                * x
                * np.sin((2 * (x - xp)) / th[2])
                + 24
                * th[1] ** 3
                * th[2]
                * th[3]
                * x
                * np.sin((2 * (x - xp)) / th[2])
                - 24
                * th[1]
                * th[2] ** 3
                * th[3] ** 2
                * x
                * np.sin((2 * (x - xp)) / th[2])
                + 8
                * th[1]
                * th[2] ** 3
                * th[3] ** 3
                * x**3
                * np.sin((2 * (x - xp)) / th[2])
                + 32
                * th[1]
                * th[2]
                * th[3]
                * xp
                * np.sin((2 * (x - xp)) / th[2])
                - 24
                * th[1] ** 3
                * th[2]
                * th[3]
                * xp
                * np.sin((2 * (x - xp)) / th[2])
                + 24
                * th[1]
                * th[2] ** 3
                * th[3] ** 2
                * xp
                * np.sin((2 * (x - xp)) / th[2])
                - 24
                * th[1]
                * th[2] ** 3
                * th[3] ** 3
                * x**2
                * xp
                * np.sin((2 * (x - xp)) / th[2])
                + 24
                * th[1]
                * th[2] ** 3
                * th[3] ** 3
                * x
                * xp**2
                * np.sin((2 * (x - xp)) / th[2])
                - 8
                * th[1]
                * th[2] ** 3
                * th[3] ** 3
                * xp**3
                * np.sin((2 * (x - xp)) / th[2])
                - 48
                * th[1] ** 2
                * th[2]
                * th[3]
                * x
                * np.sin((4 * (x - xp)) / th[2])
                + 48
                * th[1] ** 2
                * th[2]
                * th[3]
                * xp
                * np.sin((4 * (x - xp)) / th[2])
                - 8
                * th[1] ** 3
                * th[2]
                * th[3]
                * x
                * np.sin((6 * (x - xp)) / th[2])
                + 8
                * th[1] ** 3
                * th[2]
                * th[3]
                * xp
                * np.sin((6 * (x - xp)) / th[2])
            )
            / th[2] ** 4,
            False,
        )
