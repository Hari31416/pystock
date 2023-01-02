from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import zipfile
import os

FREQUENCY = {
    "D": "Daily",
    "W": "Weekly",
    "M": "Monthly",
    "Q": "Quarterly",
    "Y": "Yearly",
}

FREQUENCY_REVERSE = {
    "Daily": "D",
    "Weekly": "W",
    "Monthly": "M",
    "Quarterly": "Q",
    "Yearly": "Y",
}


class FamaFrenchFactors:
    def __init__(self):
        self.loaded = False
        self.url = (
            "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"
        )
        self.url_second = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/"

    def __load_soup(self):
        """
        Create a BeautifulSoup object from the url.
        """
        r = requests.get(self.url)
        return BeautifulSoup(r.content, "html.parser")

    def __find_links(self):
        """
        Finds all the urls in the first paragraph of the page.
        """
        soup = self.__load_soup()
        para = soup.find("p", style="width: 737px;")
        links = para.find_all("a")
        links = pd.Series(links)
        return links

    def __find_zip_links_func(self, x, frequency="D", factors=3, format="csv"):
        """
        Finds the zip file link for the given frequency and factors.

        Parameters
        ----------
        x : str
            The url to be checked.
        frequency : str, optional
            The frequency of the data. The default is "D".
        factors : int, optional
            The number of factors. The default is 3. Possible values are 3 and 5
        format : str, optional
            The format of the data. The default is "csv".

        Returns
        -------
        bool
            True if the link is the correct link. False otherwise.
        """
        try:
            x = x["href"]
        except:
            return False
        is_fff = False
        found_factors = False
        found_frequency = False
        found_format = False
        if frequency == "M":
            frequency = ""
        else:
            try:
                frequency = FREQUENCY[frequency.capitalize()].lower()
            except:
                raise ValueError(
                    "frequency can only be D, W, M, Q or Y. D for Daily, W for Weekly, M for Monthly, Q for Quarterly and Y for Yearly."
                )

        if factors == 3:
            factors = "data_factor"
        elif factors == 5:
            factors = "data_5_factor"
        else:
            raise ValueError("factors can only be 3 or 5.")

        x = x.lower()
        x = x.replace("2x3", "")
        if "research_data" in x:
            is_fff = True
        if frequency in x:
            found_frequency = True
        if factors in x:
            found_factors = True
        if format in x:
            found_format = True
        if is_fff and found_factors and found_frequency and found_format:
            return True
        else:
            return False

    def __create_zip_link(self, urls, frequency="D", factors=3, format="csv"):
        """
        Filters the urls to find the correct zip file link.

        Parameters
        ----------
        urls : list
            list of bs4 tags
        frequency : str, optional
            The frequency of the data. The default is "D".
        factors : int, optional
            The number of factors. The default is 3. Possible values are 3 and 5
        format : str, optional
            The format of the data. The default is "csv".

        Returns
        -------
        str
            The link to the zip file.
        """
        filter_links = urls[
            urls.apply(
                lambda x: self.__find_zip_links_func(
                    x, frequency=frequency, factors=factors, format=format
                )
            )
        ]
        if len(filter_links) == 0:
            return None
        else:
            link = filter_links.iloc[0]["href"]

        return self.url_second + link

    def download(self, frequency="D", factors=3, directory=".", overwrite=False):
        """
        download the Fama French Factors data.

        Parameters
        ----------
        frequency : str, optional
            The frequency of the data. The default is "D".
        factors : int, optional
            The number of factors. The default is 3. Possible values are 3 and 5
        directory : str, optional
            The directory to save the file. The default is ".".
        overwrite : bool, optional
            Whether to overwrite the file if it already exists. The default is False.

        Returns
        -------
        str
            The name of the file.
        """
        format = "csv"
        try:
            f = FREQUENCY[frequency.capitalize()]
        except:
            raise ValueError(
                "frequency can only be D, W, M, Q or Y. D for Daily, W for Weekly, M for Monthly, Q for Quarterly and Y for Yearly."
            )
        file_name = f"fff_{f.lower()}_{factors}_factors.{format}"
        if directory != ".":
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_name = os.path.join(directory, file_name)
        if os.path.exists(file_name) and not overwrite:
            print(
                "File already exists. Use load() to load the file. Or set overwrite=True to overwrite the file."
            )
            return None

        print("Downloading Fama French Factors. This may take about 10 seconds.")
        urls = self.__find_links()
        zip_link = self.__create_zip_link(
            urls, frequency=frequency, factors=factors, format=format
        )
        if zip_link is None:
            print("No file found. Please check your input.")
            return None
        r = requests.get(zip_link)
        with open(".fff.zip", "wb") as f:
            f.write(r.content)
            with zipfile.ZipFile(".fff.zip", "r") as zip_ref:
                zip_ref.extractall()
                old_name = zip_ref.namelist()[0]
                os.rename(old_name, file_name)
            os.remove(".fff.zip")
        print("Download complete. File saved as " + file_name)
        print("Use load() to load the file as a pandas dataframe.")
        return file_name

    def __load(self, directory=".", frequency="M", factors=3):
        """
        Loads the Fama French Factors data if it exists.

        Parameters
        ----------
        directory : str, optional
            The directory to save the file. The default is ".".
        frequency : str, optional
            The frequency of the data. The default is "M".
        factors : int, optional
            The number of factors. The default is 3. Possible values are 3 and 5

        Returns
        -------
        pandas.DataFrame
            The Fama French Factors data.
        """
        format = "csv"
        try:
            frequency = FREQUENCY[frequency.capitalize()].lower()
        except:
            raise ValueError(
                "frequency can only be D, W, M, Q or Y. D for Daily, W for Weekly, M for Monthly, Q for Quarterly and Y for Yearly."
            )
        file_name = f"fff_{frequency}_{factors}_factors.{format}"
        if directory == ".":
            file_name = f"fff_{frequency}_{factors}_factors.{format}"
        else:
            file_name = os.path.join(directory, file_name)
        if os.path.exists(file_name):
            return pd.read_csv(file_name, skiprows=3, index_col=0).dropna()
        else:
            raise FileNotFoundError(
                "File not found. Use download() to download the file."
            )

    def __preprocess(self, df, frequency="M"):
        """
        Preprocesses the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The Fama French Factors data.
        frequency : str, optional
            The frequency of the data. The default is "M".

        Returns
        -------
        pandas.DataFrame
            The preprocessed Fama French Factors data.
        """
        df.index = df.index.astype(str)
        if frequency.lower() == "m":
            length = 6
            df = df[df.index.str.strip().str.len() == length]
            df.index = pd.to_datetime(df.index, format="%Y%m") + MonthEnd(0)
        else:
            length = 8
            df = df[df.index.str.strip().str.len() == length]
            df.index = pd.to_datetime(df.index, format="%Y%m%d")

        for col in df.columns:
            df[col] = pd.to_numeric(df[col]) * 0.01
        frequency = FREQUENCY[frequency.capitalize()].lower()
        if frequency == "daily":
            return df
        try:
            as_freq = FREQUENCY_REVERSE[frequency.title()]
        except KeyError:
            print(
                "Invalid frequency. Please use one of the following: daily(D), weekly(W), monthly(M), quarterly, yearly(Y)."
            )
            raise KeyError
        df_new = df.asfreq(as_freq, method="ffill")
        return df_new

    def load(
        self,
        directory=".",
        frequency="M",
        factors=3,
        preprocess=True,
    ):
        """
        Loads the Fama French Factors data.

        Parameters
        ----------
        directory : str, optional
            The directory to save the file. The default is ".".
        frequency : str, optional
            The frequency of the data. The default is "M".
        factors : int, optional
            The number of factors. The default is 3. Possible values are 3 and 5
        preprocess : bool, optional
            Whether to preprocess the data. The default is True.

        Returns
        -------
        pandas.DataFrame
            The Fama French Factors data.
        """
        if preprocess:
            df = self.__load(
                directory=directory,
                frequency=frequency,
                factors=factors,
            )
            df = self.__preprocess(df, frequency=frequency)
        else:
            df = self.__load(
                directory=directory,
                frequency=frequency,
                factors=factors,
            )
        self.loaded = True
        self.frequency = frequency
        self.data = df
        return df

    def change_frequency(self, frequency="M"):
        """
        Changes the frequency of the data.

        Parameters
        ----------
        frequency : str, optional
            The frequency of the data. The default is "M".

        Returns
        -------
        pandas.DataFrame
            The Fama French Factors data.
        """
        if not self.loaded:
            print("Please load the data first.")
            return None
        df = self.data.asfreq(frequency, method="ffill")
        self.frequency = frequency
        self.data = df
        return df

    def calculate_mean_values(self):
        """
        Returns the mean values of the factors.

        Returns
        -------
        pandas.DataFrame
            The mean values of the factors.
        """
        if not self.loaded:
            print("Please load the data first.")
            return None
        means = self.data.mean()
        A = [1]
        A.extend(means)
        A = pd.Series(A, index=["const"] + list(means.index))
        return A
