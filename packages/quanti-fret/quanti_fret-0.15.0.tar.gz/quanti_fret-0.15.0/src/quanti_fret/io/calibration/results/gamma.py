from quanti_fret.core import SeriesIterator
from quanti_fret.io.base.results import StageResults
from quanti_fret.io.base.validate import (
    BackgroundEngineValidator, BooleanValidator, FloatValidator,
    IntValidator, StringValidator, Validator
)

from typing import Any
import pickle
from pathlib import Path


class GammaResults(StageResults):
    """ Manage the saving of the settings and results of the Gamma stages
    (BT and DE)

    Tuples descriptions
        * settings:
            * series name (str)
            * series used (QtfSeries): transformed in size of the series (int)
            * background used (BackgroundEngine)
            * discard low percentile (float)
            * plot sequence details (bool)
        * results:
            * gamma (float)
            * standard deviation (float)
            * Number of pixels used for gamma (float)
        * extras:
            * figures created (dict)
                * boxplot (Figure)
                * scatter (Figure)
        * triplets results: None
        * triplets extras:
            * figures created (dict)
                * hist_2d (Figure)
                * gamma (Figure)
    """

    VALIDATORS: dict[str, dict[str, Validator]] = {
        'settings': {
            'series': StringValidator(),
            'nb_seq': IntValidator(min=0),
            'background': BackgroundEngineValidator(),
            'discard_low_percentile': FloatValidator(min=0.0, max=100.0),
            'plot_seq_details': BooleanValidator(),
        },
        'results': {
            'gamma': FloatValidator(),
            'std': FloatValidator(),
            'nb_pix': IntValidator(min=0)
        }
    }

    def __init__(
        self, output_dir: Path, gamma_name: str, std_name: str
    ) -> None:
        """Constructor

        This will duplicate the `self.VALIDATORS` and change the keys
        `gamma`, and `std` to their name in the BT or DE results.

        Args:
            output_dir (Path): Path to the output directory
            gamma_name (str): Name of the gamma computed
            std_name (str): Name of the std computed
            std_name (str): Name of channel used for the gamma computation
        """
        self._gamma_name = gamma_name
        self._std_name = std_name

        # Create the new validators
        # (We can't modify self.VALIDATORS as it will be modify for all
        # instances. And we can't just pop out values as we want to keep order)
        val_settings = self.VALIDATORS['settings']
        val_results = self.VALIDATORS['results']
        validators: dict[str, dict[str, Validator]] = {
            'settings': {
                'series': val_settings['series'],
                'nb_seq': val_settings['nb_seq'],
                'background': val_settings['background'],
                'discard_low_percentile':
                    val_settings['discard_low_percentile'],
                'plot_seq_details': val_settings['plot_seq_details'],
            },
            'results': {
                self._gamma_name: val_results['gamma'],
                self._std_name: val_results['std'],
                'nb_pix': val_results['nb_pix']
            }
        }
        super().__init__(output_dir, validators)

    def save_triplet(
        self, sit: SeriesIterator, results: tuple[Any, ...]
    ) -> None:
        """ Save the results of the computation of a single triplet.

        Values saved and their order are described in each StageResults
        implementation class.

        We expect the results to be in the same order than the one returned by
        the function computing one triplet at a time.

        The final optional element of the tuple can be a dictionary containing
        all the extras values to save to the folder. Each keys can be optional.

        Args:
            sit (SeriesIterator): The series iterator to get the triplet id.
                Make sure that the sit is in the proper state.
            results (tuple[Any, ...]): Results to save
        """
        figures = results[0]
        if len(figures) != 0:
            id_str = self._get_triplet_folder_name(sit.current, sit.size)

            # Save PNG
            folder = self._output_dir / 'Details'
            folder.mkdir(parents=True, exist_ok=True)
            hist_2d_path = folder / f'{id_str}_hist2d.png'
            gamma_path = folder / f'{id_str}_{self._gamma_name}.png'
            figures['hist_2d'].savefig(hist_2d_path)
            figures['gamma'].savefig(gamma_path)

            # Save Dumps
            folder = self._dumps_dir / 'Details'
            folder.mkdir(parents=True, exist_ok=True)
            hist_2d_path = folder / f'{id_str}_hist2d.pkl'
            gamma_path = folder / f'{id_str}_{self._gamma_name}.pkl'
            with open(hist_2d_path, 'wb') as f:
                pickle.dump(figures['hist_2d'], f)
            with open(gamma_path, 'wb') as f:
                pickle.dump(figures['gamma'], f)

        self._save_triplet_id(sit)

    def get_stage_extras(
        self, key: str | list[str] | None = None, check_only: bool = False
    ) -> dict[str, Any]:
        """ Get the extra results of the given stage

        If exists, the returned value is the same dictionary as the one passed
        as last element of the result parameter to `save_stage`.

        You can load only one extra value by specifying the key to load (or the
        list of keys for nested disctionaries)

        if `check_only` is set to True, values of the dictionary will be
        booleans telling the user if the extra value exists or not.

        See class comments for more information on the dictionary layout

        Args:
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        # Check inputs
        default_value = None
        if check_only:
            default_value = False
        self._check_stage_extra_key(key)
        if type(key) is list:
            key_str = key[0]
        elif key is None:
            key_str = ''
        else:
            assert type(key) is str
            key_str = key
        if key is None:
            extras = {
                'boxplot': default_value,
                'scatter': default_value,
            }
        else:
            assert type(key_str) is str
            extras = {
                key_str: default_value
            }

        # Load extra
        if self._dumps_dir.is_dir():
            # Boxplot
            if key is None or key_str == 'boxplot':
                boxplot_file = self._dumps_dir / 'boxplot.pkl'
                if boxplot_file.is_file():
                    if check_only:
                        extras['boxplot'] = True
                    else:
                        with open(boxplot_file, 'rb') as f:
                            extras['boxplot'] = pickle.load(f)

            # Scatter
            if key is None or key_str == 'scatter':
                scatter_file = self._dumps_dir / 'scatter.pkl'
                if scatter_file.is_file():
                    if check_only:
                        extras['scatter'] = True
                    else:
                        with open(scatter_file, 'rb') as f:
                            extras['scatter'] = pickle.load(f)

        return extras

    def get_triplet_extras(
        self,
        id: int,
        key: str | list[str] | None = None,
        check_only: bool = False
    ) -> dict[str, Any]:
        """ Get the extra results of a computation of a given triplet

        If exists, the returned value is the same dictionary as the one passed
        as last element of the result parameter of `save_triplet`.

        You can load only one extra value by specifying the key to load (or the
        list of keys for nested disctionaries)

        if `check_only` is set to True, values of the dictionary will be
        booleans telling the user if the extra value exists or not.

        See class comments for more information on the dictionary layout

        Args:
            id (int): Id of the triplet to retrieve
            key (str | list[str] | None, optional): If not None, load only the
                element associated with the given key (or with the given keys
                if the dictionary is nested. Default is None.
            check_only (bool, optional): If True, will only check if the extras
                results exists. Default is False

        Raise:
            QtfException: The keys are invalid

        Returns:
            dict[str, Any]: Dictionary containing the extra results
        """
        # Check inputs
        if check_only:
            default_value = False
        else:
            default_value = None
        self._check_triplet_extra_key(key)
        if type(key) is list:
            key_str = key[0]
        elif key is None:
            key_str = ''
        else:
            assert type(key) is str
            key_str = key
        if key is None:
            extras = {
                'hist_2d': default_value,
                'gamma': default_value,
            }
        else:
            assert type(key_str) is str
            extras = {
                key_str: default_value
            }

        # Load extra
        ids = self.get_triplet_ids()
        id_str = self._get_triplet_folder_name(id, ids[-1][0])
        folder = self._dumps_dir / 'Details'
        if folder.is_dir():
            # Hist2d
            if key is None or key_str == 'hist_2d':
                hist_2d_path = folder / f'{id_str}_hist2d.pkl'
                if hist_2d_path.is_file():
                    if check_only:
                        extras['hist_2d'] = True
                    else:
                        with open(hist_2d_path, 'rb') as f:
                            extras['hist_2d'] = pickle.load(f)

            # Gamma
            if key is None or key_str == 'gamma':
                gamma_path = folder / f'{id_str}_{self._gamma_name}.pkl'
                if gamma_path.is_file():
                    if check_only:
                        extras['gamma'] = True
                    else:
                        with open(gamma_path, 'rb') as f:
                            extras['gamma'] = pickle.load(f)

        return extras

    def _get_json_results(self, results: tuple[Any, ...]) -> tuple[Any, ...]:
        """ Return all the results that are supposed to be in the json file.

        Remove the last settings element that is a figure

        Args:
            results (tuple[Any, ...]): results to save

        Results:
            tuple[Any, ...]: Results to put in the JSON
        """
        return results[:-1]

    def _save_extra(
        self, settings: tuple[Any, ...], results: tuple[Any, ...]
    ) -> None:
        """ Write every results that are not in the JSON.

        Save the figures and the CSVs

        Args:
            settings (tuple[Any, ...]): Settings to save
            results (tuple[Any, ...]): All the results to save, included the
                one already saved in the JSON.
        """
        figures: dict[str, Any] = results[-1]
        self._dumps_dir.mkdir(exist_ok=True, parents=True)

        # Box plot
        figures['boxplot'].savefig(self._output_dir / 'boxplot.png')
        with open(self._dumps_dir / 'boxplot.pkl', 'wb') as f:
            pickle.dump(figures['boxplot'], f)

        # Scatter plot
        figures['scatter'].savefig(self._output_dir / 'scatter.png')
        with open(self._dumps_dir / 'scatter.pkl', 'wb') as f:
            pickle.dump(figures['scatter'], f)

    def _check_stage_extra_key(self, key: str | list[str] | None) -> None:
        """ Check if the required stage extra key is valid

        Args:
            key (str | list[str] | None): key to check

        Raises:
            QtfException: the key is invalid
        """
        self._check_extra_key(
            key,
            [['boxplot'], ['scatter']],
            'stage'
        )

    def _check_triplet_extra_key(self, key: str | list[str] | None) -> None:
        """ Check if the required triplet extra key is valid

        Args:
            key (str | list[str] | None): key to check

        Raises:
            QtfException: the key is invalid
        """
        self._check_extra_key(
            key,
            [['hist_2d'], ['gamma']],
            'triplet'
        )
