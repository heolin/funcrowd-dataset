from typing import Text

import pandas as pd
from pytimeparse.timeparse import timeparse
from scipy.stats import mstats


def load_dataset(dataset_path: Text) -> pd.DataFrame:
    df = pd.read_csv(dataset_path)
    df['annotation__time'] = df['annotation__time'].apply(timeparse)
    df['annotation__time'] = mstats.winsorize(df['annotation__time'], limits=[0.05, 0.05])
    return df


def format_number(number, escape_percent=True):
    def _format(n):
        return "+{0:.2%}".format(n) if number > 0 else "{0:.2%}".format(n)
    number = _format(number)
    if escape_percent:
        number = number.replace("%", r"\%")
    return number
