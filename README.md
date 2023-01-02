# pystock

A small python library for stock market analysis. Especially for portfolio optimization.

## Installation

```bash
pip install pystock
```

After installation, you can import the library as follows:

```python
import pystock
```

## Usage

The end goal of the library is to provide a simple interface for portfolio optimization. The library is still in development, so the interface is not yet stable. The following example shows how to use the library to optimize a portfolio of stocks.

```python
from pysotck.portfolio import Portfolio
from pystco.models.import Model

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
risk = 0.1
model_ = "capm"
res = model.optimize_portfolio(m, risk=risk, model=model_)
print(res)
```

For more examples, please refer to the notebook [Working_With_pystock.ipynb](Working_With_pystock.ipynb). Also have a look at [Downloading_Data.ipynb](Downloading_Data.ipynb).
