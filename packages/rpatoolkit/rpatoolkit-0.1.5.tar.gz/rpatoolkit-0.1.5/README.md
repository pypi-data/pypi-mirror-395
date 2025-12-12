# rpatoolkit

A Python toolkit for Robotic Process Automation (RPA) and ETL pipelines providing solutions to common automation challenges.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
 - [Data Frame Utilities](#data-frame-utilities)
  - [File System Utilities](#file-system-utilities)
- [API Documentation](#api-documentation)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

rpatoolkit is a comprehensive Python library designed to simplify common RPA and ETL tasks. It provides utilities for reading Excel files, manipulating data frames, and handling file system operations with a focus on automation workflows.

## Features

- **Excel Reading Utilities**: Enhanced Excel reading capabilities with automatic column name cleaning, data type casting, and header row detection
- **Data Frame Utilities**: Functions for renaming, reordering, and validating columns in Polars DataFrames/LazyFrames
- **File System Utilities**: Tools for creating uniquely named directories with timestamp and UUID
- **Header Detection**: Automatic detection of header rows in Excel files with offset data
- **Column Name Cleaning**: Automatic cleaning and standardization of column names
- **Multiple Sheet Reading**: Support for reading all sheets from an Excel workbook at once

## Installation

To install rpatoolkit, you need Python 3.10 or higher. You can install it using pip:

```bash
pip install rpatoolkit
```

Or if you're using uv (recommended):

```bash
uv add rpatoolkit
```

### Development Installation

For development purposes:

```bash
# Clone the repository
git clone https://github.com/fnxL/rpatoolkit.git
cd rpatoolkit

# Install in development mode
uv sync --dev
```

## Usage

### Data Frame Utilities

#### Reading Excel Files

The main function for reading Excel files with enhanced capabilities:

```python
import polars as pl
from rpatoolkit.df import read_excel

# Basic usage
df = read_excel("data.xlsx")

# Reading a specific sheet
df = read_excel("data.xlsx", sheet_name="Sheet1")

# Casting specific columns to certain data types
df = read_excel("data.xlsx", cast={"date": pl.Date, "value": pl.Float64})

# Reading all sheets at once
all_sheets = read_excel("data.xlsx", read_all_sheets=True)

# Reading Excel with header row at an offset
df = read_excel("data.xlsx", header_row=3)
```

#### Finding Header Row

Automatically detect the header row in Excel files where headers are not at the top:

```python
from rpatoolkit.df import find_header_row, read_excel

# Find the header row
header_row_index = find_header_row("data.xlsx")
print(f"Header row found at index: {header_row_index}")

# Read the Excel file using the detected header row
df = read_excel("data.xlsx", header_row=header_row_index)

# Find header row with expected keywords
header_row_index = find_header_row("data.xlsx", expected_keywords=["name", "age", "city"])
```

#### Column Utilities

Utilities for manipulating DataFrame columns:

```python
from rpatoolkit.df import rename_columns, reorder_columns, get_missing_columns

# Rename columns
df = rename_columns(df, {"old_name": "new_name", "id": "identifier"})

# Reorder columns
df = reorder_columns(df, ["name", "age", "city"])

# Check for missing columns
required_columns = ["name", "email", "phone"]
missing = get_missing_columns(df, required_columns)
if missing:
    print(f"Missing columns: {missing}")
```

### File System Utilities

#### Creating Unique Directories

Create uniquely named directories with timestamps and UUIDs:

```python
from rpatoolkit.fs import make_unique_dir

# Create a unique directory with default settings
unique_dir = make_unique_dir(prefix="backup")

# Create a directory with custom settings
unique_dir = make_unique_dir(
    base_path="./exports",
    prefix="report",
    include_date=True,
    include_time=True,
    use_12h_format=False  # 24-hour format
)

# Create a directory without automatically creating it on filesystem
path_only = make_unique_dir(create=False, prefix="temp")
```

## API Documentation

### Data Frame Module (`rpatoolkit.df`)

#### `read_excel`

Reads an Excel file into a Polars LazyFrame with enhanced functionality.

```python
def read_excel(
    source: FileSource,
    *,
    sheet_id: int | None = None,
    sheet_name: str | None = None,
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
    read_all_sheets: bool = False,
    lower_column_names: bool = True,
    clean_column_names: bool = False,
) -> pl.LazyFrame | dict[str, pl.LazyFrame]:
```

**Parameters:**
- `source`: Path to the Excel file or file-like object to read
- `sheet_id`: Sheet number to read (cannot be used with sheet_name)
- `sheet_name`: Sheet name to read (cannot be used with sheet_id)
- `table_name`: Name of a specific table to read
- `engine`: Library used to parse the spreadsheet file ('calamine', 'openpyxl', 'xlsx2csv')
- `engine_options`: Additional options passed to the underlying engine
- `read_options`: Options passed to the underlying engine method that reads the sheet data
- `has_header`: Whether the sheet has a header row
- `columns`: Columns to read from the sheet
- `schema_overrides`: Support type specification or override of one or more columns
- `infer_schema_length`: Number of rows to infer the schema from
- `drop_empty_rows`: Remove empty rows from the result
- `drop_empty_cols`: Remove empty columns from the result
- `raise_if_empty`: Raise an exception if the resulting DataFrame is empty
- `header_row`: Row number to use as header (0-indexed)
- `cast`: Dictionary mapping column names to desired data types for casting
- `read_all_sheets`: Read all sheets in the Excel workbook
- `lower_column_names`: Convert column names to lowercase
- `clean_column_names`: Clean column names by stripping punctuation

**Returns:**
- `LazyFrame` or `dict[str, LazyFrame]` if reading multiple sheets

#### `find_header_row`

Finds the header row in an Excel file by identifying the first row with maximum consecutive non-null values.

```python
def find_header_row(
    source: FileSource,
    sheet_id: int | None = None,
    sheet_name: str | None = None,
    max_rows: int = 200,
    expected_keywords: list[str] | None = None,
) -> int:
```

**Parameters:**
- `source`: Path to the Excel file or file-like object to read
- `sheet_id`: Sheet number to read (cannot be used with sheet_name)
- `sheet_name`: Sheet name to read (cannot be used with sheet_id)
- `max_rows`: Maximum number of rows to scan for header identification
- `expected_keywords`: List of keywords to look for in the header row

**Returns:**
- `int`: The zero-based index of the header row

#### `rename_columns`

Rename columns of a Polars DataFrame or LazyFrame.

```python
def rename_columns(
    df: pl.DataFrame | pl.LazyFrame,
    columns_map: dict,
    strict: bool = True
) -> pl.DataFrame | pl.LazyFrame:
```

#### `reorder_columns`

Reorder columns of a Polars DataFrame or LazyFrame.

```python
def reorder_columns(
    df: pl.DataFrame | pl.LazyFrame,
    columns_order: list[str]
) -> pl.DataFrame | pl.LazyFrame:
```

#### `get_missing_columns`

Check if a Polars DataFrame or LazyFrame contains all required columns.

```python
def get_missing_columns(
    df: pl.DataFrame | pl.LazyFrame,
    required_columns: list[str]
) -> list[str]:
```

### File System Module (`rpatoolkit.fs`)

#### `make_unique_dir`

Creates a unique directory with an optionally formatted name based on current date/time and UUID.

```python
def make_unique_dir(
    base_path: str | Path = ".",
    prefix: str | None = "",
    suffix: str | None = str(uuid4()),
    include_date: bool = True,
    include_time: bool = True,
    use_12h_format: bool = True,
    separator: str = "_",
    time_separator: str = ".",
    date_separator: str = ".",
    create: bool = True,
) -> Path:
```

**Parameters:**
- `base_path`: The base directory path where the unique directory will be created
- `prefix`: A prefix to add to the directory name
- `suffix`: A suffix to add to the directory name (defaults to UUID4)
- `include_date`: Whether to include the current date in the directory name
- `include_time`: Whether to include the current time in the directory name
- `use_12h_format`: Whether to use 12-hour format for time (with AM/PM)
- `separator`: The separator to use between different parts of the directory name
- `time_separator`: The separator to use between time components
- `date_separator`: The separator to use between date components
- `create`: Whether to actually create the directory on the filesystem

## Dependencies

This project uses the following dependencies:

- [fastexcel](https://github.com/vinci-ai/fastexcel) (>=0.16.0) - For efficient Excel file reading
- [polars](https://github.com/pola-rs/polars) (>=1.35.2) - For DataFrame operations
- [xlsxwriter](https://github.com/jmcnamara/xlsxwriter) (>=3.2.9) - For Excel file writing capabilities

Development dependencies:
- [pytest](https://github.com/pytest-dev/pytest) (>=9.0.1) - For testing

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run the tests: `pytest`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Running Tests

To run the tests:

```bash
pytest
```

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Run tests
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 fnxL
