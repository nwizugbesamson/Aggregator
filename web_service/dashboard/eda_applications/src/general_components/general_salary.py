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

def group_salary(data: Iterator[pd.DataFrame], countries: list[str], job_fields: list[str]) -> pd.DataFrame:
    """Generate Multi index of dataset on count of job offers in given countries and job fields

    Args:
        data (Iterator[pd.DataFrame]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    cols = [DataSchema.COUNTRY, DataSchema.JOB_FIELD, DataSchema.AVERAGE_SALARY]
    result = [
                return_subset(dt, countries, job_fields, cols)\
                .groupby(by=[DataSchema.COUNTRY, DataSchema.JOB_FIELD], as_index=False)\
                [DataSchema.AVERAGE_SALARY].mean() \
                for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y]) , result
                )  
    df = df.groupby(by=['country', 'job_field'], as_index=False).mean()
    return df.drop(df[df[DataSchema.AVERAGE_SALARY] == 0].index)

def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_SALARIES, 'children'),
        [
            Input(ids.COUNTRIES_DROPDOWN, 'value'),
            Input(ids.JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_general_salary(countries: list[str], job_fields: list[str]) -> html.Div:
        dataframe  = group_salary(data, countries, job_fields)
        if dataframe.shape[0] == 0:
            return html.Div('')
       
        salaries_figure = px.bar(dataframe, 
                        x=DataSchema.COUNTRY, y=DataSchema.AVERAGE_SALARY,
                        color=DataSchema.JOB_FIELD, barmode='group',
                        template='simple_white',
                         labels={
                                    DataSchema.COUNTRY: "Country",
                                    'average_salary_usd': "Average Salary (USD)",
                                    DataSchema.JOB_FIELD: "Job Fields"
                                },
                        title="Average Salaries"
                        )
        salaries_figure.update_layout(showlegend=False)

        return html.Div(
            dcc.Graph(          
                    figure=salaries_figure
                    ),
            id=ids.GENERAL_SALARIES,
            
        )
    return html.Div(id=ids.GENERAL_SALARIES)



