import polars as pl
import logging
import re
from rpatoolkit.utils import strip_punctuation
from polars._typing import FileSource, SchemaDict, ExcelSpreadsheetEngine
from typing import Any, Sequence, Literal, NoReturn, overload

log = logging.getLogger(__name__)


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: None = ...,
    sheet_name: None = ...,
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> pl.LazyFrame: ...


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: Literal[0] | list[int] = ...,
    sheet_name: None = ...,
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> dict[str, pl.LazyFrame]: ...


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: None = ...,
    sheet_name: str = ...,
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> pl.LazyFrame: ...


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: int = ...,
    sheet_name: None = ...,
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> pl.LazyFrame: ...


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: None = ...,
    sheet_name: list[str],
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> dict[str, pl.LazyFrame]: ...


@overload
def read_excel(
    source: FileSource,
    *,
    sheet_id: int = ...,
    sheet_name: str = ...,
    table_name: str | None = ...,
    engine: ExcelSpreadsheetEngine = ...,
    engine_options: dict[str, Any] | None = ...,
    read_options: dict[str, Any] | None = ...,
    has_header: bool = ...,
    columns: Sequence[int] | Sequence[str] | str | None = ...,
    schema_overrides: SchemaDict | None = ...,
    infer_schema_length: int | None = ...,
    include_file_paths: str | None = ...,
    drop_empty_rows: bool = ...,
    drop_empty_cols: bool = ...,
    raise_if_empty: bool = ...,
    header_row: int | None = ...,
    cast: dict[str, pl.DataType] | None = ...,
    lower_column_names: bool = ...,
    clean_column_names: bool = ...,
) -> NoReturn: ...


def read_excel(
    source: FileSource,
    *,
    sheet_id: int | list[int] | None = None,
    sheet_name: str | list[str] | None = None,
    table_name: str | None = None,
    engine: ExcelSpreadsheetEngine = "calamine",
    engine_options: dict[str, Any] | None = None,
    read_options: dict[str, Any] | None = None,
    has_header: bool = True,
    columns: Sequence[int] | Sequence[str] | str | None = None,
    schema_overrides: SchemaDict | None = None,
    infer_schema_length: int | None = 100,
    include_file_paths: str | None = None,
    drop_empty_rows: bool = False,
    drop_empty_cols: bool = False,
    raise_if_empty: bool = True,
    header_row: int | None = None,
    cast: dict[str, pl.DataType] | None = None,
    lower_column_names: bool = True,
    clean_column_names: bool = False,
) -> pl.LazyFrame | dict[str, pl.LazyFrame]:
    """
    Reads an Excel file into a Polars LazyFrame.

    This function extends Polars' read_excel functionality by adding automatic
    column name cleaning and optional data type casting after cleaning the columns. It reads an excel file and returns a LazyFrame or a dictionary of LazyFrames if reading multiple sheets.

    Parameters
    ----------
    source :
        Path to the Excel file or file-like object to read
    sheet_id :
        Sheet number(s) to read (cannot be used with sheet_name). Use 0 to read all sheets as a dictionary, or a list of integers to read specific sheets as a dictionary
    sheet_name :
        Sheet name(s) to read (cannot be used with sheet_id). Use a list of strings to read multiple sheets as a dictionary
    table_name :
        Name of a specific table to read.
    engine : {'calamine', 'openpyxl', 'xlsx2csv'}
        Library used to parse the spreadsheet file; defaults to "calamine".
    engine_options :
       Additional options passed to the underlying engine's primary parsing constructor
    read_options :
        Options passed to the underlying engine method that reads the sheet data.
    has_header :
        Whether the sheet has a header row
    columns :
        Columns to read from the sheet; if not specified, all columns are read
    schema_overrides :
        Support type specification or override of one or more columns.
    infer_schema_length : int, optional
        Number of rows to infer the schema from
    include_file_paths :
        Column name for including file paths in the result
    drop_empty_rows :
        Remove empty rows from the result
    drop_empty_cols :
        Remove empty columns from the result
    raise_if_empty :
        Raise an exception if the resulting DataFrame is empty
    header_row : int, optional
        Row number to use as header (0-indexed). Overrides has_header parameter when specified
    cast : dict[str, pl.DataType], optional
        Dictionary mapping column names to desired data types for casting.
    lower_column_names : bool, default=True
        Convert column names to lowercase
    clean_column_names : bool, default=False
        Clean column names by stripping punctuation

    Returns
    -------
    LazyFrame
        A Polars LazyFrame when reading a single sheet

    dict[str, LazyFrame]
        A dictionary of LazyFrames when reading multiple sheets

    Raises
    ------
    ValueError
        If both sheet_id and sheet_name are specified
        If sheet_id is 0 (reserved for reading all sheets)

    Note:
    -----
    Column names are stripped and converted to lowercase when lower_column_names=True

    Examples
    --------
    >>> df = read_excel("data.xlsx")
    >>> df = read_excel("data.xlsx", sheet_name="Sheet1")
    >>> df = read_excel("data.xlsx", sheet_id=1)
    >>> df_dict = read_excel("data.xlsx", sheet_id=0)  # Read all sheets
    >>> df = read_excel("data.xlsx", cast={"date": pl.Date, "value": pl.Float64})
    """

    if sheet_id is not None and sheet_name is not None:
        raise ValueError("sheet_id and sheet_name cannot be both specified.")

    # Prepare read_options with header_row if specified
    if header_row is not None:
        if read_options is None:
            read_options = {"header_row": header_row}
        else:
            read_options["header_row"] = header_row

    # Read excel with all parameters
    df = pl.read_excel(
        source=source,
        sheet_id=sheet_id,
        sheet_name=sheet_name,
        table_name=table_name,
        engine=engine,
        engine_options=engine_options,
        read_options=read_options,
        has_header=has_header,
        columns=columns,
        schema_overrides=schema_overrides,
        infer_schema_length=infer_schema_length,
        include_file_paths=include_file_paths,
        drop_empty_rows=drop_empty_rows,
        drop_empty_cols=drop_empty_cols,
        raise_if_empty=raise_if_empty,
    )

    # Determine if we're dealing with multiple sheets based on input parameters
    # sheet_id=0 means read all sheets, which returns a dict
    if sheet_id == 0 or isinstance(sheet_id, list) or isinstance(sheet_name, list):
        # Multiple sheets case - df is a dict[str, pl.DataFrame]
        return _read_multiple_sheets(
            df,
            lower_column_names=lower_column_names,
            clean_column_names=clean_column_names,
            cast=cast,
        )

    # Single sheet case - df is a pl.DataFrame
    return _read_single_sheet(
        df,
        lower_column_names=lower_column_names,
        clean_column_names=clean_column_names,
        cast=cast,
    )


