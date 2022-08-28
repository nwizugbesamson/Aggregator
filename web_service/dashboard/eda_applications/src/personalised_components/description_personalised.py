import pandas as pd
import plotly.express as px
from dash import  html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.utils.process_funcs import extract_keyword_degree


from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.personalised_components import p_ids



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    """ render dash html div of plotly bar chart

        Args:
            app (DjangoDash): DjangoDash object
            data (pd.DataFrame): dataframe 
        Returns:
            dash.html.Div
    """
    @app.callback(
        Output(p_ids.P_DESCRIPTION, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
        
    )
    def update_p_descriptions(selected_country: str, selected_job_field: str) -> html.Div:
        """communicate with country and job_field dropdown object
           update bar chart
           
           Args:
            selected_country (str): value of country dropdown
            selected_job_field (str): value of job_field_dropdown
            
           Returns:
                dash.html.Div"""
        if selected_country is not None and selected_job_field is not None:
            dataframe  = data[data[DataSchema.JOB_FIELD] == selected_job_field]
            if dataframe.shape[0] == 0:
                return html.Div('')
            
            freq_words_general = extract_keyword_degree(data, 8)
            Word, Degree_of_importance = zip(*sorted(freq_words_general.items(), key=lambda item: item[1],))
            degree_df = pd.DataFrame({
                'Word': Word,
                'Frequency': Degree_of_importance
            })
            word_fig = px.bar(degree_df, y='Word', x='Frequency',
                     template='simple_white', title='Keywords in Job Descriptions', 
                    )

        return html.Div(
            dcc.Graph(          
                    figure=word_fig
                    ),
            id=p_ids.P_DESCRIPTION,
            
        )
    return html.Div(id=p_ids.P_DESCRIPTION)



