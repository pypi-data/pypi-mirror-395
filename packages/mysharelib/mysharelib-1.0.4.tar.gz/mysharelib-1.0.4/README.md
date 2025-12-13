
# mysharelib

A Python library for financial data analysis and utilities, focused on Hong Kong stock market data.

## Features

- Fetch Hong Kong stock information and financial reports from EastMoney
- Analyze major shareholders and financial statements
- Scrape Hong Kong stock news from Sina Finance
- Utility functions for logging, caching, and data handling

## Directory Structure

- `src/mysharelib/em/`: EastMoney data fetchers (stock info, balance sheet, cash flow, income, shareholder analysis)
- `src/mysharelib/sina/`: News scraping for HK stocks
- `src/mysharelib/tools.py`: Logging and utility functions
- `log/`: Cached financial data in JSON format
- `tests/`: Pytest-based unit tests

## Installation

Requires Python 3.11–3.12.

```sh
pip install .
```

Or with Poetry:

```sh
poetry install
```

## Dependencies

- openbb-core
- chinese-calendar
- akshare

## Usage Example

```python
from mysharelib.em.get_hk_info_em import get_hk_info_em
df_basic, df_compare = get_hk_info_em("01088.HK")
```

## Development

- Use the `dev` branch for development and `main` for production.
- Run tests with `pytest`.

