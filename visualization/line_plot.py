import matplotlib.pyplot as plt
import pandas as pd


def create_line_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str | None = None,
    sort_x: bool = True,
    figsize: tuple = (10, 5),
    marker: str | None = None,
):
    """
    Create a reusable, generic line plot from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    x_col : str
        Column for x-axis
    y_col : str
        Column for y-axis
    title : str, optional
        Plot title
    sort_x : bool, default=True
        Whether to sort by x column before plotting
    figsize : tuple, default=(10, 5)
        Figure size
    marker : str, optional
        Marker style (e.g. 'o')
    """

    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError("Specified columns not found in DataFrame")

    data = df[[x_col, y_col]].dropna()

    if sort_x:
        data = data.sort_values(by=x_col)

    plt.figure(figsize=figsize)
    plt.plot(data[x_col], data[y_col], marker=marker)
    plt.title(title or f"{y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.show()
