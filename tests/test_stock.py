import sys

sys.path.append("/media/hari31416/Hari_SSD/Users/harik/Desktop/pystock")

import os
from pystock.portfolio import Stock
import pytest
import pandas as pd
import copy

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
AAPL_DIR = os.path.join(CUR_DIR, "data", "AAPL.csv")


@pytest.fixture
def stock():

    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Adj Close"]
    rename_col = ["Close"]
    name = "AAPL"
    stock = Stock(name=name, directory=AAPL_DIR)
    _ = stock.load_data(
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )
    return stock


def test_stock_name_dir():
    stock = Stock("AAPL", "dir")
    assert stock.name == "AAPL", "Stock name is not AAPL"
    assert stock.directory == "dir", "Stock directory is not dir"


def test_stock_loaded():
    stock = Stock("AAPL", "dir")
    assert stock.loaded == False, "Stock is loaded"
    with pytest.raises(AttributeError):
        stock.data, "Data is loaded"


def test_stock_str():
    stock = Stock("AAPL", "dir")
    assert str(stock) == f"Stock name: AAPL"


def test_stocks_equal():
    stock1 = Stock("AAPL", "dir")
    stock2 = Stock("AAPL", "dir")
    stock3 = Stock("AAPL", "dir2")
    assert stock1 == stock2, "Stocks are not equal with same name and dir"
    assert (
        stock1 == stock3
    ), "Stocks are not equal with same name and different name dir"


def test_stocks_inequal():
    stock1 = Stock("AAPL", "dir")
    stock2 = Stock("TSLA", "dir")
    stock3 = Stock("AAPL", "dir2")
    assert stock1 != stock2, "Stocks are equal with different name and different dir"
    assert stock2 != stock3, "Stocks are equal with different name and same dir"


def test_stock_data(stock):
    assert len(stock.data) > 0, "Data not loaded"


def test_start_date(stock):
    assert stock.start_date.strftime("%Y-%m-%d") == "2010-01-01"


def test_end_date(stock):
    assert stock.end_date.strftime("%Y-%m-%d") == "2022-12-20"


def test_frequency(stock):
    assert stock.frequency == "D"


def test_column(stock):
    assert len(stock.data.columns) == 1, "More than one columns"
    assert list(stock.data.columns) == ["Close"], "Column name is not Close"


def test_stock_data_df(stock):
    assert isinstance(stock.data, pd.DataFrame)


def test_stock_name_dir_after_load(stock):
    assert stock.name == "AAPL", "Stock name is not AAPL"
    assert stock.directory == AAPL_DIR, "Stock directory is not str"


def test_change_frequency(stock):
    stock2 = copy.deepcopy(stock)
    stock2.change_frequency(frequency="M")
    assert stock2.frequency == "M"


def test_freq_return_mean(stock):
    stock2 = copy.deepcopy(stock)
    assert stock2.return_ == {}, "Return is already calculated"
    assert isinstance(
        stock2.freq_return(frequency="M", mean=True, column="Close"), float
    ), "Return is not float"


def test_freq_return_not_mean(stock):
    stock2 = copy.deepcopy(stock)
    assert stock2.return_ == {}, "Return is already calculated"
    assert isinstance(
        stock.freq_return(frequency="M", mean=False, column="Close"), pd.Series
    ), "Return is not a Series"
