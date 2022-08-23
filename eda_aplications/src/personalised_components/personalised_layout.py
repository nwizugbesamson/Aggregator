from dash import Dash, html
import pandas as pd

#/mnt/c/Users/SAMSON/DataAnalysis/projects/Aggregator/eda_aplications/src/personalised_components/country_dropdown_personal.py
from eda_aplications.src.personalised_components import(
    country_dropdown_personal
)


def create_personalised_layout(app: Dash, data: pd.DataFrame) ->  html.Div:
    return html.Div(
        className='',   # class name to add styling
        children=[
            html.H1('Summary Statistics'),
            html.Div(
                className= '',   #for styling
                children=[
                        country_dropdown_personal.render(app, data),
                        
                        
                ]
            ),
            
        ],
    )