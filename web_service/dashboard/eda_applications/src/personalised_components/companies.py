from collections.abc import Iterator
from functools import reduce
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.personalised_components import p_ids
from dashboard.eda_applications.src.utils.process_funcs import return_subset_single



def group_companies_p(data: Iterator[pd.DataFrame], country: str, job_field : str) -> pd.DataFrame:
    """Grouped dataset by company name within input country and job field

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.COUNTRY, DataSchema.JOB_FIELD, DataSchema.COMPANY_NAME]
    result = [
                return_subset_single(dt, country , job_field, cols) \
                .groupby(by=DataSchema.COMPANY_NAME, as_index=False)\
                .size().sort_values(by='size', ascending=False)[:5]\
                for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df.groupby(by=DataSchema.COMPANY_NAME, as_index=False).sum()
    return df.drop(df[df['size'] == 0].index)



def render(app: DjangoDash, data:  Iterator[pd.DataFrame]) -> html.Div:
    """ render dash html div of plotly bar chart

        Args:
            app (DjangoDash): DjangoDash object
            data (pd.DataFrame): dataframe 
        Returns:
            dash.html.Div
    """
    @app.callback(
        Output(p_ids.P_TOP_COMPANIES, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_top_companies(selected_country: str, selected_job_field: str) -> html.Div:
        """communicate with country and job_field dropdown object
           update bar chart
           
           Args:
            selected_country (str): value of country dropdown
            selected_job_field (str): value of job_field_dropdown
            
           Returns:
                dash.html.Div"""
        if selected_country is not None and selected_job_field is not None:
            dataframe  = group_companies_p(data, selected_country, selected_job_field)
            if dataframe.shape[0] == 0:
                return html.Div('Select Country And Job Field.')
            company_fig = px.bar(dataframe,
                                    y='company_name', x='size', 
                                    labels={
                                            'company_name': 'Name of Comany',
                                            'size': 'Number of Job Listings'
                                    },
                                    text='company_name',
                                    title=f'Major hiring companies',
                                    template='simple_white')
            company_fig.update_traces( textposition='auto')
            company_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            company_fig.update_yaxes(showticklabels=False, ticks='', categoryorder='total ascending' )
            return html.Div(
                dcc.Graph(          
                        figure=company_fig
                        ),
                id=p_ids.P_TOP_COMPANIES,

            )
    return html.Div(id=p_ids.P_TOP_COMPANIES)



