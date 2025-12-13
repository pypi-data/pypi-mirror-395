""" Tool to simulate the accuracy of the QuanTI-FRET autocalibration with
different spreading of fret and stochiometry values

It generates multiple experiment with differents values of deltaE and deltaS,
computes the errors of values estimated by Quanti-Fret with autocalibration,
and the theoretical values, and plot the results.

You can run the simulation using the parameters you can find in
SimulationParameters or you can specify the parameters in the command line.
For example to generate 20 deltaE between 0.01 and 0.1, and 20 deltaS between
0.05 and 0.45, run:
```
python simulation.py -e 0.01 0.1 20 -s 0.05 0.45 20
```

The tool also come with a mode that plot the intensities in a 3D plot for a
single Experiment, alongside the computed and theoretical 3D plane. For example
to generate the plane for a deltaE of 0.06, and deltaS of 0.1, run:
```
python simulation.py single -e 0.06 -s 0.1
```
"""

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import scipy
from tqdm import tqdm

from quanti_fret.algo.matrix_functions import clean_mask, gamma_xm
from quanti_fret.algo.plot import PlotGenerator
from quanti_fret.algo.xm import XMCalculator


class SimulationParameters:
    """ Default values for the simulation of multiple experiements
    """
    e_0 = 0.4
    e_delta_steps = 5
    e_delta_min = 0.05
    e_delta_max = 0.1
    e_bins = 10

    s_0 = 0.5
    s_delta_steps = 5
    s_delta_min = 0.01
    s_delta_max = 0.1

    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """ Convert the parameter to a dictionary

        Returns:
            dict[str, Any]: parameters in dictionary
        """
        return {
            'e_0': cls.e_0,
            'e_delta_steps': cls.e_delta_steps,
            'e_delta_min': cls.e_delta_min,
            'e_delta_max': cls.e_delta_max,
            'e_bins': cls.e_bins,
            's_0': cls.s_0,
            's_delta_steps': cls.s_delta_steps,
            's_delta_min': cls.s_delta_min,
            's_delta_max': cls.s_delta_max,
        }


class ExperimentsParameters:
    """ Defaults values for a single experiment
    """
    # excitation intensities (ph/µm2/s)
    La = 1e11
    Ld = 2e11
    # section efficace absorption (µm2): molecule (a/d) - excitation band (a/d)
    sigma_aa = 1e-8
    sigma_dd = 1e-8
    sigma_ad = 1e-9
    # quantum yield
    phi_a = 0.7
    phi_d = 0.4
    # detection efficiency : emission spectrum(a/d) - detection band(a/d)
    eta_aa = 0.1
    eta_dd = 0.1
    eta_da = 0.02
    # typical fluorophore number in a pixel
    donors_mean_per_pixel = 10.
    # image dimension
    img_width = 1024

    @classmethod
    def gamma_m(cls) -> float:
        """ Compute the GammaM matching the experiment parameters

        Returns:
            float: GammaM
        """
        return (cls.phi_a * cls.eta_aa) / (cls.phi_d * cls.eta_dd)

    @classmethod
    def beta_x(cls) -> float:
        """ Compute the BetaX matching the experiment parameters

        Returns:
            float: BetaX
        """
        return (cls.La * cls.sigma_aa) / (cls.Ld * cls.sigma_dd)

    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """ Convert the parameter to a dictionary

        Returns:
            dict[str, Any]: parameters in dictionary
        """
        return {
            'La': cls.La,
            'la_scientific': f'{cls.La:0.1e}',
            'Ld': cls.Ld,
            'ld_scientific': f'{cls.Ld:0.1e}',
            'sigma_aa': cls.sigma_aa,
            'sigma_dd': cls.sigma_dd,
            'sigma_ad': cls.sigma_ad,
            'phi_a': cls.phi_a,
            'phi_d': cls.phi_d,
            'eta_aa': cls.eta_aa,
            'eta_dd': cls.eta_dd,
            'eta_da': cls.eta_da,
            'gamma_m': cls.gamma_m(),
            'beta_x': cls.beta_x(),
            'donors_mean_per_pixel': cls.donors_mean_per_pixel,
            'img_width': cls.img_width,
        }


