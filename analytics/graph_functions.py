# eventually decide if it's better to render this as a simple seaborn jpeg, or as an interactive plotly graph

import plotly.express as px

import plotly.offline as pyo


def graph_results(result_array):
    """Generate an interactive graph of the result array."""
    fig = px.line(
        y=result_array,
        labels={
            "x": "Bets made (in chronological order)",  # For example, if you're plotting against time
            "y": "Results (in $$$)",  # If the y-axis represents some measurement
        },
    )

    fig.add_shape(  # add a horizontal "target" line
        type="line",
        line_color="black",
        line_width=3,
        opacity=0.25,
        x0=0,
        x1=len(result_array),
        xref="x",
        y0=0,
        y1=0,
        yref="y",
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=1)  # Set the distance between ticks to 1
    )

    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type="div")
    return graph_html
