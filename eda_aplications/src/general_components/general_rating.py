import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import plotly.tools


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.GENERAL_RATING, 'children'),
        Input(ids.COUNTRIES_DROPDOWN, 'value')
        
    )
    def update_general_salary(countries: list[str]) -> html.Div:
        dataframe  = data.query(f'{DataSchema.COUNTRY} in @countries')
        if dataframe.shape[0] == 0:
            return html.Div('Select Country And Job Field.')
        rate_fig = plt.figure(figsize=(11,6))
        for country in countries:
            data[data.country == country]['rating'].plot.kde(label = country, legend = True)
        plt.xlim((2.5, 4.7))
        rate_fig = plotly.tools.mpl_to_plotly(rate_fig)
        rate_fig.update_layout(template='simple_white', 
                               title='Ratings Given By Staff in selected countries', 
                               xaxis=dict(title='Ratings', showline=False, zeroline=False, ticks=''), 
                               yaxis=dict(title='Relative Frequency', showline=False,  ticks='', ticklabelstep=2
                               ))
        

        return html.Div(
            dcc.Graph(          
                    figure=rate_fig
                    ),
            id=ids.GENERAL_RATING,
            
        )
    return html.Div(id=ids.GENERAL_RATING)



