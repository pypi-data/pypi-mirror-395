from quanti_fret.algo.background import BackgroundEngine, substract_background
from quanti_fret.algo.plot import PlotGenerator
import quanti_fret.algo.matrix_functions as mfunc
from quanti_fret.core import QtfException, Triplet

from typing import Any

from matplotlib.figure import Figure
import numpy as np


class XMCalculator:
    """ Compute BetaX and GammaM Calibration

    To use this class on a series, you need to follow the following workflow:
        * Call `reset`
        * Set the params using `params`
        * For each triplet of the series, call `add_triplet`
        * To get the final results call `compute_results`

    This workflow can look complex but it allows you to easilly monitor the
    progess of the computation.
    """

    def __init__(self) -> None:
        self._plot = PlotGenerator()
        self._params: Any = None
        self._cells_data: list[np.ndarray] = []
        self._reset_called = True

    def reset(self) -> None:
        """ Reset the calculator internal state to discard previous results and
        starts computing on a new series.
        """
        self._cells_data.clear()
        self._reset_called = True

    def params(
        self, alpha_bt: float, delta_de: float, background: BackgroundEngine,
        percentile_range: tuple[float, float], analysis_details: bool = False,
        analysis_sampling: int = 100,
    ) -> None:
        """ Set the parameters that will be used for the futur calls.

        You can't change the parameters in the middle of a series computation.

        Args:
            alpha_bt (float): alpha_bt value
            delta_de (float): delta_de value
            background (BackgroundEngine): background engine to use
            percentile_range (tuple[float, float]): The percentile range
                outside which values will be discarded. Computed after applying
                the mask.
            analysis_details (bool): Weather or not to compute detailed data
                for analysis purposes.
            analysis_sampling (int): Keep one value every "analysis_sampling"
                values on data used to generate analysis details.

        Raises:
            QtfException: Series was not reset
        """
        if not self._reset_called:
            err = 'You need to call `reset` before settings new parameters'
            raise QtfException(err)

        self._params = (
            alpha_bt, delta_de, background, percentile_range, analysis_details,
            analysis_sampling
        )

    def add_triplet(self, triplet: Triplet) -> None:
        """ Add the given triplet to the series computation.

        This will perform all the computation possible on the given triplet
        and store the results internally for future analysis.

        Args:
            triplet (Triplet): Triplet to add to the series computation

        Raises:
            QtfException: No params were set
        """
        if self._params is None:
            err = 'You need to call `params` before calling `add_triplet`'
            raise QtfException(err)
        self._reset_called = False

        cell = self._get_cell_from_triplet(triplet, *self._params[:-2])

        self._cells_data.append(cell)

    def compute_results(
        self
    ) -> tuple[float, float, float, float, float, dict[str, Any]]:
        """ Compute the BetaX and GammaM values using the data computed on all
        the triplet added to the series computation.

        Also returns Redchi2, R2, Q and analysis data if asked.

        Analysis data are in a dictionarry organized as follow:
            {
                'general': {
                    'hist2d_e_vs_s': ...,
                    'hist2d_e_vs_iaa': ...,
                    'hist2d_s_vs_iaa': ...,
                }
            }

        Returns:
            tuple[float, float, float, float, float]:
                (BetaX, GammaM, Redchi2, R2, Q, analysis_data)
        """
        if self._params is None:
            err = 'You need to call `params` before calling `compute_results`'
            raise QtfException(err)
        if len(self._cells_data) == 0:
            return 0., 0., 0., 0., 0., {}

        # Calculation of betaX and GammaM
        all_cells = np.concatenate(self._cells_data, axis=1)
        dd = all_cells[0]
        da_corr = all_cells[1]
        aa = all_cells[2]
        beta_x, gamma_m, redchi_2, r2 = mfunc.gamma_xm(dd, da_corr, aa)

        # Compute Fret and Stochiometry
        E = mfunc.alex_fret(dd, da_corr, gamma_m)
        S = mfunc.alex_stochio(dd, da_corr, aa, gamma_m, beta_x)

        # Compute the fit confidence index Q
        q = mfunc.fit_confidence_index_q(E, S, aa, r2)

        # Optional data to plot / returns
        analysis_data: dict[str, Any] = {}
        analysis_details = self._params[-2]
        analysis_sampling = self._params[-1]
        if analysis_details:
            hist2d = self._plot_hist2d(E, S, aa, analysis_sampling)
            median_sampled, sampled_list = self._extract_sampled_data(
                self._cells_data, E, S, analysis_sampling
            )
            scatters = self._plot_analysis_median_data(median_sampled)
            boxplots = self._plot_boxplot(sampled_list)
            scatter_3d = self._generate_3d_plot(sampled_list, beta_x, gamma_m)
            analysis_data = {
                'hist2d_s_vs_e': hist2d[0],
                'hist2d_e_vs_iaa': hist2d[1],
                'hist2d_s_vs_iaa': hist2d[2],
                'median_sampled': median_sampled,
                'sampled_list': sampled_list,
                'e_boxplot': boxplots[0],
                's_boxplot': boxplots[1],
                'inspection': {
                    'triplets_per_seq': scatters[0],
                    's_per_seq': scatters[1],
                    's_vs_e': scatters[2],
                    'scatter_3d': scatter_3d
                }
            }

        # Round data
        beta_x = np.round(beta_x, 3)
        gamma_m = np.round(gamma_m, 3)
        redchi_2 = np.round(redchi_2, 3)
        r2 = np.round(r2, 3)
        q = np.round(q, 3)

        return beta_x, gamma_m, redchi_2, r2, q, analysis_data

    def _get_cell_from_triplet(
        self, triplet: Triplet, alpha_bt: float, delta_de: float,
        background: BackgroundEngine, percentile_range: tuple[float, float]
    ) -> np.ndarray:
        """ On the given triplet, compute DA corr and extract data from all
        3 channels matching the newly computed mask.

        The array returned is shape (3, N). Axis 0 represents 1 channel
        (dd, da or aa), axis 1 is the concatenation of all the computed and
        extracted values on this channel for every sequences.

        The mask used for cell extraction is created from the triplet mask.
        It is then improved removing some irrelevant values and discarding the
        given range percentile pixels.

        Args:
            triplet (Triplet): The series to use for computation
            alpha_bt (float): alpha_bt value
            delta_de (float): delta_de value
            background (BackgroundEngine): background engine to use
            percentile_range (tuple[float, float]): The percentile range
                outside which values will be discarded. Computed after applying
                the mask.

        Returns:
            np.ndarray: Data computed and extracted on the 3 channels
        """
        mask = triplet.mask_cell

        # substract background
        triplet_np = substract_background(triplet, background)

        # Compute DA corr
        triplet_np[1] = mfunc.da_corrected(triplet_np, alpha_bt, delta_de)

        # Compute Mask
        new_mask = mfunc.clean_mask(mask, triplet_np, triplet_np,
                                    percentile_range[0],
                                    percentile_range[1])

        # Extract data from mask
        triplet_np = triplet_np[:, new_mask]

        return triplet_np

    def _plot_hist2d(
        self, E: np.ndarray, S: np.ndarray, aa: np.ndarray, sampling: int
    ) -> tuple[Figure, Figure, Figure]:
        """ Plot the global XM 2D histogram

        Will plot:
            - Fret (E) vs stochiometry (S)
            - Fret (E) vs AA intensity (I_AA)
            - Stochiometry (S) vs AA intensity (I_AA)

        Args:
            E (np.ndarray): Fret
            S (np.ndarray): Stochiometry
            aa (np.ndarray): AA channel
            sampling (int):  Keep one value every "sampling" values to do the
                plots.s

        Returns:
            tuple[Figure, Figure, Figure]: s_vs_e, e_vs_iaa, s_vs_iaa
        """
        s_vs_e = self._plot.hist2d_signal_intensity(
            E, S, 'Fret', 'Stochiometry',
            range=((0, 100), (0, 100)),
            title='S vs E for all cells'
        )

        e_vs_iaa = self._plot.hist2d_signal_intensity(
            aa[::sampling], E[::sampling], 'I_AA', 'E',
            range=('percentile', (0, 100)),
            percentile_range=((1, 90), (0, 100)),
            title='E vs I_AA intensity for all cells'
        )

        s_vs_iaa = self._plot.hist2d_signal_intensity(
            aa[::sampling], S[::sampling], 'I_AA', 'S',
            range=('percentile', (0, 100)),
            percentile_range=((1, 90), (0, 100)),
            title='S vs I_AA intensity for all cells'
        )

        return s_vs_e, e_vs_iaa, s_vs_iaa

    def _extract_sampled_data(
        self, masked_channels: list[np.ndarray], E: np.ndarray, S: np.ndarray,
        sampling: int
    ) -> tuple[np.ndarray, list[np.ndarray]]:
        """ Extract sampled data from the XM computation for analysis purpose

        The value returned are computed on sampled data. They consist of:
            * median_sampled: An Array containing for each sequence a numpy of
                shape(5,) whose values represents the median value of
                (dd, da, aa, E and S)
            * sampled_list: A list containing for each sequence a numpy of
                shape(5, N) whose values represents (dd, da, aa, E and S)

        Args:
            masked_channels (list[np.ndarray]): Masked triplets for each
                sequence
            E (np.ndarray): Fret
            S (np.ndarray): Stochiometry
            sampling (int): Extract one value every "sampling" values

        Returns:
            tuple[np.ndarray, list[np.ndarray]]:
                (median_sampled, sampled_list)
        """
        sampled_list: list[np.ndarray] = []
        median_sampled_list: list[np.ndarray] = []
        start = 0
        end = 0
        for seq_idx in range(len(masked_channels)):
            end = start + masked_channels[seq_idx][0].shape[0]
            masked = masked_channels[seq_idx]
            masked_sampled = masked[:, ::sampling]
            E_sampled = E[start:end:sampling]
            S_sampled = S[start:end:sampling]
            all_sampled = np.vstack((masked_sampled, E_sampled, S_sampled))
            median = np.median(all_sampled, axis=1)
            sampled_list.append(all_sampled)
            median_sampled_list.append(median)
            start = end
        median_sampled = np.vstack(median_sampled_list)
        return (median_sampled, sampled_list)

    def _plot_boxplot(
        self, sampled_list: list[np.ndarray]
    ) -> tuple[Figure, Figure]:
        """Plot the boxplot for Fret and Stochiometry

        Args:
            sampled_list (list[np.ndarray]): Sampled data for each sequence
                with E, and S rescpetcively on channel 3, and 4

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
        S_sampled = [sampled[4] for sampled in sampled_list]
        median = np.mean(np.array([np.median(e) for e in S_sampled]))
        s_boxplot = self._plot.boxplot_seq_overview(
            'Stochiometry', S_sampled, f'mean of medians: {median:.2f}'
        )

        return e_boxplot, s_boxplot

    def _plot_analysis_median_data(
        self, median_sampled: np.ndarray
    ) -> tuple[Figure, Figure, Figure]:
        """ Generate the figures associated with the median data extracted in
        the data analysis.

        Figures created are:
            * Scatter plot of all median values of the 3 channels for each
                sequence
            * Scatter plot of the median values of S for each sequence
            * Scatter plot of all median values of S vs E

        Args:
            median_sampled (np.ndarray): the median values of DD, DA, AA, E, S
                for each sequence.

        Returns:
            tuple[Figure, Figure, Figure]:
                (triplets_per_seq_f, s_per_seq_f, s_vs_e_f)
        """
        seq_indices = np.array(range(median_sampled.shape[0])) + 1

        triplets_per_seq_f = self._plot.scatterplot(
            'Sequence', seq_indices, 'Mean Intensity', median_sampled[:, :3],
            legends=['DD', 'DA', 'AA'],
            title='Median Intensity of Triplets for each sequence',
            integer_on_x=True)

        s_per_seq_f = self._plot.scatterplot(
            'Sequence', seq_indices, 'Stochiometry', median_sampled[:, 4],
            title='Median Stochiometry for each sequence',
            integer_on_x=True)

        s_vs_e_f = self._plot.scatterplot(
            'E', median_sampled[:, 3], 'S', median_sampled[:, 4],
            title='Median Stochiometry over Fret')

        return triplets_per_seq_f, s_per_seq_f, s_vs_e_f

    def _generate_3d_plot(
        self, sampled_list: list[np.ndarray], beta_x: float, gamma_m: float
    ) -> Figure:
        """ Generate the 3D plot with the plane.

        Args:
            sampled_list (list[np.ndarray]): Sampled data for each sequence
                with DD, DA, AA on channel 0, 1, and 2
            beta_x (float): beta_x computed (used for plane)
            gamma_m (float): gamma_m computed (used for plane)

        Returns:
            Figure: The plot figure
        """
        dds = np.concatenate([s[0] for s in sampled_list], axis=0)
        das = np.concatenate([s[1] for s in sampled_list], axis=0)
        aas = np.concatenate([s[2] for s in sampled_list], axis=0)

        idx = self._3d_plot_mask(aas)

        fig = self._plot.scatterplot_3d(
            'I_DD', dds[idx], 'I_DA', das[idx], 'I_AA', aas[idx],
            (beta_x * gamma_m, beta_x)
        )

        return fig

    def _3d_plot_mask(
        self, channel: np.ndarray, n_bins: int = 20,
        max_samples_per_bins: int = 20,
    ) -> np.ndarray:
        """ Compute the mask to apply on every channel of a triplet in order to
        plot the 3D plane.

        The mask is computed on one channel and is expected to be apply on
        every channels before plotting. It will discards data too close to
        each others in order to keep them evenly spread out all along the
        range. It is usefull for plotting a 3D plane to avoid too many points
        at the same place, but still having enough to see it clearly.

        The algorithm work as the following:
            * We divide the range covered by the data into `n_bins` bins.
                For each bins, we keep only (at max) `max_samples_per_bins`
                values.
            * To select the values for each bins : we extract the all the
                values inside the bin into a subvector - we sort it - we take
                `max_samples_per_bins` indices evenly spread out from 0 to the
                size of this vector - We take the values associated with this
                indices.

        for example:
            Settings:
                * Input: [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 14, 25]
                * bins: 5
                * max_samples_per_bins: 2
            bins: [0, 5[, [5, 10[, [10, 15[, [15, 20[, [20, 25]
                * [0, 5[ -> vals = [0, 1, 2, 3, 4] -> extracted = [1, 3]
                * [5, 10[ -> vals = [5, 6, 8, 9] -> extracted = [6, 8]
                * [10, 15[ -> vals = [10, 11, 14] -> extracted = [11, 14]
                * [15, 20[ -> vals = [] -> extracted = []
                * [20, 25[ -> vals = [25] -> extracted = [25]
            Res: [1, 3, 6, 8, 11, 14, 25]

        Args:
            channel (np.ndarray): The channel to use to compute the mask on
            n_bins (int, optional): Number of bins to divide the data in.
                Defaults to 20.
            max_samples_per_bins (int, optional): Number of samples to extract
                per bins. Defaults to 20.

        Returns:
            np.ndarray: The computed mask
        """
        if channel.ndim != 1:
            err = f'Array must be of dimension 1, found ({channel.ndim})'
            raise QtfException(err)

        if len(channel) == 0:
            return np.empty(channel.shape)

        # Create bins
        bins = np.linspace(channel.min(), channel.max(), n_bins + 1)

        # Create mask
        mask = np.full(channel.shape, False)
        for i in range(n_bins):
            # Get the mask containing all the values within the bin
            if i == n_bins - 1:
                mask_bin = (channel >= bins[i]) & (channel <= bins[i+1])
            else:
                mask_bin = (channel >= bins[i]) & (channel < bins[i+1])
            nb_match = mask_bin.sum()

            # If we found more than `max_samples_per_bins` values for this bin,
            # we select only `max_samples_per_bins` values to extract,
            # otherwise we keep all
            if nb_match > max_samples_per_bins:
                # sort the values within the bins and keep the indices they
                # had before sorting
                sorted_indices = channel[mask_bin].argsort()

                # Considering n values found in this bin, we want to extract
                # max_samples_per_bins indices that are evenly spread out in
                # this range
                extract_indices = np.linspace(0, len(sorted_indices),
                                              max_samples_per_bins + 2)[1:-1]
                extract_indices = np.floor(extract_indices).astype(int)

                # Now we now we want to extract the indices `extract_indices`
                # on the sorted values within the bin (represented by
                # `sorted_indices`), we go back to the indices we want to
                # extract inside the channel array.
                bin_indices = np.where(mask_bin)[0]
                indices = bin_indices[sorted_indices[extract_indices]]

                extract_mask = np.full(channel.shape, False)
                extract_mask[indices] = True
                mask = mask | extract_mask
            else:
                mask = mask | mask_bin

        return mask
