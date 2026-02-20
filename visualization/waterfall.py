import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def plot_waterfall(
    start_value,
    step_labels,
    step_values,
    final_label="Total",
    start_label="Start",
    colors=None,
    step_colors=None,
    figsize=(10, 6),
    value_format="{:,.0f}",
    y_formatter=None
):
    """
    Fully generic waterfall chart.

    Parameters
    ----------
    start_value : float
    step_labels : list[str]
    step_values : list[float]
    final_label : str
    start_label : str

    colors : dict (optional)
        {
            "positive": "green",
            "negative": "red",
            "total": "grey"
        }

    step_colors : list[str] (optional)
        Explicit color per step (overrides positive/negative logic)

    """

    if len(step_labels) != len(step_values):
        raise ValueError("step_labels and step_values must have same length")

    if step_colors and len(step_colors) != len(step_values):
        raise ValueError("step_colors must match number of steps")

    if colors is None:
        colors = {
            "positive": "#2ca02c",
            "negative": "#d62728",
            "total": "#7f7f7f"
        }

    # --- cumulative ---
    cumulative = [start_value]
    for v in step_values:
        cumulative.append(cumulative[-1] + v)

    final_value = cumulative[-1]

    fig, ax = plt.subplots(figsize=figsize)

    # --- Start bar ---
    ax.bar(start_label, start_value, color=colors["total"])
    ax.text(0, start_value/2, value_format.format(start_value),
            ha="center", va="center", color="white", fontweight="bold")

    # --- Steps ---
    for i, (label, value) in enumerate(zip(step_labels, step_values)):
        bottom = cumulative[i]

        # priority: explicit step_colors > auto positive/negative
        if step_colors:
            color = step_colors[i]
        else:
            color = colors["positive"] if value >= 0 else colors["negative"]

        ax.bar(label, value, bottom=bottom, color=color)

        ax.text(
            i+1,
            bottom + value/2,
            value_format.format(value),
            ha="center",
            va="center",
            color="white",
            fontweight="bold"
        )

    # --- Final total ---
    ax.bar(final_label, final_value, color=colors["total"])
    ax.text(len(step_values)+1, final_value/2,
            value_format.format(final_value),
            ha="center", va="center",
            color="white", fontweight="bold")

    if y_formatter:
        ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))

    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    return fig, ax