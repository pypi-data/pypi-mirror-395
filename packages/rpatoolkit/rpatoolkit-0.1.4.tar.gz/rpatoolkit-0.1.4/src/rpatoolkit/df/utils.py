import logging
import polars as pl
from polars._typing import FileSource
from typing import overload
from rpatoolkit.utils import strip_punctuation

log = logging.getLogger(__name__)


@overload
def normalize_columns(
    df: pl.LazyFrame,
    mapping: dict[str, list[str] | str] = ...,
    remove_punctuation: bool = ...,
    lowercase_columns: bool = ...,
) -> pl.LazyFrame: ...


@overload
def normalize_columns(
    df: pl.DataFrame,
    mapping: dict[str, list[str] | str] = ...,
    remove_punctuation: bool = ...,
    lowercase_columns: bool = ...,
) -> pl.DataFrame: ...


def normalize_columns(
    df: pl.DataFrame | pl.LazyFrame,
    mapping: dict[str, list[str] | str],
    remove_punctuation: bool = True,
    lowercase_columns: bool = True,
) -> pl.DataFrame | pl.LazyFrame:
    """
    Rename columns in a Polars DataFrame based on a mapping dictionary.
    Args:
        df: Input Polars DataFrame
        column_mapping: Dictionary mapping final column names to lists of possible
                       original column names. Format:
                       {"final_name": ["possible_name1", "possible_name2", ...]}

    Returns:
        DataFrame with renamed columns

    Raises:
        ValueError: If multiple columns in the DataFrame map to the same final name
    """
    # Build a reverse mapping for O(1) lookup of actual_column_names to final_column_name
    reverse_mapping = {}
    for final_name, possible_names in mapping.items():
        if isinstance(possible_names, str):
            possible_names = [possible_names]

        for name in possible_names:
            name = name.lower()
            if name in reverse_mapping:
                prev_final = reverse_mapping[name]
                raise ValueError(
                    f"Duplicate column name found. Ambiguous mapping: column '{name}' maps to both "
                    f"'{prev_final}' and '{final_name}'"
                )

            reverse_mapping[name] = final_name

    # First remove all punctuations from the df.columns
    if remove_punctuation:
        if isinstance(df, pl.LazyFrame):
            clean_columns = [
                strip_punctuation(col.strip()) for col in df.collect_schema().names()
            ]
            temp_rename_dict = {
                k: v for k, v in zip(df.collect_schema().names(), clean_columns)
            }
            df = df.rename(temp_rename_dict)
        else:
            clean_columns = [strip_punctuation(col.strip()) for col in df.columns]
            df.columns = clean_columns

    if lowercase_columns:
        if isinstance(df, pl.LazyFrame):
            lowercase_cols = [
                col.strip().lower() for col in df.collect_schema().names()
            ]
            temp_rename_dict = {
                k: v for k, v in zip(df.collect_schema().names(), lowercase_cols)
            }
            df = df.rename(temp_rename_dict)
        else:
            clean_columns = [col.strip().lower() for col in df.columns]
            df.columns = clean_columns

    rename_dict = {}
    finalized_names = {}
    df_cols = (
        df.columns if isinstance(df, pl.DataFrame) else df.collect_schema().names()
    )
    for col in df_cols:
        col = col.strip().lower()
        if col in reverse_mapping:
            final_name = reverse_mapping[col]

            # Check if multiple df columns map to the same final name
            if final_name in finalized_names:
                raise ValueError(
                    f"Conflict: multiple columns map to the same final name: {final_name}"
                    f"'{finalized_names[final_name]}' and '{col}'"
                )

            # Add to the rename_dict if col and final_name are different
            if col != final_name:
                rename_dict[col] = final_name
                finalized_names[final_name] = col

    if rename_dict:
        return df.rename(rename_dict)

    return df


def reorder_columns(
    df: pl.DataFrame | pl.LazyFrame, columns_order: list[str]
) -> pl.DataFrame | pl.LazyFrame:
    """
    Reorder columns of a Polars DataFrame or LazyFrame.

    Args:
        df (pl.DataFrame | pl.LazyFrame): The input DataFrame or LazyFrame.
        columns_order (list[str]): A list specifying the desired order of columns or subset of columns that you want to be ordered.

    Returns:
        pl.DataFrame | pl.LazyFrame: The DataFrame or LazyFrame with reordered columns.

    Example:
        >>> import polars as pl
        >>> df = pl.DataFrame({
        ...     "A": [1, 2, 3],
        ...     "B": [4, 5, 6],
        ...     "C": [7, 8, 9]
        ... })
        >>> reordered_df = reorder_columns(df, ["C", "A"])
        >>> print(reordered_df)
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ C   ┆ A   ┆ B   │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 7   ┆ 1   ┆ 4   │
        │ 8   ┆ 2   ┆ 5   │
        │ 9   ┆ 3   ┆ 6   │
        └─────┴─────┘

    """
    # Select the specified columns in the desired order, then append any remaining columns
    selected_cols = [pl.col(col) for col in columns_order if col in df.columns]
    remaining_cols = [pl.col(col) for col in df.columns if col not in columns_order]
    return df.select(selected_cols + remaining_cols)


