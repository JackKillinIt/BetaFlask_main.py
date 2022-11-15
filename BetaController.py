import LabData
import pandas
import numpy as np


def get_returns_for_a_stock(stock_price_list):
    """
    first, we create a data frame from the stock price list that was sent in. This list is a list of the raw data from the LabData/data probider
    Then from the data frame we select just the adjClose "columns" (adjClose is the key for the values we want). This returns a pandas array and we call pct_change() ont that which gives a new list
    Third that new list probably has some null and bad values on it, so we call dropna() which returns us a clean list that represents the percent change between the adjPrice in the data list
    :param stock_price_list:
    :return: a cleaned list of returns or pct_change from adjPrice
    """
    print("In Beta Controller's get_returns_for_a_stock Debug: Going to create a chart with the following values",
          "stock_price_list lengths: ",
          len(stock_price_list), sep='\n')

    ###
    #  This is here so the code compiles)
    clean_percent_list = []
    ###

    #######
    # Uncomment and complete the below:
    df = pandas.DataFrame(stock_price_list)
    percent_change_list = df['adjClose'].pct_change()
    clean_percent_list = percent_change_list.dropna()
    #####

    return clean_percent_list


def calculate_beta(stock, market):
    """
    stock is a list of cleaned prices/returns for a stock
    market is a clean list of returns for the market
    first we calculate the covariance is the cov function of the stock and the market. This numpy function returns a matrics of values.
    covariance[0, 1] is the covariance. covariance[1, 1] is the variance
    beta is calculated as  covariance[0, 1] / covariance[1, 1]

    :param stock:  a list of cleaned prices/returns for a stock
    :param market: a clean list of returns for the market
    :return: the beta for the stock and the market
    """
    ###
    # This is here so the code compiles)
    beta = 1
    #######
    # Uncomment and complete the below:
    covariance = np.cov(stock, market)
    # once the above is complete uncomment the below
    beta = covariance[0, 1] / covariance[1, 1]
    print("Debug: Going to use covariance: {} to calculate Beta: {} ".format(covariance, beta))
    return beta


def get_beta_by_chunks(stock_returns, market_returns, number_of_chunks):
    """
    Since we want to "chunk" or create separate groups of calculations, this function takes cleaned and calculated returns beta values for each chunk split number_of_chunks ways
    when number of chunks = 1 that's the same as saying the overall beta of the stack.

    first we split the stock_returns number of chunk ways, this split gives us a new chunked_stock list.
    second we split the market_returns number of chunk ways, this split gives us a new chunked_stock list.
    then we loop through the chunked stocks list (now number_of_chunks long)
        and calculate the beta for the chunked stocks and chunked markets (from 1 and 2 described above)
        for each beta we append it to a list before the loop ends
    end the end we return our list of betas
    :param stock_returns:
    :param market_returns:
    :param number_of_chunks:
    :return: a list of calculated betas
    """
    print("In Beta Controller's get_beta_by_chunks Debug: Going to create a chart with the following values",
          "stock_returns lengths: ", len(stock_returns), "market_returns length", len(market_returns), sep='\n')

    ###
    # This is here so the code compiles)
    chunked_stocks = []
    chunked_markets = []
    ###

    betas = []
    #######
    # Uncomment and complete the below:
    chunked_stocks = np.array_split(stock_returns, number_of_chunks)
    chunked_markets = np.array_split(market_returns, number_of_chunks)
    for x in range(len(chunked_stocks)):
        beta = calculate_beta(chunked_stocks[x], chunked_markets[x])
        betas.append(beta)
    return betas


def do_calculations(stockName, chunks):
    """
    This is the "master" caller. it takes in a stocks name and the number of chunks we will split it down into
    we fetch the raw data for the stock from the data source
    we fetch the raw data for the market from the data source
    we calculate the returns for the market
    we calculate the returns for the stock
    using those calculated returns, we calculate the base beta bt calling get data by chunks with the return list for stock and the return list for market and give a chunk of 1. we store that for return.

    using those calculated returns, we calculate the base beta bt calling get data by chunks with the return list for stock and the return list for market and give a chunk of _chunks_ which is passed in.

    we make sure that the base_beta list is the same length as the chunked beta list by using a for loop to append to base base_betas[0]

    we return the base_betas and the chunked_betas lists
    

    :param stockName:
    :param chunks:
    :return:
    """
    ###
    # This is here so the code compiles)
    base_betas = [1, 1, 1, 1]
    chunked_betas = [1, 1, 1, 1]
    ####

    market_returns = get_returns_for_a_stock(LabData.HISTORICAL_MARKET_PRICES)
    stock_returns = get_returns_for_a_stock(LabData.GetOneStock(stockName))

    #######
    # Uncomment and complete the below:
    base_betas = get_beta_by_chunks(stock_returns, market_returns, 1)
    print("base_betas: ", base_betas)
    chunked_betas = get_beta_by_chunks(stock_returns, market_returns, chunks)
    return base_betas, chunked_betas


if __name__ == '__main__':
    base_betas, chunked_betas = do_calculations("AAPL", 10)
    print(base_betas, chunked_betas)
