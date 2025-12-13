"""
To smooth data and estimate derivatives and their errors.

Covariance functions can either be linear, squared exponential, neural
network-like, or squared exponential with a linear trend.

An example workflow to smooth data (x, y), where the columns of y are
replicates, is

>>> import gaussianprocessderivatives as gp
>>> g= gp.maternGP({0: (-4, 4), 1: (-4, 4), 2: (-4, -2)}, x, y)

The dictionary sets bounds on the hyperparameters, so that 0: (-4, 4) means
that the bounds on the first hyperparameter are 1e-4 and 1e4.

>>> g.info()

explains what each hyperparameter does.

Once g is instantiated,

>>> g.findhyperparameters()
>>> g.results()
>>> g.predict(x, derivs= 2)

optimises the hyperparameters and determines a smoothed version of the data
and estimates the derivatives.

The results can be visualised by

>>> import matplotlib.pylab as plt
>>> plt.figure()
>>> plt.subplot(2,1,1)
>>> g.sketch('.')
>>> plt.subplot(2,1,2)
>>> g.sketch('.', derivs= 1)
>>> plt.show()

and are available as g.f and g.fvar (smoothed data and error), g.df and
g.dfvar (estimate of dy/dx), and g.ddf and g.ddfvar (estimate of d2y/dx2).
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg
from scipy.optimize import minimize

version = "0.1.68"
rng = np.random.default_rng()


class gaussianprocess:
    """
    Optimise and interpolate with a Gaussian process.

    A parent class that requires a child class to specify the
    particular Gaussian process to use.
    """

    def __init__(self, lthbounds, x, y, merrors=None, warnings=True):
        """
        Create a Gaussian process.

        Parameters
        ---------
        lthbounds: dict
            A dictionary of pairs of the bounds on the hyperparameters
            in log10 space, such as {0: [0,6], 1: [-3,4], 2: [-6,-4]}
        x: array
            A 1-D array of the abscissa data, typically times.
        y: array
            A 1-D array of the ordinate data. Any replicates should be strung
            together into a 1-D array.
        merrors: array
            If specified, a 1-d array of the measurement errors
            (assumed to be variances).

        Example
        -------
        For a 1D array of x and a matrix with multiple replicates of y as
        columns, with the values in each row corresponding to a single
        value in x:

        >>> x1 = np.tile(x, y.shape[1])
        >>> y1 = np.reshape(y, np.size(y), order="F")
        >>> g = gp.maternGP(bd, x1, y1)
        """
        x = np.asarray(x)
        y = np.asarray(y)
        if (x.size == 0 or y.size == 0) or (x.shape != y.shape):
            raise gaussianprocessException(
                "x or y is incorrectly initialised."
            )
        else:
            if warnings and len(x) > 1000:
                print(
                    f"GP Warning: large data set - {len(x)} data points"
                    " - may slow optimisation."
                )

            if np.any(np.diff(x) < 0):
                # sort data
                if warnings:
                    print("GP Warning: input data is not sorted. Sorting.")
                y = y[np.argsort(x)]
                x = np.sort(x)
            # store data as attributes
            self.lb = [lthbounds[a] for a in lthbounds.keys()]
            self.x = x
            self.y = y
            self.merrors = merrors
            self.__version__ = version

    def covfn(self):
        """Covariance function."""
        raise NotImplementedError(
            " No covariance function specified"
            + f"in class {self.__class__.__name__}"
        )

    def d1covfn(self):
        """First derivative of covariance function."""
        raise NotImplementedError(
            " No first derivative of the covariance function"
            + f" specified in class {self.__class__.__name__}"
        )

    def d1d2covfn(self):
        """Second derivative of covariance function."""
        raise NotImplementedError(
            " No second derivative of the covariance function"
            + f"specified in class {self.__class__.__name__}"
        )

    def kernelmatrix(self, lth, x):
        """
        Return kernel matrix K(X,X) supplemented with measurement noise.

        Parameters
        ----------
        lth: array
            The log of the hyperparameters.
        x: 1D array
            The abscissa values.

        Returns
        -------
        k: array
            The kernel matrix.
        L: array
            The Cholesky decomposition of the kernel matrix.
        """
        k = np.empty((len(x), len(x)))
        for i in range(len(x)):
            k[i, :] = self.covfn(x[i], x, lth)[0]
        if np.any(self.merrors):
            kn = k + np.exp(lth[-1]) * np.diag(self.merrors)
        else:
            kn = k + np.exp(lth[-1]) * np.identity(len(x))
        try:
            L = linalg.cho_factor(kn)
        except np.linalg.LinAlgError:
            raise gaussianprocessException(
                "Kernel matrix is not positive definite."
            )
        return k, L

    def nlml(self, lth):
        """
        Find the negative of log marginal likelihood.

        Parameters
        ----------
        lth: array
            The log of the hyperparameters.

        Returns
        -------
        nlml: float
            The negative of the log of the marginal likelihood.
        """
        x, y = self.x, self.y
        k, L = self.kernelmatrix(lth, x)
        try:
            al = linalg.cho_solve(L, y)
        except np.linalg.LinAlgError:
            raise gaussianprocessException("Evaluating nlml failed")
        halfdetK = np.sum(np.log(np.diagonal(L[0])))
        nlml = (
            0.5 * np.dot(y, al) + halfdetK + 0.5 * len(y) * np.log(2 * np.pi)
        )
        return nlml

    def jacnlml(self, lth):
        """
        Find the Jacobian of negative log marginal likelihood.

        The Jacobian is calculated with respect to the hyperparameters
        assuming the hyperparmaters are given in log space.

        Parameters
        ----------
        lth: array
            The log of the hyperparameters.

        Returns
        -------
        jac: array
            The Jacobian.
        """
        x, y = self.x, self.y
        k, L = self.kernelmatrix(lth, x)
        # find derivatives of kernel matrix wrt hyperparameters
        kjac = np.empty((len(x), len(x), len(lth)))
        for i in range(len(x)):
            kjac[i, :, :-1] = self.covfn(x[i], x, lth)[1]
        if np.any(self.merrors):
            kjac[:, :, -1] = np.diag(self.merrors) * np.exp(lth[-1])
        else:
            kjac[:, :, -1] = np.identity(len(x)) * np.exp(lth[-1])
        # calculate jacobian
        al = linalg.cho_solve(L, y)
        alal = np.outer(al, al)
        Kinv = linalg.cho_solve(L, np.identity(len(x)))
        jac = np.asarray(
            [
                -0.5 * np.trace(np.dot(alal - Kinv, kjac[:, :, i]))
                for i in range(len(lth))
            ]
        )
        return jac

    def sample_lth(self, lb_e):
        """Sample lth assuming uniform bounded prior."""
        lth = [rng.uniform(lb_e[j][0], lb_e[j][1]) for j in range(len(lb_e))]
        return lth

    def find_initial_parameters(self, lb_e, noinits):
        """Find initial parameters by comparing random guesses."""
        bestnlml = np.inf
        stvals = None
        for k in range(noinits):
            lth = self.sample_lth(lb_e)
            try:
                trialnlml = self.nlml(lth)
                if trialnlml < bestnlml:
                    bestnlml = trialnlml
                    stvals = lth
            except gaussianprocessException:
                pass
        return stvals

    def findhyperparameters(
        self,
        noruns=1,
        noinits=100,
        exitearly=False,
        stvals=False,
        optmethod="L-BFGS-B",
        optmessages=False,
        quiet=True,
        linalgmax=3,
    ):
        """
        Find the best-fit hyperparameters.

        Parameters
        ----------
        noruns: integer
            The number of attempts to find the optimal hyperparameters,
            with the best of all the runs chosen.
        noinits: integer
            The number of attempts to find a good initial condition before
            running the optimisation.
        exitearly: boolean
            If True, fitting stops at the first successful attempt.
        stvals: array, optional
            Initial values for the log hyperparameters.
        optmethod: string
            The optimisation routine to be used by scipy's minimize,
            either 'L-BFGS-B' (default) or 'TNC'.
        optmessages: boolean
            If True, display messages from the optimisation routine.
        quiet: boolean
            If False, print warning if an optimal hyperparameter is at a bound.
        linalgmax: integer, optional
            The number of attempts to make (default is 3) if a linear algebra
            (numerical) error is generated
        """
        self.hparamerr = []
        lmlml = np.full(noruns, np.nan)
        lthf = np.full((noruns, len(self.lb)), np.nan)
        successful_runs = np.full(noruns, False)
        # convert bounds into exponential base
        lb_e = np.array(self.lb) * np.log(10)
        # run optimization
        for i in range(noruns):
            stvals = self.find_initial_parameters(lb_e, noinits)
            linalgerror = 0
            # try multiple times to avoid a linalg error
            while linalgerror < linalgmax:
                try:
                    if np.any(stvals):
                        # initial values given for hyperparameters
                        lth = stvals
                    else:
                        # choose random initial values for hyperparameters
                        lth = self.sample_lth(lb_e)
                    # minimise negative log maximum likelihood
                    res = minimize(
                        self.nlml,
                        x0=lth,
                        method=optmethod,
                        jac=self.jacnlml,
                        bounds=lb_e,
                        options={"disp": optmessages},
                    )
                    successful_runs[i] = res.success
                    if res.success:
                        # optimal theta
                        lthf[i, :] = res.x
                        # negative maximum likelihood
                        lmlml[i] = res.fun
                        # exit loop checking for linalg errors
                        break
                except gaussianprocessException:
                    print(
                        """"
                        Warning: linear algebra error.
                        Trying another initial condition.
                        """
                    )
                    stvals = None
                linalgerror += 1
            if successful_runs[i] is False or np.any(np.isnan(lthf[i, :])):
                print(
                    f" Warning: optimising hyperparameters failed at run {i}."
                )
                # stop optimising initial condition
                noinits = 0
            else:
                if exitearly:
                    break
        if np.any(successful_runs):
            self.store_results(successful_runs, lthf, lmlml, lb_e, quiet)
            self.success = True
        else:
            print("Optimisation of hyperparameters failed.")
            self.success = False

    def store_results(self, successful_runs, lthf, lmlml, lb_e, quiet):
        """Find and store best optimisation result."""
        # find successes
        lmlml = lmlml[successful_runs]
        lthf = lthf[successful_runs, :]
        # find best choice
        lthb = lthf[lmlml.argmin()]
        self.lth_opt = lthb
        self.nlml_opt = lmlml.min()
        # print warning
        for i in range(len(lb_e)):
            if lthb[i] == lb_e[i][1] or lthb[i] == lb_e[i][0]:
                if not quiet:
                    print(f" Warning: hparam[{i}] is at a boundary.")
                    print(
                        f"\thparam[{i}]={np.exp(lthb[i]):e} "
                        f"[{np.exp(lb_e[i][0]):e}, {np.exp(lb_e[i][1]):e}]"
                    )
                if lthb[i] == lb_e[i][1]:
                    self.hparamerr.append([i, "u"])
                else:
                    self.hparamerr.append([i, "l"])

    def results(self, warning=True):
        """
        Display results from optimising hyperparameters.

        Parameters
        --
        warning: boolean
            If True, warn when a hyperparameter hits a boundary.
        """
        if hasattr(self, "success") and self.success:
            print(f"log(max likelihood)= {-self.nlml_opt:e}")
            for j, pv in enumerate(np.exp(self.lth_opt)):
                print(
                    f"hparam[{j}]= {pv:e} [{10 ** self.lb[j][0]:e}, "
                    + f"{10 ** self.lb[j][1]:e}]"
                )
            if warning and hasattr(self, "hparamerr"):
                for el in self.hparamerr:
                    if el[1] == "l":
                        print(
                            f"Warning: hyperparameter {el[0]}"
                            " is at a lower bound."
                        )
                    else:
                        print(
                            f"Warning: hyperparameter {el[0]}"
                            " is at an upper bound."
                        )
        else:
            print("No results.")

    def sample(self, nosamples=1, derivs=0):
        """
        Generate samples from the Gaussian process as an array.

        Parameters
        ----------
        nosamples: integer
            The number of samples.
        derivs: integer, either 0, 1, or 2
            If 0, only the latent function is sampled;
            if 1, the latent function and the first derivative are sampled;
            if 2, the latent function and the first and second derivatives
            are sampled
        """
        try:
            # the values called by predict
            xnew = self.xnew
            ss = np.transpose(
                rng.multivariate_normal(self.mnp, self.covp, nosamples)
            )
            if derivs == 0:
                return ss[: len(xnew), :]
            elif derivs == 1:
                return ss[: len(xnew), :], ss[len(xnew) : 2 * len(xnew), :]
            elif derivs == 2:
                return (
                    ss[: len(xnew), :],
                    ss[len(xnew) : 2 * len(xnew), :],
                    ss[2 * len(xnew) :, :],
                )
        except AttributeError:
            print(" Run gp.predict() before sampling.")

    def sampleprior(self, size=1, lth=None):
        """
        Generate samples from the prior of the Gaussian process as an array.

        Parameters
        ----------
        size: integer
            The number of samples.
        lth: array, optional
            The log hyperparameters to use.
            If unspecified, the hyperparameters are chosen at random and
            uniformly between their bounds.

        Returns
        -------
        samples: array
            An array with each row a sample.
        """
        x, lb = self.x, self.lb
        if np.any(lth):
            # hyperparameters are given (measurement error is not necessary)
            if len(lth) == self.noparams:
                lth = np.concatenate((lth, [1.0]))
        else:
            # sample random hyperparameters
            lth = np.log(
                np.power(
                    10,
                    [rng.uniform(lb[i][0], lb[i][1]) for i in range(len(lb))],
                )
            )
        cov = self.kernelmatrix(lth, x)[0]
        samples = np.transpose(
            rng.multivariate_normal(np.zeros(len(x)), cov, size)
        )
        return samples

    def find_kv_km(self, x, xnew, derivs):
        """Find kv (1D) and km (2D), defined in Eq 16 and used to predict."""
        lth = self.lth_opt
        Knewold = np.empty((len(xnew), len(x)))
        Knewnew = np.empty((len(xnew), len(xnew)))
        if derivs > 0:
            d1Knewold = np.empty((len(xnew), len(x)))
            d1Knewnew = np.empty((len(xnew), len(xnew)))
            d1d2Knewnew = np.empty((len(xnew), len(xnew)))
        if derivs > 1:
            d12Knewold = np.empty((len(xnew), len(x)))
            d12Knewnew = np.empty((len(xnew), len(xnew)))
            d12d2Knewnew = np.empty((len(xnew), len(xnew)))
            d12d22Knewnew = np.empty((len(xnew), len(xnew)))
        for i in range(len(xnew)):
            Knewold[i, :] = self.covfn(xnew[i], x, lth)[0]
            Knewnew[i, :] = self.covfn(xnew[i], xnew, lth)[0]
            if derivs > 0:
                d1Knewold[i, :] = self.d1covfn(xnew[i], x, lth)[0]
                d1Knewnew[i, :] = self.d1covfn(xnew[i], xnew, lth)[0]
                d1d2Knewnew[i, :] = self.d1d2covfn(xnew[i], xnew, lth)[0]
            if derivs > 1:
                d12Knewold[i, :] = self.d12covfn(xnew[i], x, lth)[0]
                d12Knewnew[i, :] = self.d12covfn(xnew[i], xnew, lth)[0]
                d12d2Knewnew[i, :] = self.d12d2covfn(xnew[i], xnew, lth)[0]
                d12d22Knewnew[i, :] = self.d12d22covfn(xnew[i], xnew, lth)[0]
        if derivs == 0:
            kv = Knewold
            km = Knewnew
        elif derivs == 1:
            kv = np.bmat([[Knewold], [d1Knewold]])
            km = np.bmat(
                [
                    [Knewnew, np.transpose(d1Knewnew)],
                    [d1Knewnew, d1d2Knewnew],
                ]
            )
        elif derivs == 2:
            kv = np.bmat([[Knewold], [d1Knewold], [d12Knewold]])
            km = np.bmat(
                [
                    [
                        Knewnew,
                        np.transpose(d1Knewnew),
                        np.transpose(d12Knewnew),
                    ],
                    [
                        d1Knewnew,
                        d1d2Knewnew,
                        np.transpose(d12d2Knewnew),
                    ],
                    [d12Knewnew, d12d2Knewnew, d12d22Knewnew],
                ]
            )
        return kv, km

    def predict(self, xnew, derivs, addnoise=False, merrorsnew=False):
        """
        Determine the predicted mean latent function and its derivatives.

        Arguments
        --
        xnew: array
            Abscissa values for which predicted ordinate values are desired.
        derivs: integer
            If 0, only the latent function is inferred;
            if 1, the latent function and the first derivative are inferred;
            if 2, the latent function and the first and second derivatives
            are inferred
        addnoise: boolean
            If True, add measurement noise to the predicted variance.
        merrorsnew: array, optional
            If addnoise is True, the expected measurements errors at xnew.
            Do not define if xnew = x.
        """
        if self.success:
            # work with an array of length 3*N:
            # the first N values being the function,
            # the second N values being the first derivative,
            # and the last N values being the second derivative
            xnew = np.asarray(xnew)
            if np.array_equiv(self.x, xnew):
                xold = True
            else:
                xold = False
            if np.any(self.merrors) and not np.any(merrorsnew) and not xold:
                print("Length of xnew is different from x.")
                raise gaussianprocessException(
                    "Measurement errors were used to find the hyperparameters."
                    "\nThey are also required for any predictions."
                )
            else:
                # set up
                self.xnew = xnew
                lth, x, y = self.lth_opt, self.x, self.y
                kv, km = self.find_kv_km(x, xnew, derivs)
                # find mean prediction
                k, L = self.kernelmatrix(lth, x)
                m = np.dot(kv, linalg.cho_solve(L, y))
                # mnp is the the mean latent function and its mean derivatives
                mnp = np.reshape(np.array(m), np.size(m))
                self.mnp = mnp
                # find covariance matrix of predictions
                covp = km - np.dot(kv, linalg.cho_solve(L, np.transpose(kv)))
                self.covp = covp
                varp = np.diag(covp)
                # mean latent function
                self.f = mnp[: len(xnew)]
                fvar = varp[: len(xnew)]
                if addnoise:
                    # add measurement error to the latent function's variance
                    if np.any(self.merrors):
                        if xold:
                            self.fvar = fvar + np.exp(lth[-1]) * self.merrors
                        elif np.any(merrorsnew):
                            self.fvar = fvar + merrorsnew
                        else:
                            raise gaussianprocessException(
                                " Measurement errors for new x values must be"
                                " specified."
                            )
                    else:
                        self.fvar = fvar + np.exp(lth[-1]) * np.ones(len(xnew))
                else:
                    # just take the variance of the latent function
                    self.fvar = fvar
                if derivs > 0:
                    self.df = mnp[len(xnew) : 2 * len(xnew)]
                    self.dfvar = varp[len(xnew) : 2 * len(xnew)]
                if derivs > 1:
                    self.ddf = mnp[2 * len(xnew) :]
                    self.ddfvar = varp[2 * len(xnew) :]
        else:
            raise gaussianprocessException(
                "There are no optimised hyperparameters."
            )

    def batchpredict(
        self, xnew, merrorsnew=False, derivs=0, addnoise=False, maxlen=1000
    ):
        """
        Run batch predictions to increase speed and reduce memory.

        Note that you must run predict not batchpredict if you wish to
        generate samples from the Gaussian process.

        Arguments
        --
        xnew: array
            Abscissa values for which predicted ordinate values are desired.
        merrorsnew: array, optional
            If specified, the expected measurements errors at xnew
            (should not be defined if xnew = x).
        derivs: integer
            If 0, only the latent function is inferred;
            if 1, the latent function and the first derivative are inferred;
            if 2, the latent function and the first and second derivatives
            are inferred
        addnoise: boolean
            If True, add measurement noise to the predicted variance.
        maxlen: integer
            The number of data points to process in batches (default: 1000).
        """
        if len(xnew) < maxlen:
            self.predict(xnew, merrorsnew, derivs, addnoise)
        else:
            f = np.zeros(len(xnew))
            fvar = np.zeros(len(xnew))
            if derivs > 0:
                df = np.zeros(len(xnew))
                dfvar = np.zeros(len(xnew))
            if derivs > 1:
                ddf = np.zeros(len(xnew))
                ddfvar = np.zeros(len(xnew))
            bs = np.append(np.arange(0, len(xnew), maxlen), len(xnew) + 1)
            for i in range(1, len(bs)):
                self.predict(
                    xnew[bs[i - 1] : bs[i]], merrorsnew, derivs, addnoise
                )
                f[bs[i - 1] : bs[i]] = self.f
                fvar[bs[i - 1] : bs[i]] = self.fvar
                if derivs > 0:
                    df[bs[i - 1] : bs[i]] = self.df
                    dfvar[bs[i - 1] : bs[i]] = self.dfvar
                if derivs > 1:
                    ddf[bs[i - 1] : bs[i]] = self.ddf
                    ddfvar[bs[i - 1] : bs[i]] = self.ddfvar
            self.f = f
            self.fvar = fvar
            if derivs > 0:
                self.df = df
                self.dfvar = dfvar
            if derivs > 1:
                self.ddf = ddf
                self.ddfvar = ddfvar

    def sketch(self, datasymbol="o", derivs=0, GPcolor="blue", nostds=2):
        """
        Plot data with the mean prediction.

        A lighter band shows the errors as a multiple of the standard deviation.

        Parameters
        ----------
        datasymbol: string
            The symbol used to mark the data points.
            If None, no data points are plotted.
        derivs: integer
            If 0, plot data and mean prediction;
            if 1, plot first derivative with respect to x;
            if 2, plot second derivative.
        GPcolor: string
            The color used to draw the mean and standard deviation of the
            Gaussian process.
        nostds: float
            The number of standard deviations to use as errorbars.
        """
        if hasattr(self, "xnew"):
            x, y, xnew = self.x, self.y, self.xnew
            if derivs == 0:
                f = self.f
                sd = np.sqrt(self.fvar)
                if datasymbol:
                    plt.plot(x, y, "r" + datasymbol)
            elif derivs == 1:
                f = self.df
                sd = np.sqrt(self.dfvar)
            elif derivs == 2:
                f = self.ddf
                sd = np.sqrt(self.ddfvar)
            else:
                print("sketch: error in derivs.")
            plt.plot(xnew, f, color=GPcolor)
            plt.fill_between(
                xnew,
                f - nostds * sd,
                f + nostds * sd,
                facecolor=GPcolor,
                alpha=0.2,
            )
        else:
            print("You must run gp.predict() first.")


class gaussianprocessException(Exception):
    """Custom error class."""

    __doc__ = ""
    pass
