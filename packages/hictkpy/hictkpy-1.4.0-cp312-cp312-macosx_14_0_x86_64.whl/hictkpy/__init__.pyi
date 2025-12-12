from collections.abc import Sequence
import os
import pathlib
from typing import Annotated, overload

import numpy
from numpy.typing import NDArray
import pandas
import pyarrow
import scipy

from . import cooler as cooler, hic as hic, logging as logging
import hictkpy


__hictk_version__: str = '2.2.0'

def is_cooler(path: str | os.PathLike) -> bool:
    """Test whether path points to a cooler file."""

def is_mcool_file(path: str | os.PathLike) -> bool:
    """Test whether path points to a .mcool file."""

def is_scool_file(path: str | os.PathLike) -> bool:
    """Test whether path points to a .scool file."""

def is_hic(path: str | os.PathLike) -> bool:
    """Test whether path points to a .hic file."""

class Bin:
    """Class representing a genomic Bin (i.e., a BED interval)."""

    @property
    def id(self) -> int:
        """Get the bin ID."""

    @property
    def rel_id(self) -> int:
        """
        Get the relative bin ID (i.e., the ID that uniquely identifies a bin within a chromosome).
        """

    @property
    def chrom(self) -> str:
        """Get the name of the chromosome to which the Bin refers to."""

    @property
    def start(self) -> int:
        """Get the Bin start position."""

    @property
    def end(self) -> int:
        """Get the Bin end position."""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class BinTable:
    """Class representing a table of genomic bins."""

    @overload
    def __init__(self, chroms: dict[str, int], resolution: int) -> None:
        """
        Construct a table of bins given a dictionary mapping chromosomes to their sizes and a resolution.
        """

    @overload
    def __init__(self, bins: pandas.DataFrame) -> None:
        """
        Construct a table of bins from a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    def __repr__(self) -> str: ...

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def resolution(self) -> int:
        """
        Get the bin size for the bin table. Return 0 in case the bin table has a variable bin size.
        """

    def type(self) -> str:
        """
        Get the type of table underlying the BinTable object (i.e. fixed or variable).
        """

    def __len__(self) -> int:
        """Get the number of bins in the bin table."""

    def __iter__(self) -> hictkpy.BinTableIterator:
        """
        Implement iter(self). The resulting iterator yields objects of type hictkpy.Bin.
        """

    @overload
    def get(self, bin_id: int) -> hictkpy.Bin:
        """Get the genomic coordinate given a bin ID."""

    @overload
    def get(self, bin_ids: Sequence[int]) -> pandas.DataFrame:
        """
        Get the genomic coordinates given a sequence of bin IDs. Genomic coordinates are returned as a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    @overload
    def get(self, chrom: str, pos: int) -> hictkpy.Bin:
        """Get the bin overlapping the given genomic coordinate."""

    @overload
    def get(self, chroms: Sequence[str], pos: Sequence[int]) -> pandas.DataFrame:
        """
        Get the bins overlapping the given genomic coordinates. Bins are returned as a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    def get_id(self, chrom: str, pos: int) -> int:
        """Get the ID of the bin overlapping the given genomic coordinate."""

    def get_ids(self, chroms: Sequence[str], pos: Sequence[int]) -> Annotated[NDArray[numpy.int64], dict(shape=(None,))]:
        """Get the IDs of the bins overlapping the given genomic coordinates."""

    def merge(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        Merge genomic coordinates corresponding to the given bin identifiers. Bin identifiers should be provided as a pandas.DataFrame with columns "bin1_id" and "bin2_id". Genomic coordinates are returned as a pandas.DataFrame containing the same data as the DataFrame given as input, plus columns ["chrom1", "start1", "end1", "chrom2", "start2", "end2"].
        """

    def to_arrow(self, range: str | None = None, query_type: str = 'UCSC') -> pyarrow.Table:
        """
        Return the bins in the BinTable as a pyarrow.Table. The optional "range" parameter can be used to only fetch a subset of the bins in the BinTable.
        """

    def to_pandas(self, range: str | None = None, query_type: str = 'UCSC') -> pandas.DataFrame:
        """
        Return the bins in the BinTable as a pandas.DataFrame. The optional "range" parameter can be used to only fetch a subset of the bins in the BinTable.
        """

    def to_df(self, range: str | None = None, query_type: str = 'UCSC') -> pandas.DataFrame:
        """Alias to to_pandas()."""

