from dash import html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import pandas as pd

#/mnt/c/Users/SAMSON/DataAnalysis/projects/Aggregator/eda_aplications/src/personalised_components/country_dropdown_personal.py
from web_service.dashboard.eda_applications.src.personalised_components import(
    country_dropdown_personal,
    job_fields_dropdown_personal,
    locations_personalised,
    companies,
    rating_personalised,
    salary_personalised,
    description_personalised 
)


def create_personalised_layout(app: DjangoDash, data: pd.DataFrame) ->  html.Div:
    return html.Div(
        className='',   # class name to add styling
        children=[
            html.Div(
                className= '',   #for styling
                children=[
                        country_dropdown_personal.render(data),
                        job_fields_dropdown_personal.render(data)
                        
                ]
            ),
            dbc.Row([
                    dbc.Col(
                    locations_personalised.render(app, data),
                    width=12, lg={'size':6}
                            ),
                    dbc.Col(
                    companies.render(app, data),
                    width=12, lg={'size':6}
                            ),
                    ]),
            dbc.Row([
                    dbc.Col(
                    rating_personalised.render(app, data),
                    width=12, lg={'size':6}
                            ),
                    dbc.Col(
                    salary_personalised.render(app, data),
                    width=12, lg={'size':6}
                            )
                    ]),


            dbc.Row(
                    dbc.Col(
                            description_personalised.render(app, data),
                            width=12
                    )
                    )
        ],
    )