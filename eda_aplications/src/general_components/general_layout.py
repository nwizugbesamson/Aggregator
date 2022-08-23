from dash import Dash, html
import pandas as pd
from eda_aplications.src.general_components import (
    country_dropdown, 
    job_field_dropdown, 
    general_job_count, 
    general_salary, 
    general_location,
    general_job_type,
    general_rating
    )


def create_general_layout(app: Dash, data: pd.DataFrame) ->  html.Div:
    return html.Div(
        className='',   # class name to add styling
        children=[
            html.H1('Insights'),    #change this heading
            html.Div(
                className= '',   #for styling
                children=[
                        country_dropdown.render(app, data),
                        job_field_dropdown.render(app),
                        
                ]
            ),
            general_job_count.render(app, data),
            html.Hr(),
            html.Br(),
            general_salary.render(app, data),
            html.Hr(),
            html.Br(),
            general_location.render(app, data),
            html.Hr(),
            html.Br(),
            general_job_type.render(app, data),
            html.Hr(),
            html.Br(),
            general_rating.render(app, data)
        ],
    )