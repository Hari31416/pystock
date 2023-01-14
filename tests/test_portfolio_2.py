import sys

sys.path.append("/media/hari31416/Hari_SSD/Users/harik/Desktop/pystock")

import os
import pytest
import pandas as pd
import copy
from pystock.portfolio import Portfolio, Stock
from pystock.exceptions import *

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
AAPL_DIR = os.path.join(CUR_DIR, "data", "AAPL.csv")
GOOGL_DIR = os.path.join(CUR_DIR, "data", "GOOGL.csv")
SNP_DIR = os.path.join(CUR_DIR, "data", "GSPC.csv")
DATA_DIR = os.path.join(CUR_DIR, "data")

FREQUENCY = {
    "D": "Daily",
    "W": "Weekly",
    "M": "Monthly",
    "Q": "Quarterly",
    "Y": "Yearly",
}


@pytest.fixture
def empty_portfolio():
    stock_names = []
    stock_dirs = []
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
def loaded_portfolio(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["Close"]
    portfolio2 = copy.deepcopy(portfolio)
    portfolio2.load_benchmark(
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )
    portfolio2.load_all(
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )
    return portfolio2


def test_load_one_stock_empty_error(empty_portfolio):
    portfolio = empty_portfolio
    with pytest.raises(ValueError):
        portfolio.load_one_stock("AAPL")


def test_load_one_stock(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-17"
    frequency = "M"
    column = ["Close"]
    rename_col = ["close"]
    _ = portfolio2.load_one_stock(
        name="AAPL",
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    assert portfolio2["AAPL"].loaded == True, "Data not loaded"
    assert portfolio2["GOOGL"].loaded == False, "Other stock Data loaded"
    assert portfolio2["AAPL"].frequency == frequency, "Frequency is incorrect"
    assert portfolio2["AAPL"].start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio2["AAPL"].end_date.strftime("%Y-%m-%d") == end_date
    assert list(portfolio2["AAPL"].data.columns) == rename_col


def test_load_one_stock_overwrite_true(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-17"
    frequency = "M"
    column = ["Close"]
    rename_col = ["close"]
    _ = portfolio2.load_one_stock(
        name="AAPL",
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    start_date_2 = "2010-03-01"
    end_date_2 = "2022-12-20"
    frequency_2 = "D"
    column_2 = ["Open"]
    rename_col_2 = ["o"]

    _ = portfolio2.load_one_stock(
        name="AAPL",
        start_date=start_date_2,
        end_date=end_date_2,
        frequency=frequency_2,
        columns=column_2,
        rename_cols=rename_col_2,
        overwrite=True,
    )

    assert portfolio2["AAPL"].loaded == True, "Data not loaded"
    assert portfolio2["GOOGL"].loaded == False, "Other stock Data loaded"
    assert portfolio2["AAPL"].frequency == frequency_2, "Frequency is incorrect"
    assert portfolio2["AAPL"].start_date.strftime("%Y-%m-%d") == start_date_2
    assert portfolio2["AAPL"].end_date.strftime("%Y-%m-%d") == end_date_2
    assert list(portfolio2["AAPL"].data.columns) == rename_col_2


def test_load_one_stock_overwrite_false(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-17"
    frequency = "M"
    column = ["Close"]
    rename_col = ["close"]
    _ = portfolio2.load_one_stock(
        name="AAPL",
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    start_date_2 = "2010-03-01"
    end_date_2 = "2022-12-20"
    frequency_2 = "D"
    column_2 = ["Open"]
    rename_col_2 = ["o"]

    _ = portfolio2.load_one_stock(
        name="AAPL",
        start_date=start_date_2,
        end_date=end_date_2,
        frequency=frequency_2,
        columns=column_2,
        rename_cols=rename_col_2,
        overwrite=False,
    )

    assert portfolio2["AAPL"].loaded == True, "Data not loaded"
    assert portfolio2["GOOGL"].loaded == False, "Other stock Data loaded"
    assert portfolio2["AAPL"].frequency == frequency, "Frequency is incorrect"
    assert portfolio2["AAPL"].start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio2["AAPL"].end_date.strftime("%Y-%m-%d") == end_date
    assert list(portfolio2["AAPL"].data.columns) == rename_col


def test_load_all(portfolio):
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-17"
    frequency = "M"
    column = ["Close"]
    rename_col = ["close"]
    _ = portfolio2.load_all(
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    assert portfolio2["AAPL"].loaded == True, "Data not loaded"
    assert portfolio2["GOOGL"].loaded == True, "Data not loaded"
    assert portfolio2["AAPL"].frequency == frequency, "Frequency is incorrect"
    assert portfolio2["GOOGL"].frequency == frequency, "Frequency is incorrect"
    assert portfolio2["AAPL"].start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio2["AAPL"].end_date.strftime("%Y-%m-%d") == end_date
    assert list(portfolio2["AAPL"].data.columns) == rename_col
    assert portfolio2["GOOGL"].start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio2["GOOGL"].end_date.strftime("%Y-%m-%d") == end_date
    assert list(portfolio2["GOOGL"].data.columns) == rename_col


def test_add_stocks_Stock_not_load(empty_portfolio):
    portfolio = copy.deepcopy(empty_portfolio)
    apple = Stock("AAPL", AAPL_DIR)
    google = Stock("GOOGL", GOOGL_DIR)
    stocks = [apple, google]

    portfolio.add_stocks(stocks=stocks, load_data=False)

    assert len(portfolio) == 3, "Stocks not created"
    assert len(portfolio.stocks) == 2, "Stocks not created"
    assert portfolio.stocks[0].loaded == False, "Stock Loaded"
    assert portfolio.stocks[1].loaded == False, "Stock Loaded"
    with pytest.raises(AttributeError):
        portfolio.stocks[0].frequency


def test_add_stocks_Stock_load(empty_portfolio):
    portfolio = copy.deepcopy(empty_portfolio)
    apple = Stock("AAPL", AAPL_DIR)
    google = Stock("GOOGL", GOOGL_DIR)
    stocks = [apple, google]
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["close"]
    portfolio.add_stocks(
        stocks=stocks,
        load_data=True,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    assert len(portfolio) == 3, "Stocks not created"
    assert len(portfolio.stocks) == 2, "Stocks not created"
    assert portfolio.stocks[0].loaded == True, "Stock not Loaded"
    assert portfolio.stocks[1].loaded == True, "Stock not Loaded"
    assert (
        portfolio.stocks[0].frequency == portfolio.stocks[0].frequency == frequency
    ), "Frequency not correct"


def test_add_stocks_Stock_load_overwrite_false(empty_portfolio):
    portfolio = copy.deepcopy(empty_portfolio)
    apple = Stock("AAPL", AAPL_DIR)
    google = Stock("GOOGL", GOOGL_DIR)
    stocks = [apple, google]
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["close"]
    portfolio.add_stocks(
        stocks=stocks,
        load_data=True,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
        overwrite=False,
    )

    start_date_2 = "2010-03-01"
    end_date_2 = "2022-12-20"
    frequency_2 = "D"
    column_2 = ["Open"]
    rename_col_2 = ["o"]
    portfolio.add_stocks(
        stocks=stocks,
        load_data=True,
        start_date=start_date_2,
        end_date=end_date_2,
        frequency=frequency_2,
        columns=column_2,
        rename_cols=rename_col_2,
        overwrite=False,
    )

    assert len(portfolio) == 3, "Stocks not created"
    assert len(portfolio.stocks) == 2, "Stocks not created"
    assert portfolio.stocks[0].loaded == True, "Stock not Loaded"
    assert portfolio.stocks[1].loaded == True, "Stock not Loaded"
    assert (
        portfolio.stocks[0].frequency == portfolio.stocks[0].frequency == frequency
    ), "Frequency not correct"
    assert portfolio.stocks[0].start_date.strftime("%Y-%m-%d") == start_date
    assert portfolio.stocks[0].end_date.strftime("%Y-%m-%d") == end_date


def test_add_stocks_Stock_load_overwrite_true(empty_portfolio):
    portfolio = copy.deepcopy(empty_portfolio)
    apple = Stock("AAPL", AAPL_DIR)
    google = Stock("GOOGL", GOOGL_DIR)
    stocks = [apple, google]
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["close"]
    portfolio.add_stocks(
        stocks=stocks,
        load_data=True,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    start_date_2 = "2010-03-01"
    end_date_2 = "2022-12-20"
    frequency_2 = "D"
    column_2 = ["Open"]
    rename_col_2 = ["o"]
    portfolio.add_stocks(
        stocks=stocks,
        load_data=True,
        start_date=start_date_2,
        end_date=end_date_2,
        frequency=frequency_2,
        columns=column_2,
        rename_cols=rename_col_2,
        overwrite=True,
    )

    assert len(portfolio) == 3, "Stocks not created"
    assert len(portfolio.stocks) == 2, "Stocks not created"
    assert portfolio.stocks[0].loaded == True, "Stock not Loaded"
    assert portfolio.stocks[1].loaded == True, "Stock not Loaded"
    assert (
        portfolio.stocks[0].frequency == portfolio.stocks[0].frequency == frequency_2
    ), "Frequency not correct"
    assert portfolio.stocks[0].start_date.strftime("%Y-%m-%d") == start_date_2
    assert portfolio.stocks[0].end_date.strftime("%Y-%m-%d") == end_date_2
    assert portfolio._all_set == False, "All set not False"


def test_add_stocks_directory(empty_portfolio):
    portfolio = copy.deepcopy(empty_portfolio)
    directory = [AAPL_DIR, GOOGL_DIR]
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "D"
    column = ["Close"]
    rename_col = ["close"]
    portfolio.add_stocks(
        stock_names=["AAPL", "GOOGL"],
        stock_dirs=directory,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        columns=column,
        rename_cols=rename_col,
    )

    assert len(portfolio) == 3, "Stocks not created"
    assert len(portfolio.stocks) == 2, "Stocks not created"
    assert portfolio.stocks[0].loaded == True, "Stock not Loaded"
    assert portfolio.stocks[1].loaded == True, "Stock not Loaded"
    assert (
        portfolio.stocks[0].frequency == portfolio.stocks[0].frequency == frequency
    ), "Frequency not correct"


def test_remove_stocks_single(portfolio):
    portfolio2 = copy.deepcopy(portfolio)

    portfolio2.remove_stocks(["AAPL"])

    assert len(portfolio2) == 2, "Stocks not removed"
    assert len(portfolio2.stocks) == 1, "Stocks not removed"
    assert portfolio2._all_set == False, "All set not False"


def test_remove_stocks_multiple(portfolio):
    portfolio2 = copy.deepcopy(portfolio)

    portfolio2.remove_stocks(["AAPL", "GOOGL"])

    assert len(portfolio2) == 1, "Stocks not removed"
    assert len(portfolio2.stocks) == 0, "Stocks not removed"


def test_get_stock_return_not_loaded(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(NotLoadedError):
        r, v = portfolio.get_stock_return(
            "AAPL",
            frequency="M",
            column="Close",
        )


def test_get_stock_return_no_stock(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(StockException):
        r, v = portfolio.get_stock_return(
            "MSFT",
            frequency="M",
            column="Close",
        )


def test_get_stock_return_no_column(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    with pytest.raises(ColumnNotFound):
        r, v = portfolio.get_stock_return(
            "AAPL",
            frequency="M",
            column="foo",
        )


def test_get_stock_r_v(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    r, v = portfolio.get_stock_return(
        "AAPL",
        frequency="M",
        column="Close",
    )

    assert isinstance(r, float), "Return not correct"
    assert isinstance(v, float), "Variance not correct"


def test_get_all_stock_returns_not_loaded(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(NotLoadedError):
        r, v = portfolio.get_all_stock_returns(
            frequency="M",
            column="Close",
        )


def test_get_all_stock_returns(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    df = portfolio.get_all_stock_returns(
        frequency="M",
        column="Close",
    )

    assert isinstance(df, pd.DataFrame), "Incorrect return type"
    assert len(df) == 2, "Return not correct"
    assert len(df.columns) == 3, "Return not correct"
    assert df.columns[0] == "Stock", "Return not correct"
    assert df.columns[1] == f"{FREQUENCY['M']}_Mean_Return", "Frequency is incorrect"
    assert df.columns[2] == f"{FREQUENCY['M']}_Return_STD", "Frequency is incorrect"


def test_stock_prepare_params_not_loaded(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(NotLoadedError):
        portfolio._Portfolio__stock_params_prepare(
            "AAPL",
            frequency="M",
            column="Close",
        )

    with pytest.raises(StockException):
        portfolio._Portfolio__stock_params_prepare(
            "HMM",
            frequency="M",
            column="Close",
        )


def test_stock_prepare_params_loaded_wrong_column(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)

    with pytest.raises(ColumnNotFound):
        portfolio._Portfolio__stock_params_prepare(
            "AAPL",
            frequency="M",
            column="HMM",
        )


def test_stock_prepare_params_loaded(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    name = "AAPL"
    column = "Close"
    df = portfolio._Portfolio__stock_params_prepare(
        name,
        frequency="M",
        column=column,
    )

    assert (
        df.shape[1] == 2
    ), f"Number of colmuns {df.shape[1]}, Data not merged properly."
    assert df.shape[0] > 0, "No data found"

    assert list(df.columns) == [f"{name}_{column}", f"S&P 500_{column}"]


def test_get_stock_params_not_loaded(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(NotLoadedError):
        portfolio.get_stock_params(
            "AAPL",
            frequency="M",
            how="inner",
            column="Close",
        )


def test_get_stock_params_loaded(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    a, b = portfolio.get_stock_params(
        "AAPL",
        frequency="M",
        how="inner",
        column="Close",
    )
    assert isinstance(a, float), "alpha is not float"
    assert isinstance(b, float), "beta is not float"
    assert portfolio["AAPL"].alpha == a, "Different alpha saved"
    assert portfolio["AAPL"].beta == b, "Different beta saved"
    with pytest.raises(AttributeError):
        portfolio["GOOGL"].alpha


def test_get_all_stock_params_not_loaded(portfolio):
    portfolio = copy.deepcopy(portfolio)
    with pytest.raises(NotLoadedError):
        portfolio.get_all_stock_params(
            frequency="M",
            how="inner",
            column="Close",
        )


def test_get_all_stock_params_loaded_dict(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    dict_ = portfolio.get_all_stock_params(
        frequency="M",
        how="inner",
        column="Close",
        return_dict=True,
    )

    assert isinstance(dict_, dict), "Incorrect format"
    assert list(dict_.keys()) == ["Stock", "Alpha", "Beta"]


def test_get_all_stock_params_loaded_df(loaded_portfolio):
    portfolio = copy.deepcopy(loaded_portfolio)
    df = portfolio.get_all_stock_params(
        frequency="M",
        how="inner",
        column="Close",
        return_dict=False,
    )

    assert isinstance(df, pd.DataFrame), "Incorrect format"
    assert len(df) == 2, "Length incorrect"
    assert list(df.columns) == ["Stock", "Alpha", "Beta"]


def test_portfolio_return_not_loaded(portfolio):
    portfolio = portfolio
    with pytest.raises(NotLoadedError):
        portfolio.get_portfolio_return()


def test_portfolio_return_loaded(loaded_portfolio):
    portfolio = loaded_portfolio
    r, v = portfolio.get_portfolio_return()
    assert isinstance(r, float), "Return not correct"
    assert isinstance(v, float), "Variance not correct"


def test_summary_print_too(loaded_portfolio):
    portfolio = loaded_portfolio
    portfolio.summary()
    assert isinstance(portfolio.cov_matrix, pd.DataFrame)


def test_summary_just_params(loaded_portfolio):
    portfolio = loaded_portfolio
    portfolio.summary(just_load=False)
    assert isinstance(portfolio.cov_matrix, pd.DataFrame)


def test_calculate_fff_params_one_local_not_loaded(portfolio):
    portfolio = portfolio
    assert portfolio["AAPL"].loaded == False
    with pytest.raises(NotLoadedError):
        portfolio.calculate_fff_params_one(
            "AAPL",
            directory=DATA_DIR,
            download=False,
        )


def test_calculate_fff_params_one_local_loaded(loaded_portfolio):
    portfolio = loaded_portfolio
    res = portfolio.calculate_fff_params_one(
        "AAPL", directory=DATA_DIR, download=False, factors=5
    )

    assert isinstance(res, pd.Series)
    assert len(res) == 7


def test_calculate_fff_params_all_local_loaded_five(loaded_portfolio):
    portfolio = loaded_portfolio
    _ = portfolio.calculate_fff_params(
        directory=DATA_DIR,
        download=False,
        factors=5,
    )

    assert isinstance(portfolio.stock_fff_params, dict), "Not a dict"
    assert len(portfolio.stock_fff_params) == len(portfolio), "Not all stocks"
    assert isinstance(portfolio.stock_fff_params["AAPL"], pd.Series), "Not a series"
    assert portfolio.stock_fff_params["Coefficients"] == [
        "const",
        "Mkt-RF",
        "SMB",
        "HML",
        "RMW",
        "CMA",
        "rf",
    ], "Not correct order"


def test_calculate_fff_params_all_local_loaded_three(loaded_portfolio):
    portfolio = loaded_portfolio
    _ = portfolio.calculate_fff_params(
        directory=DATA_DIR,
        download=False,
        factors=3,
    )

    assert isinstance(portfolio.stock_fff_params, dict), "Not a dict"
    assert len(portfolio.stock_fff_params) == len(portfolio), "Not all stocks"
    assert isinstance(portfolio.stock_fff_params["AAPL"], pd.Series), "Not a series"
    assert portfolio.stock_fff_params["Coefficients"] == [
        "const",
        "Mkt-RF",
        "SMB",
        "HML",
        "rf",
    ], "Not correct order"


# def test_calculate_fff_params_one_download(loaded_portfolio):
#     portfolio = loaded_portfolio
#     res = portfolio.calculate_fff_params_one(
#         "AAPL", directory=DATA_DIR, download=True, factors=3
#     )

#     assert isinstance(res, pd.Series)
#     assert len(res) == 5


# def test_calculate_fff_params_all_download(loaded_portfolio):
#     portfolio = loaded_portfolio
#     portfolio.calculate_fff_params(
#         factors=5,
#         directory=DATA_DIR,
#         frequency="M",
#         column="Close",
#         verbose=0,
#         download=True,
#     )

#     assert isinstance(portfolio.stock_params, dict)
#     assert len(portfolio.stock_params) == 2
