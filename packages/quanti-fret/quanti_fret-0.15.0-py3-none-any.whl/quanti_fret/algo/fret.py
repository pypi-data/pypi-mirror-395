from quanti_fret.algo.background import BackgroundEngine, substract_background
from quanti_fret.algo.plot import PlotGenerator
import quanti_fret.algo.matrix_functions as mfunc
from quanti_fret.core import Triplet, QtfException

from typing import Any

from matplotlib.figure import Figure
import numpy as np


class FretCalculator:
    """ Compute the Fret value of a Triplet

    This class can be used with two modes:
        * Single mode: it computes the fret on a single triplet, without
            keeping information on the series it can be part of, or without
            doing more analysis on it.
        * Series mode: The goal is to consider the input as part of a series.
            This mode keeps sampled data in order to perform analysis on the
            given dataset.

    To run on Single mode, just call the method `single_run`.

    To run on Series mode, you need to:
        * First call `series_reset`
        * Then set the parameters that will be used for the series by calling
            `series_params`
        * Then for each triplet of the series, you nee to call `series_next`
            that computes E, S, Ew and some plots you need to use on your side.
        * Finally, you can perform analysis on the series by calling
            `series_analysis`.
    """

    def __init__(self) -> None:
        """ Constructor
        """
        self._plot = PlotGenerator()
        self._sampled_list: list[np.ndarray] = []
        self._reset_called = True
        self._params: Any = None

    def series_reset(self) -> None:
        """ Starts a new series by reseting the class internal state to discard
            previous results.
        """
        self._sampled_list.clear()
        self._reset_called = True

    def series_params(
        self, alpha_bt: float, delta_de: float,  beta_X: float, gamma_m: float,
        background: BackgroundEngine, sigma_s: float,
        target_s: float, sigma_gauss: float, weights_threshold: float,
        analysis_details: bool = False, analysis_sampling: int = 100,
    ) -> None:
        """ Set the Fret parameters that will be used for the whole series.

        You can't change the parameters in the middle of a series run.

        Args:
            alpha_bt (float): alpha_bt value from calibration
            delta_de (float): delta_de value from calibration
            background (BackgroundEngine): background engine to use
            beta_x (float): beta_x value from calibration
            gamma_m (float): gamma_m value from calibration
            sigma_S (float): standard deviation of the gaussian distribution of
                the stochiometry
            target_S (float): Mean value of the gaussian distribution of the
                stochiometry
            sigma_gauss (float): standard deviation of the gaussian kernel for
                filtering
            weights_threshold (float): threshold for the local "quality of the
                data".  discard if
                mean(local weight in the window) < weights_threshold.
            analysis_details (bool): Weather or not to compute detailed data
                for analysis purposes. Default to False.
            analysis_sampling (int): Keep one value every "analysis_sampling"
                values on data used to generate analysis details. Default to
                100.

        Raises:
            QtfException: Series was not reset
        """
        if not self._reset_called:
            err = 'You need to call `series_reset` before settings new ' \
                  'parameters'
            raise QtfException(err)

        self._params = (
            alpha_bt, delta_de,  beta_X, gamma_m, background, sigma_s,
            target_s, sigma_gauss, weights_threshold, analysis_details,
            analysis_sampling
        )

    def series_run(
        self, triplet: Triplet
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray,
               dict[str, Figure | np.ndarray]]:
        """ Compute the Fret on the given triplet, and keep sampled data for
        future analysis.

        The values returned are:
            * E: Fret
            * Ew: Fret Filtered
            * S: Stochiometry
            * extras:
                * 'hist2d_s_vs_e': S vs E 2D histogram,
                * 'hist2d_e_vs_iaa': E vs I_AA 2D histogram,
                * 'hist2d_s_vs_iaa': S vs I_AA 2D histogram,
                * 'sampled': Sampled data extracted within the mask. It is a
                    numpy array of shape (6, N) whose second axis represents
                    the samples values from the mask of DD/DA/AA/E/S/Ew.

        If `analysis_details` was set to `False`, Plots wil not be computed
        (dictionary will be empty) and sampled data will not be kept. In
        consequences, the extra dictionary returned will be empty.

        Args:
            triplet (Triplet): Triplet to compute the Fret on

        Raises:
            QtfException: No params where found

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Figure]]:
                E, Ew, S, plots_figures, sampled
        """
        if self._params is None:
            err = 'You need to call `set_params` before calling `series_run`'
            raise QtfException(err)
        self._reset_called = False

        E, Ew, S, extras = self.single_run(triplet, *self._params)

        analysis_details = self._params[-2]
        if analysis_details:
            assert 'sampled' in extras
            assert isinstance(extras['sampled'], np.ndarray)
            self._sampled_list.append(extras['sampled'])

        return E, Ew, S, extras

    def series_analysis(
        self
    ) -> dict[str, Figure | np.ndarray] | None:
        """ Compute and plot analysis data on the sampled data extracted from
        the series.

        Analysis data are:
            * Boxplot of E and S for each triplet
            * 2D histogram of S vs E compued on all sampled values of the
                series
            * An array containing the median values for DD/DA/AA/E/Ew/S for
                each triplets.

        Raises:
            QtfException: No data computed
        """
        if self._params is None:
            err = 'You need to call `set_params` before calling ' \
                  '`series_analysis`'
            raise QtfException(err)
        analysis_details = self._params[-2]
        if not analysis_details:
            return None
        if len(self._sampled_list) == 0:
            return None

        boxplots = self._plot_boxplot(self._sampled_list)
        hist2d = self._plot_series_hist2d(self._sampled_list)
        median_sampled = self._compute_median_sampled(self._sampled_list)
        extras: dict[str, Figure | np.ndarray] = {
            'e_boxplot': boxplots[0],
            's_boxplot': boxplots[1],
            'hist_2d': hist2d,
            'median_sampled': median_sampled
        }
        return extras

    def single_run(
        self, triplet: Triplet, alpha_bt: float, delta_de: float,
        beta_X: float, gamma_m: float, background: BackgroundEngine,
        sigma_s: float, target_s: float, sigma_gauss: float,
        weights_threshold: float,
        analysis_details: bool = False, analysis_sampling: int = 100,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray,
               dict[str, Figure | np.ndarray]]:
        """ Compute the Fret value of a triplet outside any series
        consideration.

        It returns:
            * The Fret value E
            * The Fret filtered Ew
            * The Stochiometry value S
            * extras data:
                * 'hist2d_s_vs_e': S vs E 2D histogram,
                * 'hist2d_e_vs_iaa': E vs I_AA 2D histogram,
                * 'hist2d_s_vs_iaa': S vs I_AA 2D histogram,
                * 'sampled': Sampled data extracted within the mask. It is a
                    numpy array of shape (6, N) whose second axis represents
                    the samples values from the mask of DD/DA/AA/E/S/Ew.

        If `analysis_details` is set to `False`, Plots will not be computed
        (dictionary will be empty) and sampled data will not be kept. In
        consequences, the extra dictionary returned will be empty.

        Args:
            triplet (Triplet): Triplet to compute the sequence on
            alpha_bt (float): alpha_bt value from calibration
            delta_de (float): delta_de value from calibration
            background (BackgroundEngine): background engine to use
            beta_x (float): beta_x value from calibration
            gamma_m (float): gamma_m value from calibration
            sigma_S (float): standard deviation of the gaussian distribution of
                the stochiometry
            target_S (float): Mean value of the gaussian distribution of the
                stochiometry
            sigma_gauss (float, optional): standard deviation of the gaussian
                kernel for filtering
            weights_threshold (float, optional): threshold for the local
                "quality of the data".  discard if
                mean(local weight in the window) < weights_threshold.
            analysis_details (bool): Weather or not to compute detailed data
                for analysis purposes.
            analysis_sampling (int): Keep one value every "analysis_sampling"
                values on data used to generate analysis details.

        Returns:
            tuple[float, float, float, float, float]:
                (E, Ew, S, plots_hist2d, sampled_data)
        """
        # substract background
        channels = substract_background(triplet, background)

        # Compute DA corr
        channels[1] = mfunc.da_corrected(channels, alpha_bt, delta_de)

        # Compute Fret and Stochiometry
        E = mfunc.alex_fret(channels[0], channels[1], gamma_m)
        S = mfunc.alex_stochio(channels[0], channels[1], channels[2], gamma_m,
                               beta_X)

        # Compute the weighted gaussian filter
        Ew = mfunc.weighted_gaussian_filter(
            E, S, sigma_s, target_s, sigma_gauss, weights_threshold
        )

        extras: dict[str, Figure | np.ndarray] = {}
        if analysis_details:
            # Compute Mask and extract data
            if triplet.has_mask_cell():
                mask = triplet.mask_cell
                new_mask = mfunc.clean_mask(mask, channels, channels)
                channels_masked = channels[:, new_mask]
                E_masked = E[new_mask]
                S_masked = S[new_mask]
                Ew_masked = Ew[new_mask]
            else:
                channels_masked = channels.reshape(channels.shape[0], -1)
                E_masked = E.flatten()
                S_masked = S.flatten()
                Ew_masked = Ew.flatten()

            # Extract sampled data
            channels_sampled = channels_masked[:, ::analysis_sampling]
            E_sampled = E_masked[::analysis_sampling]
            S_sampled = S_masked[::analysis_sampling]
            Ew_sampled = Ew_masked[::analysis_sampling]
            extras['sampled'] = np.vstack(
                [channels_sampled, E_sampled, Ew_sampled, S_sampled]
            )

            # Plot 2D hist
            s_vs_e, e_vs_iaa, s_vs_iaa = self._plot_hist2d(
                E_masked, S_masked, channels_masked[2]
            )
            extras['hist2d_s_vs_e'] = s_vs_e
            extras['hist2d_e_vs_iaa'] = e_vs_iaa
            extras['hist2d_s_vs_iaa'] = s_vs_iaa

        return E, Ew, S, extras

    def _plot_hist2d(
        self, E: np.ndarray, S: np.ndarray, aa: np.ndarray,
    ) -> tuple[Figure, Figure, Figure]:
        """ Plot the Fret 2D histograms for a given Triplet

        Will plot:
            - Fret (E) vs stochiometry (S)
            - Fret (E) vs AA intensity (I_AA)
            - Stochiometry (S) vs AA intensity (I_AA)

        Args:
            E (np.ndarray): Fret
            S (np.ndarray): Stochiometry
            aa (np.ndarray): AA channel

        Returns:
            tuple[Figure, Figure, Figure]: s_vs_e, e_vs_iaa, s_vs_iaa
        """
        s_vs_e = self._plot.hist2d_signal_intensity(
            E, S, 'Fret', 'Stochiometry',
            range=((0, 100), (0, 100)),
            title='S vs E'
        )

        e_vs_iaa = self._plot.hist2d_signal_intensity(
            aa, E, 'I_AA', 'E',
            range=('percentile', (0, 100)),
            percentile_range=((1, 90), (0, 100)),
            title='E vs I_AA intensity'
        )

        s_vs_iaa = self._plot.hist2d_signal_intensity(
            aa, S, 'I_AA', 'S',
            range=('percentile', (0, 100)),
            percentile_range=((1, 90), (0, 100)),
            title='S vs I_AA intensity'
        )

        return s_vs_e, e_vs_iaa, s_vs_iaa

    def _plot_boxplot(
        self, sampled_list: list[np.ndarray]
    ) -> tuple[Figure, Figure]:
        """Plot the boxplot for Fret and Stochiometry

        Args:
            sampled_list (list[np.ndarray]): Sampled data for each sequence
                with E, and S respectively on channel 3, and 5

        Returns:
            tuple[Figure, Figure]: Fret boxplot, Stochiometry boxplot
        """
        # Boxplot for E
        E_sampled = [sampled[3] for sampled in sampled_list]
        median = np.mean(np.array([np.median(e) for e in E_sampled]))
        e_boxplot = self._plot.boxplot_seq_overview(
            'Fret', E_sampled, f'mean of medians: {median:.2f}'
        )

        # Boxplot for S
        S_sampled = [sampled[5] for sampled in sampled_list]
        median = np.mean(np.array([np.median(e) for e in S_sampled]))
        s_boxplot = self._plot.boxplot_seq_overview(
            'Stochiometry', S_sampled, f'mean of medians: {median:.2f}'
        )

        return e_boxplot, s_boxplot

    def _plot_series_hist2d(self, sampled_list: list[np.ndarray]) -> Figure:
        """ Plot the 2D histogram of S vs E of all sampled data for the
        whole series.

        Args:
            sampled_list (list[np.ndarray]): Sampled data for each triplets.
                First axis select DD/DA/AA/E/Ew/S and second axis is the
                data.

        Returns:
            Figure: The 2D histogram
        """
        E_sampled = np.concatenate([sampled[3] for sampled in sampled_list])
        S_sampled = np.concatenate([sampled[5] for sampled in sampled_list])
        s_vs_e = self._plot.hist2d_signal_intensity(
            E_sampled, S_sampled, 'Fret', 'Stochiometry',
            range=((0, 100), (0, 100)),
            title='S vs E'
        )
        return s_vs_e

    def _compute_median_sampled(
        self, sampled_list: list[np.ndarray]
    ) -> np.ndarray:
        """ Compute the median of all the sampled data extracted from the
        triplets.

        The output is a numpy array of shape (nb_triplets, 6) with one row
        per triplet, and whose colums are DD/DA/AA/E/Ew/S.

        Args:
            sampled_list (list[np.ndarray]): Sampled data for each triplets.
                First axis select DD/DA/AA/E/Ew/S and second axis is the
                data.

        Returns:
            np.ndarray: Median of channels and fret of all triplets
        """
        median_list = [
            np.median(sampled, axis=1) for sampled in sampled_list
        ]
        return np.vstack(median_list)
