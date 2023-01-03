# pystock

[![PyPI version](https://badge.fury.io/py/pystock0.svg)](https://badge.fury.io/py/pystock0)
[![Downloads](https://static.pepy.tech/personalized-badge/pystock0?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/pystock0)

A small python library for stock market analysis. Especially for portfolio optimization.

## Installation

```bash
pip install pystock0
```

> Note: The library is still in development, so the version number is 0. You will need to call `pip install pystock0` to install the library. However, you can import the library as `import pystock`.

After installation, you can import the library as follows:

```python
import pystock
```

## Usage

The end goal of the library is to provide a simple interface for portfolio optimization. The library is still in development, so the interface is not yet stable. The following example shows how to use the library to optimize a portfolio of stocks.

```python
from pystock.portfolio import Portfolio
from pystock.models import Model

#Creating the benchmark and stocks
benchmark_dir = "Data/GSPC.csv"
benchmark_name = "S&P"

stock_dirs = ["Data/AAPL.csv", "Data/MSFT.csv", "Data/GOOG.csv", "Data/TSLA.csv"]
stock_names = ["AAPL", "MSFT", "GOOG", "TSLA"]

#Setting the frequency to monthly
frequency = "M"

# Creating a Portfolio object
pt = Portfolio(benchmark_dir, benchmark_name, stock_dirs, stock_names)
start_date = "2012-01-01"
end_date = "2022-12-20"

# Loading the data
pt.load_benchmark(
    columns=["Adj Close"],
    rename_cols=["Close"],
    start_date=start_date,
    end_date=end_date,
    frequency=frequency,
)
pt.load_all(
    columns=["Adj Close"],
    rename_cols=["Close"],
    start_date=start_date,
    end_date=end_date,
    frequency=frequency,
)

# Creating a Model object and adding the portfolio
model = Model()
model.add_portfolio(pt, weights="equal")

# Optimizing the portfolio using CAPM
risk = 0.5
model_ = "capm"
res = model.optimize_portfolio(risk=risk, model=model_)
print(res)
```

```output
Optimized successfully.
Expected return: 1.1155%
Variance: 0.5000%
Expected weights:
--------------------
AAPL: 47.20%
MSFT: 0.00%
GOOG: 36.08%
TSLA: 16.73%
{'weights': array([0.4719528 , 0.        , 0.36076392, 0.16728327]), 'expected_return': 1.1154876799508255, 'variance': 0.5000100787030565, 'std': 0.7071139078699107}
```

## More Examples

For more examples, please refer to the notebook [Working_With_pystock.ipynb](https://github.com/Hari31416/pystock/blob/main/Working_With_pystock.ipynb). Also have a look at [Downloading_Data.ipynb](https://github.com/Hari31416/pystock/blob/main/Downloading_Data.ipynb).

## Documentation

The documentation is available at [https://hari31416.github.io/pystock/](https://hari31416.github.io/pystock/).
