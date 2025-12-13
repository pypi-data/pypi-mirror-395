#!/usr/bin/env python3
import numpy as np
from gaussianprocessderivatives.gaussianprocess import gaussianprocess


class spectralmixtureGP(gaussianprocess):
    """
    Gaussian process with a spectral mixture covariance function.

    From Wilson & Adams, 2013.

    UNFINISHED.
    """

    description = "spectral mixture covariance function"

    @property
    def info(self):
        print(
            "hparams are grouped in threes for each Gaussian in the spectral density"
        )
        print("hparam[0] determines the variance")
        print("hparam[1] determines the mean")
        print("hparam[2] determines the weight")

    def covfn(self, x, xp, lth):
        """Find the kernel function and its jacobian."""
        th = np.exp(lth)
        xp = np.asarray(xp)
        noparams = len(self.b) - 1
        k = 0
        for i in np.arange(0, noparams, 3):
            k += (
                np.exp(-((x - xp) ** 2) * th[i] / 2)
                * np.sqrt(th[i])
                * th[i + 2]
                * np.cos(2 * np.pi * (x - xp) * th[i + 1])
            )
        jk = np.empty((len(xp), noparams))
        for i in np.arange(0, noparams, 3):
            smexp = np.exp(-((x - xp) ** 2) * th[i] / 2)
            jk[:, i] = (
                -th[i + 2]
                * (-1 + th[i] * (x - xp) ** 2)
                * np.cos(2 * np.pi * th[i + 1] * (x - xp))
                / 2
                / np.sqrt(th[i])
            )
            jk[:, i + 1] = (
                -2
                * np.pi
                * np.sqrt(th[i])
                * th[i + 2]
                * (x - xp)
                * np.sin(2 * np.pi * th[i + 1] * (x - xp))
            )
            jk[:, i + 2] = np.sqrt(th[i]) * np.cos(
                2 * np.pi * th[i + 1] * (x - xp)
            )
        return k, jk

    def plotspectrum(self, npts=100):
        th = np.exp(self.lth_opt)
        noparams = len(self.b) - 1
        # need to choose points around each mu
        s = np.append(
            np.linspace(th[1] - 5 * np.sqrt(th[0]), th[1], npts),
            np.linspace(th[1], th[1] + 5 * np.sqrt(th[0]), npts),
        )
        for i in np.arange(1, noparams, 3):
            s = np.append(
                s, np.linspace(th[i + 1] - 5 * np.sqrt(th[i]), th[i + 1], npts)
            )
            s = np.append(
                s, np.linspace(th[i + 1], th[i + 1] + 5 * np.sqrt(th[i]), npts)
            )
        s = np.sort(np.unique(s))
        sp = np.sum(
            [
                th[i + 2]
                * np.exp(-((s - th[i + 1]) ** 2) / 2 / th[i])
                / np.sqrt(th[i])
                for i in np.arange(0, noparams, 3)
            ],
            axis=0,
        )
        plt.figure()
        plt.plot(s, sp)
        plt.yscale("log")
        plt.show()
