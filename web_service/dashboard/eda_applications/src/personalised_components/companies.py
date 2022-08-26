import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output


from web_service.dashboard.eda_applications.src.data.loader import DataSchema
from web_service.dashboard.eda_applications.src.personalised_components import p_ids



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
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
                return html.Div('')
            company_df = dataframe.groupby(by=[ 'company_name'], as_index=False).size().sort_values(by='size', ascending=False)[:5]

            company_fig = px.bar(company_df,
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



