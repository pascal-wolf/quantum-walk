from dash import Dash, dcc, html


def create_app():
    """
    Create and configure the Dash application.
    """
    external_stylesheets = [
        {
            "href": (
                "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
            ),
            "rel": "stylesheet",
        },
    ]
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = "Discret Quantum Walk"
    app.layout = create_layout()
    return app


def create_layout():
    """
    Create the layout for the Dash application.
    """
    return html.Div(
        children=[
            create_header(),
            create_menu(),
            create_menu_b(),
            create_wrapper(),
        ]
    )


def create_header():
    """
    Create the header for the Dash application.
    """
    return html.Div(
        children=[
            html.H3(children="Quantum Walk", className="header-title"),
            html.P(
                children=("Simulation of a Discret Quantum walk"),
                className="header-description",
            ),
        ],
        className="header",
    )


def create_menu():
    """
    Create the menu for the Dash application.
    """
    return html.Div(
        children=[
            create_dropdown("Type", ["Random", "Quantum"], "Quantum", "type-filter"),
            create_dropdown("Coin", ["0", "1", "Symmetric"], "1", "coin-filter"),
        ],
        className="menu",
    )


def create_menu_b():
    """
    Create the secondary menu for the Dash application.
    """
    return html.Div(
        children=[
            create_slider("Number of Qubits", 3, 10, 1, 7, "n_qubits-filter"),
            create_slider("Number of Steps", 1, 100, 1, 30, "n_steps-filter"),
            create_slider("Repetition", 5000, 10000, 500, 5000, "repetitions-filter"),
        ],
        className="menu-b",
    )


def create_wrapper():
    """
    Create the wrapper for the Dash application.
    """
    return html.Div(
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
    )


def create_dropdown(title, options, default, id):
    """
    Create a dropdown menu with the given parameters.

    Args:
        title (str): The title of the dropdown menu.
        options (list): The options for the dropdown menu.
        default (str): The default value of the dropdown menu.
        id (str): The id of the dropdown menu.

    Returns:
        dash_html_components.Div: A Div component containing the dropdown menu.
    """
    return html.Div(
        children=[
            html.Div(children=title, className="menu-title"),
            dcc.Dropdown(
                options,
                default,
                id=id,
                clearable=False,
                searchable=False,
                className="dropdown",
            ),
        ]
    )


def create_slider(title, min, max, step, default, id):
    """
    Create a slider with the given parameters.

    Args:
        title (str): The title of the slider.
        min (int): The minimum value of the slider.
        max (int): The maximum value of the slider.
        step (int): The step value of the slider.
        default (int): The default value of the slider.
        id (str): The id of the slider.

    Returns:
        dash_html_components.Div: A Div component containing the slider.
    """
    return html.Div(
        children=[
            html.Div(children=title, className="menu-title-b"),
            dcc.Slider(
                min,
                max,
                step,
                value=default,
                id=id,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ]
    )
