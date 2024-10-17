
# eventually decide if it's better to render this as a simple seaborn jpeg, or as an interactive plotly graph

import plotly.express as px

def graph_results(result_array):
    """Generate an interactive graph of the result array."""
    fig = px.line(result_array)
    fig.show()
