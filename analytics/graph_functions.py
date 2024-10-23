
# eventually decide if it's better to render this as a simple seaborn jpeg, or as an interactive plotly graph

import plotly.express as px

import plotly.offline as pyo

def graph_results(result_array):
    """Generate an interactive graph of the result array."""
    fig = px.line(y=result_array, labels={
            "x": "Bets made (in chronological order)",  # For example, if you're plotting against time
            "y": "Result (in $)"      # If the y-axis represents some measurement
        })
    
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')
    return graph_html
