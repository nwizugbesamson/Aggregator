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



            

def group_country(data: Iterator[pd.DataFrame], countries: list[str], job_fields: list[str]) -> pd.DataFrame:
    """Generate Multi index of dataset on count of job offers in given countries and job fields

    Args:
        data (Iterator[pd.DataFrame]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    cols = [DataSchema.COUNTRY, DataSchema.JOB_FIELD]
    result = [
                return_subset(dt, countries, job_fields, cols)\
                .groupby(by=[DataSchema.COUNTRY, DataSchema.JOB_FIELD], as_index=False)\
                .size() for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df.groupby(by=['country', 'job_field'], as_index=False).sum()
    return df.drop(df[df['size'] == 0].index)





def render(app: DjangoDash, data: Iterator[pd.DataFrame]) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_JOB_OFFERS, 'children'),
        [
            Input(ids.COUNTRIES_DROPDOWN, 'value'),
            Input(ids.JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_job_count(countries: list[str], job_fields: list[str]) -> html.Div:
        dataframe  = group_country(data, countries, job_fields)
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        country_field = px.bar(dataframe, 
                            x=DataSchema.COUNTRY, y='size',
                            color=DataSchema.JOB_FIELD, barmode='group',
                            template='simple_white',
                             labels={
                                        DataSchema.COUNTRY: "Country",
                                        'size': "Number of Available offers",
                                        DataSchema.JOB_FIELD: "Job Fields"
                                    },
                            title=f"Job offers Recorded on Indeed",
                            

                            )
        country_field.update_layout(legend=dict(x=1.02), legend_title='')

        return html.Div(
            dcc.Graph(          
                    figure=country_field
                    ),
            id=ids.GENERAL_JOB_OFFERS,
            
        )
    return html.Div(id=ids.GENERAL_JOB_OFFERS)



