import os
from os import PathLike
from typing import Any, Union, cast

import narwhals as nw
import pandas as pd
import pyarrow as pa
from narwhals import Boolean, String
from narwhals.typing import IntoDataFrame
from pydantic import JsonValue
from shortuuid import uuid

from .._util.instances import get_instances, track_instance
from .param import Param
from .selection import Selection


class Data:
    """Data source for visualizations.

    Data sources can be created from any standard Python data frame (e.g. Pandas, Polars, etc.) or from a path pointing to a data file in a standard format (e.g. csv, parquet, etc.)
    """

    @classmethod
    def from_dataframe(cls, df: IntoDataFrame) -> "Data":
        """Create `Data` from a standard Python data frame (e.g. Pandas, Polars, PyArrow, etc.).

        Args:
           df: Data frame to read.
        """
        return Data(df)

    @classmethod
    def from_file(cls, file: Union[str, PathLike[str]]) -> "Data":
        """Create `Data` from a data file (e.g. csv, parquet, feather, etc.).

        Args:
           file: File to read data from. Supported formats include csv, json, xslx, parquet, feather, sas7bdat, dta, and fwf.
        """
        return Data(file)

    def __init__(self, data: Union[IntoDataFrame, str, PathLike[str]]) -> None:
        # assign a unique table name
        self._table = uuid()

        # create a default selection
        self._selection = Selection(select="intersect", unique=self._table)

        # convert to pandas if its a path
        if isinstance(data, (str, PathLike)):
            data = _read_df_from_file(data)

        # convert to narwhals
        self._ndf = nw.from_native(data)

        # create buffer
        reader = pa.ipc.RecordBatchStreamReader.from_stream(self._ndf)
        table = reader.read_all()
        buffer = pa.BufferOutputStream()
        with pa.RecordBatchStreamWriter(buffer, table.schema) as writer:
            writer.write_table(table)
        self._data: bytes = buffer.getvalue().to_pybytes()

        # track whether we have been collected
        self._collected = False

        # track instances
        track_instance("data", self)

    @property
    def table(self) -> str:
        return self._table

    @property
    def selection(self) -> Selection:
        return self._selection

    @property
    def columns(self) -> list[str]:
        """Column names for data source."""
        return self._ndf.columns

    def column_unique(self, column: str) -> list[Any]:
        return self._ndf[column].unique().to_list()

    def column_min(self, column: str) -> Any:
        return self._ndf[column].min()

    def column_max(self, column: str) -> Any:
        return self._ndf[column].max()

    def _plot_from(self, filter_by: Selection | None = None) -> dict[str, JsonValue]:
        return {"from": self.table, "filterBy": filter_by or f"${self.selection.id}"}

    def _get_data(self) -> bytes:
        return self._data

    def _collect_data(self) -> bytes:
        if not self._collected:
            self._collected = True
            return self._data
        else:
            return bytes()

    def __str__(self) -> str:
        lines = [
            f"Viz Data ({len(self._ndf):,} rows x {len(self._ndf.columns):,} columns)",
            "-" * 80,
        ]
        for col_name, dtype in self._ndf.schema.items():
            lines.append(f"{col_name:<40} {str(dtype):<40}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return self._ndf.__len__()

    @classmethod
    def _get_all(cls) -> list["Data"]:
        """Get all data."""
        return cast(list["Data"], get_instances("data"))


def _read_df_from_file(path: str | PathLike[str]) -> pd.DataFrame:
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".csv":
        return pd.read_csv(path)
    elif ext == ".xlsx" or ext == ".xls":
        return pd.read_excel(path)
    elif ext == ".json":
        return pd.read_json(path)
    elif ext == ".parquet":
        return pd.read_parquet(path)
    elif ext == ".feather":
        return pd.read_feather(path)
    elif ext == ".sas7bdat":
        return pd.read_sas(path)
    elif ext == ".dta":
        return pd.read_stata(path)
    elif ext == ".txt" or ext == ".dat":
        # Try to guess the delimiter
        return pd.read_csv(path, sep=None, engine="python")
    elif ext == ".fwf":
        return pd.read_fwf(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def validate_data(data: Data) -> None:
    # valdate type for people not using type-checkers
    if not isinstance(data, Data):
        raise TypeError(
            "Passed data is not of type vz.Data. Did you forget to wrap it in vz.Data()?"
        )


def validate_bindings(data: Data, column: str, param: Param | None = None) -> None:
    def raise_type_error(type: str) -> None:
        raise TypeError(
            f"Parameter passed for column '{column}' must be a {type} type."
        )

    # validate df and ensure it is on the client
    validate_data(data)

    # validate that the column in in the data frame
    dtype = data._ndf.schema.get(column, None)
    if dtype is None:
        raise ValueError(
            f"Column '{column}' does not exist in the data (expected one of {', '.join(data.columns)})."
        )

    # if a param is specified ensure that the type matches the column type
    if param is not None:
        if dtype.is_numeric() and not param._is_numeric():
            raise_type_error("numeric")
        elif dtype.is_temporal() and not param._is_datetime():
            raise_type_error("datetime")
        elif isinstance(dtype, Boolean) and not param._is_bool():
            raise_type_error("boolean")
        elif isinstance(dtype, String) and not param._is_string():
            raise_type_error("string")
