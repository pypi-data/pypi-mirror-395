from quanti_fret.core.exception import QtfException
from quanti_fret.core.sequence import TripletSequence

from typing import Iterator, TYPE_CHECKING
if TYPE_CHECKING:
    from quanti_fret.core.iterator import SeriesIterator


class QtfSeries:
    """ Represent a series of sequences of triplets.

    Can be iterated as a list, and provide usefull functions to get information
    on the set of sequences.

    If you want to iterate over all the triplets of the series, either by
    sampling each sequence of not, it is suggested to use the `iterator` method
    that returns a SeriesIterator.
    """

    def __init__(self, sequences: list[TripletSequence]) -> None:
        """ Constructor

        Args:
            sequences (list[TripletSequence]): The list of sequences associated
                with the series
        """
        self._sequences = sequences

    @property
    def size(self):
        """ Returns the number of sequences in the series
        """
        return len(self._sequences)

    @property
    def nb_triplets(self):
        """ Returns the number of triplets in the series
        """
        return sum(s.size for s in self._sequences)

    def iterator(self, sample_sequences: bool = False) -> 'SeriesIterator':
        """ Get the iterator associated with the series

        Args:
            sample_sequences (bool, optional): If True, will sample the
                sequences to only get one triplet per series. Defaults to
                False.

        Returns:
            SeriesIterator: The iterator
        """
        # prevent circular import
        from quanti_fret.core.iterator import SeriesIterator
        return SeriesIterator(self, sample_sequences)

    def have_all_mask_bckg(self) -> bool:
        """ Check if all the Triplet have a background mask

        Returns:
            bool: True if all triplet have a background mask
        """
        return all([s.have_all_mask_bckg() for s in self._sequences])

    def have_all_mask_cell(self) -> bool:
        """ Check if all the Triplet have a cell mask

        Returns:
            bool: True if all triplet have a cell mask
        """
        return all([s.have_all_mask_cell() for s in self._sequences])

    def get_only_enabled(self) -> 'QtfSeries':
        """ Returns a series containing only sequences that are enabled
        """
        return QtfSeries([s for s in self._sequences if s.is_enabled()])

    def __add__(self, o: 'QtfSeries') -> 'QtfSeries':
        new_list = self._sequences + o._sequences
        return QtfSeries(new_list)

    def __iter__(self) -> Iterator[TripletSequence]:
        for triplet_seq in self._sequences:
            yield triplet_seq

    def __getitem__(self, index: int) -> TripletSequence:
        if index > len(self._sequences):
            raise QtfException('Index out of range')
        return self._sequences[index]
