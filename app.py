import pandas as pd
from dash import Dash, Input, Output, dcc, html

from walk import perform_quantum_walk, perform_random_walk

# data = (
#     pd.read_csv("avocado.csv")
#     .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
#     .sort_values(by="Date")
# )
#
# regions = data["region"].sort_values().unique()
# avocado_types = data["type"].sort_values().unique()
#
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Discret Quantum Walk"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(children="Quantum Walk", className="header-title"),
                html.P(
                    children=("Simulation of a Discret Quantum walk"),
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
                        html.Div(children="Coin", className="menu-title"),
                        dcc.Dropdown(
                            ["0", "1", "Symmetric"],
                            "1",
                            id="coin-filter",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Number of Qubits", className="menu-title-b"),
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
                        html.Div(children="Number of Steps", className="menu-title-b"),
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
                        html.Div(children="Repetition", className="menu-title-b"),
                        dcc.Slider(
                            5000,
                            10000,
                            500,
                            value=5000,
                            id="repetitions-filter",
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ]
                ),
            ],
            className="menu-b",
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
    Input("coin-filter", "value"),
)
def update_charts(n_qubits, n_steps, repetitions, walk_type, coin):
    if walk_type.lower() == "quantum":
        symmetric = False
        if coin == "0":
            coin_set = False
        else:
            coin_set = True

            if coin.lower() == "symmetric":
                symmetric = True
        x_array, y_array = perform_quantum_walk(
            int(n_qubits),
            int(n_steps),
            int(repetitions),
            coin_set=coin_set,
            symmetric=symmetric,
            verbose=False,
        )
    elif walk_type.lower() == "random":
        x_array, y_array = perform_random_walk(repetitions, n_steps)
    else:
        x_array, y_array = [], []
        walk_type = ""
        print("No walk type selected. Setting arrays to zero!")

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
                "text": "Result for " + walk_type,
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
