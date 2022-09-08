from collections.abc import Iterator
from functools import reduce
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.general_components import ids
from dashboard.eda_applications.src.utils.process_funcs import return_subset



def group_rating(data: Iterator[pd.DataFrame], countries: list[str], job_fields: list[str]) -> pd.DataFrame:
    """Return dataset where rating is not null

    Args:
        data (Iterator[pd.DataFrame]): 

    Returns:
        pd.DataFrame: 
    """
    cols = [DataSchema.COUNTRY, DataSchema.RATING]
    result = [
                return_subset(dt, countries,  job_fields, cols)\
                .dropna(subset=[DataSchema.RATING]) \
                for dt in data
            ]
    df = pd.DataFrame()
    df = reduce(
            lambda x, y: pd.concat([x, y], ignore_index=True) , result
                )  
 
    return df



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_RATING, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        
    )
    def update_general_rating(countries: list[str]) -> html.Div:
        dataframe  = group_rating(data, countries, job_fields=None)
        if dataframe.shape[0] == 0:
            return html.Div('')
        hist_data = [dataframe[dataframe[DataSchema.COUNTRY] == cnt]['rating'] for cnt in list(dataframe[DataSchema.COUNTRY].unique()) ]
        group_labels = list(dataframe[DataSchema.COUNTRY].unique())
        rate_fig = ff.create_distplot(hist_data, group_labels, bin_size=.2,show_hist=False, show_rug=False)

        rate_fig.update_layout(title_text='Ratings of Companies given by Staff', template='simple_white', xaxis=dict(range=[2.25, 5]),
                                xaxis_title="Rating",
                                yaxis_title="Frequency(Scaled)",)


        return html.Div(
            dcc.Graph(          
                    figure=rate_fig
                    ),
            id=ids.GENERAL_RATING,
            
        )
    return html.Div(id=ids.GENERAL_RATING)



