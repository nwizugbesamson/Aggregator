from collections.abc import Iterator
from functools import reduce
import plotly.express as px
import pandas as pd
from dash import  html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.personalised_components import p_ids
from dashboard.eda_applications.src.utils.process_funcs import return_subset_single

FILTERED_LOCATIONS = ['remote', 'hybrid']

def group_locations_p(data: Iterator[pd.DataFrame], country: str, job_field : str) -> pd.DataFrame:
    """Generate Multi index of dataset on count of popular location offers in given country

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.COUNTRY, DataSchema.JOB_FIELD, DataSchema.CLEAN_LOCATION]
    result = [
                return_subset_single(dt, country , job_field, cols) \
                .groupby(by=DataSchema.CLEAN_LOCATION, as_index=False)\
                .size()\
                for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df[~df[DataSchema.CLEAN_LOCATION].isin(FILTERED_LOCATIONS)].groupby(by=DataSchema.CLEAN_LOCATION, as_index=False).sum()
    return df.drop(df[df['size'] == 0].index)\
           .sort_values(by='size', ascending=False)[:5]


def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    """ render dash html div of plotly bar chart

        Args:
            app (DjangoDash): DjangoDash object
            data (pd.DataFrame): dataframe 
        Returns:
            dash.html.Div
    """
    @app.callback(
        Output(p_ids.P_TOP_LOCATIONS, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_top_locations(selected_country: str, selected_job_field: str) -> html.Div:
        """communicate with country and job_field dropdown object
           update bar chart
           
           Args:
            selected_country (str): value of country dropdown
            selected_job_field (str): value of job_field_dropdown
            
           Returns:
                dash.html.Div"""
        if selected_country is not None and selected_job_field is not None:
            dataframe  = group_locations_p(data, selected_country, selected_job_field)
            if dataframe.shape[0] == 0:
                return html.Div('')
            location_fig = px.bar(dataframe,
            x='clean_location', y='size', 
            labels={
                    'clean_location': 'Location',
                    'size': 'Number of Job Listings'
            },
            title=f'High Employment Location',
            template='simple_white')
            return html.Div(
                dcc.Graph(          
                        figure=location_fig
                        ),
                id=p_ids.P_TOP_LOCATIONS,

            )
    return html.Div(id=p_ids.P_TOP_LOCATIONS)



