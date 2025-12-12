from quanti_fret.core import QtfException

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import ImageGrid  # type: ignore
import numpy as np


DataRange = str | tuple[float, float]


class PlotGenerator:
    """ Provide a set of methods to plot figures for the QuanTI-FRET results
    usig Matplotlib.
    """

    def __init__(self, use_plt: bool = False) -> None:
        """Constructor

        Args:
            use_plt (bool): whether or not to use plt to create figures
        """
        self._figures_size = (15, 8)
        self._title_size = 20
        self._sub_title_size = int(self._title_size * 0.6)
        self._label_size = int(self._title_size * 0.8)
        self._use_plt = use_plt
        # TODO: Smart computation of the two below
        self._path_label_size = int(self._label_size * 0.5)
        self._max_path_length = 25
        self._markers = ['o', 'v', 'x', 's', '^', 'D', '*', '+']

    def boxplot_seq_overview(
        self, signal_name: str, signal: list[np.ndarray], subtitle: str = ''
    ) -> Figure:
        """ Create a figure with a boxplot plotting information about the given
        signal for each sequence (represented by their index).

        Args:
            signal_name (str): Name of the signal
            signal (list[np.ndarray]): Signal to extract information from.
                Must be a list of one array per sequence, in the same order
                than the one returned by the series iterator.
            subtitle (str): Optional subtitle to print onthe figure

        Returns:
            Figure: The figure created
        """
        # Create figure
        title = f'{signal_name[0].upper() + signal_name[1:]}' \
                ' overview for each sequence'
        fig = self._get_figure(title, subtitle)

        # Boxplot
        ax = fig.add_subplot()
        ax.boxplot(signal, showmeans=True)
        ax.set_xlabel('Sequences Index', fontsize=self._label_size)
        ax.set_ylabel(signal_name, fontsize=self._label_size)
        ax.tick_params(axis='x', labelsize=self._path_label_size)

        return fig

    def scatterplot(
        self,
        x_name: str, x_signal: np.ndarray,
        y_name: str, y_signal: np.ndarray,
        legends: list[str] = [],
        title: str = '',
        subtitle: str = '',
        integer_on_x: bool = False,
        integer_on_y: bool = False,
    ) -> Figure:
        """ Create a scatter plot figure.

        Args:
            x_name (str): Name of the X axis
            x_signal (list[np.ndarray]): Data of the X axis
            y_name (str): Name of the Y axis
            y_signal (list[np.ndarray]): Data of the Y axis. Can be a 1d
                data or 2d data to plot with differents markers and colors
            legends (list[str]): Legend to print for each data on the Y axis.
                If not set, no legends will be printed
            title (str): title of the figure
            subtitle (str): subtitle of the figure
            integer_on_x (bool): True to force integer values on X axis
            integer_on_y (bool): True to force integer values on Y axis

        Returns:
            Figure: The figure created
        """
        # Check Y signal
        if y_signal.ndim > 2:
            raise QtfException('Y labels cannot be higher dimension than 2')
        elif y_signal.ndim == 1:
            y_signal = np.expand_dims(y_signal, axis=0)
        else:
            y_signal = y_signal.T

        # Check legend
        legend_l = len(legends)
        y_signal_l = len(y_signal)
        if not legend_l == 0:
            if legend_l != y_signal_l:
                err = f'Length of legends ({legend_l}) and y signal ' \
                      f'({y_signal_l}) do not match'
                raise QtfException(err)
        else:
            legends = ['' for _ in y_signal]

        # Create figure
        fig = self._get_figure(title, subtitle)

        # scatter
        ax = fig.add_subplot(111)
        ax.set_xlabel(x_name, fontsize=self._label_size)
        ax.set_ylabel(y_name, fontsize=self._label_size)
        if integer_on_x:
            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        if integer_on_y:
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # Scatter for each Y signal
        index_marker = 0
        for signal, legend in zip(y_signal, legends):
            ax.scatter(x_signal, signal, label=legend,
                       marker=self._markers[index_marker])
            index_marker = (index_marker + 1) % len(self._markers)

        # Plot legend
        if legend_l > 0:
            ax.legend(loc='upper left')

        return fig

    def scatterplot_signal_intensity(
        self,
        x_name: str, x_signal: list[float],
        y_name: str, y_signal: list[float]
    ) -> Figure:
        """ Function to ease the call of `self.scatter` to plot a 1d signal vs
        intensity scatter.

        Args:
            x_name (str): Name of the X axis
            x_signal (list[float]): Data of the X axis
            y_name (str): Name of the Y axis
            y_signal (list[float]): Data of the Y axis

        Returns:
            Figure: The figure created
        """
        title = f'{y_name} versus {x_name}'
        x_signal_np = np.array(x_signal)
        y_signal_np = np.array(y_signal)
        fig = self.scatterplot(x_name, x_signal_np, y_name, y_signal_np,
                               title=title)
        return fig

    def scatterplot_3d(
        self,
        x_name: str, x_signal: np.ndarray,
        y_name: str, y_signal: np.ndarray,
        z_name: str, z_signal: np.ndarray,
        plane_x_y_factors: tuple[float, float] | None = None,
        title: str = '',
        subtitle: str = '',
    ) -> Figure:
        """ Create a 3D scatter plot figure.

        Args:
            x_name (str): Name of the X axis
            x_signal (list[np.ndarray]): Data of the X axis
            y_name (str): Name of the Y axis
            y_signal (list[np.ndarray]): Data of the Y axis.
            z_name (str): Name of the Z axis
            z_signal (list[np.ndarray]): Data of the Z axis.
            title (str): title of the figure
            subtitle (str): subtitle of the figure

        Returns:
            Figure: The figure created
        """
        # Create figure
        fig = self._get_figure(title, subtitle)

        # scatter
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel(x_name, fontsize=self._label_size)
        ax.set_ylabel(y_name, fontsize=self._label_size)
        ax.set_zlabel(z_name, fontsize=self._label_size)  # type: ignore

        # Plane
        if plane_x_y_factors is not None:
            X = np.linspace(1, x_signal.max(), 200)
            Y = np.linspace(1, y_signal.max(), 200)
            X, Y = np.meshgrid(X, Y)
            Z = plane_x_y_factors[0]*X + plane_x_y_factors[1]*Y
            ax.plot_wireframe(  # type: ignore
                X, Y, Z, linewidth=0.2, rstride=5, cstride=5, color='grey'
            )

        # Scatter for each Y signal
        ax.scatter(x_signal, y_signal, z_signal)

        return fig

    def hist2d_signal_intensity(
        self,
        dataX: np.ndarray,
        dataY: np.ndarray,
        xlabel: str,
        ylabel: str,
        range: str | tuple[DataRange, DataRange] = ((0, 100), (0, 100)),
        percentile_range: tuple[tuple[float, float], tuple[float, float]] =
        ((1., 99.), (1., 99.)),
        normed_hist: bool = False,
        title: str = '',
        subtitle: str = ''
    ) -> Figure:
        """ Plots a 2D histogram from dataX and dataY.

        This will create 3 plots:
            * The 2D histogram itself
            * The 1D histogram for the X data
            * The 1D histogram for the Y data

        Args:
            dataX (np.ndarray): Data on X value (must be same size than dataY)
            dataY (np.ndarray): Data on Y value (must be same size than dataX)
            xlabel (str): Label for the X axis
            ylabel (str): Label for the Y axis
            range (str | tuple[tuple[float, float], tuple[float, float]]):
                Range of the data to display:
                * 'minimaxi': min and max of each data set are choosen,
                * 'percentile': range is between the first and the last
                    percentile (1-99)
                * ((xmin, xmax), (ymin, ymax)): custom range
            percentile_range (tuple[tuple[float, float], tuple[float, float]]):
                percentile in between the range will be set if
                `range` == 'percentile'.
            normed_hist: Normalize or not the histogram
            title (str): Title of the graph
            subtitle (str): Subtitle of the graph

        Returns:
            Figure: The figure created
        """
        # Clean inputs
        dataX = dataX.ravel()
        dataY = dataY.ravel()
        range_v = self._get_range_XY(dataX, dataY, range, percentile_range)

        # Generate 2D histogram
        H, xedges, yedges = np.histogram2d(
            dataX, dataY, bins=100, range=range_v, density=normed_hist
        )
        # Transpose as x is first dimension and y seconds, and we want the
        # opposite.
        H = H.T  # Let each row list bins with common y range.
        # Mask zeros for nicer display
        Hmasked = np.ma.masked_where(H == 0, H)

        # Create the figure
        fig = self._get_figure(title, subtitle)

        # Create the grid
        gs = GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[1, 3])
        gs.update(wspace=0.1, hspace=0.1)

        # Create the joint histogram
        ax_joint = fig.add_subplot(gs[1, 0])
        ax_joint.pcolormesh(xedges, yedges, Hmasked, cmap='plasma')
        ax_joint.set_xticks(np.linspace(range_v[0][0], range_v[0][1], 6))
        ax_joint.set_yticks(np.linspace(range_v[1][0], range_v[1][1], 6))
        ax_joint.set_xlabel(xlabel, fontsize=self._label_size)
        ax_joint.set_ylabel(ylabel, fontsize=self._label_size)

        # Create individual histograms for X
        ax_x_only = fig.add_subplot(gs[0, 0])
        ax_x_only.hist(dataX, bins=100, range=range_v[0], density=normed_hist)
        ax_x_only.set_xlim(range_v[0][0], range_v[0][1])
        ax_x_only.xaxis.set_ticklabels([])
        ax_x_only.set_ylabel(xlabel + ' count', fontsize=self._label_size)

        # Create individual histograms for Y
        ax_y_only = fig.add_subplot(gs[1, 1])
        ax_y_only.hist(dataY, bins=100, range=range_v[1], density=normed_hist,
                       orientation="horizontal")
        ax_y_only.xaxis.tick_top()
        ax_y_only.yaxis.set_ticklabels([])
        ax_y_only.set_ylim(range_v[1][0], range_v[1][1])
        ax_y_only.set_xlabel(ylabel + ' count', fontsize=self._label_size)

        return fig

    def image_with_colorbar(
        self,
        image: np.ndarray,
        title: str = '',
        subtitle: str = '',
        range: DataRange = 'percentile',
        percentile_range: tuple[float, float] = (1, 99),
        mask: np.ndarray | None = None,
        nticks: int = 10
    ) -> Figure:
        """
        Plot in a figure an image with its colorbar.

        Args:
            image (np.ndarray): Image to plot
            title (str): Title of the plot
            subtitle (str): Subtitle of the plot
            range (str | tuple[float, float]): Range of the colomap. It can be:
                * 'percentile': Range is computed in between the two percentile
                    set in percentile_range
                * 'minimaxi': range is minimum to maximul values of the image
                * (vmin, vmax): use custom values
            percentile_range (tuple[float, float]): Percentile in between to
                the range will be set if `range` == 'percentile'.
            mask (np.ndarray | None): if not None, and the range is a str, it
                is the area used to compute the range
            nticks (int): Number of ticks to display

        Returns:
            Figure: The figure created
        """
        # Compute settings
        if mask is None:
            masked_image = image
        else:
            masked_image = image[mask]
        range_v = self._get_range_single(masked_image, range, percentile_range)

        # Create figure and grid
        fig = self._get_figure(title, subtitle)
        grid = ImageGrid(
            fig,
            111,
            nrows_ncols=(1, 1),
            axes_pad=0.15,
            share_all=False,
            cbar_location="right",
            cbar_mode="each",
            cbar_size="5%",
            cbar_pad=0.15
        )

        # Image
        im = grid[0].imshow(
            image, interpolation='none', cmap='inferno', vmin=range_v[0],
            vmax=range_v[1]
        )
        grid[0].axis('off')

        # Colorbar
        cbar = grid[0].cax.colorbar(im)
        cbar.ax.tick_params(labelsize=self._label_size)
        cbar.ax.yaxis.set_major_locator(ticker.LinearLocator(nticks))

        return fig

    def _get_figure(self, title: str = '', subtitle: str = '') -> Figure:
        """ Get a figure with the given title and subtitle.

        Args:
            title (str, optional): Title. Defaults to ''.
            subtitle (str, optional): Subtitle. Defaults to ''.

        Returns:
            Figure: Newly created figure
        """
        if self._use_plt:
            fig = plt.figure(figsize=self._figures_size)
        else:
            fig = Figure(figsize=self._figures_size)

        if title != '':
            fig.suptitle(title, fontsize=self._title_size)
        if subtitle != '':
            fig.text(0.5, 0.91, subtitle, ha='center',
                     fontsize=self._sub_title_size, style='italic')
        return fig

    def _get_range_single(
        self,
        data: np.ndarray,
        range: DataRange,
        percentile_range: tuple[float, float] = (1., 99.),
    ) -> tuple[float, float]:
        """ Compute the range to display for a single dataset.

        The range can be:
            * 'minimaxi': min and max of the dataset are choosen for range
            * 'percentile': range is between the two percentile set in
                percentile_range parameter for each data set
            * (min, max): custom range
        Args:
            data (np.ndarray): Data to compute the range on
            range (DataRange): range asked. Can be 'minimaxi','percentile'
                or a custom range
            percentile_range (tuple[float, float]):
                percentile in between the range will be set if
                `range` == 'percentile'.

        Raises:
            QtfException: The range asked is incorrect

        Returns:
            tuple[float, float]: The range calculated
        """
        if type(range) is tuple:
            if range[0] > range[1]:
                msg = f'Min range ({range[0]}) is bigger than max range ' \
                      f'({range[1]})'
                raise QtfException(msg)
            range_v = range
        else:
            if range == 'minimaxi':
                range_v = (data.min(), data.max())
            elif range == 'percentile':
                min_percentile = percentile_range[0]
                max_percentile = percentile_range[1]
                if min_percentile > max_percentile:
                    msg = f'Min percentile_range ({min_percentile}) is ' \
                          f'bigger than max percentile_range ' \
                          f'({max_percentile})'
                    raise QtfException(msg)
                if min_percentile < 0 or min_percentile > 100:
                    msg = f'Bad value for min percentile_range ' \
                          f'({min_percentile}). Must be between 0 and 100. '
                    raise QtfException(msg)
                if max_percentile > 100:
                    msg = f'Bad value for max percentile_range ' \
                          f'({max_percentile}). Must be between 0 and 100. '
                    raise QtfException(msg)
                range_v = (
                    float(np.nanpercentile(data, min_percentile)),
                    float(np.nanpercentile(data, max_percentile))
                )
            else:
                msg = 'Invalid range, must be (xmin, xmax) or in ' \
                      '["minimaxi", "percentile"]'
                raise QtfException(msg)

        return range_v

    def _get_range_XY(
        self,
        dataX: np.ndarray,
        dataY: np.ndarray,
        range: str | tuple[DataRange, DataRange],
        percentile_range: tuple[tuple[float, float], tuple[float, float]] =
        ((1., 99.), (1., 99.)),
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """ Compute the range to display for a 2D figure with two separated
        dataset.

        The range can be:
            * 'minimaxi': min and max of each data set are choosen
            * 'percentile': range is between the two percentile set in
                percentile_range for each data set
            * ((xmin, xmax), (ymin, ymax)): custom range

        Args:
            dataX (np.ndarray): Data on the X axis
            dataY (np.ndarray): Data on the Y axis
            range (str | tuple[tuple[float, float], tuple[float, float]]):
                Range asked. Can be 'minimaxi', 'percentile' or a custom range
            percentile_range (tuple[tuple[float, float], tuple[float, float]]):
                percentile in between the range will be set if
                `range` == 'percentile'.

        Raises:
            QtfException: The range asked is incorrect

        Returns:
            tuple[tuple[float, float], tuple[float, float]]:
                The range calculated
        """
        range_x: str | tuple[float, float]
        range_y: str | tuple[float, float]
        if type(range) is tuple:
            range_x = range[0]
            range_y = range[1]
        elif type(range) is str:
            range_x = range
            range_y = range
        else:
            raise QtfException(f'Invalid type for range ({range})')
        range_v_x = self._get_range_single(dataX, range_x, percentile_range[0])
        range_v_y = self._get_range_single(dataY, range_y, percentile_range[1])
        range_v = (range_v_x, range_v_y)

        return range_v
