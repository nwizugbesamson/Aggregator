import plotly.express as px
import pandas as pd
from dash import html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output


from web_service.dashboard.eda_applications.src.data.loader import DataSchema
from web_service.dashboard.eda_applications.src.personalised_components import p_ids



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(p_ids.P_RATING, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
        
    )
    def update_p_ratings(selected_country: str, selected_job_field: str) -> html.Div:
        if selected_country is not None and selected_job_field is not None:
            # dataframe  = data.query(f'{DataSchema.COUNTRY} == selected_country & {DataSchema.JOB_FIELD} == selected_job_field')
            dataframe  = data[(data[DataSchema.COUNTRY] == selected_country) & (data[DataSchema.JOB_FIELD] == selected_job_field)]
            if dataframe.shape[0] == 0:
                return html.Div('')
        rate_fig = px.histogram(dataframe, x='rating', template='simple_white', nbins=12, 
                               labels = {
                                'count': '',
                                'rating': 'Rating'
                               })
        rate_fig.update_layout(template='simple_white', 
                               title=f'Staff Ratings of Companies'
                               
                               )
        

        return html.Div(
            dcc.Graph(          
                    figure=rate_fig
                    ),
            id=p_ids.P_RATING,
            
        )
    return html.Div(id=p_ids.P_RATING)



