import pandas as pd
from django_plotly_dash import DjangoDash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.figure_factory as ff


from web_service.dashboard.eda_applications.src.data.loader import DataSchema
from web_service.dashboard.eda_applications.src.general_components import ids



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_RATING, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        
    )
    def update_general_rating(countries: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        dataframe = dataframe.dropna(subset=[DataSchema.RATING])
        hist_data = [dataframe[dataframe[DataSchema.COUNTRY] == cnt]['rating'] for cnt in list(dataframe[DataSchema.COUNTRY].unique()) ]
        group_labels = list(dataframe[DataSchema.COUNTRY].unique())
        print('Dataframe divided')
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



