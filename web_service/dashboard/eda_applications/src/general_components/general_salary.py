import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output


from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.general_components import ids



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_SALARIES, 'children'),
        [
            Input(ids.COUNTRIES_DROPDOWN, 'value'),
            Input(ids.JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_general_salary(countries: list[str], job_fields: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries & {DataSchema.JOB_FIELD} in @job_fields')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        salary_df = dataframe.groupby(by=[DataSchema.COUNTRY, DataSchema.JOB_FIELD], as_index=False)[DataSchema.AVERAGE_SALARY].mean()
        salaries_figure = px.bar(salary_df, 
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



