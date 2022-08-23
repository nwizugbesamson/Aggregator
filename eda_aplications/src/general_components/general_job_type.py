import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_JOB_TYPE, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        
    )
    def update_general_salary(countries: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        job_type_df = dataframe[dataframe['job_type'].isin(['contract', 'full-time', 'permanent', 'part-time', 'internship' ])]\
                        .groupby(by=['country', 'job_type'], as_index=False).size()
        job_type_figure = px.bar(job_type_df, 
                                x='country', y='size',
                                template='simple_white',
                                color='job_type', barmode='group',
                                labels={
                                    'country': 'Country',
                                    'size' : 'Number of Jobs',
                                    'job_type': 'Employment Offer Category'
                                },
                                log_y=True,
                                title='Categories of Employment offers In Countries Selected')

        return html.Div(
            dcc.Graph(          
                    figure=job_type_figure
                    ),
            id=ids.GENERAL_JOB_TYPE,
            
        )
    return html.Div(id=ids.GENERAL_JOB_TYPE)



