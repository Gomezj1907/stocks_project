import pandas as pd
import numpy as np


def calculate_returns(df):
    
    """
    Calculate the returns of a given dataframe of stock prices.
    
    Parameters
    ----------
    df : pandas.DataFrame
        A dataframe of stock prices.
    
    Returns
    -------
    pandas.DataFrame
        A dataframe of returns for each ticker.
    
    Notes
    -----
    The returns are calculated as the log of the change in price.
    The returns are then aggregated to the mean.
    """
    
    df = np.log(df / df.shift(1))
    
    #Return the aggregated returns in mean
    df = df.mean(axis=0)
    df = df.to_frame().T
    
    #Return the returns for each ticker
    
    return df


def select_top_n(df, n):
    """
    Select the top n tickers based on their percentage change
    over the given period.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the tickers and their
        percentage change.
    n : int
        The number of tickers to return.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the top n tickers and their
        percentage change.
    """
    #return the top n
    top = df.iloc[0].sort_values(ascending=False).head(n)
    return top.to_frame().T

def select_bottom_n(df, n):
    """
    Select the bottom n tickers based on their percentage change
    over the given period.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame with the closing prices of the tickers
    n : int
    """
    
    bottom = df.iloc[0].sort_values(ascending=True).head(n)
    return bottom.to_frame().T    


if __name__ == '__main__':
    #Generate an example DataFrame with 5 dates and 5 tickers
    df = pd.DataFrame(np.random.rand(5, 5), columns=['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB'], index=pd.date_range(start='2022-01-01', periods=5, freq='D'))
    
    df = calculate_returns(df)
    print(df)
    
    bottom_n = select_bottom_n(df, 3)
    print(bottom_n)
    
    top_n = select_top_n(df, 3)
    print(top_n)