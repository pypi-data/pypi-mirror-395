from collections.abc import Sequence
import os
import pathlib
from typing import Annotated, overload

import numpy
from numpy.typing import NDArray
import pandas
import pyarrow

import hictkpy
import hictkpy._hictkpy


class FileWriter:
    """Class representing a file handle to create .hic files."""

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolution: int, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one resolution.
        """

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolutions: Sequence[int], assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a list of chromosomes with their sizes and one or more resolutions.
        """

    @overload
    def __init__(self, path: str | os.PathLike, bins: hictkpy._hictkpy.BinTable, assembly: str = 'unknown', n_threads: int = 1, chunk_size: int = 10000000, tmpdir: str | os.PathLike = ..., compression_lvl: int = 10, skip_all_vs_all_matrix: bool = False) -> None:
        """
        Open a .hic file for writing given a BinTable. Only BinTable with a fixed bin size are supported.
        """

    def __repr__(self) -> str: ...

    def __enter__(self) -> FileWriter: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def resolutions(self) -> Annotated[NDArray[numpy.int64], dict(shape=(None,), order='C')]:
        """Get the list of resolutions in bp."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def bins(self, resolution: int) -> hictkpy.BinTable:
        """Get table of bins for the given resolution."""

    def add_pixels(self, pixels: pandas.DataFrame | pyarrow.Table, validate: bool = True) -> None:
        """
        Add pixels from a pandas.DataFrame or pyarrow.Table containing pixels in COO or BG2 format (i.e. either with columns=[bin1_id, bin2_id, count] or with columns=[chrom1, start1, end1, chrom2, start2, end2, count]).
        When sorted is True, pixels are assumed to be sorted by their genomic coordinates in ascending order.
        When validate is True, hictkpy will perform some basic sanity checks on the given pixels before adding them to the .hic file.
        """

    def add_pixels_from_dict(self, columns: Dict[str, Iterable[str | int | float]], validate: bool = True) -> None:
        """
        Add pixels from a dictionary containing containing columns corresponding to pixels in COO or BG2 format (i.e. either with keys=[bin1_id, bin2_id, count] or with keys=[chrom1, start1, end1, chrom2, start2, end2, count]).
        When sorted is True, pixels are assumed to be sorted by their genomic coordinates in ascending order.
        When validate is True, hictkpy will perform some basic sanity checks on the given pixels before adding them to the Cooler file.
        """

    def finalize(self, log_lvl: str | None = None) -> hictkpy._hictkpy.File:
        """Write interactions to file."""

