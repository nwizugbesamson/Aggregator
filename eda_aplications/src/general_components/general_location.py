import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_LOCATION, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        # [
        #     Input(ids.COUNTRIES_DROPDOWN, 'value'),
        #     Input(ids.JOB_FIELD_DROPDOWN, 'value')
        # ]
    )
    def update_general_salary(countries: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries ')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        location_df =  dataframe.groupby(by=[DataSchema.COUNTRY, DataSchema.LOCATION_GROUP], as_index=False)[DataSchema.LOCATION_GROUP].size()
        loction_figure = px.bar(location_df, 
                        x=DataSchema.COUNTRY, y='size',
                        color=DataSchema.LOCATION_GROUP, barmode='group',
                        template='simple_white',
                         labels={
                                    DataSchema.COUNTRY: "country",
                                    "size": "Job Location",
                                    DataSchema.JOB_FIELD: "Fields"
                                },
                        title="Work Location of Recorded Indeed Offerings In Countries Selected"
                        )

        return html.Div(
            dcc.Graph(          
                    figure=loction_figure
                    ),
            id=ids.GENERAL_LOCATION,
            
        )
    return html.Div(id=ids.GENERAL_LOCATION)



