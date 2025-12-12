from quanti_fret.algo.background import BackgroundEngine, substract_background
from quanti_fret.algo.plot import PlotGenerator
import quanti_fret.algo.matrix_functions as mfunc
from quanti_fret.core import QtfException, Triplet

import abc

from matplotlib.figure import Figure
import numpy as np


class GammaCalculator(abc.ABC):
    """ Abstract class that compute the gamma value from a given series.

    A gamma value is the matrix obtained by dividing the DA channel image by
    either the DD or the AA channel image.

    This class then add multiple operation allowing to compute the gamma on
    relevant values (taking only values from the object analysed, discarding
    useless values, ...) and returns the median values of all gammas.

    To use this class on a series, you need to follow the following workflow:
        * Call `reset`
        * Set the params using `params`
        * For each triplet of the series, call `add_triplet`
        * To get the final results call `compute_results`
    This workflow can look complex but it allows you to easilly monitor the
    progess of the computation.

    This class is intended to be inherited. You have to pass the gamma name to
    this class constructor (can be for example 'alpha_BT' or 'delta_DE' and you
    must define the following:
        * `_get_gamma_channels_index`: returns the index of the gamma channel
        * `_get_gamma_plot_params`: returns some params for plots
    """

    def __init__(self, gamma_name: str, channel_name) -> None:
        """ Constructor

        Args:
            gamma_name (str): Name of the gamma value to compute
            channel_name (str): Name of the channel used to compute gamma
        """
        self._plot = PlotGenerator()
        self._gamma_name = gamma_name
        self._channel_name = channel_name

        self._params: tuple[BackgroundEngine, float, bool] | None = None
        self._reset_called = True
        self._index = 1
        self._gammas: list[np.ndarray] = []
        self._median_intensities: list[float] = []

    def reset(self) -> None:
        """ Reset the calculator internal state to discard previous results and
        starts computing on a new series.
        """
        self._gammas.clear()
        self._median_intensities.clear()
        self._reset_called = True
        self._index = 1

    def params(
        self, background: BackgroundEngine, discard_low_percentile: float = 0.,
        plot_sequence_details: bool = False
    ) -> None:
        """ Set the parameters that will be used for the futur calls.

        You can't change the parameters in the middle of a series computation.

        Args:
            background (BackgroundEngine): backgroung engien to use
            discard_low_percentile (float): percentile of pixels to discard
                under this value, after applying the mask.
            plot_sequence_details (float): True to plot the hist2d and gamma
                figures for each dequences

        Raises:
            QtfException: Series was not reset
        """
        if not self._reset_called:
            err = 'You need to call `reset` before settings new parameters'
            raise QtfException(err)

        self._params = (
            background, discard_low_percentile, plot_sequence_details,
        )

    def add_triplet(
        self, triplet: Triplet, folder: str = ''
    ) -> dict[str, Figure]:
        """ Add the given triplet to the series computation.

        This will perform all the computation possible on the given triplet
        and store the results internally for future analysis.

        Args:
            triplet (Triplet): Triplet to add to the series computation
            folder (str, optional): If set, will display the triplet folder in
                the plot. Default to ''

        Raises:
            QtfException: No params were set

        Returns:
            dict[str, Figure]: Figures associated with the triplet if
                plot_sequence_details is set to True. Otherwise the dictionary
                is empty. The keys are:
                * 'hist_2d': figure plotting the 2d histogram
                * 'gamma': figure containing the gamma image
        """
        if self._params is None:
            err = 'You need to call `params` before calling `add_triplet`'
            raise QtfException(err)
        self._reset_called = False

        gammas, median_intensities, figures = \
            self._compute_and_extract_gammas(triplet, *self._params, folder)

        self._gammas.append(gammas)
        self._median_intensities.append(median_intensities)
        self._index += 1

        return figures

    def compute_results(self) -> tuple[float, float, int, dict[str, Figure]]:
        """ Compute the Gamma value and the standard deviation using the data
        computed on all the triplet added to the series computation.

        Returns:
            tuple[float, float, int, dict[str, Any]]:
                The median of all Gamma value computed
                The Standard Deviation
                The Number of pixels used to compute the median gamma
                Figures detailing the data. keys are 'boxplot' and 'scatter'
        """
        if self._params is None:
            err = 'You need to call `params` before calling `compute_results`'
            raise QtfException(err)
        if len(self._gammas) == 0:
            return 0.0, 0.0, 0, {}

        # Compute gamma_median, gamma_std and gamma_nb_pix
        gammas_array = np.concatenate([np.array(i) for i in self._gammas])
        gamma_median = np.round(np.median(gammas_array), 3)
        # Compute the standard deviation of gamma over all pixels
        # We get rid of zero values coming from NaN
        # TODO: check wether we also need to get rid of those values for the
        # median?? Median is less sensitive to outliers
        gamma_std = np.round(np.std(gammas_array > 0.0), 3)
        gamma_nb_pix = len(gammas_array)

        # Create plots
        boxplot, scatter = self._summary_plots(
            self._gammas, self._median_intensities
        )
        figures = {
            'boxplot': boxplot,
            'scatter': scatter,
        }

        return float(gamma_median), float(gamma_std), gamma_nb_pix, figures

    def _compute_and_extract_gammas(
        self,
        triplet: Triplet,
        background: BackgroundEngine,
        discard_low_percentile: float = 0.,
        plot_sequence_details: bool = False,
        folder: str = ''
    ) -> tuple[np.ndarray, float, dict[str, Figure]]:
        """ Compute the gamma value for the given triplet. The gamma returned
        represents only the values within a mask. Return also the median
        intensities within the same mask.

        The mask is created from the triplet mask. It is then improved removing
        some irrelevant values and discarding the given low percentile pixels.

        Args:
            series (QtfSeries): Series to use to compute the gamma
            bckg_gamma (float): backgroung of the gamma channel
            bckg_da (float): backgroung of the da channel
            discard_low_percentile (float): percentile of pixels to discard
                under this value, after applying the mask.
            plot_sequence_details (float): True to plot the hist2d and gamma
                figures for each dequences
            folder (str, optional): If set, will display the triplet folder in
                the plot. Default to ''

        Returns:
            tuple[np.ndarray, float, dict[str, Figure]]:
               Tuple value with:
                    * Gammas values for each sequence within the computed mask.
                        Array is dimension 1
                    * The median intensity for each sequence whithin the mask.
                        Array is dimension 1
                    * The figures associated to each sequence, if
                        plot_sequence_details is set to True. The keys are
                        * 'hist_2d': figure plotting the 2d histogram
                        * 'gamma': figure containing the gamma image
        """
        mask = triplet.mask_cell

        # substract background
        triplet_np = substract_background(triplet, background)

        # select channels
        channel = triplet_np[self._get_gamma_channels_index()]
        da = triplet_np[1]

        # Compute Gamma
        gamma = mfunc.gamma(channel, da)

        # Compute Mask
        new_mask = mfunc.clean_mask(mask, channel, gamma,
                                    discard_low_percentile)

        # Extract data from mask
        masked_gamma = gamma[new_mask]
        masked_intensity = channel[new_mask]

        # Plot histogram (itensity / gamme) and gamma
        figures: dict[str, Figure] = {}
        if plot_sequence_details:
            figures = self._detail_seq_plot(
                self._index, gamma, masked_gamma, masked_intensity, folder
            )

        return masked_gamma, float(np.median(masked_intensity)), figures

    def _summary_plots(
        self, seq_gammas: list[np.ndarray], seq_intensities_median: list[float]
    ) -> tuple[Figure, Figure]:
        """ Plot the summary figures.

        The summary figures are:
            * the Boxplot of gammas per sequence
            * The scatter plot of median gamma per sequence with regards to
                medium intensity per sequence

        Args:
            seq_gammas (list[np.ndarray]): the gamma computed per sequence
            seq_intensities_median (list[float]): the median intensity on the
                gamma channel per sequence

        Returns:
            tuple[Figure, Figure]: The two figures created
        """
        seq_gamma_median = [float(np.median(g)) for g in seq_gammas]
        mean_seq_gamma_median = np.mean(seq_gamma_median)
        std_seq_gamma_median = np.std(seq_gamma_median)
        boxplot_subtitle = f"Median's mean = {mean_seq_gamma_median:.3f} / " \
                           f"Median's std = {std_seq_gamma_median:.3f}"
        fig_boxplot = self._plot.boxplot_seq_overview(
            self._gamma_name, seq_gammas, boxplot_subtitle
        )
        fig_scatter = self._plot.scatterplot_signal_intensity(
            'median intensity', seq_intensities_median,
            f'median {self._gamma_name[0].upper() + self._gamma_name[1:]}',
            seq_gamma_median
        )
        return fig_boxplot, fig_scatter

    def _detail_seq_plot(
        self, index: int, gamma: np.ndarray,  masked_gamma: np.ndarray,
        seq_intensity: np.ndarray, folder: str = '',
    ) -> dict[str, Figure]:
        """ Plot the figure representing the details of the specific sequence.

        Args:
            index (int): index of the sequence in the process
            gamma (np.ndarray): The gamma computed
            masked_gamma (np.ndarray): The gamma values extracted from the mask
            seq_intensity (np.ndarray): The intensity values extracted from
                the mask
            folder (str, optional): If set, will display the triplet folder in
                the plot. Default to ''

        Returns:
            dict[str, str | Figure]: The plot in the form of a dict with:
                * 'index': index of the sequence
                * 'hist_2d': 2d histogram figure
                * ''gamma'': gamma image figure
        """
        # Subtitles
        hist_2d_subtitle = f'Sequence: {index} - '
        if folder != '':
            hist_2d_subtitle += f'Folder: {folder} - '
        hist_2d_subtitle += f'median({self._gamma_name}): ' \
                            f'{np.median(masked_gamma):.3f}'
        img_subtitle = f'Sequence: {index}'
        if folder != '':
            img_subtitle += f' - Folder: {folder}'

        # Hist 2d
        hist_2d_fig = self._plot.hist2d_signal_intensity(
            seq_intensity, masked_gamma,
            f'I_{self._channel_name}', self._gamma_name,
            range='minimaxi',
            title=f'Dependence of {self._gamma_name} on intensity '
                  f'I_{self._channel_name}',
            subtitle=hist_2d_subtitle
        )

        # Img
        range, nticks = self._get_gamma_plot_params()
        gamma_fig = self._plot.image_with_colorbar(
            gamma,
            title=self._gamma_name.title(),
            subtitle=img_subtitle,
            range=range, nticks=nticks
        )

        # Returns
        figures: dict[str, Figure] = {
            'hist_2d': hist_2d_fig,
            'gamma': gamma_fig
        }
        return figures

    @abc.abstractmethod
    def _get_gamma_channels_index(self) -> int:
        """ Return the gama channels index associated with the given sequence.

        Returns:
            int: The gamma channels index
        """
        pass

    @abc.abstractmethod
    def _get_gamma_plot_params(self) -> tuple[tuple[float, float], int]:
        """ Get the range and nticks params to give to the mfunction to plot
        the gamma image

        Args:
            seq (TripletSequence): The associated sequence

        Returns:
            tuple[tuple[float, float], int]: range, nticks
        """
        pass
