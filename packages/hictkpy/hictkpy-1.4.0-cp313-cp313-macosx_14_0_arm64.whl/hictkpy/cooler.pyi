import os
import pathlib
from typing import overload

import pandas
import pyarrow

import hictkpy
import hictkpy._hictkpy


class SingleCellFile:
    """Class representing a file handle to a .scool file."""

    def __init__(self, path: str | os.PathLike) -> None:
        """Open a single-cell Cooler file (.scool)."""

    def __repr__(self) -> str: ...

    def __enter__(self) -> SingleCellFile: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def close(self) -> None:
        """Manually close the file handle."""

    def resolution(self) -> int:
        """Get the bin size in bp."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def bins(self) -> hictkpy.BinTable:
        """Get table of bins."""

    def attributes(self) -> dict:
        """Get file attributes as a dictionary."""

    def cells(self) -> list[str]:
        """Get the list of available cells."""

    def __getitem__(self, cell_id: str) -> hictkpy._hictkpy.File:
        """Open the Cooler file corresponding to the cell ID given as input."""

class FileWriter:
    """Class representing a file handle to create .cool files."""

    @overload
    def __init__(self, path: str | os.PathLike, chromosomes: dict[str, int], resolution: int, assembly: str = 'unknown', tmpdir: str | os.PathLike = ..., compression_lvl: int = 6) -> None:
        """
        Open a .cool file for writing given a list of chromosomes with their sizes and a resolution.
        """

    @overload
    def __init__(self, path: str | os.PathLike, bins: hictkpy._hictkpy.BinTable, assembly: str = 'unknown', tmpdir: str | os.PathLike = ..., compression_lvl: int = 6) -> None:
        """Open a .cool file for writing given a table of bins."""

    def __repr__(self) -> str: ...

    def __enter__(self) -> FileWriter: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def resolution(self) -> int:
        """Get the resolution in bp."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def bins(self) -> hictkpy.BinTable:
        """Get table of bins."""

    def add_pixels(self, pixels: pandas.DataFrame | pyarrow.Table, sorted: bool = False, validate: bool = True) -> None:
        """
        Add pixels from a pandas.DataFrame or pyarrow.Table containing pixels in COO or BG2 format (i.e. either with columns=[bin1_id, bin2_id, count] or with columns=[chrom1, start1, end1, chrom2, start2, end2, count]).
        When sorted is True, pixels are assumed to be sorted by their genomic coordinates in ascending order.
        When validate is True, hictkpy will perform some basic sanity checks on the given pixels before adding them to the Cooler file.
        """

    def add_pixels_from_dict(self, columns: Dict[str, Iterable[str | int | float]], sorted: bool = False, validate: bool = True) -> None:
        """
        Add pixels from a dictionary containing containing columns corresponding to pixels in COO or BG2 format (i.e. either with keys=[bin1_id, bin2_id, count] or with keys=[chrom1, start1, end1, chrom2, start2, end2, count]).
        When sorted is True, pixels are assumed to be sorted by their genomic coordinates in ascending order.
        When validate is True, hictkpy will perform some basic sanity checks on the given pixels before adding them to the Cooler file.
        """

    def finalize(self, log_lvl: str | None = None, chunk_size: int = 500000, update_frequency: int = 10000000) -> hictkpy._hictkpy.File:
        """Write interactions to file."""

