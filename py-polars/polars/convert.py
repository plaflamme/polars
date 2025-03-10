from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Sequence, overload

from polars.datatypes import N_INFER_DEFAULT, SchemaDefinition, SchemaDict
from polars.dependencies import numpy as np
from polars.dependencies import pandas as pd
from polars.dependencies import pyarrow as pa
from polars.internals import DataFrame, Series
from polars.utils import deprecated_alias

if TYPE_CHECKING:
    from polars.internals.type_aliases import Orientation


def from_dict(
    data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
    columns: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a dictionary of sequences.

    This operation clones data, unless you pass in a ``Dict[str, pl.Series]``.

    Parameters
    ----------
    data : dict of sequences
        Two-dimensional data represented as a dictionary. dict must contain
        Sequences.
    columns : Sequence of str, default None
        Column labels to use for resulting DataFrame. If specified, overrides any
        labels already present in the data. Must match data dimensions.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the columns param will be overridden.

    Returns
    -------
    :class:`DataFrame`

    Examples
    --------
    >>> df = pl.from_dict({"a": [1, 2], "b": [3, 4]})
    >>> df
    shape: (2, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 3   │
    │ 2   ┆ 4   │
    └─────┴─────┘

    """
    return DataFrame._from_dict(
        data=data, schema=columns, schema_overrides=schema_overrides
    )


@deprecated_alias(schema="schema_overrides")
def from_dicts(
    dicts: Sequence[dict[str, Any]],
    infer_schema_length: int | None = N_INFER_DEFAULT,
    *,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a sequence of dictionaries. This operation clones data.

    Parameters
    ----------
    dicts
        Sequence with dictionaries mapping column name to value
    infer_schema_length
        How many dictionaries/rows to scan to determine the data types
        if set to `None` all rows are scanned. This will be slow.
    schema_overrides : dict, default None
        Support override of inferred types for one or more columns.

    Returns
    -------
    :class:`DataFrame`

    Examples
    --------
    >>> data = [{"a": 1, "b": 4}, {"a": 2, "b": 5}, {"a": 3, "b": 6}]
    >>> df = pl.from_dicts(data)
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    >>> # overwrite first column name and dtype
    >>> pl.from_dicts(data, schema_overrides={"c": pl.Int32})
    shape: (3, 2)
    ┌─────┬─────┐
    │ c   ┆ b   │
    │ --- ┆ --- │
    │ i32 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    >>> # let polars infer the dtypes
    >>> # but inform about a 3rd column
    >>> pl.from_dicts(
    ...     data, schema_overrides={"a": pl.Unknown, "b": pl.Unknown, "c": pl.Int32}
    ... )
    shape: (3, 3)
    ┌─────┬─────┬──────┐
    │ a   ┆ b   ┆ c    │
    │ --- ┆ --- ┆ ---  │
    │ i64 ┆ i64 ┆ i32  │
    ╞═════╪═════╪══════╡
    │ 1   ┆ 4   ┆ null │
    │ 2   ┆ 5   ┆ null │
    │ 3   ┆ 6   ┆ null │
    └─────┴─────┴──────┘

    """
    return DataFrame._from_dicts(
        dicts, infer_schema_length, schema_overrides=schema_overrides
    )


def from_records(
    data: Sequence[Sequence[Any]],
    columns: Sequence[str] | None = None,
    orient: Orientation | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a sequence of sequences. This operation clones data.

    Note that this is slower than creating from columnar memory.

    Parameters
    ----------
    data : Sequence of sequences
        Two-dimensional data represented as a sequence of sequences.
    columns : Sequence of str, default None
        Column labels to use for resulting DataFrame. Must match data dimensions.
        If not specified, columns will be named `column_0`, `column_1`, etc.
    orient : {None, 'col', 'row'}
        Whether to interpret two-dimensional data as columns or as rows. If None,
        the orientation is inferred by matching the columns and data dimensions. If
        this does not yield conclusive results, column orientation is used.
    infer_schema_length
        How many dictionaries/rows to scan to determine the data types
        if set to `None` all rows are scanned. This will be slow.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the columns param will be overridden.

    Returns
    -------
    :class:`DataFrame`

    Examples
    --------
    >>> data = [[1, 2, 3], [4, 5, 6]]
    >>> df = pl.from_records(data, columns=["a", "b"])
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    """
    return DataFrame._from_records(
        data,
        columns=columns,
        schema_overrides=schema_overrides,
        orient=orient,
        infer_schema_length=infer_schema_length,
    )


def from_numpy(
    data: np.ndarray[Any, Any],
    columns: Sequence[str] | None = None,
    orient: Orientation | None = None,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a numpy ndarray. This operation clones data.

    Note that this is slower than creating from columnar memory.

    Parameters
    ----------
    data : :class:`numpy.ndarray`
        Two-dimensional data represented as a numpy ndarray.
    columns : Sequence of str, default None
        Column labels to use for resulting DataFrame. Must match data dimensions.
        If not specified, columns will be named `column_0`, `column_1`, etc.
    orient : {None, 'col', 'row'}
        Whether to interpret two-dimensional data as columns or as rows. If None,
        the orientation is inferred by matching the columns and data dimensions. If
        this does not yield conclusive results, column orientation is used.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the columns param will be overridden.

    Returns
    -------
    :class:`DataFrame`

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([[1, 2, 3], [4, 5, 6]])
    >>> df = pl.from_numpy(data, columns=["a", "b"], orient="col")
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    """
    return DataFrame._from_numpy(
        data, columns=columns, orient=orient, schema_overrides=schema_overrides
    )


def from_arrow(
    a: pa.Table | pa.Array | pa.ChunkedArray,
    rechunk: bool = True,
    schema: Sequence[str] | None = None,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame | Series:
    """
    Create a DataFrame or Series from an Arrow Table or Array.

    This operation will be zero copy for the most part. Types that are not
    supported by Polars may be cast to the closest supported type.

    Parameters
    ----------
    a : :class:`pyarrow.Table` or :class:`pyarrow.Array`
        Data representing an Arrow Table or Array.
    rechunk : bool, default True
        Make sure that all data is in contiguous memory.
    schema : Sequence of str, dict, default None
        Column labels to use for resulting DataFrame. Must match data dimensions.
        If not specified, existing Array table columns are used, with missing names
        named as `column_0`, `column_1`, etc.
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The resulting DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if the type is None, it will be auto-inferred.
        * As a list of column names; in this case types are all automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If you supply a list of column names that does not match the names in the
        underlying data, the names supplied here will overwrite them. The number
        of names given in the schema should match the underlying data dimensions.

    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the schema param will be overridden.

    Returns
    -------
    :class:`DataFrame` or :class:`Series`

    Examples
    --------
    Constructing a DataFrame from an Arrow Table:

    >>> import pyarrow as pa
    >>> data = pa.table({"a": [1, 2, 3], "b": [4, 5, 6]})
    >>> df = pl.from_arrow(data)
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    Constructing a Series from an Arrow Array:

    >>> import pyarrow as pa
    >>> data = pa.array([1, 2, 3])
    >>> series = pl.from_arrow(data)
    >>> series
    shape: (3,)
    Series: '' [i64]
    [
        1
        2
        3
    ]

    """
    if isinstance(a, pa.Table):
        return DataFrame._from_arrow(
            a, rechunk=rechunk, columns=schema, schema_overrides=schema_overrides
        )
    elif isinstance(a, (pa.Array, pa.ChunkedArray)):
        return Series._from_arrow("", a, rechunk)
    else:
        raise ValueError(f"Expected Arrow Table or Array, got {type(a)}.")


@overload
def from_pandas(
    df: pd.DataFrame,
    rechunk: bool = True,
    nan_to_none: bool = True,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    ...


@overload
def from_pandas(
    df: pd.Series | pd.DatetimeIndex,
    rechunk: bool = True,
    nan_to_none: bool = True,
    schema_overrides: SchemaDict | None = None,
) -> Series:
    ...


def from_pandas(
    df: pd.DataFrame | pd.Series | pd.DatetimeIndex,
    rechunk: bool = True,
    nan_to_none: bool = True,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame | Series:
    """
    Construct a Polars DataFrame or Series from a pandas DataFrame or Series.

    This operation clones data.

    This requires that :mod:`pandas` and :mod:`pyarrow` are installed.

    Parameters
    ----------
    df: :class:`pandas.DataFrame`, :class:`pandas.Series`, :class:`pandas.DatetimeIndex`
        Data represented as a pandas DataFrame, Series, or DatetimeIndex.
    rechunk : bool, default True
        Make sure that all data is in contiguous memory.
    nan_to_none : bool, default True
        If data contains `NaN` values PyArrow will convert the ``NaN`` to ``None``
    schema_overrides : dict, default None
        Support override of inferred types for one or more columns.

    Returns
    -------
    :class:`DataFrame`

    Examples
    --------
    Constructing a :class:`DataFrame` from a :class:`pandas.DataFrame`:

    >>> import pandas as pd
    >>> pd_df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["a", "b", "c"])
    >>> df = pl.from_pandas(pd_df)
    >>> df
        shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 1   ┆ 2   ┆ 3   │
    │ 4   ┆ 5   ┆ 6   │
    └─────┴─────┴─────┘

    Constructing a Series from a :class:`pd.Series`:

    >>> import pandas as pd
    >>> pd_series = pd.Series([1, 2, 3], name="pd")
    >>> df = pl.from_pandas(pd_series)
    >>> df
    shape: (3,)
    Series: 'pd' [i64]
    [
        1
        2
        3
    ]

    """
    if isinstance(df, (pd.Series, pd.DatetimeIndex)):
        return Series._from_pandas("", df, nan_to_none=nan_to_none)
    elif isinstance(df, pd.DataFrame):
        return DataFrame._from_pandas(
            df,
            rechunk=rechunk,
            nan_to_none=nan_to_none,
            schema_overrides=schema_overrides,
        )
    else:
        raise ValueError(f"Expected pandas DataFrame or Series, got {type(df)}.")
