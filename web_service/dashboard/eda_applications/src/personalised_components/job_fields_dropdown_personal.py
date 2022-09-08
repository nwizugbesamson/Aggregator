from dash import  html, dcc
import pandas as pd
from dashboard.eda_applications.src.data.loader import DataSchema, count_unique
from dashboard.eda_applications.src.personalised_components import p_ids




def render(data: pd.DataFrame) -> html.Div:
    """render Dash dropdown
    
    Arg:
        data (pd.DataFrame) : dataframe object
    Returns:
        dash.html.div
    """
    all_fields = count_unique(DataSchema.COUNTRY, data)
    return html.Div(
        children= [
            html.H6('Job Field'),
            dcc.Dropdown(
                id=p_ids.P_JOB_FIELD_DROPDOWN,
                options = [{'label': field, 'value': field} for field in all_fields],
                value = '',
                placeholder="Select a Field",
            )
        ],
    )