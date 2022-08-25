from django_plotly_dash import DjangoDash
from eda_aplications.src.data.loader import load_data
from web_service.dashboard.eda_applications.src.general_components.general_layout import create_general_layout
from web_service.dashboard.eda_applications.src.personalised_components.personalised_layout import  create_personalised_layout



data = load_data()
app = DjangoDash(name='general_dashboard') #, use_pages=True
app.title = "Job Aggregator GENERAL"
app.layout = create_general_layout(app, data)


personalised_app = DjangoDash(name='personalised_dashboard')
personalised_app.title = "Job Aggregator GENERAL"
personalised_app.layout = create_personalised_layout(app, data)
