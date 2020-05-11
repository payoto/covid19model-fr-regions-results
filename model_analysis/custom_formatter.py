import numpy as np
from matplotlib.dates import num2date, DateFormatter, date2num, ConciseDateFormatter

import pandas as pd


class PandasToMpl_ConciseDateFormatter(ConciseDateFormatter):
    """ Formatter which goes from pandas d-units date times to matplotlibs
    Concise Date Formatter.
    """
    def __init__(self, *args, pd_date_unit="D", **kwargs):
        self.pd_date_unit = pd_date_unit
        super().__init__(*args, **kwargs)

    def format_ticks(self, values):
        values = pd.to_datetime(values, unit=self.pd_date_unit)
        values = date2num(values)
        return super().format_ticks(values)
