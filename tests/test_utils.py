import sys

sys.path.append("/media/hari31416/Hari_SSD/Users/harik/Desktop/pystock")

import os
import pytest
import pandas as pd
import datetime
from pystock.utils import *
import numpy as np

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
AAPL_DIR = os.path.join(CUR_DIR, "data", "AAPL.csv")
GOOGL_DIR = os.path.join(CUR_DIR, "data", "GOOGL.csv")

df = pd.read_csv(AAPL_DIR, parse_dates=["Date"], index_col="Date")
df.sort_index(inplace=True)
smallest_date = df.index[0]
largest_date = df.index[-1]
all_columns = df.columns


def test_convert_str_to_date_str_given():
    date = convert_str_to_date("2019-01-01")
    assert isinstance(date, datetime.date), "Date is not a datetime.date object"
    assert date.year == 2019, "Date year is not 2019"
    assert date.month == 1, "Date month is not 1"
    assert date.day == 1, "Date day is not 1"
    with pytest.raises(ValueError):
        convert_str_to_date("")


def test_convert_str_to_date_date_given():
    date = convert_str_to_date(datetime.date(2019, 1, 1))
    assert isinstance(date, datetime.date), "Date is not a datetime.date object"
    assert date.year == 2019, "Date year is not 2019"
    assert date.month == 1, "Date month is not 1"
    assert date.day == 1, "Date day is not 1"


def test_bigger_frequency_smaller():
    f1 = "D"
    f2 = "W"
    assert not bigger_frequency(f1, f2), "W is not bigger than D"


def test_bigger_frequency_bigger():
    f1 = "W"
    f2 = "D"
    assert bigger_frequency(f1, f2), "W is not bigger than D"


def test_bigger_frequency_equal():
    f1 = "W"
    f2 = "W"
    assert not bigger_frequency(f1, f2), "W is not equal to W"


def test_create_weights_equal():
    weights = create_weight(3, "equal")
    assert np.equal(
        weights, np.array([1 / 3, 1 / 3, 1 / 3])
    ).all(), "Weights are not equal"


def test_create_weights_other():
    with pytest.raises(ValueError):
        create_weight(3, "other")


def test_load_data_start_date_error():
    directory = AAPL_DIR
    start_date = "1970-01-01"

    with pytest.raises(ValueError):
        load_data(directory, start_date=start_date)


def test_load_data_end_date_error():
    directory = AAPL_DIR
    end_date = "2070-01-01"

    with pytest.raises(ValueError):
        load_data(directory, end_date=end_date)


def test_load_data_dates_none():
    directory = AAPL_DIR
    start_date = None
    end_date = None

    df = load_data(directory, start_date=start_date, end_date=end_date)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert df.index[0] == smallest_date, "Data start date is not smallest date"
    assert df.index[-1] == largest_date, "Data end date is not largest date"


def test_load_data_dates():
    directory = AAPL_DIR
    start_date = "2018-01-02"
    end_date = "2018-12-31"

    df = load_data(directory, start_date=start_date, end_date=end_date)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert (
        df.index[0].strftime("%Y-%m-%d") == start_date
    ), "Data start date is not start date"
    assert (
        df.index[-1].strftime("%Y-%m-%d") == end_date
    ), "Data end date is not end date"


def test_load_data_columns_none():
    directory = AAPL_DIR
    columns = None

    df = load_data(directory, columns=columns)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert df.columns.all() == all_columns.all(), "Data columns are not all columns"


def test_load_data_rename_columns():
    directory = AAPL_DIR
    columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    rename_columns = ["open", "high", "low", "close", "adj_close", "volume"]

    df = load_data(directory, columns=columns, rename_cols=rename_columns)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert list(df.columns) == rename_columns, "Data columns are not all columns"


def test_load_data_frequency():
    directory = AAPL_DIR
    frequency = "W"

    df = load_data(directory, frequency=frequency)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert df.index.freq == frequency, "Data frequency is not W"


def test_load_data_few_columns_without_rename():
    directory = AAPL_DIR
    columns = ["Open", "High"]

    df = load_data(directory, columns=columns)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert list(df.columns) == columns, "Data columns are not all columns"


def test_load_data_few_columns_with_rename():
    directory = AAPL_DIR
    columns = ["Open", "High"]
    rename_columns = ["open", "high"]

    df = load_data(directory, columns=columns, rename_cols=rename_columns)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert list(df.columns) == rename_columns, "Data columns are not all columns"


def test_merge_dfs_columns():
    df1 = pd.read_csv(AAPL_DIR, index_col=0, parse_dates=True)
    df2 = pd.read_csv(GOOGL_DIR, index_col=0, parse_dates=True)

    df = merge_dfs([df1, df2], join="inner")
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert len(df.columns) == len(df1.columns) + len(
        df2.columns
    ), "Data columns are not all columns"


def test_merge_dfs_rows():
    df1 = pd.read_csv(AAPL_DIR, index_col=0, parse_dates=True)
    df2 = pd.read_csv(GOOGL_DIR, index_col=0, parse_dates=True)

    df = merge_dfs([df1, df2], join="inner")
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert len(df) == min(len(df1), len(df2)), "Data rows are correct"


def test_merge_dfs_rows_outer():
    df1 = pd.read_csv(AAPL_DIR, index_col=0, parse_dates=True)
    df2 = pd.read_csv(GOOGL_DIR, index_col=0, parse_dates=True)

    df = merge_dfs([df1, df2], join="outer")
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert len(df) == max(len(df1), len(df2)), "Data rows are not correct"


def test_merge_dfs_column_names_with_df_names():
    df1 = pd.read_csv(AAPL_DIR, index_col=0, parse_dates=True)
    df2 = pd.read_csv(GOOGL_DIR, index_col=0, parse_dates=True)

    df = merge_dfs([df1, df2], join="inner", df_names=["AAPL", "GOOGL"])
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert list(df.columns) == [
        "AAPL_Open",
        "AAPL_High",
        "AAPL_Low",
        "AAPL_Close",
        "AAPL_Adj Close",
        "AAPL_Volume",
        "GOOGL_Open",
        "GOOGL_High",
        "GOOGL_Low",
        "GOOGL_Close",
        "GOOGL_Volume",
    ], "Data columns are not correct"


def test_merge_dfs_columns_names_without_df_names():
    df1 = pd.read_csv(AAPL_DIR, index_col=0, parse_dates=True)
    df2 = pd.read_csv(GOOGL_DIR, index_col=0, parse_dates=True)

    df = merge_dfs([df1, df2], join="inner")
    print(df.columns)
    assert isinstance(df, pd.DataFrame), "Data is not a DataFrame"
    assert list(df.columns) == [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ], "Data columns are not correct"
