import sys

sys.path.append("/media/hari31416/Hari_SSD/Users/harik/Desktop/pystock")

import os
import pytest
import pandas as pd
import copy
from pystock.portfolio import Portfolio, Stock
from pystock.models import Model
from pystock.exceptions import *

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
AAPL_DIR = os.path.join(CUR_DIR, "data", "AAPL.csv")
GOOGL_DIR = os.path.join(CUR_DIR, "data", "GOOGL.csv")
SNP_DIR = os.path.join(CUR_DIR, "data", "GSPC.csv")
DATA_DIR = os.path.join(CUR_DIR, "data")
TOL = 1e-3

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


@pytest.fixture
def empty_model():
    model = Model(
        frequency="D",
        risk_free_rate=0.02,
    )
    return model


@pytest.fixture
def model_with_empty_portfolio(empty_model, empty_portfolio):
    model = copy.deepcopy(empty_model)
    model.portfolio = empty_portfolio
    return model


@pytest.fixture
def model_with_portfolio(empty_model, portfolio):
    model = copy.deepcopy(empty_model)
    model.add_portfolio(portfolio, weights="equal", print_summary=False)
    return model


@pytest.fixture
def model_with_loaded_portfolio(empty_model, loaded_portfolio):
    model = copy.deepcopy(empty_model)
    model.add_portfolio(loaded_portfolio, weights="equal", print_summary=False)
    return model


