import sys

sys.path.append("/media/hari31416/Hari_SSD/Users/harik/Desktop/pystock")

import os
import pytest
import pandas as pd
import copy
from pystock.portfolio import Portfolio, Stock

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
AAPL_DIR = os.path.join(CUR_DIR, "data", "AAPL.csv")
GOOGL_DIR = os.path.join(CUR_DIR, "data", "GOOGL.csv")
SNP_DIR = os.path.join(CUR_DIR, "data", "GSPC.csv")


@pytest.fixture
def portfolio():
    stock_names = ["AAPL", "GOOGL"]
    stock_dirs = [AAPL_DIR, GOOGL_DIR]
    benchmark_name = "S&P 500"
    benchmark_dir = SNP_DIR
    weights = "equal"

    portfolio = Portfolio(
        benchmark_dir=benchmark_dir,
        benchmark_name=benchmark_name,
        stock_dirs=stock_dirs,
        stock_names=stock_names,
        weights=weights,
    )
    return portfolio


@pytest.fixture
def portfolio_benchmark_loaded(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["close"]
    portfolio2 = copy.deepcopy(portfolio)
    portfolio2.load_benchmark(
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )
    return portfolio2


def test_length():
    portfolio = Portfolio(
        benchmark_dir=SNP_DIR,
        benchmark_name="S&P 500",
        stock_dirs=[AAPL_DIR, GOOGL_DIR],
        stock_names=["AAPL", "GOOGL"],
        weights="equal",
    )
    assert len(portfolio) == 3, "Length of portfolio is not 3"


# Tetsing __init__ method

# Regular cases
def test_init_benchmark(portfolio):
    assert isinstance(portfolio.benchmark, Stock), "Benchmark is not of type Stock"
    assert portfolio.benchmark.name == "S&P 500", "Benchmark is not S&P 500"
    assert portfolio.benchmark_dir == SNP_DIR, "Benchmark directory is not correct"


def test_init_stocks_is_Stock(portfolio):
    assert isinstance(portfolio.stocks, list), "Stocks is not a list"
    assert len(portfolio.stocks) == 2, "Number of stocks is not 2"
    assert isinstance(portfolio.stocks[0], Stock), "First stock is not of type Stock"
    assert isinstance(portfolio.stocks[1], Stock), "Second stock is not of type Stock"


def test_init_stock_names(portfolio):
    assert len(portfolio.stocks) == 2, "Number of stocks is not 2"
    assert portfolio.stock_names == ["AAPL", "GOOGL"], "Stock names are not correct"
    assert portfolio.stocks[0].name == "AAPL", "First stock is not AAPL"
    assert portfolio.stocks[1].name == "GOOGL", "Second stock is not GOOGL"


def test_init_stock_dirs(portfolio):
    assert len(portfolio.stocks) == 2, "Number of stocks is not 2"
    assert portfolio.stock_dirs == [
        AAPL_DIR,
        GOOGL_DIR,
    ], "Stock directories are not correct"
    assert (
        portfolio.stocks[0].directory == AAPL_DIR
    ), "First stock directory is not correct"
    assert (
        portfolio.stocks[1].directory == GOOGL_DIR
    ), "Second stock directory is not correct"


# Stocks should not be loaded


def test_init_stock_loaded(portfolio):
    assert not portfolio.stocks[0].loaded
    assert not portfolio.stocks[0].loaded
    assert not portfolio.benchmark.loaded


# Exception cases


def test_init_without_dirs():
    portfolio = Portfolio(
        benchmark_dir=SNP_DIR,
        benchmark_name="S&P 500",
        stock_dirs=[],
        stock_names=[],
        weights="equal",
    )

    assert portfolio.stocks == [], "Stocks is not empty"
    assert portfolio.stock_names == [], "Stock names is not empty"
    assert portfolio.stock_dirs == [], "Stock directories is not empty"
    assert list(portfolio.weights) == [], "Weights is not empty"

    assert isinstance(portfolio.benchmark, Stock), "Becnchmark is not created"


def test_init_without_names():
    portfolio = Portfolio(
        benchmark_dir=SNP_DIR,
        benchmark_name="S&P 500",
        stock_dirs=[AAPL_DIR, GOOGL_DIR],
        weights="equal",
    )
    assert portfolio.stocks[0].name == "df1", "Default name is not df1"
    assert portfolio.stocks[1].name == "df2", "Default name is not df2"


def test_init_other_params(portfolio):
    assert portfolio.stock_fff_params == {}
    assert portfolio.mean_values is None


# Testing Special Methods


def test_string_representation(portfolio):
    assert (
        str(portfolio)
        == "Portfolio with benchmark S&P 500 and stocks ['AAPL', 'GOOGL']"
    )


def test_represenation(portfolio):
    assert repr(portfolio) == "Portfolio(S&P 500, ['AAPL', 'GOOGL'])"


def test_contains_stock(portfolio):
    assert "AAPL" in portfolio, "AAPL is not in portfolio"
    assert "GOOGL" in portfolio, "GOOGL is not in portfolio"
    assert "S&P 500" in portfolio, "S&P 500 is not in portfolio"
    assert "MSFT" not in portfolio, "MSFT is in portfolio"


def test_iterate_over_stocks(portfolio):
    stocks = [(stock, name) for stock, name in portfolio]
    assert len(stocks) == 3, "Number of stocks is not 3"
    assert isinstance(stocks[0][0], Stock), "Stock is not of type Stock"
    assert stocks[1][1] == "AAPL", "First stock is not AAPL"
    assert stocks[2][1] == "GOOGL", "Second stock is not GOOGL"
    assert stocks[0][1] == "S&P 500", "Third stock is not S&P 500"


def test_get_item_stock(portfolio):
    assert isinstance(portfolio["AAPL"], Stock), "AAPL is not of type Stock"
    assert isinstance(portfolio["GOOGL"], Stock), "GOOGL is not of type Stock"
    assert isinstance(portfolio["S&P 500"], Stock), "S&P 500 is not of type Stock"
    with pytest.raises(KeyError):
        portfolio["MSFT"]


def test_get_item_stock_name(portfolio):
    assert portfolio["AAPL"].name == "AAPL", "AAPL is not in portfolio"
    assert portfolio["GOOGL"].name == "GOOGL", "GOOGL is not in portfolio"
    assert portfolio["S&P 500"].name == "S&P 500", "S&P 500 is not in portfolio"
    with pytest.raises(KeyError):
        portfolio["MSFT"]


# load_benchmark method


def test_load_benchmark(portfolio_benchmark_loaded):
    portfolio2 = copy.deepcopy(portfolio_benchmark_loaded)

    assert portfolio2.benchmark.loaded, "Data not loaded"
    assert isinstance(portfolio2.benchmark.data, pd.DataFrame), "data is not DataFrame"
    assert portfolio2.benchmark.frequency == "D"
    assert portfolio2.benchmark.start_date.strftime("%Y-%m-%d") == "2010-01-01"
    assert portfolio2.benchmark.end_date.strftime("%Y-%m-%d") == "2022-12-20"
    assert list(portfolio2.benchmark.data.columns) == ["close"]


def test_change_benchmark_prev_params_not_load(portfolio_benchmark_loaded):
    portfolio2 = copy.deepcopy(portfolio_benchmark_loaded)
    new_benchmark_dir = GOOGL_DIR
    new_benchmark_name = "Google"
    portfolio2.change_benchmark(
        new_benchmark_dir,
        new_benchmark_name,
        load=False,
    )

    assert portfolio2.benchmark.name == "Google"
    assert portfolio2.benchmark.directory == GOOGL_DIR
    assert not portfolio2.benchmark.loaded, "Data not loaded"
    with pytest.raises(AttributeError):
        portfolio2.benchmark.frequency


def test_change_benchmark_prev_params_load(portfolio_benchmark_loaded):
    portfolio2 = copy.deepcopy(portfolio_benchmark_loaded)
    new_benchmark_dir = GOOGL_DIR
    new_benchmark_name = "Google"
    portfolio2.change_benchmark(
        new_benchmark_dir,
        new_benchmark_name,
        load=True,
    )

    assert portfolio2.benchmark.name == "Google"
    assert portfolio2.benchmark.directory == GOOGL_DIR
    assert portfolio2.benchmark.loaded, "Data not loaded"
    assert portfolio2.benchmark.frequency == "D"
    assert portfolio2.benchmark.start_date.strftime("%Y-%m-%d") == "2010-01-01"
    assert portfolio2.benchmark.end_date.strftime("%Y-%m-%d") == "2022-12-20"
    assert list(portfolio2.benchmark.data.columns) == ["close"]


def test_change_benchmark_not_prev_params(portfolio_benchmark_loaded):
    portfolio2 = copy.deepcopy(portfolio_benchmark_loaded)
    new_benchmark_dir = GOOGL_DIR
    new_benchmark_name = "Google"
    start_date = "2010-01-06"
    end_date = "2022-12-16"
    frequency = "M"
    column = ["Open"]
    rename_col = ["open"]
    portfolio2.change_benchmark(
        new_benchmark_dir,
        new_benchmark_name,
        load=True,
        use_prev=False,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    assert portfolio2.benchmark.name == "Google", "Benchmark not changed"
    assert portfolio2.benchmark.directory == GOOGL_DIR, "Directory not changed"
    assert portfolio2.benchmark.loaded, "Data not loaded"
    assert portfolio2.benchmark.frequency == frequency, "Frequency is incorrect"
    assert portfolio2.benchmark.start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio2.benchmark.end_date.strftime("%Y-%m-%d") == end_date
    assert list(portfolio2.benchmark.data.columns) == rename_col
