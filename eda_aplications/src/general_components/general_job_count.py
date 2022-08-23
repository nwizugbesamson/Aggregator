import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_JOB_OFFERS, 'children'),
        [
            Input(ids.COUNTRIES_DROPDOWN, 'value'),
            Input(ids.JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_job_count(countries: list[str], job_fields: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries & {DataSchema.JOB_FIELD} in @job_fields')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        country_field_df = dataframe.groupby(by=[DataSchema.COUNTRY, DataSchema.JOB_FIELD], as_index=False)['company_name'].count()
        country_field = px.bar(country_field_df, 
                            x=DataSchema.COUNTRY, y=DataSchema.COMPANY_NAME,
                            color=DataSchema.JOB_FIELD, barmode='group',
                            template='simple_white',
                             labels={
                                        DataSchema.COUNTRY: "Country",
                                        DataSchema.COMPANY_NAME: "Number of Available offers",
                                        DataSchema.JOB_FIELD: "Job Fields"
                                    },
                            title=f"Job offers Recorded on Indeed"
                            )

        return html.Div(
            dcc.Graph(          
                    figure=country_field
                    ),
            id=ids.GENERAL_JOB_OFFERS,
            
        )
    return html.Div(id=ids.GENERAL_JOB_OFFERS)