@pytest.fixture
def final_model(portfolio):
    model = Model(
        frequency="M",
        risk_free_rate=1 / 3,
    )
    portfolio2 = copy.deepcopy(portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    frequency = "M"
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
    model.add_portfolio(portfolio2, weights="equal", print_summary=True)
    model.calculate_fff_params(
        factors=5,
        directory=DATA_DIR,
        frequency="M",
        column="Close",
        verbose=0,
        download=False,
    )
    return model


def test_init(empty_model):
    model = empty_model
    assert model.portfolio is None, "Portfolio is not None"
    assert model.frequency == "D", "Frequency is not D"
    assert model._Model__risk_free_rate == 0.02, "Risk free rate is not 0.02"


def test_representation(empty_model):
    model = empty_model
    assert repr(model) == "Model(frequency=D, rf=0.02)", "Representation is not correct"


def test_get_item_portfolio_error(empty_model):
    model = empty_model
    with pytest.raises(NoPortfolioCreated):
        model["AAPL"]


def test_get_item_portfolio_error2(model_with_empty_portfolio):
    model = model_with_empty_portfolio
    with pytest.raises(KeyError):
        model["AAPL"]


def test_get_item_portfolio(model_with_portfolio):
    model = model_with_portfolio
    assert model["AAPL"].name == "AAPL", "Stock name is not AAPL"
    assert model["GOOGL"].name == "GOOGL", "Stock name is not GOOGL"
    with pytest.raises(KeyError):
        model["MSFT"]


def test_risk_free_setter_getter(empty_model):
    model = empty_model

    assert model.get_risk_free_rate() == 0.02, "Risk free rate is not 0.02"

    model.set_risk_free_rate(0.03)
    assert model.get_risk_free_rate() == 0.03, "Risk free rate is not 0.03"

    with pytest.raises(ValueError):
        model.set_risk_free_rate(-0.03)


def test_add_portfolio_unloaded_portfolio(empty_model, portfolio):
    model = copy.deepcopy(empty_model)
    model.add_portfolio(portfolio, weights="equal", print_summary=False)
    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model.portfolio.weights is not None, "Weights is None"
    assert model.portfolio.benchmark.name == "S&P 500", "Benchmark name is not S&P 500"
    assert model.portfolio.stocks[0].name == "AAPL", "Stock name is not AAPL"
    assert model.portfolio.stocks[1].name == "GOOGL", "Stock name is not GOOGL"
    assert model.portfolio.weights[0] == 0.5, "Weight is not 0.5"
    assert model.portfolio.weights[1] == 0.5, "Weight is not 0.5"

    model = copy.deepcopy(empty_model)
    with pytest.raises(NotLoadedError):
        model.add_portfolio(portfolio, weights=[0.3, 0.7], print_summary=True)


def test_add_portfolio_loaded_portfolio(empty_model, loaded_portfolio):
    model = copy.deepcopy(empty_model)
    model.add_portfolio(loaded_portfolio, weights="equal", print_summary=False)
    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model.portfolio.weights is not None, "Weights is None"
    assert model.portfolio.benchmark.name == "S&P 500", "Benchmark name is not S&P 500"
    assert model.portfolio.stocks[0].name == "AAPL", "Stock name is not AAPL"
    assert model.portfolio.stocks[1].name == "GOOGL", "Stock name is not GOOGL"
    assert model.portfolio.weights[0] == 0.5, "Weight is not 0.5"
    assert model.portfolio.weights[1] == 0.5, "Weight is not 0.5"
    with pytest.raises(AttributeError):
        model.portfolio.cov_matrix

    model = copy.deepcopy(empty_model)
    model.add_portfolio(loaded_portfolio, weights=[0.3, 0.7], print_summary=True)
    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is not None"
    assert model.portfolio.weights is not None, "Weights is not None"
    assert model.portfolio.benchmark.name == "S&P 500", "Benchmark name is not S&P 500"
    assert model.portfolio.stocks[0].name == "AAPL", "Stock name is not AAPL"
    assert model.portfolio.stocks[1].name == "GOOGL", "Stock name is not GOOGL"
    assert model.portfolio.weights[0] == 0.3, "Weight is not 0.3"
    assert model.portfolio.weights[1] == 0.7, "Weight is not 0.7"

    assert model.portfolio.stocks[0].data is not None, "Stock data is None"
    assert model.portfolio.stocks[1].data is not None, "Stock data is None"
    assert isinstance(
        model.portfolio.stocks_summary, pd.DataFrame
    ), "Stock summary is not a DataFrame"
    assert isinstance(model.portfolio.params, dict), "Stock summary is not a dictionary"
    assert isinstance(
        model.portfolio.cov_matrix, pd.DataFrame
    ), "Benchmark summary is not a DataFrame"


def test_add_portfolio_exist(empty_model, loaded_portfolio):
    model = copy.deepcopy(empty_model)
    model.add_portfolio(loaded_portfolio, weights="equal", print_summary=False)
    with pytest.raises(PortfolioExists):
        model.add_portfolio(loaded_portfolio, weights="equal", print_summary=False)


def test_load_portfolio_no_portfolio_error(empty_model):
    model = empty_model
    with pytest.raises(NoPortfolioCreated):
        model.load_portfolio()


def test_load_portfolio_no_summary(model_with_portfolio):
    model = copy.deepcopy(model_with_portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    column = ["Close"]
    rename_col = ["Close"]
    frequency = "D"
    model.load_portfolio(
        columns=column,
        rename_cols=rename_col,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        print_summary=False,
    )

    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model.portfolio.weights is not None, "Weights is None"
    assert model.portfolio.benchmark.name == "S&P 500", "Benchmark name is not S&P 500"
    assert model.portfolio.stocks[0].name == "AAPL", "Stock name is not AAPL"
    assert model.portfolio.stocks[1].name == "GOOGL", "Stock name is not GOOGL"
    assert model.portfolio.weights[0] == 0.5, "Weight is not 0.5"
    assert model.portfolio.weights[1] == 0.5, "Weight is not 0.5"


def test_load_portfolio_with_summary(model_with_portfolio):
    model = copy.deepcopy(model_with_portfolio)
    start_date = "2010-01-01"
    end_date = "2022-12-20"
    column = ["Close"]
    rename_col = ["Close"]
    frequency = "D"
    model.load_portfolio(
        columns=column,
        rename_cols=rename_col,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        print_summary=True,
    )

    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model.portfolio.weights is not None, "Weights is None"
    assert model.portfolio.benchmark.name == "S&P 500", "Benchmark name is not S&P 500"
    assert model.portfolio.stocks[0].name == "AAPL", "Stock name is not AAPL"
    assert model.portfolio.stocks[1].name == "GOOGL", "Stock name is not GOOGL"
    assert model.portfolio.weights[0] == 0.5, "Weight is not 0.5"
    assert model.portfolio.weights[1] == 0.5, "Weight is not 0.5"

    assert model.portfolio.stocks[0].data is not None, "Stock data is None"
    assert model.portfolio.stocks[1].data is not None, "Stock data is None"
    assert isinstance(
        model.portfolio.stocks_summary, pd.DataFrame
    ), "Stock summary is not a DataFrame"
    assert isinstance(model.portfolio.params, dict), "Stock summary is not a dictionary"
    assert isinstance(
        model.portfolio.cov_matrix, pd.DataFrame
    ), "Benchmark summary is not a DataFrame"


def test_create_portfolio_not_load(empty_model):
    model = copy.deepcopy(empty_model)
    stock_names = ["AAPL", "GOOGL"]
    stock_dirs = [AAPL_DIR, GOOGL_DIR]
    benchmark_name = "S&P 500"
    benchmark_dir = SNP_DIR
    weights = "equal"

    model.create_portfolio(
        stock_names=stock_names,
        stock_dirs=stock_dirs,
        benchmark_name=benchmark_name,
        benchmark_dir=benchmark_dir,
        weights=weights,
        load_data=False,
    )

    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model["AAPL"].loaded == False, "AAPL is loaded"
    assert model.portfolio._all_set == False, "All set is True"


def test_create_portfolio_load(empty_model):
    model = copy.deepcopy(empty_model)
    stock_names = ["AAPL", "GOOGL"]
    stock_dirs = [AAPL_DIR, GOOGL_DIR]
    benchmark_name = "S&P 500"
    benchmark_dir = SNP_DIR
    weights = "equal"
    columns = ["Close"]
    rename_cols = ["Close"]
    start_date = "2010-01-05"
    end_date = "2022-12-20"
    frequency = "D"

    model.create_portfolio(
        stock_names=stock_names,
        stock_dirs=stock_dirs,
        benchmark_name=benchmark_name,
        benchmark_dir=benchmark_dir,
        weights=weights,
        load_data=True,
        print_summary=True,
        columns=columns,
        rename_cols=rename_cols,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )
    assert model.portfolio is not None, "Portfolio is None"
    assert model.portfolio.benchmark is not None, "Benchmark is None"
    assert model.portfolio.stocks is not None, "Stocks is None"
    assert model["AAPL"].loaded == True, "AAPL is not loaded"
    assert model.portfolio._all_set == True, "All set is False"
    assert model.portfolio.stocks[0].data is not None, "Stock data is None"
    assert (
        model.portfolio["AAPL"].data.columns[0] == "Close"
    ), "Column name is not Close"
    assert (
        model.portfolio["AAPL"].start_date.strftime("%Y-%m-%d") == "2010-01-05"
    ), "Start date is not 2010-01-05"
    assert (
        model.portfolio["AAPL"].end_date.strftime("%Y-%m-%d") == "2022-12-20"
    ), "End date is not 2022-12-20"


def test_optimize_portfolio_err_fff_models(model_with_loaded_portfolio):
    model = copy.deepcopy(model_with_loaded_portfolio)
    with pytest.raises(AttributeError):
        model.optimize_portfolio(model="fff3")
    with pytest.raises(AttributeError):
        model.optimize_portfolio(model="fff5")

    assert isinstance(
        model.optimize_portfolio(model="capm"), dict
    ), "Result of capm is not a dict"
    assert isinstance(
        model.optimize_portfolio(model="sim"), dict
    ), "Result of ff3 is not a dict"


def test_optimize_portfolio_err_other_models(model_with_loaded_portfolio):
    model = copy.deepcopy(model_with_loaded_portfolio)
    with pytest.raises(ValueError):
        model.optimize_portfolio(model="other")


def test_optimize_portfolio_all_models_format(model_with_loaded_portfolio):
    model = copy.deepcopy(model_with_loaded_portfolio)
    model.calculate_fff_params(
        factors=5,
        directory=DATA_DIR,
        frequency="M",
        column="Close",
        verbose=0,
        download=False,
    )
    assert isinstance(
        model.optimize_portfolio(model="capm"), dict
    ), "Result of capm is not a dict"
    assert isinstance(
        model.optimize_portfolio(model="sim"), dict
    ), "Result of ff3 is not a dict"
    assert isinstance(
        model.optimize_portfolio(model="fff3"), dict
    ), "Result of ff3 is not a dict"
    assert isinstance(
        model.optimize_portfolio(model="fff5"), dict
    ), "Result of ff5 is not a dict"


def test_optimize_capm(final_model):
    model = copy.deepcopy(final_model)
    res = model.optimize_portfolio(model="capm", risk=1.0)
    assert isinstance(res, dict), "Result of ff5 is not a dict"
    assert res["expected_return"] > 0, "Expected return is not positive"
    assert res["expected_return"] > 1.0, "Expected return is too low"
    assert res["expected_return"] < 2, "Expected return is not less than 2"
    assert res["variance"] > 0, "variance is not positive"
    assert res["variance"] < 1, "variance is not less than 2"
    assert res["weights"] is not None, "Weights is None"
    assert abs(sum(res["weights"]) - 1) < TOL, "Weights do not sum to 1"


def test_optimize_sim(final_model):
    model = copy.deepcopy(final_model)
    res = model.optimize_portfolio(model="sim", risk=1.0)
    assert isinstance(res, dict), "Result of ff5 is not a dict"
    assert res["expected_return"] > 0, "Expected return is not positive"
    assert res["expected_return"] > 1.0, "Expected return is too low"
    assert res["expected_return"] < 2, "Expected return is not less than 2"
    assert res["variance"] > 0, "variance is not positive"
    assert res["variance"] < 1, "variance is not less than 2"
    assert res["weights"] is not None, "Weights is None"
    assert abs(sum(res["weights"]) - 1) < TOL, "Weights do not sum to 1"


def test_optimize_fff3(final_model):
    model = copy.deepcopy(final_model)
    res = model.optimize_portfolio(model="fff3", risk=1.0)
    assert isinstance(res, dict), "Result of fff3 is not a dict"
    assert res["expected_return"] > 0, "Expected return is not positive"
    assert res["expected_return"] > 1.5, "Expected return is too low"
    assert res["expected_return"] < 2, "Expected return is not less than 2"
    assert res["variance"] > 0, "variance is not positive"
    assert res["variance"] < 1, "variance is not less than 2"
    assert res["weights"] is not None, "Weights is None"
    assert abs(sum(res["weights"]) - 1) < TOL, "Weights do not sum to 1"

def test_optimize_fff5(final_model):
    model = copy.deepcopy(final_model)
    res = model.optimize_portfolio(model="fff5", risk=1.0)
    assert isinstance(res, dict), "Result of fff5 is not a dict"
    assert res["expected_return"] > 0, "Expected return is not positive"
    assert res["expected_return"] > 1.5, "Expected return is too low"
    assert res["expected_return"] < 2, "Expected return is not less than 2"
    assert res["variance"] > 0, "variance is not positive"
    assert res["variance"] < 1, "variance is not less than 2"
    assert res["weights"] is not None, "Weights is None"
    assert abs(sum(res["weights"]) - 1) < TOL, "Weights do not sum to 1"
