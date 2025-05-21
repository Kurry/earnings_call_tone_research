import alphalens as al
import pandas as pd

from .load import prices


def make_tearsheet(factor: pd.Series, out="outputs/tearsheet.html"):
    fd = al.utils.get_clean_factor_and_forward_returns(
        factor, prices(), periods=[5, 10], quantiles=5
    )
    al.tears.create_full_tear_sheet(fd, long_short=True, output_filename=out)
