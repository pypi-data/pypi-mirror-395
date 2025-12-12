from quanti_fret.core.exception import QtfException
from quanti_fret.core.series import QtfSeries
from quanti_fret.core.sequence import TripletSequence
from quanti_fret.core.triplet import Triplet

from typing import Iterator


class SeriesIterator:
    """ Iterator to iterate over a series.

    It has two modes:
        - Default: Will iterate over all triplets of all the sequences
        - sample_sequences: Will return one chosen triplet per sequence

    It also gives a bunch of tools to allow the user the know the progress
    of the iteration, and to get an ID of the current triplet being returned

    Current id, sequence id ans triplet id start at 1
    """

    def __init__(
        self, series: QtfSeries, sample_sequences: bool = False
    ) -> None:
        """ Constructor

        Args:
            series (QtfSeries): Series to iterate
            sample_sequences (bool, optional): Whether or not to extract only
                one triplet per sequence. Default to False.
        """
        self._series = series
        self._sample_sequences = sample_sequences

        self._sequence_index: int
        self._triplet_index: int
        self._current_index: int
        self._reset()

    def __iter__(self) -> Iterator[Triplet]:
        """ Iterate though the series.

        If `sample_sequences` is set to false, will iterate on all the triplets
        of all the sequences. Otherwise will select the fist triplet of
        every sequences.

        Yields:
            Iterator[Triplet]: The next triplet
        """
        while self._sequence_index < self._series.size:
            # Find next indice
            if not self._sample_sequences:
                if self._sequence_index == -1:
                    self._sequence_index = 0
                    self._triplet_index = 0
                else:
                    current_seq_size = self._series[self._sequence_index].size
                    self._triplet_index += 1
                    if self._triplet_index >= current_seq_size:
                        self._triplet_index = 0
                        self._sequence_index += 1
            else:
                self._sequence_index += 1
                self._triplet_index = self._get_sampled_index()

            # Break if too far
            if self._sequence_index == self._series.size:
                break

            # Avoid empty sequences
            if self._series[self._sequence_index].size == 0:
                continue

            # yield current triplet
            self._current_index += 1
            yield self._series[self._sequence_index][self._triplet_index]

        self._reset()

    @property
    def size(self) -> int:
        """ Returns the number of triplets that the iterator will returns nu
        """
        if self._sample_sequences:
            return sum(seq.size > 0 for seq in self._series)
        else:
            return self._series.nb_triplets

    @property
    def current(self) -> int:
        """ Returns the current Id iterated
        """
        return self._current_index + 1

    @property
    def id(self) -> tuple[int, int, int]:
        """ Returns the id of the current triplet.

        The id returned is a tuple containing in order:
            - The current index in all the iteration process
            - The index of the sequence
            - The index of the tuple in the sequence
        """
        return (
            self.current, self._sequence_index + 1, self._triplet_index + 1
        )

    @property
    def current_sequence(self) -> TripletSequence:
        """ Returns the current sequence iterated
        """
        if self._sequence_index == -1:
            err = 'Cannot call `current_sequence` outside iteration'
            raise QtfException(err)
        return self._series[self._sequence_index]

    @property
    def current_triplet(self) -> Triplet:
        """ Returns the current triplet iterated
        """
        if self._sequence_index == -1:
            err = 'Cannot call `current_triplet` outside iteration'
            raise QtfException(err)
        return self.current_sequence[self._triplet_index]

    def _get_sampled_index(self) -> int:
        """ Get the sampled index of the current sequence.

        For now, returns the first element
        """
        return 0

    def _reset(self) -> None:
        """ Reset the iterator state
        """
        self._sequence_index = -1
        self._triplet_index = -1
        self._current_index = -1
        if self._sample_sequences:
            self._triplet_index = self._get_sampled_index()
