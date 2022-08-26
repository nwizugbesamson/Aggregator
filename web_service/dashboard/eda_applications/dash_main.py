from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from web_service.dashboard.eda_applications.src.data.loader import load_data
from web_service.dashboard.eda_applications.src.general_components.general_layout import create_general_layout
from web_service.dashboard.eda_applications.src.personalised_components.personalised_layout import  create_personalised_layout



data = load_data()
app = DjangoDash(name='general_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP]) 
# , meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0,maximum-scale=1.2, minimum-scale=0.5,'}]
app.title = "Job Aggregator GENERAL"
app.layout = create_general_layout(app, data)


personalised_app = DjangoDash(name='personalised_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])
personalised_app.title = "Job Aggregator GENERAL"
personalised_app.layout = create_personalised_layout(personalised_app, data)
