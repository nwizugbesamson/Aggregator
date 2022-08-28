import plotly.express as px
import pandas as pd
from dash import  html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output


from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.personalised_components import p_ids



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
            dataframe  = data[(data[DataSchema.COUNTRY] == selected_country) & (data[DataSchema.JOB_FIELD] == selected_job_field)]
            if dataframe.shape[0] == 0:
                return html.Div('Select Country And Job Field.')
            location_df = dataframe.groupby(by=[ 'clean_location'], as_index=False).size()
            top_locations = location_df[~location_df['clean_location'].isin(['remote', 'hybrid'])].sort_values(by='size', ascending=False)[:5]

            location_fig = px.bar(top_locations,
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