class Experiment:
    """ Generate an experiement with given parameters

    To generate an experiment we use the ExperimentsParameters values for the
    physical constraints. Then we:
        * Generate the nb_donors matrix containing the value of donors per
            pixel (using a laplace distribution troncated on ]o, inf])
        * Generate a Stochiometry matrix for each pixels (by default using
            a uniform distribution between min and max value for S)
        * From donors and acceptors, we generate the nb_acceptors matrix
            containing the number of acceptors per pixels
        * Generate the fret matrix E. We split the rows in e_bins
            subset, for each of them, we fix the fret to a linear distribution
            between fret min and fret max
        * From all these generated matrices, and the physical values, we
            generate the different intensities matrices, then we apply a
            poisson noise to them.

    All matrices generated are squares of width ExperimentsParameters.img_width
    """
    def __init__(self) -> None:
        """ Construtor
        """
        self.EP = ExperimentsParameters
        self.rng = np.random.default_rng()
        self._I_DD: np.ndarray | None = None
        self._I_DA: np.ndarray | None = None
        self._I_AA: np.ndarray | None = None
        self._E: np.ndarray | None = None
        self._S: np.ndarray | None = None
        self.e_delta: float = 0
        self.s_delta: float = 0

    @property
    def I_DD(self) -> np.ndarray:
        assert self._I_DD is not None
        return self._I_DD

    @property
    def I_DA(self) -> np.ndarray:
        assert self._I_DA is not None
        return self._I_DA

    @property
    def I_AA(self) -> np.ndarray:
        assert self._I_AA is not None
        return self._I_AA

    @property
    def E(self) -> np.ndarray:
        assert self._E is not None
        return self._E

    @property
    def S(self) -> np.ndarray:
        assert self._S is not None
        return self._S

    def generate(
        self, e_0: float, e_delta: float, e_bins: int, s_0: float,
        s_delta: float
    ) -> None:
        """ Generate the experiement that match the parameters given.

        It creates E, S, I_DD, I_DA, I_AA matrices matching the parameters
        given, and the physical constraints.

        For more details on how they are computed, see the class description.

        Args:
            e_0 (float): Median fret value to generate distribution arround
            e_delta (float): Maximum distance accepted from e_0 to generate the
                distribution of fret values
            e_bins (int): Number of different values E will take (between
                e_0 - e_delta and e_0 + e_delta)
            s_0 (float): Median stochiometry value to generate distribution
                arround
            s_delta (float): Maximum distance accepted from e_0 to generate the
                distribution of stochiometry values
        """
        # Generate experience
        nb_donors = self._generate_donors()
        S = self._generate_stochio_uniform(s_0, s_delta)
        nb_acceptors = self._generate_acceptors(nb_donors, S)
        E = self._generate_fret(e_0, e_delta, e_bins)
        I_DD, I_DA, I_AA = self._compute_intensities(
            E, nb_donors, nb_acceptors
        )

        self._I_DD = I_DD
        self._I_DA = I_DA
        self._I_AA = I_AA
        self._E = E
        self._S = S
        self.e_delta = e_delta
        self.s_delta = s_delta

    def _generate_donors(self) -> np.ndarray:
        """ Generate the matrix containing the number of donors per pixels

        The generation is performed using a laplace distribution arround 0 that
        is trunked to keep only positive values.

        Returns:
            np.ndarray: The matrix of size containing the number of donors
                per pixels
        """
        donors_mean_per_pixel = self.EP.donors_mean_per_pixel
        N = self.EP.img_width
        loc = 0.
        # We generate more than twice the values to keep only N*N positive
        # values.
        s = self.rng.laplace(loc, donors_mean_per_pixel, 2*N*N + 5000)
        ind = np.nonzero(s >= 0)
        indices = ind[0][0:N*N]
        nb_donors = np.reshape(s[indices], (N, N))
        return nb_donors

    def _generate_stochio_uniform(
        self, s_0: float, delta: float
    ) -> np.ndarray:
        """ Generate the stochiometry matrix using a uniform distribution
        between s_0 - delta / 2 and s_0 + delta / 2

        Args:
            s_0 (float): Median value of the distribution
            delta (float): Size of the interval arround s_0

        Returns:
            np.ndarray: The stochiometry matrix per pixels
        """
        N = self.EP.img_width
        S = self.rng.uniform(s_0 - delta / 2, s_0 + delta / 2, (N, N))
        return S

    def _generate_stochio_normal(self, s_0: float, delta: float) -> np.ndarray:
        """ Generate the stochiometry matrix using a normal distribution
        arround s_0 with a sigma = delta / 4.

        The distribution is truncated between  s_0 - delta / 2 and
        s_0 + delta / 2 to avoid extreme values (S = 0 or S = 1)

        Args:
            s_0 (float): Median value of the distribution
            delta (float): Size of the interval arround s_0

        Returns:
            np.ndarray: The stochiometry matrix per pixels
        """
        N = self.EP.img_width
        sigma = delta / 4
        S_min = s_0 - delta / 2
        S_max = s_0 + delta / 2
        mean = s_0
        a, b = (S_min - mean) / sigma, (S_max - mean) / sigma
        S = scipy.stats.truncnorm.rvs(a, b, loc=s_0, scale=sigma, size=(N, N))
        assert isinstance(S, np.ndarray)
        return S

    def _generate_stochio_from_acceptors(
        self, nb_donors: np.ndarray, nb_acceptors: np.ndarray
    ) -> np.ndarray:
        """ Generate the stochiometry matrix using the donors and accpetors
        matrices

        S = nb_donors / (nb_acceptors + nb_donors)

        Args:
            nb_donors (np.ndarray): Number of donors per pixels
            nb_acceptors (np.ndarray): Number of acceptors per pixels

        Returns:
            np.ndarray: The stochiometry matrix per pixels
        """
        S = nb_donors / (nb_donors + nb_acceptors)
        return S

    def _generate_acceptors(
        self, nb_donors: np.ndarray, S: np.ndarray
    ) -> np.ndarray:
        """ Generate the matrix containing the number of acceptors per pixel.

        This generation uses the number of donors per pixels, and the
        stochiometry per pixels, with the formula:
        nb_acceptors = (1-S) / S * nb_donnors

        Args:
            nb_donors (np.ndarray): Number of donors per pixel
            S (np.ndarray): Stochiometry per pixels

        Returns:
            np.ndarray: The matrix of size containing the number of acceptors
                per pixels
        """
        np.seterr(divide='ignore', invalid='ignore')
        nb_acceptors = ((1 - S) / S) * nb_donors
        np.seterr(divide='warn', invalid='warn')
        nb_acceptors[nb_acceptors == np.inf] = 0.

        return nb_acceptors

    def _generate_acceptors_realistic(
        self, nb_donors: np.ndarray, s_0: float, s_delta: float
    ) -> np.ndarray:
        """ Generate the matrix containing the number of acceptors per pixel,
        with the idea to have an equivalent number of donors and acceptors
        in total.

        In order to do so, we compute for each pixels the number of acceptors
        possible to stay in s_0 - s_delta / 2 and s_0 + s_delta / 2. Then we
        take the same distribution that generated the donors, but we truncate
        it to the given interval, and we chose a number of acceptors that
        follows this constraint distribution

        Args:
            nb_donors (np.ndarray): Number of donors per pixel
            s_0 (float): Median value of the stochiometry distribution
            delta (float): Size of the interval arround s_0
        Returns:
            np.ndarray: The matrix of size containing the number of acceptors
                per pixels
        """
        # Compute the range of accepted values
        # S_max_diff = nb_donors - nb_acceptors_for_s_max (> 0)
        # Using S_max = nb_donors / (nb_donors + nb_acceptors_fo_s_max)
        # We get S_max_diff = nb_donors * (2 - (1 / S_max))
        # Same apply for S_min_diff
        S_max = s_0 + s_delta / 2
        S_min = s_0 - s_delta / 2
        S_max_diff = nb_donors * (2 - (1 / S_max))
        S_min_diff = nb_donors * ((1 / S_min) - 2)

        # Generate acceptors
        acceptors_min = nb_donors - S_max_diff
        acceptors_max = nb_donors + S_min_diff
        cdf_a = scipy.stats.laplace.cdf(acceptors_min, loc=0,
                                        scale=self.EP.donors_mean_per_pixel)
        cdf_b = scipy.stats.laplace.cdf(acceptors_max, loc=0,
                                        scale=self.EP.donors_mean_per_pixel)
        u = self.rng.uniform(cdf_a, cdf_b)
        nb_acceptors = scipy.stats.laplace.ppf(
            u, loc=0, scale=self.EP.donors_mean_per_pixel
        )

        return nb_acceptors

    def _generate_fret(
        self, e_0: float, delta: float, bins: int
    ) -> np.ndarray:
        """ Generate the fret matrix E for each pixel.

        To generate the fret matrix, we split it into `bins` set of rows. All
        pixel from a set will be assigned to a same value. The values for each
        set are chosen using evenly spaced numbers between e_0 - delta / 2 and
        e_0 + delta / 2

        Args:
            e_0 (float): Median fret value to generate distribution arround
            e_delta (float): Size of the interval arround e_0 in which to
                generate the distribution of fret values
            bins (int): Number of different values E will take (between
                e_0 - e_delta / 2 and e_0 + e_delta / 2)

        Returns:
            np.ndarray: The Fret per pixels Matrix
        """
        N = self.EP.img_width
        e_min = max(0.0, e_0 - delta / 2)
        e_max = min(1.0, e_0 + delta / 2)
        E = np.full((N, N), e_min)
        w = int(np.fix(N / bins))
        for i in range(bins):
            E[N-(i+1)*w:N-i*w, :] = e_max - (i * (e_max-e_min) / (bins-1))
        return E

    def _compute_intensities(
        self, E: np.ndarray, nb_donors: np.ndarray, nb_acceptors: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """ Compute the DD, DA, and AA intensities matrices

        The intensities are computed using the donors, acceptors and Fret
        matrices in addition of the physical parameters of the experiements.
        For more realism, we add a poisson noise the the intensities.

        Args:
            E (np.ndarray): Fret matrix per pixel
            nb_donors (np.ndarray): Donors per pixels
            nb_acceptors (np.ndarray): Acceptors per pixels

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray]: I_DD, I_DA, and I_AA
                intensities per pixels
        """
        # Get parameters
        La = self.EP.La
        Ld = self.EP.Ld
        sigma_aa = self.EP.sigma_aa
        sigma_dd = self.EP.sigma_dd
        phi_a = self.EP.phi_a
        phi_d = self.EP.phi_d
        eta_aa = self.EP.eta_aa
        eta_dd = self.EP.eta_dd

        # Compute intensities
        I_AA_i = nb_acceptors * La * sigma_aa * phi_a * eta_aa
        I_DD_i = nb_donors * Ld * sigma_dd * (1 - E) * phi_d * eta_dd
        I_DA_i = nb_donors * Ld * sigma_dd * E * phi_a * eta_aa

        # Add noise
        I_AA = self.rng.poisson(lam=I_AA_i)
        I_AA[I_AA <= 0] = 0
        I_DD = self.rng.poisson(lam=I_DD_i)
        I_DD[I_DD <= 0] = 0
        I_DA = self.rng.poisson(lam=I_DA_i)
        I_DA[I_DA <= 0] = 0

        return I_DD, I_DA, I_AA


class Analyser:
    """ Class to perform analysis on an experiments.

    It allows tools to
        * computes the GammaM and BetaX values that would return the
            QuanTI-FRET algorithm.
        * compute the error between the computed values and the theoretical
            ones for GammaM, BetaX ans E.
        * ot the 3D graph of the intensities, alongside the computed and
            theoretical plane defined by GammaM and BetaX
    """

    def __init__(self, exp: Experiment) -> None:
        """ Constructor

        Args:
            exp (Experiment): Experiment to analyze
        """
        self.exp = exp
        self.mask: np.ndarray | None = None

        self.beta_x = float('inf')
        self.gamma_m = float('inf')

        self._beta_x_t = ExperimentsParameters.beta_x()
        self._gamma_m_t = ExperimentsParameters.gamma_m()

    def xm(self, plot_details: bool = False) -> None:
        """ Compute BetaX and GammaM values using the QuanTI-FRET algorithm.

        Args:
            plot_details (bool, optional): If True, plot in 3D all the
                intensities alongside the computed and theoretical plane.
                Defaults to False.
        """
        exp = self.exp
        triplet = np.stack((exp.I_DD, exp.I_DA, exp.I_AA), axis=0)
        mask = np.full(exp.I_AA.shape, True)

        mask = clean_mask(mask, triplet, triplet)

        triplet = triplet[:, mask]

        self.beta_x, self.gamma_m, _, _ = gamma_xm(
            triplet[0], triplet[1], triplet[2]
        )

        self.mask = mask

        if plot_details:
            self._plot_plane()

    def get_xm_deviations(
        self
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """ Compute the error of GammaM and BetaX computed compare to their
        Theoretical values.

        Error are returned in absolute and relative compare to the théoretical
        value

        Returns:
            tuple[tuple[float, float], tuple[float, float]]: [
                [GammaM absolute error, GammaM relative error]
                [BetaX absolute error, BetaX relative error]
            ]
        """
        assert self.gamma_m != float('inf')
        assert self.beta_x != float('inf')

        # Deviation for GammaM
        delta_gamma_m_abs = abs(self.gamma_m - self._gamma_m_t)
        delta_gamma_m_rel = delta_gamma_m_abs / self._gamma_m_t * 100
        delta_gamma_m = (delta_gamma_m_abs, delta_gamma_m_rel)

        # Deviation for BetaX
        delta_beta_x_abs = abs(self.beta_x - self._beta_x_t)
        delta_beta_x_rel = delta_beta_x_abs / self._beta_x_t * 100
        delta_beta_x = (delta_beta_x_abs, delta_beta_x_rel)

        return delta_gamma_m, delta_beta_x

    def get_E_deviations(
        self
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """ Compute the error of the Fret computed using GammaM returned by
        QuanTI-FRET compare to the one computed using the theoretical gammaM

        The error returned is the median of all the errors for each pixels

        The error is returned in absolute and relative compare to the
        theoretical value. It also return the standard deviation in absolute
        and relative.

        Returns:
            tuple[tuple[float, float], tuple[float, float]]: [
                [E median absolute error, E median relative error]
                [E std absolute error, E std relative error]
            ]
        """
        assert self.gamma_m != float('inf')
        assert self.beta_x != float('inf')

        # Compute E estimated
        I_DA = self.exp.I_DA[self.mask]
        I_DD = self.exp.I_DD[self.mask]
        gamma_m = self.gamma_m
        E_estimated = I_DA / (I_DA + gamma_m * I_DD)

        # Compute errors
        # E_real = self.exp.E[self.mask]
        E_real = I_DA / (I_DA + self._gamma_m_t * I_DD)
        delta_E_abs_matrix = np.abs(E_real - E_estimated)
        delta_E_rel_matrix = delta_E_abs_matrix / E_real * 100

        # Compute Median error
        delta_E_abs_median = float(np.median(delta_E_abs_matrix))
        delta_E_rel_median = float(np.median(delta_E_rel_matrix))
        delta_E_median = (delta_E_abs_median, delta_E_rel_median)

        # Compute Relative Error
        delta_E_abs_std = float(np.std(delta_E_abs_matrix))
        delta_E_rel_std = float(np.std(delta_E_rel_matrix))
        delta_E_std = (delta_E_abs_std, delta_E_rel_std)

        return delta_E_median, delta_E_std

    def _plot_plane(self) -> None:
        """ Plot the Intensities in 3D with the theoretical and computed plane.

        The intensities are plot with:
            X: I_DD
            Y: I_DA
            Z: I_AA

        The planes are the one solving the equation:
        GammaM * BetaX * I_DD + BetaX * I_DA = S
        """
        assert self.gamma_m != float('inf')
        assert self.beta_x != float('inf')

        # Prepare data and compute mask
        beta_x = self.beta_x
        gamma_m = self.gamma_m
        I_DD_f = self.exp.I_DD.flatten()
        I_DA_f = self.exp.I_DA.flatten()
        I_AA_f = self.exp.I_AA.flatten()
        xmc = XMCalculator()
        mask = xmc._3d_plot_mask(I_AA_f)
        # mask = np.full(I_AA_f.shape, True)
        I_DD_fm = I_DD_f[mask]
        I_DA_fm = I_DA_f[mask]
        I_AA_fm = I_AA_f[mask]

        # Plot the 3D points
        plot = PlotGenerator(use_plt=True)
        fig = plot.scatterplot_3d(
            'I_DD', I_DD_fm, 'I_DA', I_DA_fm, 'I_AA', I_AA_fm,
            (beta_x * gamma_m, beta_x),
            title=f'DeltaE = {self.exp.e_delta} / SigmaS = {self.exp.s_delta}'
        )

        # Add real plane
        X = np.linspace(I_DD_fm.min(), I_DD_fm.max(), 200)
        Y = np.linspace(I_DA_fm.min(), I_DA_fm.max(), 200)
        X, Y = np.meshgrid(X, Y)
        Z = self._beta_x_t * self._gamma_m_t * X + self._beta_x_t * Y
        fig.axes[0].plot_wireframe(  # type: ignore
            X, Y, Z, linewidth=0.2, rstride=5, cstride=5, color='purple'
        )

        # Show figure
        fig.canvas.mpl_connect('key_press_event', self._on_press)
        plt.show()
        plt.close()

    def _on_press(self, event: Any) -> None:
        """ Quit the program when Q is pressed

        Args:
            event (Any): The event caught
        """
        plt.close()
        if event.key == 'q':
            plt.close()
            sys.exit(0)


class Simulation:
    """ Main class of the simulation, it creates as many experiments as
    required, concatenate the errors and plot the results
    """
    def __init__(
        self, output_path: Path, plot_details: bool = False,
        geomspace: bool = False, no_progress: bool = False
    ) -> None:
        """ Constructor

        Args:
            output_path (Path): Folder xhere to store the results
            plot_details (bool, optional): Plot the 3D plane of every
                experiments. Defaults to False.
            geomspace (bool, optional): Use geomspace instead of linspace to
                create the delta E and delta S interval. Defaults to False.
            no_progress (bool, optional): Disable progress bar. Defaults to
                False.
        """
        self.params = SimulationParameters
        self._output_path = Path(output_path)
        self._plot_details = plot_details
        self._no_progress = no_progress
        self.space: Callable[[float, float, int], np.ndarray]
        if geomspace:
            self.space = np.geomspace
        else:
            self.space = np.linspace
        self._output_path.mkdir(exist_ok=True, parents=True)
        self._intensity_samples = 5

    def generate(self) -> None:
        """ Generate the simulation data.

        The simulation works as the following:
        It generates:
            * e_delta_steps values for e_delta between e_delta_min, and
                e_delta_max
            * s_delta_steps values for s_delta between s_delta_min, and
                s_delta_max
        For each couple (e_delta, s_delta):
            * It generate an experiment
            * It computes it's GammaM and BetaX values
            * It computes their error to their theoretical values
            * It computes the Fret error to its theoretical values
            * It stores all the errors into matrices with e_delta for the x
                axis, and s_delta for the y axis
        It also extract the intensity matrices of 5 experiments (take the most
        cental value the one in the 4 diagonals)

        All results are stored for future modifications on the plots.
        """
        # Retrieve parameters
        e_0 = self.params.e_0
        e_bins = self.params.e_bins
        s_0 = self.params.s_0
        e_delta_range = (self.params.e_delta_min, self.params.e_delta_max)
        e_delta_steps = self.params.e_delta_steps
        s_delta_range = (self.params.s_delta_min, self.params.s_delta_max)
        s_delta_steps = self.params.s_delta_steps

        # Instanciate results heatmaps
        heatmap_shape = (2, s_delta_steps, e_delta_steps)
        self.heatmap_gamma_m = np.zeros(heatmap_shape)
        self.heatmap_beta_x = np.zeros(heatmap_shape)
        self.heatmap_e_median = np.zeros(heatmap_shape)
        self.heatmap_e_std = np.zeros(heatmap_shape)

        # Prepare the matrices that will store the 5 chosen experiment
        # intensities and prepare the intensity_indexes that will be used to
        # select them.
        # To select the experiment, we choose the pixel in the middle, and the
        # 4 pixel closest on each diagonal.
        ci = (int(s_delta_steps / 2), int(e_delta_steps / 2))
        intensity_indexes = [
            (ci[0] + i, ci[1] + j) for i in [-1, 0, 1] for j in [-1, 0, 1]
            if not ((i == 0) ^ (j == 0))
        ]
        width = ExperimentsParameters.img_width
        self.idd_samples = np.zeros((self._intensity_samples, width, width))
        self.ida_samples = np.zeros((self._intensity_samples, width, width))
        self.iaa_samples = np.zeros((self._intensity_samples, width, width))
        intensity_index = 0

        # Create steps intervals
        self.e_deltas = self._generate_interval(e_delta_range, e_delta_steps)
        self.s_deltas = self._generate_interval(s_delta_range, s_delta_steps,
                                                True)

        # Simulate one experiment for each couple e_delta / s_delta
        for i_s in tqdm(range(self.s_deltas.size), leave=False,
                        disable=self._no_progress):
            s_delta = self.s_deltas[i_s]
            for i_e in tqdm(range(self.e_deltas.size), leave=False,
                            disable=self._no_progress):
                e_delta = self.e_deltas[i_e]

                # Create the experiment and compute GammaM and BetaX
                exp = Experiment()
                ana = Analyser(exp)
                exp.generate(e_0, e_delta, e_bins, s_0, s_delta)
                ana.xm(self._plot_details)

                # Get GammaM and BetaX errors
                delta_gamma_m, delta_beta_x = ana.get_xm_deviations()
                self.heatmap_gamma_m[0, i_s, i_e] = delta_gamma_m[0]
                self.heatmap_gamma_m[1, i_s, i_e] = delta_gamma_m[1]
                self.heatmap_beta_x[0, i_s, i_e] = delta_beta_x[0]
                self.heatmap_beta_x[1, i_s, i_e] = delta_beta_x[1]

                # Get Fret errors
                delta_E_median, delta_E_std = ana.get_E_deviations()
                self.heatmap_e_median[0, i_s, i_e] = delta_E_median[0]
                self.heatmap_e_median[1, i_s, i_e] = delta_E_median[1]
                self.heatmap_e_std[0, i_s, i_e] = delta_E_std[0]
                self.heatmap_e_std[1, i_s, i_e] = delta_E_std[1]

                # Get Intensities
                if (i_s, i_e) in intensity_indexes:
                    self.idd_samples[intensity_index] = exp.I_DD
                    self.ida_samples[intensity_index] = exp.I_DA
                    self.iaa_samples[intensity_index] = exp.I_AA
                    intensity_index += 1

        self.save_results()

    def save_results(self) -> None:
        """ Save the results of the simulation.

        The purpose is to generate report file describings the settings used
        and to save any data that would allow us to regenerate the plots
        """
        # Save simulation results
        output_dir = self._output_path / 'data'
        output_dir.mkdir(exist_ok=True, parents=True)
        self.heatmap_gamma_m.dump(output_dir / 'gamma.npy')
        self.heatmap_beta_x.dump(output_dir / 'beta.npy')
        self.heatmap_e_median.dump(output_dir / 'e_median.npy')
        self.heatmap_e_std.dump(output_dir / 'e_std.npy')
        self.e_deltas.dump(output_dir / 'e_deltas.npy')
        self.s_deltas.dump(output_dir / 's_deltas.npy')

        # Save intensities
        self.idd_samples.dump(output_dir / 'idd.npy')
        self.ida_samples.dump(output_dir / 'ida.npy')
        self.iaa_samples.dump(output_dir / 'iaa.npy')

        # Save simulation report
        report = {}
        exp = ExperimentsParameters.as_dict()
        simu = SimulationParameters.as_dict()
        report['parameters'] = {
            'experiments': exp,
            'simulation': simu
        }
        report['intensities'] = {
            'I_DD': {
                'mean': float(np.mean(self.idd_samples)),
                'median': float(np.median(self.idd_samples)),
            },
            'I_DA': {
                'mean': float(np.mean(self.ida_samples)),
                'median': float(np.median(self.ida_samples)),
            },
            'I_AA': {
                'mean': float(np.mean(self.iaa_samples)),
                'median': float(np.median(self.iaa_samples)),
            },
        }
        report['cutoff_10_percent'] = {}
        with open(self._output_path / 'report.json', 'w') as f:
            json.dump(report, f, indent=4)

    def load_results(self) -> None:
        """ Load previous simulation results.

        The purpose is to regenerate the plots without reruning the simulation
        """
        # Load errors
        output_dir = self._output_path / 'data'
        self.heatmap_gamma_m = np.load(
            output_dir / 'gamma.npy', allow_pickle=True
        )
        self.heatmap_beta_x = np.load(
            output_dir / 'beta.npy', allow_pickle=True
        )
        self.heatmap_e_median = np.load(
            output_dir / 'e_median.npy', allow_pickle=True
        )
        self.heatmap_e_std = np.load(
            output_dir / 'e_std.npy', allow_pickle=True
        )
        self.e_deltas = np.load(
            output_dir / 'e_deltas.npy', allow_pickle=True
        )
        self.s_deltas = np.load(
            output_dir / 's_deltas.npy', allow_pickle=True
        )

        # load intensities
        self.idd_samples = np.load(
            output_dir / 'idd.npy', allow_pickle=True
        )
        self.ida_samples = np.load(
            output_dir / 'ida.npy', allow_pickle=True
        )
        self.iaa_samples = np.load(
            output_dir / 'iaa.npy', allow_pickle=True
        )

    def plot_results(self) -> None:
        """ Plots the results of the simulations.

        The results consists of:
            * Printing on the console the 10% cut off, which is the delta E
                interval under which the E error is more than 10%
            * Ploting 4 heatmaps
                * Fret absolute error for each couple deltaE / deltaS
                * Fret relative error for each couple deltaE / deltaS
                * GammaM absolute error for each couple deltaE / deltaS
                * BetaX absolute error for each couple deltaE / deltaS
            * 3 histograms, one for each intensities samples
        """
        # Compute and print cutoff
        mean_relative_error_per_delta_e = np.mean(self.heatmap_e_median[1],
                                                  axis=0)
        mean_absolute_error_per_delta_e = np.mean(self.heatmap_e_median[0],
                                                  axis=0)
        indices_cutoff = np.where(mean_relative_error_per_delta_e >= 10)
        delta_e_cutoff = [
            float(self.e_deltas[indices_cutoff[0][-1]]),
            float(self.e_deltas[indices_cutoff[0][-1]+1])
        ]
        error_cutoff = [
            float(mean_absolute_error_per_delta_e[indices_cutoff[0][-1]]),
            float(mean_absolute_error_per_delta_e[indices_cutoff[0][-1]+1])
        ]
        print(f'10% Cut Off: {delta_e_cutoff}')
        with open(self._output_path / 'report.json', 'r+') as f:
            report = json.load(f)
            report['cutoff_10_percent']['delta_e_range'] = delta_e_cutoff
            report['cutoff_10_percent']['error_associated'] = error_cutoff
            f.seek(0)
            json.dump(report, f, indent=4)
            f.truncate()

        # Plot heatmaps
        self._plot_heatmap(
            self.heatmap_e_median[0], r'Error on E', r'|$E$ - $E_{th}$|',
            self._output_path / 'fret.png', 0.15, with_mean_plot=True
        )
        self._plot_heatmap(
            self.heatmap_e_median[1], 'Error on E relative',
            r'|E - $E_{th}$| / $E_{th}$',
            self._output_path / 'fret-rel.png',
            40, with_mean_plot=True,
        )
        self._plot_heatmap(
            self.heatmap_gamma_m[0],
            r'Error on $\gamma^M$', r'|$\gamma^M$ - $\gamma^M_{th}$|',
            self._output_path / 'gamma_m.png',
            0.90,
        )
        self._plot_heatmap(
            self.heatmap_beta_x[0],
            r'Error on $\beta^X$', r'|$\beta^X$ - $\beta^X_{th}$|',
            self._output_path / 'beta_x.png',
            1.0,
        )

        # Plot Intensities histo
        self._plot_histo(self.idd_samples, r'$I_{DD}$',
                         self._output_path / 'i_dd.png')
        self._plot_histo(self.ida_samples, r'$I_{DA}$',
                         self._output_path / 'i_da.png')
        self._plot_histo(self.iaa_samples, r'$I_{AA}$',
                         self._output_path / 'i_aa.png')

        plt.show()

    def _get_figure(
        self, title: str = '', subtitle: str = '', with_mean_plot: bool = False
    ) -> Figure:
        """ Get a figure with the given title and subtitle.

        Args:
            title (str, optional): Title. Defaults to ''.
            subtitle (str, optional): Subtitle. Defaults to ''.
            with_mean_plot (bool, optional): If the plot contains the mean
                plot or not. Defaults to False.

        Returns:
            Figure: Newly created figure
        """
        if with_mean_plot:
            figures_size = (9, 8)
            subtitle_y = 0.905
        else:
            figures_size = (9, 8)
            subtitle_y = 0.9
        title_size = 25
        sub_title_size = int(title_size * 0.6)

        fig = plt.figure(figsize=figures_size)
        if title != '':
            fig.suptitle(title, fontsize=title_size)
        if subtitle != '':
            fig.text(0.5, subtitle_y, subtitle, ha='center',
                     fontsize=sub_title_size, style='italic')
        return fig

    def _plot_heatmap(
        self, array: np.ndarray, title: str, subtitle: str, output_path: Path,
        color_max: float, with_mean_plot: bool = False
    ) -> None:
        """ Plot a Heatmap of the given error value

        Args:
            array (np.ndarray): Heatmap to plot
            title (str): Title of the heatmap
            subtitle (str): Subtitle of the heatmap
            output_path (Path): File to save the plot to
            color_max (float): Maximum value of the colorbar
            with_mean_plot (bool, optional): Weather or not to add a plot
                above the heatmap showing the mean value of all error for a
                given DeltaE. Defaults to False.
        """
        e_deltas = self.e_deltas
        s_deltas = self.s_deltas
        label_size = 25
        label_pad = 10
        ticks_size = 17

        # Create the figure
        fig = self._get_figure(title, subtitle, with_mean_plot)
        fig.subplots_adjust(left=0.15)
        if with_mean_plot:
            rows = 2
            heatmap_index = 1
            height_ration = [1, 4]
        else:
            rows = 1
            heatmap_index = 0
            height_ration = [1]
        gs = fig.add_gridspec(
            rows, 2, height_ratios=height_ration, width_ratios=[20, 1],
            hspace=0.1, wspace=0.1
        )

        # Add the mean plot
        ax_plot = None
        if with_mean_plot:
            ax_plot = fig.add_subplot(gs[0, 0])
            mean = np.mean(array, axis=0)
            x_values = e_deltas
            ax_plot.plot(x_values, mean)
            ax_plot.tick_params(labelbottom=False)
            ax_plot.set_ylabel(
                subtitle, size=label_size, labelpad=label_pad+5
            )
            ax_plot.tick_params(axis='both', labelsize=ticks_size)
            ax_plot.set_ylim(0, 0.15)

        # Add the heatmap
        ax_heatmap = fig.add_subplot(gs[heatmap_index, 0], sharex=ax_plot)
        pcm = ax_heatmap.imshow(
            array,
            cmap="plasma",
            aspect='auto',
            extent=(e_deltas[0], e_deltas[-1], s_deltas[-1], s_deltas[0]),
            vmin=0.0, vmax=color_max,
            interpolation=None
        )
        ax_heatmap.set_xlabel(r'$\Delta$E', size=label_size,
                              labelpad=label_pad)
        ax_heatmap.set_ylabel(r'$\Delta$S', size=label_size,
                              labelpad=label_pad)
        ax_heatmap.yaxis.set_major_locator(MaxNLocator(5))
        ax_heatmap.xaxis.set_major_locator(MaxNLocator(5))
        ax_heatmap.tick_params(axis='both', labelsize=ticks_size)

        # Add the coloarbar
        ax_colorbar = fig.add_subplot(gs[heatmap_index, 1])
        fig.colorbar(pcm, cax=ax_colorbar)
        ax_colorbar.tick_params(axis='both', labelsize=ticks_size)
        ax_colorbar.yaxis.set_major_locator(MaxNLocator(6))

        # Save the figure
        fig.savefig(output_path)

    def _plot_histo(self, array, name, path) -> None:
        """ Plot the histogram of the given intensity channel

        Args:
            array (array: np.ndarray): Intensity array to plot
            name (str): Name of the intensity channel
            path (Path): File to save the plot to
        """
        class KTicksFormater:
            """ Class that alloxs you to format high value above 1000 by
            dividing them by 1000 and adding a "k" behind them.

            It is meant to be used by Matplotlib FuncFormatter
            """
            def __init__(self) -> None:
                """ Constructor
                """
                self.modify = True

            def to_k_format(self, value: float, tick_number: int) -> str:
                """ Format the value to its k-representation

                If the first value incontered is below 1000, no values will be
                converted

                Args:
                    value (float): Value to convert
                    tick_number (int): position of the ticks

                Returns:
                    str: Value to print in the tick
                """
                if tick_number == 1:
                    if value < 1000:
                        self.modify = False
                if self.modify:
                    return f'{int(value / 1000)}k'
                else:
                    return str(int(value))

        f = array.flatten()
        fig = self._get_figure(f"Distribution of {name}")
        ax = fig.subplots(1, 1)
        ax.hist(f, bins=200,
                weights=np.ones(f.shape[0])/self._intensity_samples)
        ax.set_xlabel(name, size=25, labelpad=10)
        ax.set_ylabel('Count', size=25, labelpad=15)
        ax.tick_params(axis='both', labelsize=17)
        x_formatter = KTicksFormater()
        y_formatter = KTicksFormater()
        ax.xaxis.set_major_formatter(FuncFormatter(x_formatter.to_k_format))
        ax.yaxis.set_major_formatter(FuncFormatter(y_formatter.to_k_format))
        fig.subplots_adjust(left=0.15, bottom=0.13)
        fig.savefig(path)

    def _generate_interval(
        self, range: tuple[float, float], num: int, reverse: bool = False
    ) -> np.ndarray:
        """ Generate values spread along an interval.

        The algorithm can be either linspace or geomspace depending on the
        parameters given to the constructor

        Args:
            range (tuple[float, float]): Minimum and maximum value in the
                interval
            num (int): number of values to generate
            reverse (bool, optional): If in geomspace and if set to True, will
                generate more high values than low values. Defaults to False.

        Returns:
            np.ndarray: _description_
        """
        min = range[0]
        max = range[1]
        if reverse:
            # If in geomspace, generate more high values than low values
            return (max + min) - self.space(max, min, num)
        else:
            # Return the distribution from numpy
            return self.space(min, max, num)


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        argparse.Namespace: populated namespace
    """
    # Parser
    parser = argparse.ArgumentParser(
        description='Utility tool to run simulations to estimate the accuracy '
                    'of the QuanTI-FRET autocalibration with different '
                    'spreading of fret and stochiometry values')

    subparsers = parser.add_subparsers(dest='mode', required=False)

    # Single Mode
    single_parser = subparsers.add_parser(
        'single',
        help='Run a single experiment simulation and print the 3D plane'
    )
    single_parser.add_argument(
        '-e', '--delta_e',
        type=str,
        required=True,
        help='Delta E variation expected'
    )
    single_parser.add_argument(
        '-s', '--delta_s',
        type=str,
        required=True,
        help='Delta S variation expected'
    )

    # Multiple Mode (default)
    SP = SimulationParameters
    parser.add_argument(
        '-e', '--delta_e_range', nargs=3, type=float,
        default=[SP.e_delta_min, SP.e_delta_max, SP.e_delta_steps],
        help='Min and max and number of values for delta e'
    )
    parser.add_argument(
        '-s', '--delta_s_range', nargs=3, type=float,
        default=[SP.s_delta_min, SP.s_delta_max, SP.s_delta_steps],
        help='Min and max and number of values for delta s'
    )
    parser.add_argument(
        '-p', '--plot_details', action='store_true',
        help='Plot the 3D plane of each steps'
    )
    parser.add_argument(
        '-g', '--geomspace', action='store_true',
        help='use geomspace instead of linspace to compute different values of'
             'delta_e and delta_s'
    )
    parser.add_argument(
        '-n', '--no_progress', action='store_true',
        help='Disable progress bar'
    )
    parser.add_argument(
        '-o', '--output_dir', type=str, default='output',
        help='Folder where to store the results'
    )
    parser.add_argument(
        '-l', '--load', action='store_true',
        help='Load results from output instead of generating them'
    )
    # Parse args
    return parser.parse_args()


def main():
    args = parse_args()

    if args.mode == 'single':
        # Generate a single experiment, compute estimated GammaM, BetaX and
        # plot the 3Dplane
        e_0 = SimulationParameters.e_0
        e_bins = SimulationParameters.e_bins
        s_0 = SimulationParameters.s_0
        e_delta = float(args.delta_e)
        s_delta = float(args.delta_s)

        exp = Experiment()
        exp.generate(e_0, e_delta, e_bins, s_0, s_delta)

        ana = Analyser(exp)
        ana.xm(plot_details=True)
    else:
        # Generate multiple experiments, compute the Fret, GammaM and BetaX
        # errors and plot them

        # Get params
        plot_detais = args.plot_details
        geomspace = args.geomspace
        no_progress = args.no_progress
        output_dir = args.output_dir

        # Update SimulationParameters
        SimulationParameters.e_delta_min = float(args.delta_e_range[0])
        SimulationParameters.e_delta_max = float(args.delta_e_range[1])
        SimulationParameters.e_delta_steps = int(args.delta_e_range[2])
        SimulationParameters.s_delta_min = float(args.delta_s_range[0])
        SimulationParameters.s_delta_max = float(args.delta_s_range[1])
        SimulationParameters.s_delta_steps = int(args.delta_s_range[2])

        # Run the simulation
        simu = Simulation(
            output_dir, plot_details=plot_detais, geomspace=geomspace,
            no_progress=no_progress
        )
        if not args.load:
            simu.generate()
        else:
            simu.load_results()
        simu.plot_results()


if __name__ == '__main__':
    main()