def _read_single_sheet(
    df: pl.DataFrame,
    lower_column_names: bool = True,
    clean_column_names: bool = False,
    cast: dict[str, pl.DataType] | None = None,
) -> pl.LazyFrame:
    if lower_column_names:
        df = _lower_column_names(df)

    if clean_column_names:
        df = _clean_column_names(df)
    df = _cast_columns(df, cast=cast)
    return df.lazy()


def _read_multiple_sheets(
    df: dict[str, pl.DataFrame],
    lower_column_names: bool = True,
    clean_column_names: bool = False,
    cast: dict[str, pl.DataType] | None = None,
) -> dict[str, pl.LazyFrame]:
    result_dfs: dict[str, pl.LazyFrame] = {}
    for sheet_name, df in df.items():
        if lower_column_names:
            df = _lower_column_names(df)

        if clean_column_names:
            df = _clean_column_names(df)

        df = _cast_columns(df, cast=cast)
        result_dfs[sheet_name.lower()] = df.lazy()

    return result_dfs


def _clean_column_names(df: pl.DataFrame) -> pl.DataFrame:
    df.columns = [strip_punctuation(col) for col in df.columns]
    return df


def _lower_column_names(df: pl.DataFrame) -> pl.DataFrame:
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def _cast_columns(
    df: pl.DataFrame, cast: dict[str, pl.DataType] | None = None
) -> pl.DataFrame:
    if cast is not None:
        for col, dtype in cast.items():
            col = col.strip().lower()
            if col not in df.columns:
                log.warning(f"Column {col} not found in dataframe.")
                continue

            df = df.with_columns(pl.col(col).cast(dtype, strict=False))

    return df
