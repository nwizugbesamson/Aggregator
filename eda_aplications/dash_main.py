from dash import Dash, html
from eda_aplications.src.data.loader import load_data
from eda_aplications.src.general_components.general_layout import create_general_layout
from eda_aplications.src.personalised_components.personalised_layout import  create_personalised_layout


def dash_main() -> None:
    data = load_data()
    app = Dash()
    app.title = "Job Aggregator"
    app.layout = create_personalised_layout(app, data)
    app.run()