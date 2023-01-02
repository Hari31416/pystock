import pandas as pd
import datetime
import numpy as np


def _convert_str_to_date_(self, string, format="%Y-%m-%d"):
    """
    Convert string to date

    Parameters
    ----------
    string : str
        String to convert
    format : str, optional
        Format of the string, by default "%Y-%m-%d"

    Returns
    -------
    datetime.date
        Date
    """
    if isinstance(string, datetime.date):
        return string
    if not string:
        return None
    return datetime.datetime.strptime(string, format)


def load_data(
    directory,
    start_date=None,
    end_date=None,
    columns=None,
    frequency="D",
    rename_cols=None,
):
    """
    Read data from a csv file and return a dataframe.
    Assumes that the dataframe has column `Date` containing dates.

    Parameters
    ----------
    start_date : str, optional
        Start date of the data, by default None
    end_date : str, optional
        End date of the data, by default None
    columns : list, optional
        Columns to keep, by default None which means keep all columns
    frequency : str, optional
        Frequency of the data, by default "D"
    rename_cols : list, optional
        Columns to rename, by default None

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(directory, parse_dates=["Date"], index_col="Date")

    df.sort_index(inplace=True)
    smallest_date = df.index[0]
    largest_date = df.index[-1]
    start_date = _convert_str_to_date_(start_date)
    end_date = _convert_str_to_date_(end_date)

    if start_date and start_date < smallest_date:
        raise ValueError(
            "Start date is before the data starts. If you don't want to specify a start date, set it to None."
        )

    if end_date and end_date > largest_date:
        raise ValueError(
            "End date is after the data ends. If you don't want to specify an end date, set it to None."
        )

    if not start_date:
        start_date = df.index[0]
    if not end_date:
        end_date = df.index[-1]
    date_range = (start_date, end_date)
    df = df[(df.index >= date_range[0]) & (df.index <= date_range[1])]
    if columns:
        try:
            df = df[columns]
        except KeyError:
            print("Column not found. Please check the column names.")
            raise (KeyError)
    if rename_cols:
        try:
            df.columns = rename_cols
        except ValueError:
            print("Number of columns to rename does not match the number of columns.")
            raise (ValueError)
    df = df.asfreq(frequency, "ffill").dropna()
    return df


def merge_dfs(dfs, df_names=None, join="inner"):
    """
    Merges a list of dataframes into one. Uses the index as the key and `pd.concat` to merge the dataframes

    Parameters
    ----------
    dfs : list
        List of dataframes to merge
    df_names : list, optional
        Names of the dataframes, by default None Uses this to rename the columns of the merged dataframe
    join : str, optional
        How to join the dataframes, by default "inner"

    Returns
    -------
    pd.DataFrame
        Merged dataframe
    """
    df = pd.concat(dfs, axis=1, join=join)
    if df_names:
        cols = []
        for stock, name in zip(dfs, df_names):
            stock_cols = [f"{name}_{col}" for col in stock.columns]
            cols.extend(stock_cols)
        df.columns = cols
    return df


def create_weight(num_stock, weight_type="equal"):
    """
    Create a list of weights for a portfolio with `num_stock` stocks

    Parameters
    ----------
    num_stock : int
        Number of stocks in the portfolio

    Returns
    -------
    list
        List of weights
    """
    if weight_type == "equal":
        return np.ones(num_stock) / num_stock

    else:
        raise ValueError("Weight type not supported")


def bigger_frequency(freq1, freq2):
    """
    Check if `freq1` is a bigger frequency than `freq2`

    Parameters
    ----------
    freq1 : str
        Frequency 1
    freq2 : str
        Frequency 2

    Returns
    -------
    bool
        True if `freq1` is bigger than `freq2`
    """

    freq_map = {
        "D": 1,
        "W": 2,
        "M": 3,
        "Q": 4,
        "Y": 5,
    }
    return freq_map[freq1] > freq_map[freq2]