class Pixel:
    """Class modeling a Pixel in COO or BG2 format."""

    @overload
    def __init__(self, arg: "hictk::ThinPixel<unsigned char>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<unsigned char>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<unsigned short>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<unsigned short>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<unsigned int>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<unsigned int>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<unsigned long long>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<unsigned long long>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<signed char>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<signed char>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<short>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<short>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<int>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<int>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<long long>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<long long>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: int, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<float>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<float>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: float, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: float, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @overload
    def __init__(self, arg: "hictk::ThinPixel<double>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg: "hictk::Pixel<double>", /) -> None:
        """Private constructor."""

    @overload
    def __init__(self, arg0: Bin, arg1: Bin, arg2: float, /) -> None:
        """Construct a Pixel given a pair of Bins and the number of interactions."""

    @overload
    def __init__(self, arg0: int, arg1: int, arg2: float, /) -> None:
        """
        Construct a Pixel given a pair of Bin identifiers and the number of interactions.
        """

    @property
    def bin1_id(self) -> int:
        """Get the ID of bin1."""

    @property
    def bin2_id(self) -> int:
        """Get the ID of bin2."""

    @property
    def bin1(self) -> Bin:
        """Get bin1."""

    @property
    def bin2(self) -> Bin:
        """Get bin2."""

    @property
    def chrom1(self) -> str:
        """Get the chromosome associated with bin1."""

    @property
    def start1(self) -> int:
        """Get the start position associated with bin1."""

    @property
    def end1(self) -> int:
        """Get the end position associated with bin1."""

    @property
    def chrom2(self) -> str:
        """Get the chromosome associated with bin2."""

    @property
    def start2(self) -> int:
        """Get the start position associated with bin2."""

    @property
    def end2(self) -> int:
        """Get the end position associated with bin2."""

    @property
    def count(self) -> int | float:
        """Get the number of interactions."""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class PixelSelector:
    """
    Class representing pixels overlapping with the given genomic intervals.
    """

    @overload
    def __init__(self, arg0: "std::__1::shared_ptr<hictk::cooler::PixelSelector const>", arg1: type, arg2: bool, arg3: int, /) -> None:
        """
        Private constructor. PixelSelector objects are supposed to be created by calling the fetch() method on hictkpy.File objects.
        """

    @overload
    def __init__(self, arg0: "std::__1::shared_ptr<hictk::hic::PixelSelector const>", arg1: type, arg2: bool, arg3: int, /) -> None: ...

    @overload
    def __init__(self, arg0: "std::__1::shared_ptr<hictk::hic::PixelSelectorAll const>", arg1: type, arg2: bool, arg3: int, /) -> None: ...

    def __repr__(self) -> str: ...

    def coord1(self) -> tuple[str, int, int] | None:
        """
        Get query coordinates for the first dimension. Returns None when query spans the entire genome.
        """

    def coord2(self) -> tuple[str, int, int] | None:
        """
        Get query coordinates for the second dimension. Returns None when query spans the entire genome.
        """

    def size(self, upper_triangular: bool = True) -> int:
        """Get the number of pixels overlapping with the given query."""

    def dtype(self) -> type:
        """Get the dtype for the pixel count."""

    def __iter__(self) -> hictkpy.PixelIterator:
        """
        Implement iter(self). The resulting iterator yields objects of type hictkpy.Pixel.
        """

    def to_arrow(self, query_span: str = "upper_triangle") -> pyarrow.Table:
        """Retrieve interactions as a pyarrow.Table."""

    def to_pandas(self, query_span: str = "upper_triangle") -> pandas.DataFrame:
        """Retrieve interactions as a pandas DataFrame."""

    def to_df(self, query_span: str = "upper_triangle") -> pandas.DataFrame:
        """Alias to to_pandas()."""

    def to_numpy(self, query_span: str = 'full') -> Annotated[NDArray, dict(shape=(None, None), order='C')]:
        """Retrieve interactions as a numpy 2D matrix."""

    def to_coo(self, query_span: str = "upper_triangle", low_memory: bool = False) -> scipy.sparse.coo_matrix:
        """
        Retrieve interactions as a SciPy COO matrix. When low_memory=True, the heuristic used to minimize the number of memory allocations is turned off, and a two-pass algorithm that allocates a matrix with the exact shape is used instead.
        """

    def to_csr(self, query_span: str = "upper_triangle", low_memory: bool = False) -> scipy.sparse.csr_matrix:
        """
        Retrieve interactions as a SciPy CSR matrix. When low_memory=True, the heuristic used to minimize the number of memory allocations is turned off, and a two-pass algorithm that allocates a matrix with the exact shape is used instead.
        """

    def describe(self, metrics: Sequence[str] = ..., keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False, exact: bool = False) -> dict:
        """
        Compute one or more descriptive metrics in the most efficient way possible. Known metrics: nnz, sum, min, max, mean, variance, skewness, kurtosis. When a metric cannot be computed (e.g. because metrics=["variance"], but selector overlaps with a single pixel), the value for that metric is set to None. When keep_infs or keep_nans are set to True, and keep_zeros=True, nan and/or inf values are treated as zeros. By default, metrics are estimated by doing a single pass through the data. The estimates are stable and usually very accurate. However, if you require exact values, you can specify exact=True.
        """

    def nnz(self, keep_nans: bool = False, keep_infs: bool = False) -> int:
        """
        Get the number of non-zero entries for the current pixel selection. See documentation for describe() for more details.
        """

    def sum(self, keep_nans: bool = False, keep_infs: bool = False) -> int | float:
        """
        Get the total number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def min(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False) -> int | float | None:
        """
        Get the minimum number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def max(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False) -> int | float | None:
        """
        Get the maximum number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def mean(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False) -> float | None:
        """
        Get the average number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def variance(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False, exact: bool = False) -> float | None:
        """
        Get the variance of the number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def skewness(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False, exact: bool = False) -> float | None:
        """
        Get the skewness of the number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

    def kurtosis(self, keep_nans: bool = False, keep_infs: bool = False, keep_zeros: bool = False, exact: bool = False) -> float | None:
        """
        Get the kurtosis of the number of interactions for the current pixel selection. See documentation for describe() for more details.
        """

class File:
    """Class representing a file handle to a .cool or .hic file."""

    def __init__(self, path: str | os.PathLike, resolution: int | None = None, matrix_type: str = 'observed', matrix_unit: str = 'BP') -> None:
        """
        Construct a file object to a .hic, .cool or .mcool file given the file path and resolution.
        Resolution is ignored when opening single-resolution Cooler files.
        """

    def __repr__(self) -> str: ...

    def __enter__(self) -> File: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    def uri(self) -> str:
        """Return the file URI."""

    def path(self) -> pathlib.Path:
        """Return the file path."""

    def is_hic(self) -> bool:
        """Test whether file is in .hic format."""

    def is_cooler(self) -> bool:
        """Test whether file is in .cool format."""

    def close(self) -> None:
        """Manually close the file handle."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get chromosome sizes as a dictionary mapping names to sizes."""

    def bins(self) -> hictkpy.BinTable:
        """Get table of bins."""

    def resolution(self) -> int:
        """Get the bin size in bp."""

    def nbins(self) -> int:
        """Get the total number of bins."""

    def nchroms(self, include_ALL: bool = False) -> int:
        """Get the total number of chromosomes."""

    def attributes(self) -> dict:
        """Get file attributes as a dictionary."""

    def fetch(self, range1: str | None = None, range2: str | None = None, normalization: str | None = None, count_type: type | str = 'int32', join: bool = False, query_type: str = 'UCSC', diagonal_band_width: int | None = None) -> PixelSelector:
        """Fetch interactions overlapping a region of interest."""

    def avail_normalizations(self) -> list[str]:
        """Get the list of available normalizations."""

    def has_normalization(self, normalization: str) -> bool:
        """Check whether a given normalization is available."""

    @overload
    def weights(self, name: str, divisive: bool = True) -> Annotated[NDArray[numpy.float64], dict(shape=(None,), order='C')] | None:
        """Fetch the balancing weights for the given normalization method."""

    @overload
    def weights(self, names: Sequence[str], divisive: bool = True) -> pandas.DataFrame:
        """
        Fetch the balancing weights for the given normalization methods.Weights are returned as a pandas.DataFrame.
        """

class MultiResFile:
    """Class representing a file handle to a .hic or .mcool file"""

    def __init__(self, path: str | os.PathLike) -> None:
        """Open a multi-resolution Cooler file (.mcool) or .hic file."""

    def __repr__(self) -> str: ...

    def __enter__(self) -> MultiResFile: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def is_mcool(self) -> bool:
        """Test whether the file is in .mcool format."""

    def is_hic(self) -> bool:
        """Test whether the file is in .hic format."""

    def close(self) -> None:
        """Manually close the file handle."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get the chromosome sizes as a dictionary mapping names to sizes."""

    def resolutions(self) -> Annotated[NDArray[numpy.int64], dict(shape=(None,), order='C')]:
        """Get the list of available resolutions."""

    def attributes(self) -> dict:
        """Get file attributes as a dictionary."""

    def __getitem__(self, arg: int, /) -> File:
        """
        Open the Cooler or .hic file corresponding to the resolution given as input.
        """

