# pystock

[![PyPI version](https://badge.fury.io/py/pystock0.svg)](https://badge.fury.io/py/pystock0)
[![Downloads](https://static.pepy.tech/personalized-badge/pystock0?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/pystock0)
![example event parameter](https://github.com/hari31416/pystock/actions/workflows/python-package.yml/badge.svg?event=push)

A small python library for stock market analysis. Especially for portfolio optimization.

## Installation

```bash
pip install pystock0
```

> Note: You will need to call `pip install pystock0` to install the library. However, you can import the library as `import pystock`. The library is still in development, so, a lot of changes will be made to the code.

After installation, you can import the library as follows:

```python
import pystock
```

## Usage

The end goal of the library is to provide a simple interface for portfolio optimization. The library is still in development, so the interface is not yet stable. For now, this is how you can use the library to optimize a portfolio of stocks.

```python
from pystock.portfolio import Portfolio
from pystock.models import Model

# Creating the benchmark and stocks
benchmark_dir = "Data/GSPC.csv"
benchmark_name = "S&P"

stock_dirs = ["Data/AAPL.csv", "Data/MSFT.csv", "Data/GOOGL.csv", "Data/TSLA.csv"]
stock_names = ["AAPL", "MSFT", "GOOGL", "TSLA"]

# Setting the frequency to monthly
frequency = "M"

# Creating a Portfolio object
pt = Portfolio(benchmark_dir, benchmark_name, stock_dirs, stock_names)
start_date = "2012-01-01"
end_date = "2022-12-20"

# Loading the data
pt.load_benchmark(
    columns=["Close"],
    start_date=start_date,
    end_date=end_date,
    frequency=frequency,
)
pt.load_all(
    columns=["Close"],
    start_date=start_date,
    end_date=end_date,
    frequency=frequency,
)

# Creating a Model object and adding the portfolio
model = Model(frequency=frequency, risk_free_rate=0.33)
model.add_portfolio(pt, weights="equal")

# Optimizing the portfolio using CAPM
risk = 0.5
model_ = "capm"
res = model.optimize_portfolio(risk=risk, model=model_)
print(res)

```

```output
Optimized successfully.

Expected return: 1.1159%
Risk:            0.5000%
Expected weights:
--------------------
AAPL      :  47.40%
MSFT      :   0.00%
GOOGL     :  35.83%
TSLA      :  16.77%

{'weights': array([0.474 , 0.    , 0.3583, 0.1677]), 'expected_return': 1.115892062822632, 'variance': 0.5000278422222152, 'std': 0.707126468336616}
```

## More Examples

For more examples, please refer to the notebook [Working_With_pystock.ipynb](https://github.com/Hari31416/pystock/blob/main/Working_With_pystock.ipynb). Also have a look at [Downloading_Data.ipynb](https://github.com/Hari31416/pystock/blob/main/Downloading_Data.ipynb).

## Documentation

The documentation is available at [https://hari31416.github.io/pystock/](https://hari31416.github.io/pystock/).
