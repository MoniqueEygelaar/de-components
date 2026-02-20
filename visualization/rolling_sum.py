import os
from typing import List, Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def rolling_sum_plot(
    df: pd.DataFrame,
    date_col: str,
    value_cols: List[str],
    window: str = "90D",
    min_periods: int = 1,
    figsize: tuple = (12, 6),
    output_dir: Optional[str] = None,
    filename_prefix: Optional[str] = None,
    add_year_separators: bool = True,
    thousands_formatter: bool = False,
):
    """
    Generate rolling sum plots for specified value columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    date_col : str
        Column containing datetime values
    value_cols : List[str]
        Columns to compute rolling sums for
    window : str, default="90D"
        Rolling window (time-based, e.g. '30D', '90D', '180D')
    min_periods : int, default=1
        Minimum periods for rolling calculation
    figsize : tuple
        Size of the plot
    output_dir : str, optional
        Directory to save plots
    filename_prefix : str, optional
        Prefix for saved filenames
    add_year_separators : bool, default=True
        Whether to draw vertical lines at start of each year
    thousands_formatter : bool, default=False
        Format y-axis in thousands (e.g. 12000 -> 12k)
    """

    if date_col not in df.columns:
        raise ValueError(f"{date_col} not found in DataFrame")

    missing_cols = [col for col in value_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns not found: {missing_cols}")

    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    data = data.sort_values(date_col).set_index(date_col)

    # Compute rolling sums
    for col in value_cols:
        data[f"{col}_rolling"] = (
            data[col]
            .rolling(window, min_periods=min_periods)
            .sum()
        )

    # Year separator logic
    if add_year_separators:
        year_starts = (
            data.index.to_series()
            .groupby(data.index.year)
            .min()
        )
    else:
        year_starts = None

    # Create plots
    for i, col in enumerate(value_cols, start=1):

        plt.figure(figsize=figsize)
        plt.plot(
            data.index,
            data[f"{col}_rolling"],
            linewidth=2
        )

        if year_starts is not None:
            for date in year_starts:
                plt.axvline(date, linestyle="--", alpha=0.5)

        if thousands_formatter:
            plt.gca().yaxis.set_major_formatter(
                FuncFormatter(lambda x, _: f"{int(x/1000)}k")
            )

        plt.xlabel("Date")
        plt.ylabel(f"{window} Rolling Sum of {col}")
        plt.title(f"{window} Rolling Sum of {col}")
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            prefix = filename_prefix or "rolling"
            filepath = os.path.join(
                output_dir,
                f"{prefix}_{col}.png"
            )
            plt.savefig(filepath)

        plt.show()
        plt.close()
