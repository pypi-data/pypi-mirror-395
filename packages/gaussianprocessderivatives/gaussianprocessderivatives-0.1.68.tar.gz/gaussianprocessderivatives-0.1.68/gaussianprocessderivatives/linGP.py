#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class linGP(gaussianprocess):
    """Gaussian process with a linear kernel function."""

    noparams = 2
    description = "linear Gaussian process"

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        k = th[0] + th[1] * x * xp
        jk = np.empty((len(xp), self.noparams))
        jk[:, 0] = th[0] * np.ones(len(xp))
        jk[:, 1] = th[1] * x * xp
        return k, jk

    def d1covfn(self, x, xp, lth):
        """Find d/dx of the kernel function."""
        th = np.exp(lth)
        grad = th[1] * xp
        return grad, False

    def d1d2covfn(self, x, xp, lth):
        """Find d/dx d/xp of the kernel function."""
        th = np.exp(lth)
        hess = th[1] * np.ones(len(xp))
        return hess, False
