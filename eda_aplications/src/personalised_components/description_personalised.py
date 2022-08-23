import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Analysis.process_funcs import IRRELEVANT_WORDS, slice_dataframe, extract_keyword_degree


from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.personalised_components import p_ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(p_ids.P_DESCRIPTION, 'children'),
        [
            Input(p_ids.P_COUNTRIES_DROPDOWN, 'value'),
            Input(p_ids.P_JOB_FIELD_DROPDOWN, 'value')
        ]
        
    )
    def update_p_ratings(selected_country: str, selected_job_field: str) -> html.Div:
        if selected_country is not None and selected_job_field is not None:
            dataframe  = data[data[DataSchema.JOB_FIELD] == selected_job_field]
            if dataframe.shape[0] == 0:
                return html.Div('Select Job Field.')
            

            fig = make_subplots(rows=2, cols=2, shared_xaxes=True, vertical_spacing=0.085, horizontal_spacing=0.12)
            for i, country in enumerate(data['country'].unique()[:2]):
                temp_data = slice_dataframe(data, country=country, job_field='ui ux designer')
                freq_words_general = extract_keyword_degree(temp_data, 8)
                Word, Degree_of_importance = zip(*sorted(freq_words_general.items(), key=lambda item: item[1],))
                plot_max = max(Degree_of_importance) + 500
                fig.add_trace(
                go.Bar(y=Word, x=Degree_of_importance, orientation='h', showlegend=False),
                row=1, col=i+1

            )
                fig.update_xaxes(title_text=country, row=1, col=i+1)
            for i, country in enumerate(data['country'].unique()[2:]):
                temp_data = slice_dataframe(data, country=country, job_field='ui ux designer')
                freq_words_general = extract_keyword_degree(temp_data, 8)
                Word, Degree_of_importance = zip(*sorted(freq_words_general.items(), key=lambda item: item[1],))
                plot_max = max(Degree_of_importance) + 500
                fig.add_trace(
                go.Bar(y=Word, x=Degree_of_importance, orientation='h', showlegend=False),
                row=2, col=i+1)
                fig.update_xaxes(title_text=country, row=2, col=i+1)

            fig.update_layout(height=600, width=800, template='simple_white', title_text=f"Important Key Phrases in {selected_job_field} Job Description Listings")



        

        return html.Div(
            dcc.Graph(          
                    figure=fig
                    ),
            id=p_ids.P_DESCRIPTION,
            
        )
    return html.Div(id=p_ids.P_DESCRIPTION)



