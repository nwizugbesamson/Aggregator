import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.personalised_components import p_ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(p_ids.P_TOP_COMPANIES, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
    )
    def update_top_companies(selected_country: str, selected_job_field: str) -> html.Div:
        if selected_country is not None and selected_job_field is not None:
            dataframe  = data[(data[DataSchema.COUNTRY] == selected_country) & (data[DataSchema.JOB_FIELD] == selected_job_field)]
            if dataframe.shape[0] == 0:
                return html.Div('Select Country And Job Field.')
            company_df = data.groupby(by=['country', 'job_field', 'company_name'], as_index=False).size()
            top_companies = company_df.sort_values(by='size', ascending=False)[:5]

            company_fig = px.bar(top_companies,
                                    x='company_name', y='size', 
                                    labels={
                                            'company_name': 'Name of Comany',
                                            'number_of_offers': 'Number of Job Listings'
                                    },
                                    title=f'Major hiring companies within {selected_country} in the {selected_job_field} field',
                                    template='simple_white')
            return html.Div(
                dcc.Graph(          
                        figure=company_fig
                        ),
                id=p_ids.P_TOP_COMPANIES,

            )
    return html.Div(id=p_ids.P_TOP_COMPANIES)



