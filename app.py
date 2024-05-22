from dash import Input, Output
from layout import create_app
from walk import perform_quantum_walk, perform_random_walk

app = create_app()


@app.callback(
    Output("price-chart", "figure"),
    Input("n_qubits-filter", "value"),
    Input("n_steps-filter", "value"),
    Input("repetitions-filter", "value"),
    Input("type-filter", "value"),
    Input("coin-filter", "value"),
)
def update_charts(n_qubits, n_steps, repetitions, walk_type, coin):
    """
    Update the charts based on the selected parameters.
    """
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

    price_chart_figure = create_chart_figure(x_array, y_array, walk_type)

    return price_chart_figure


def create_chart_figure(x_array, y_array, walk_type):
    """
    Create the chart figure.
    """
    return {
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
                "text": "Result for a " + walk_type + " Walk",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True, "title": "Step"},
            "yaxis": {"fixedrange": True, "title": "Probability"},
            "colorway": ["#17B897"],
        },
    }


if __name__ == "__main__":
    app.run_server(debug=True)
