#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class nnGP(gaussianprocess):
    """Gaussian process with a neural network kernel function."""

    noparams = 2
    description = "neural network Gaussian process"

    @property
    def info(self):
        print("hparam[0] determines the initial value")
        print("hparam[1] determines the flexibility")
        print("hparam[2] determines the variance of the measurement error")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        k = (
            (
                np.arcsin(
                    2
                    * (th[0] + x * xp * th[1])
                    / np.sqrt(1 + 2 * (th[0] + x**2 * th[1]))
                    / np.sqrt(1 + 2 * (th[0] + xp**2 * th[1]))
                )
            )
            * 2
            / np.pi
        )
        jk = np.empty((len(xp), self.noparams))
        den = (
            np.pi
            * (1 + 2 * th[0] + 2 * th[1] * x**2)
            * (1 + 2 * th[0] + 2 * th[1] * xp**2)
            * np.sqrt(
                1
                + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                + 2 * th[1] * (x**2 + xp**2)
            )
        )
        jk[:, 0] = (
            (
                4
                * (
                    1
                    + 2 * th[0] * (1 + th[1] * (x - xp) ** 2)
                    - 2 * th[1] ** 2 * x * (x - xp) ** 2 * xp
                    + 2 * th[1] * (x**2 - x * xp + xp**2)
                )
            )
            / den
            * th[0]
        )
        jk[:, 1] = (
            -(
                4
                * (
                    2 * th[0] ** 2 * (x - xp) ** 2
                    - x * xp * (1 + th[1] * (x**2 + xp**2))
                    + th[0]
                    * (
                        -2 * th[1] * x**3 * xp
                        + xp**2
                        - 2 * x * xp * (2 + th[1] * xp**2)
                        + x**2 * (1 + 4 * th[1] * xp**2)
                    )
                )
            )
            / den
            * th[1]
        )
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find the d/dx of the kernel function."""
        th = np.exp(lth)
        return (
            4
            * th[1]
            * (-2 * th[0] * x + xp + 2 * th[0] * xp)
            / (1 + 2 * th[0] + 2 * th[1] * x**2)
            / np.sqrt(
                1
                + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                + 2 * th[1] * (x**2 + xp**2)
            )
            / np.pi,
            False,
        )

    def d1d2covfn(self, x, xp, lth):
        """Find the d/dx d/dxp of the kernel function."""
        th = np.exp(lth)
        return (
            4
            * (th[1] + 4 * th[0] * th[1])
            / (
                1
                + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                + 2 * th[1] * (x**2 + xp**2)
            )
            ** 1.5
            / np.pi,
            False,
        )

    def d12covfn(self, x, xp, lth):
        """Find d^2/dx^2 of the kernel function."""
        th = np.exp(lth)
        return (
            -8
            * th[1]
            * (
                8 * th[0] ** 3
                + th[0] ** 2
                * (
                    6
                    - 8 * th[1] * x * (x - 3 * xp)
                    - 16 * th[1] ** 2 * x * (x - xp) ** 3
                )
                + th[1]
                * x
                * xp
                * (3 + 6 * th[1] * x**2 + 4 * th[1] * xp**2)
                + th[0]
                * (
                    1
                    - 2 * th[1] * x * (x - 9 * xp)
                    - 8
                    * th[1] ** 2
                    * x
                    * (
                        x**3
                        - 3 * x**2 * xp
                        + 3 * x * xp**2
                        - 2 * xp**3
                    )
                )
            )
            / (
                np.pi
                * (1 + 2 * th[0] + 2 * th[1] * x**2) ** 2
                * (
                    1
                    + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                    + 2 * th[1] * (x**2 + xp**2)
                )
                ** 1.5
            ),
            False,
        )

    def d12d2covfn(self, x, xp, lth):
        """Find d^2/dx^2 d/dxp of the kernel function."""
        th = np.exp(lth)
        return (
            -24
            * (1 + 4 * th[0])
            * th[1] ** 2
            * (x + 2 * th[0] * x - 2 * th[0] * xp)
            / (
                np.pi
                * (
                    1
                    + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                    + 2 * th[1] * (x**2 + xp**2)
                )
                ** 2.5
            ),
            False,
        )

    def d12d22covfn(self, x, xp, lth):
        """Find d^2/dx^2 d^2/dxp^2 of the kernel function."""
        th = np.exp(lth)
        return (
            -48
            * (1 + 4 * th[0])
            * th[1] ** 2
            * (
                4 * th[0] ** 2 * (-1 + 4 * th[1] * (x - xp) ** 2)
                - 5 * th[1] * x * xp
                + th[0]
                * (-1 + 4 * th[1] * (2 * x**2 - 5 * x * xp + 2 * xp**2))
            )
            / (
                np.pi
                * (
                    1
                    + 4 * th[0] * (1 + th[1] * (x - xp) ** 2)
                    + 2 * th[1] * (x**2 + xp**2)
                )
                ** 3.5
            ),
            False,
        )
