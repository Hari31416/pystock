import pandas as pd
from scipy.optimize import minimize
import plotly.express as px

from pystock.exceptions import *
from pystock.utils import *
from pystock.portfolio import *

FREQUENCY = {
    "D": "Daily",
    "W": "Weekly",
    "M": "Monthly",
    "Q": "Quarterly",
    "Y": "Yearly",
}


class Model:
    def __init__(
        self,
        frequency="M",
        risk_free_rate=1 / 3,
    ) -> None:
        self.frequency = frequency
        self.portfolio = None
        self.__risk_free_rate = risk_free_rate

    def __getitem__(self, key):
        if not self.portfolios:
            raise NoPortfolioCreated(
                "No portfolio has been created yet. Use create_portfolio() to create one."
            )
        return self.portfolio[key]

    def __repr__(self) -> str:
        return f"Model(frequency={self.frequency})"

    def set_risk_free_rate(self, rate):
        """
        Sets the risk free rate
        """
        self.__risk_free_rate = rate

    def get_risk_free_rate(self):
        """
        Returns the risk free rate
        """
        return self.__risk_free_rate

    def add_portfolio(self, portfolio: Portfolio, weights="equal", print_summary=False):
        """
        Adds given the portfolio

        Parameters
        ----------
        portfolio : Portfolio
            New portfolio
        weights : list, optional
            List of weights of the stocks, by default None
        print_summary : bool, optional
            Whether to print the summary of the portfolio, by default False

        Returns
        -------
        None
        """
        if self.portfolio:
            raise PortfolioExists(
                "Portfolio already exists. Use update_portfolio() to update it."
            )
        self.market_return = 100 * portfolio.benchmark_return(
            frequency=self.frequency, column="Close"
        )
        # Check if calling summary is needed
        if not portfolio.cov_matrix or print_summary:
            self.portfolio.summary(frequency=self.frequency, weights=weights)
        self.portfolio = portfolio

    def update_portfolio(
        self, portfolio: Portfolio, weights="equal", print_summary=False
    ):
        """
        Updates the portfolio to the new portfolio

        Parameters
        ----------
        portfolio : Portfolio
            New portfolio
        weights : list, optional
            List of weights of the stocks, by default "equal"
        print_summary : bool, optional
            Whether to print the summary of the portfolio, by default False

        Returns
        -------
        None
        """
        self.market_return = 100 * portfolio.benchmark_return(
            frequency=self.frequency, column="Close"
        )

        # Check if calling summary is needed
        if not portfolio.cov_matrix or print_summary:
            self.portfolio.summary(frequency=self.frequency, weights=weights)
        self.portfolio = portfolio

    def load_portfolio(
        self,
        columns=["Adj Close"],
        rename_cols=["Close"],
        frequency="M",
        start_date=None,
        end_date=None,
    ):
        """
        Loads the portfolio data

        Parameters
        ----------
        columns : list, optional
            List of columns to be loaded, by default ["Adj Close"]
        rename_cols : list, optional
            List of columns to be renamed, by default ["Close"]
        frequency : str, optional
            Frequency of the data, by default "M"
        start_date : str, optional
            Start date of the data, by default None
        end_date : str, optional
            End date of the data, by default None

        Raises
        ------
        NoPortfolioCreated
            If no portfolio has been created yet

        Returns
        -------
        None
        """
        if not self.portfolio:
            raise NoPortfolioCreated(
                "No portfolio has been created yet. Use create_portfolio() to create one. Or use add_portfolio() to add one."
            )
        print("Loading benchmark...")
        self.portfolio.load_benchmark(
            columns=columns,
            rename_cols=rename_cols,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )
        print("Loading stocks...")
        self.portfolio.load_all(
            columns=columns,
            rename_cols=rename_cols,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )
        print("Calculating other results...")
        self.market_return = 100 * self.portfolio.benchmark_return(
            frequency=self.frequency, column="Close"
        )
        self.portfolio.summary(frequency=self.frequency)

    def create_portfolio(
        self,
        benchmark_dir,
        benchmark_name,
        stock_dirs=None,
        stock_names=None,
        weights="equal",
        columns=["Adj Close"],
        frequency="M",
        rename_cols=["Close"],
        start_date=None,
        end_date=None,
    ):
        """
        Create a portfolio object from the data directories

        Parameters
        ----------
        benchmark_dir : str
            Directory of the benchmark
        benchmark_name : str
            Name of the benchmark
        stock_dirs : list, optional
            List of directories of the stocks, by default None
        stock_names : list, optional
            List of names of the stocks, by default None
        weights : list, optional
            List of weights of the stocks, by default "equal"
        columns : list, optional
            List of columns to be loaded, by default ["Adj Close"]
        frequency : str, optional
            Frequency of the data, by default "M"
        rename_cols : list, optional
            List of columns to be renamed, by default ["Close"]
        start_date : str, optional
            Start date of the data, by default None
        end_date : str, optional
            End date of the data, by default None

        Returns
        -------
        Portfolio
            Portfolio object
        """
        portfolio = Portfolio(
            benchmark_dir=benchmark_dir,
            benchmark_name=benchmark_name,
            stock_dirs=stock_dirs,
            stock_names=stock_names,
            weights=weights,
        )
        print("Loading benchmark...")
        portfolio.load_benchmark(
            columns=columns,
            rename_cols=rename_cols,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )
        print("Loading stocks...")
        portfolio.load_all(
            columns=columns,
            rename_cols=rename_cols,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )
        print("Calculating other results...")
        self.portfolio = portfolio
        self.market_return = 100 * portfolio.benchmark_return(
            frequency=self.frequency, column="Close"
        )
        self.portfolio.summary(frequency=self.frequency)

        return portfolio

    def _capm_expected_return(self, beta, rm):
        """
        Calculate the expected return of a single stock

        Parameters
        ----------
        beta : float
            Beta of the stock
        rm : float
            Expected return of the market

        Returns
        -------
        float
        """
        return self.__risk_free_rate + beta * (rm - self.__risk_free_rate)

    def _sim_expected_return(self, alpha, beta, rm):
        """
        Calculate the expected return of a single stock using the Single Index Model

        Parameters
        ----------
        alpha : float
            Alpha of the stock
        beta : float
            Beta of the stock
        rm : float
            Expected return of the market

        Returns
        -------
        float
        """
        return self.__risk_free_rate + beta * (rm - self.__risk_free_rate) + alpha

    def _fff_expected_return(self, params, means):
        return np.dot(params, means) * 100

    def expected_return_of_stock(self, stock, model="capm"):
        """
        Calculate the expected return of a single stock

        Parameters
        ----------
        stock : Stock
            Stock object
        model : str, optional
            Model to use for calculating expected return, by default "capm"

        Returns
        -------
        float
        """
        try:
            _ = stock.beta
        except AttributeError:
            raise ValueError(
                "Stock does not have beta value. Please call self.portfolio.summary() to calculate it."
            )
        try:
            _ = stock.params
        except AttributeError:
            print(
                "Warning. FFF params have not been calculated. Using ff3 or ff5 model will result in error."
            )

        if model == "capm":
            _exp_return = self._capm_expected_return(stock.beta, self.market_return)

        elif model == "sim":
            _exp_return = self._sim_expected_return(
                stock.alpha, stock.beta, self.market_return
            )

        elif model == "fff5":
            params = stock.params
            mean_values = self.portfolio.mean_values
            _exp_return = self._fff_expected_return(params=params, means=mean_values)

        elif model == "fff3":
            mask = [0, 1, 2, 3, -1]
            params = stock.params.iloc[mask]
            mean_values = self.portfolio.mean_values.iloc[mask]
            _exp_return = self._fff_expected_return(params=params, means=mean_values)

        else:
            raise ValueError(
                "Model not supported. Supported models are 'capm', 'sim', 'fff3' and 'fff5'."
            )
        stock.expected_return = _exp_return
        return _exp_return

    def portfolio_expected_value(self, weights, expected_returns):
        """
        Get expected value of a portfolio

        Parameters
        ----------
        weights : list
            Weights of the portfolio
        expected_returns : list
            Expected returns of the stocks in the portfolio

        Returns
        -------
        float
            Expected value of the portfolio
        """
        return np.dot(weights, expected_returns)

    def portfolio_variance(self, weights, cov_matrix):
        """
        Get variance of a portfolio

        Parameters
        ----------
        weights : list
            Weights of the portfolio
        cov_matrix : np.array
            Covariance matrix of the stocks in the portfolio

        Returns
        -------
        float
            Variance of the portfolio
        """
        return np.dot(weights, np.dot(cov_matrix, weights)) * 100

    def portfolio_std(self, weights, cov_matrix):
        """
        Get standard deviation of a portfolio

        Parameters
        ----------
        weights : list
            Weights of the portfolio
        cov_matrix : np.array
            Covariance matrix of the stocks in the portfolio

        Returns
        -------
        float
            Standard deviation of the portfolio
        """
        return np.sqrt(self.portfolio_variance(weights, cov_matrix))

    def portfolio_info(self, weights="equal", model="capm"):
        """
        Get expected value, variance and standard deviation of a portfolio

        Parameters
        ----------
        weights : list
            Weights of the portfolio
        model : str
            Model to use for calculating expected returns. Supported models are 'capm' and 'sim'

        Returns
        -------
        tuple
            Expected value, variance and standard deviation of the portfolio
        """
        expected_returns = []
        weights = self.portfolio.set_weights(weights)
        for stock in self.portfolio.stocks:
            expected_returns.append(self.expected_return_of_stock(stock, model=model))
        expected_returns = np.array(expected_returns)
        return (
            self.portfolio_expected_value(weights, expected_returns),
            self.portfolio_variance(weights, self.portfolio.cov_matrix),
            self.portfolio_std(weights, self.portfolio.cov_matrix),
        )

    def portfolio_frontier(self, model="capm"):
        """
        Plots the portfolio frontier for two stocks. Assumes that the portfolio has only two stocks.

        Parameters
        ----------
        model : str
            Model to use for calculating expected returns. Supported models are 'capm' and 'sim'

        Returns
        -------
        None
        """
        if len(self.portfolio.stocks) != 2:
            raise ValueError("Only 2 stocks are supported for now.")
        weights1 = np.linspace(0, 1, 100)
        weights2 = 1 - weights1
        expected_returns = []
        variances = []
        for i in range(len(weights1)):
            weight = np.array([weights1[i], weights2[i]])
            return_, variance, _ = self.portfolio_info(weights=weight, model=model)
            expected_returns.append(return_)
            variances.append(variance)

        variance = np.array(variances)
        expected_returns = np.array(expected_returns)
        assert (
            len(variance) == len(expected_returns) == len(weights1) == len(weights2)
        ), "Lengths of variance and expected returns are not equal."

        plot_df = pd.DataFrame(
            {
                "variance": variance,
                "expected_returns": expected_returns,
                "weights1": weights1,
                "weights2": weights2,
            }
        )
        fig = px.line(
            plot_df,
            x="variance",
            y="expected_returns",
            labels={"x": "Standard deviation", "y": "Expected return"},
            title="Efficient frontier",
            custom_data=["weights1", "weights2"],
        )

        fig.update_traces(
            hovertemplate="Standard deviation: %{x:.4f}%<br>Expected return: %{y:.4f}%<br>Apple weight: %{customdata[0]:.4f}<br>Google weight: %{customdata[1]:.4f}"
        )
        fig.show()

    def optimize_portfolio(self, model="capm", risk=0.5, can_short=False):
        """
        Optimize the portfolio using scipy.optimize.minimize

        Parameters
        ----------
        model : str
            Model to use for calculating expected returns. Supported models are 'capm' and 'sim'
        risk : float
            Risk of the portfolio
        can_short : bool
            Whether the portfolio can short stocks

        Returns
        -------
        dict
            Dictionary containing the optimized weights, expected return, variance and standard deviation
        """
        weights = self.portfolio.set_weights("equal")
        cov_matrix = self.portfolio.cov_matrix
        expected_returns = []

        for stock in self.portfolio.stocks:
            expected_returns.append(self.expected_return_of_stock(stock, model=model))
        expected_returns = np.array(expected_returns)

        if can_short:
            bounds = tuple((-1, 1) for _ in range(len(weights)))
        else:
            bounds = tuple((0, 1) for _ in range(len(weights)))

        constraints = (
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
            {
                "type": "ineq",
                "fun": lambda x: risk - self.portfolio_variance(x, cov_matrix),
            },
        )

        optimized = minimize(
            lambda x: -self.portfolio_expected_value(x, expected_returns),
            weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if optimized["success"]:
            print("Optimized successfully.")
        else:
            print(f"Optimization failed. {optimized['message']}")
            print("Here are the last results:")

        weights = optimized["x"]
        weights = np.round(weights, 4)
        weights = weights / np.sum(weights)
        expected_return, variance, std = self.portfolio_info(
            weights=weights, model=model
        )

        print(f"Expected return: {-optimized['fun']:.4f}%")
        print(f"Variance: {variance:.4f}%")
        print("Expected weights:")
        print("-" * 20)
        for i, stock in enumerate(self.portfolio.stocks):
            print(f"{stock.name}: {weights[i]*100:.2f}%")

        return {
            "weights": weights,
            "expected_return": expected_return,
            "variance": variance,
            "std": std,
        }
