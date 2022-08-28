from dash import html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import pandas as pd


from dashboard.eda_applications.src.personalised_components import(
    country_dropdown_personal,
    job_fields_dropdown_personal,
    locations_personalised,
    companies,
    rating_personalised,
    salary_personalised,
    description_personalised 
)


def create_personalised_layout(app: DjangoDash, data: pd.DataFrame) ->  html.Div:
        """create dash application layout

        Args:
            app (DjangoDash): DjangoDash object
            data (pd.DataFrame): dataframe

        Returns:
            html.Div: 
        """
        return html.Div(
            className='',   # class name to add styling
            children=[
                html.Div(
                    className= '',   #for styling
                    children=[
                            country_dropdown_personal.render(data),
                            job_fields_dropdown_personal.render(data)

                    ]
                ),
                dbc.Row([
                        dbc.Col(
                        locations_personalised.render(app, data),
                        width=12, lg={'size':6}
                                ),
                        dbc.Col(
                        companies.render(app, data),
                        width=12, lg={'size':6}
                                ),
                        ]),
                dbc.Row([
                        dbc.Col(
                        rating_personalised.render(app, data),
                        width=12, lg={'size':6}
                                ),
                        dbc.Col(
                        salary_personalised.render(app, data),
                        width=12, lg={'size':6}
                                )
                        ]),


                dbc.Row(
                        dbc.Col(
                                description_personalised.render(app, data),
                                width=12
                        )
                        )
            ],
        )