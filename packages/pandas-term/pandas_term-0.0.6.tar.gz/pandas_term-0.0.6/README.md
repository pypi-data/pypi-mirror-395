# pandas-term

pandas-term is a CLI bringing [pandas](https://pandas.pydata.org/) operations to the command line.

![Demo](https://vhs.charm.sh/vhs-4JpdYavE1bMhCkcupUKOiY.gif)

> **Note:** Still in early experimental development and may change

## Installation

```bash
pipx install pandas-term
```

or

```bash
uv tool install pandas-term
```

## Usage

All commands accept an input file path (or `-` for stdin) and support `-o/--output` for file output (default: stdout).

### Command Reference

| Command           | Pandas Equivalent      | Description                |
| ----------------- | ---------------------- | -------------------------- |
| `pd select`       | `df[columns]`          | Select columns             |
| `pd drop`         | `df.drop()`            | Drop columns               |
| `pd rename`       | `df.rename()`          | Rename columns             |
| `pd sort`         | `df.sort_values()`     | Sort by columns            |
| `pd dedup`        | `df.drop_duplicates()` | Remove duplicate rows      |
| `pd merge`        | `pd.merge()`           | Merge two dataframes       |
| `pd concat`       | `pd.concat()`          | Concatenate dataframes     |
| `pd batch`        | `df.iloc[]`            | Split into batches         |
| `pd query`        | `df.query()`           | Filter with query expr     |
| `pd head`         | `df.head()`            | First n rows               |
| `pd tail`         | `df.tail()`            | Last n rows                |
| `pd dropna`       | `df.dropna()`          | Drop rows with nulls       |
| `pd describe`     | `df.describe()`        | Descriptive statistics     |
| `pd unique`       | `df[col].unique()`     | Unique values in column    |
| `pd shape`        | `df.shape`             | Dimensions (rows, columns) |
| `pd columns`      | `df.columns`           | Column names               |
| `pd dtypes`       | `df.dtypes`            | Column data types          |
| `pd value-counts` | `df.value_counts()`    | Count unique values        |
| `pd groupby`      | `df.groupby().agg()`   | Group by and aggregate     |

### Transform

```bash
# Select columns
pd select name,age data.csv

# Drop, sort & rename
pd drop unwanted_column data.csv
pd sort age data.csv --descending
pd rename "name:full_name,age:years" data.csv

# Remove duplicates
pd dedup data.csv
pd dedup --subset name,email data.csv

# Merge two dataframes
pd merge left.csv right.csv --on user_id --how inner

# Concatenate files (supports glob patterns)
pd concat file1.csv file2.csv
pd concat "data_*.csv"

# Split into batches
pd batch data.csv --sizes 100 -o "batch_{}.csv"
```

### Filter

```bash
# Query expression
pd query "age > 30 and city == 'NYC'" data.csv

# First/last N rows
pd head --n 100 data.csv
pd tail --n 50 data.csv

# Drop rows with nulls
pd dropna data.csv
pd dropna --subset "name,age" data.csv
```

### Stats

```bash
pd describe data.csv
pd unique country data.csv
pd shape data.csv
pd columns data.csv
pd dtypes data.csv
```

### Aggregate

```bash
# Count unique values
pd value-counts city data.csv
pd value-counts city,department data.csv --normalize

# Group by and aggregate
pd groupby department data.csv --col salary --agg sum
pd groupby "city,department" data.csv --col salary,age --agg mean
```

### Piping

All commands support piping through stdin/stdout. When piping, you can omit the input file argument (it defaults to stdin):

```bash
cat data.csv | pd query "age > 30" | pd select name,age

pd sort age data.csv --descending | pd head --n 10 | pd select name,age
```

### Output Formats

Use `-f`/`--format` for stdout format (default: csv):

```bash
pd head --n 10 data.csv -f json
pd head --n 10 data.csv -f tsv
pd head --n 10 data.csv -f md
```

`--json`/`-j` is shorthand for `-f json`.

File output format is determined by extension:

```bash
pd select name,age data.csv -o output.xlsx
pd query "age > 30" data.json -o filtered.parquet
```

Supported: csv, tsv, json, xlsx, parquet, md

For other extensions, use redirection: `pd select name data.csv -f csv > output.txt`

## Developer setup

Requires [uv](https://docs.astral.sh/uv/)

```bash
# Create venv & install dependencies
uv sync
```

| Command         | Description            |
| --------------- | ---------------------- |
| `make check`    | Format, lint, and test |
| `make test`     | Run tests              |
| `make format`   | Format code            |
| `make lint`     | Linting only           |
| `make coverage` | Tests with coverage    |
