import plotly.express as px
from functools import reduce
from collections.abc import Iterator
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.general_components import ids
from dashboard.eda_applications.src.utils.process_funcs import return_subset



SELECTED_TYPES = ['contract', 'full-time', 'permanent', 'part-time', 'internship' ]
def group_type(data: Iterator[pd.DataFrame], countries: list[str], job_fields: list[str]) -> pd.DataFrame:
    """Generate Multi index of dataset on count of jobtypes in given countries

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.COUNTRY, DataSchema.JOB_TYPE]
    result = [
                return_subset(dt, countries, job_fields, cols )\
                .query('job_type in @SELECTED_TYPES')
                .groupby(by=cols, as_index=False)\
                .size() for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df.groupby(by=cols, as_index=False).sum()
    return df.drop(df[df['size'] == 0].index)



def render(app: DjangoDash, data: Iterator[pd.DataFrame]) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_JOB_TYPE, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        
    )
    def update_general_job_type(countries: list[str]) -> html.Div:
        dataframe  = group_type(data, countries, job_fields=None)
        if dataframe.shape[0] == 0:
            return html.Div('')
        job_type_figure = px.bar(dataframe, 
                                x='country', y='size',
                                template='simple_white',
                                color='job_type', barmode='group',
                                labels={
                                    'country': 'Country',
                                    'size' : 'Number of Jobs',
                                    'job_type': 'Employment Offer Category'
                                },
                                log_y=True,
                                title='Categories of Employment offers')
        job_type_figure.update_layout(legend=dict(
                                                x=1.02
                                                ), legend_title='')
        return html.Div(
            dcc.Graph(          
                    figure=job_type_figure
                    ),
            id=ids.GENERAL_JOB_TYPE,
            
        )
    return html.Div(id=ids.GENERAL_JOB_TYPE)



