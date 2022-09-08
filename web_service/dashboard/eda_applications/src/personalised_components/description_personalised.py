from collections.abc import Iterator
from functools import reduce
import pandas as pd
import plotly.express as px
from dash import  html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from dashboard.eda_applications.src.utils.process_funcs import return_extracted_keywords, return_subset_single, NUMBER_OF_KEYWORDS
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.personalised_components import p_ids




def group_descriptions_p(data: Iterator[pd.DataFrame], country: str, job_field : str) -> pd.DataFrame:
    """return dataframe containing top words in selected country and job field

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.JOB_DESCRIPTION]
    result = [
                return_extracted_keywords(
                                         return_subset_single(dt, country , job_field, cols)
                                        ) for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y], ignore_index=True) , result
                )  
    return df.sort_values(by='Frequency').head(NUMBER_OF_KEYWORDS)


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
            dataframe  = group_descriptions_p(data, selected_country, selected_job_field)
            if dataframe.shape[0] == 0:
                return html.Div('')
            
            word_fig = px.bar(dataframe, y='Word', x='Frequency',
                     template='simple_white', title='Keywords in Job Descriptions', 
                    )

        return html.Div(
            dcc.Graph(          
                    figure=word_fig
                    ),
            id=p_ids.P_DESCRIPTION,
            
        )
    return html.Div(id=p_ids.P_DESCRIPTION)



