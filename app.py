import pandas as pd
from dash import Dash, Input, Output, dcc, html

from walk import perform_quantum_walk

data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Quantum and Random Walk"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(children="Quantum Walk", className="header-title"),
                html.P(
                    children=("Unterschied zwischen Quantum und Random Walk"),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            ["Random", "Quantum"],
                            "Quantum",
                            id="type-filter",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Number of Qubits", className="menu-title"),
                        dcc.Slider(
                            3,
                            10,
                            1,
                            value=7,
                            id="n_qubits-filter",
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Number of Steps", className="menu-title"),
                        dcc.Slider(
                            1,
                            100,
                            1,
                            value=30,
                            id="n_steps-filter",
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Repetition", className="menu-title"),
                        dcc.Input(
                            5000,
                            id="repetitions-filter",
                            type="number",
                            min=1,
                            max=10000,
                            step=1,
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Input("n_qubits-filter", "value"),
    Input("n_steps-filter", "value"),
    Input("repetitions-filter", "value"),
    Input("type-filter", "value"),
)
def update_charts(n_qubits, n_steps, repetitions, walk_type):
    x_array, y_array = perform_quantum_walk(
        int(n_qubits), int(n_steps), int(repetitions), verbose=False
    )
    price_chart_figure = {
        "data": [
            {
                "x": x_array,
                "y": y_array,
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Result",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "title": "Step"},
            "yaxis": {"fixedrange": True, "title": "Amount"},
            "colorway": ["#17B897"],
        },
    }

    return price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
