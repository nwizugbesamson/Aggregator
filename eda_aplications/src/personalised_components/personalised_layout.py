from dash import Dash, html
import pandas as pd

#/mnt/c/Users/SAMSON/DataAnalysis/projects/Aggregator/eda_aplications/src/personalised_components/country_dropdown_personal.py
from eda_aplications.src.personalised_components import(
    country_dropdown_personal,
    job_fields_dropdown_personal,
    locations_personalised,
    companies,
    rating_personalised,
    salary_personalised,
    description_personalised 
)


def create_personalised_layout(app: Dash, data: pd.DataFrame) ->  html.Div:
    return html.Div(
        className='',   # class name to add styling
        children=[
            html.H1('Insights'),    #change this heading
            html.Div(
                className= '',   #for styling
                children=[
                        country_dropdown_personal.render(data),
                        job_fields_dropdown_personal.render(data)
                        
                ]
            ),
            locations_personalised.render(app, data),
            html.Hr(),
            html.Br(),
            companies.render(app, data),
            html.Hr(),
            html.Br(),
            rating_personalised.render(app, data),
            html.Hr(),
            html.Br(),
            salary_personalised.render(app, data),
            html.Hr(),
            html.Br(),
            description_personalised.render(app, data)
        ],
    )