def get_missing_columns(
    df: pl.DataFrame | pl.LazyFrame, required_columns: list[str]
) -> list[str]:
    """
    Check if a Polars DataFrame or LazyFrame contains all required columns and return a list of missing columns.

    Args:
        df (pl.DataFrame | pl.LazyFrame): The input DataFrame or LazyFrame.
        required_columns (list[str]): A list of required column names.

    Returns:
        list
            A list of missing columns from the required_columns list.

    Example:
        >>> import polars as pl
        >>> df = pl.DataFrame({
        ...     "A": [1, 2, 3],
        ...     "B": [4, 5, 6],
        ...     "C": [7, 8, 9]
        ... })
        >>> missing_columns = get_missing_columns(df, ["C", "E"])
        >>> print(missing_columns)
        ['E']
    """

    if isinstance(df, pl.LazyFrame):
        available_columns = [col.lower() for col in df.collect_schema().names()]
    else:
        available_columns = [col.lower() for col in df.columns]

    missing_cols = [
        col for col in required_columns if col.lower() not in available_columns
    ]
    return missing_cols


def find_header_row(
    source: FileSource,
    sheet_id: int | None = None,
    sheet_name: str | None = None,
    max_rows: int = 200,
    expected_keywords: list[str] | None = None,
) -> int:
    """
    Find the header row in an Excel file by identifying the first row with maximum consecutive non-null values.

    This function is designed for Excel sheets where headers are not at the top row and the rows
    above the header row contain data. It identifies the most likely header row by scanning for
    the row with the highest number of consecutive non-null string values.

    Parameters
    ----------
    source : FileSource
        Path to the Excel file or file-like object to read
    sheet_id : int, optional
        Sheet number to read (cannot be used with sheet_name)
    sheet_name : str, optional
        Sheet name to read (cannot be used with sheet_id)
    max_rows : int, default=100
        Maximum number of rows to scan for header identification
    expected_keywords : list[str], optional
        List of keywords to look for in the header row. If a row contains all of these keywords, it is considered a header row.

    Returns
    -------
    int
        The zero-based index of the first row with maximum consecutive non-null values. If expected_keywords is provided, this is the first row with all expected keywords and maximum consecutive non-null values.

    Examples
    --------
    >>> header_row_index = find_header_row("data.xlsx")
    >>> df = read_excel("data.xlsx", header_row=header_row_index)

    Notes
    -----
    - If the first few rows are empty and the header is at the top of the data section,
      use `read_excel` directly instead of this function
    - The function considers consecutive non-null values from the beginning of each row
    - Only one of `sheet_id` or `sheet_name` can be specified
    """
    if sheet_id is not None and sheet_name is not None:
        raise ValueError("sheet_id and sheet_name cannot be both specified.")

    # Read first max_rows without assuming header row
    df = pl.read_excel(
        source,
        sheet_id=sheet_id,
        sheet_name=sheet_name,
        drop_empty_cols=False,
        drop_empty_rows=False,
        has_header=False,
    ).head(max_rows)

    max_consecutive = 0
    header_row_index = 0
    for i, row in enumerate(df.rows()):
        consecutive_count = 0
        # If expected keywords are provided, check if all of them are present in the row
        all_keywords_present = False
        if expected_keywords:
            row_values = [
                str(value).strip().lower() for value in row if value is not None
            ]
            all_keywords_present = all(
                keyword.lower() in row_values for keyword in expected_keywords
            )

        # Check for non-null consecutive values
        for value in row:
            if value is not None and str(value).strip() != "":
                consecutive_count += 1
            else:
                break

        if consecutive_count > max_consecutive:
            max_consecutive = consecutive_count
            header_row_index = i
            if expected_keywords and all_keywords_present:
                # This is the first row with all expected keywords, and highest consecutive non-null count, so its most likely the header row
                log.info(
                    "Found first header row with all expected keywords and maximum consecutive non-null values"
                )
                break

    log.info(
        f"Identified header row at index: {header_row_index} with {max_consecutive} consecutive non-null values"
    )
    return header_row_index
