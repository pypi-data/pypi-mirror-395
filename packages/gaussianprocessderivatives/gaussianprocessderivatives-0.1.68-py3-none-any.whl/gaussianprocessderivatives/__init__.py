"""
for smoothing and finding the derivatives of time-series data

    Follows Rasmussen and Williams (2006): the Gaussian process
    algorithms come from chapter 3 and the Jacobian of the negative
    log likelihood from chapter 5.

    Covariance, kernel, functions can be

        squared exponential (sqexp),
        squared exponential with a linear trend (sqexplin)
        neural network-like (nn),
        twice differentiable Matern (matern),
        periodic (periodic),
        locally periodic (localperiodic).

    Bounds for hyperparameters are specified in log10 space.
    Hyperparameters are given in log space.

    Example
    -------
    First, generate some data:

    >>> import numpy as np
    >>> x = np.linspace(0, 10, 100)
    >>> y = np.sin(x) + np.random.randn(np.size(x))*0.1

    Second, import and optimise the Gaussian process:

    >>> import gaussianprocessderivatives as gp
    >>> g = gp.maternGP({0: (-4, 4), 1: (-4, 4), 2: (-4, -2)}, x, y)
    >>> g.findhyperparameters()
    >>> g.results()

    Third, evaluate the Gaussian process at the x-points of interest:

    >>> g.predict(x, derivs=1)

    Plot the results:

    >>> plt.figure()
    >>> plt.subplot(2,1,1)
    >>> g.sketch('.')
    >>> plt.subplot(2,1,2)
    >>> g.sketch('.', derivs=1)
    >>> plt.show()

    After running g.predict, the mean of the fitted GP is g.f and its
    variance is g.fvar.

    Running g.predict(x, derivs= 2) returns g.df, g.dfvar, g.ddf,
    and g.ddfvar.

    The meaning of the different hyperparmeters is given by

    >>> g.info

    Prior functions can also be sampled. For example,

    >>> g = gp.sqexplinGP({0: (-2,2), 1: (-2,2), 2: (-2,2), 3: (-2,2),
                     4: (-2,2)}, x, y)
    >>> plot(x, g.sampleprior(3, th=[1.0, 0.1, 3.1, 1.3]))

    will plot three samples of the prior latent functions with
    hyperparameters 1.0, 0.1, 3.1, and 1.3. There is no need to
    specify the hyperparameter for measurement error: it is not used to
    generate prior functions.
"""

from gaussianprocessderivatives.maternGP import maternGP
from gaussianprocessderivatives.linGP import linGP
from gaussianprocessderivatives.localperiodicGP import localperiodicGP
from gaussianprocessderivatives.periodicGP import periodicGP
from gaussianprocessderivatives.nnGP import nnGP
from gaussianprocessderivatives.sqexpGP import sqexpGP
from gaussianprocessderivatives.sqexplinGP import sqexplinGP
from gaussianprocessderivatives.gaussianprocess import gaussianprocessException
