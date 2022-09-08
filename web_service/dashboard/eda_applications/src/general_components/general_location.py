from collections.abc import Iterator
from functools import reduce
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.general_components import ids
from dashboard.eda_applications.src.utils.process_funcs import return_subset





def group_location(data: Iterator[pd.DataFrame], countries: list[str], job_fields: list[str]) -> pd.DataFrame:
    """Generate Multi index of dataset on count of jobtypes in given countries

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.COUNTRY, DataSchema.LOCATION_GROUP]
    result = [
                return_subset(dt, countries, job_fields, cols)\
                .groupby(by=cols, as_index=False)\
                .size() for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df.groupby(by=cols, as_index=False).sum()
    return df.drop(df[df['size'] == 0].index)



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_LOCATION, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        # [
        #     Input(ids.COUNTRIES_DROPDOWN, 'value'),
        #     Input(ids.JOB_FIELD_DROPDOWN, 'value')
        # ]
    )
    def update_general_location(countries: list[str]) -> html.Div:
        dataframe  = group_location(data, countries, job_fields=None)
        if dataframe.shape[0] == 0:
            return html.Div('')
        loction_figure = px.bar(dataframe, 
                        x=DataSchema.COUNTRY, y='size',
                        color=DataSchema.LOCATION_GROUP, barmode='group',
                        template='simple_white',
                         labels={
                                    DataSchema.COUNTRY: "country",  
                                    "size": "Job Location",
                                },
                        title="Work Locations In Countries Selected"
                        )

        return html.Div(
            dcc.Graph(          
                    figure=loction_figure
                    ),
            id=ids.GENERAL_LOCATION,
            
        )
    return html.Div(id=ids.GENERAL_LOCATION)



