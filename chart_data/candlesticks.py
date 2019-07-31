import pandas as pd
from utils import convert_period_into_pandas_freq

def parse_candles(content):
    """parses candles from json to pandas DataFrame

    Args:
        content (string): candles in json format
    """
    df = pd.read_json(content, orient='records')
    df = df.reindex(columns=['date', 'open', 'high', 'low', 'close'])
    df.set_index('date', inplace=True)
    return df



def resample_candles(df, period):
    """aggregates candles according to a (new) given period of time in order to
    obtain candles in a different period.

    Args:
        df (pd.DataFrame): source data frame with data about candles
        period (string): period that was used in the request
    """
    new_period = convert_period_into_pandas_freq(period)
    resampled = df.resample(new_period).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
    resampled.reset_index(inplace=True)
    return resampled