import pandas as pd
from plotly import graph_objects as go

from aecg.maps import LEADS


def plot_seq_set(
    df: pd.DataFrame,
    time_mode="relative",
    plot_mode="multiple",
    title="ECG sequence set",
) -> go.Figure:
    """
    Plot ECG dataframe.
    """
    if time_mode == "absolute":
        ts_col = "ABSOLUTE_TS"
        x_title = "Time"
        hover_template = "<b>%{y}</b> mV at <b>%{x}</b>"
    elif time_mode == "relative":
        ts_col = "RELATIVE_TS"
        x_title = "Time (ms)"
        hover_template = "<b>%{y}</b> mV at <b>%{x}</b> ms"
    else:
        raise ValueError(f"time_mode should be absolute or relative (not {time_mode})")

    leads = df.columns[2:]
    leads_names = list(map(lambda x: LEADS.get(x, x), leads))

    if plot_mode == "one":
        nrows = 1
    elif plot_mode == "multiple":
        nrows = len(leads)
    else:
        raise ValueError(f"plot_mode should be one or multiple (not {plot_mode})")

    layout = dict(
        hoversubplots="axis",
        title="Stock Price Changes",
        hovermode="x",
        grid=dict(rows=nrows, columns=1),
        xaxis_title=x_title,
        yaxis_title="Voltage (mV)",
        legend_title="Leads",
    )

    data = []
    y_axis_layout = dict()
    range_v = [df[leads].min().min(), df[leads].max().max()]

    for i, (lead, lead_name) in enumerate(zip(leads, leads_names), 1):
        if plot_mode == "one":
            yaxis = "y"
            color = None
        elif plot_mode == "multiple":
            yaxis = f"y{i}"
            color = "firebrick"
            y_axis_layout[f"yaxis{i}"] = dict(
                title=f"{lead_name} (mV)",
                range=range_v,
                showgrid=True,
                gridwidth=1,
                dtick=0.3,
            )

        fig_part = go.Scatter(
            x=df[ts_col],
            y=df[lead],
            xaxis="x",
            yaxis=yaxis,
            line=dict(color=color, width=1.1),
            name=lead_name,
            hovertemplate=hover_template,
            text=[lead_name],
            textposition="top left",
        )

        data.append(fig_part)

    fig = go.Figure(data=data, layout=layout)

    height = 500 if plot_mode == "one" else 250 * len(leads)

    fig.update_layout(
        height=height,
        title_text=title,
        template="ggplot2",
        **y_axis_layout,
    )

    return fig
