from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dashboard.eda_applications.src.data.loader import load_data, optimize_dtype
from dashboard.eda_applications.src.general_components.general_layout import create_general_layout
from dashboard.eda_applications.src.personalised_components.personalised_layout import  create_personalised_layout



data = list(load_data())
app = DjangoDash(name='general_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP]) 
app.title = "Job Aggregator GENERAL"
app.layout = create_general_layout(app, data)


personalised_app = DjangoDash(name='personalised_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])
personalised_app.title = "Job Aggregator Personalised"
personalised_app.layout = create_personalised_layout(personalised_app, data)
