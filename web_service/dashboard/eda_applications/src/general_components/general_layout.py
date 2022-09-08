from dash import html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import pandas as pd
from dashboard.eda_applications.src.general_components import (
    country_dropdown, 
    job_field_dropdown, 
    general_job_count, 
    general_salary, 
    general_location,
    general_job_type,
    general_rating
    )


def create_general_layout(app: DjangoDash, data: pd.DataFrame) ->  html.Div:
    return html.Div(
        className='',   # class name to add styling
        children=[
              
            ## DROPDOWNS ##
            html.Div(
                className= '',   #for styling
                children=[
                        country_dropdown.render(app, data),
                        job_field_dropdown.render(app, data),   
                ]
            ),


            ## first row  ##
            dbc.Row([
                dbc.Col(
                         general_job_count.render(app, data),
                         width=12, lg={'size':6}
                        ),
           
                dbc.Col(
                        general_salary.render(app, data),
                         width=12, lg={'size':6}
                    ),
            ]),
        
            html.Br(),
            general_location.render(app, data),
            
            # second_row
            dbc.Row([
                dbc.Col(
            general_job_type.render(app, data),
                         width=12, lg={'size':6}
                        ),
           
                dbc.Col(
            general_rating.render(app, data),
                         width=12, lg={'size':6}
                        )
            ])
        ]
    )