import pandas as pd
import re
from Scraper.resources.utils import COUNTRY_CURRENCY_CONVERSION 




def salary_to_yearly(value:str):
        """return the yearly equivalent pay for jobs with hourly, daily and monthly pay offers

        Args:
            value (int): integer for operation

        Returns:
            value(int): result of operation
        """
        if pd.isna(value):
            return value
        if 'k' in value.lower():
            return float(value.lower().replace('k', '')) * 1000 
        if float(value) < 200:
            return float(value) * 8 * 260
        if float(value) < 2600:
            return float(value) * 260
        if float(value) < 7000:
            return float(value) * 12
        return float(value)




def curr_to_usd(row:pd.Series) -> pd.Series:
    """Convert all currencies to usd

    Args:
        row (_pd.Series_): dataframe row for operation

    Returns:
        row (_pd.Series_): transformed row
    """
    if pd.notna(row['lower_salary_range_usd']) and row['country'] in COUNTRY_CURRENCY_CONVERSION:
        row['lower_salary_range_usd'] = round(row['lower_salary_range_usd'] * COUNTRY_CURRENCY_CONVERSION[row['country']], 2)
    if pd.notna(row['upper_salary_range_usd']) and row['country'] in COUNTRY_CURRENCY_CONVERSION:
        row['upper_salary_range_usd'] = round(row['upper_salary_range_usd'] * COUNTRY_CURRENCY_CONVERSION[row['country']], 2)
    return row


def calculate_avg_salary(row):
    """Calculate average salary column with lower and upper salary range,
       return lower_salary_range if upper_salary_range is NaN

    Args:
        row (_pd.Series_): dataframe row for operation

    Returns:
        row (_pd.Series_): transformed row
    """
    row['average_salary_usd'] = row['lower_salary_range_usd']
    if pd.notna(row['lower_salary_range_usd']) and pd.notna(row['upper_salary_range_usd']):
        row['average_salary_usd'] = (row['lower_salary_range_usd'] + row['upper_salary_range_usd'])/2
    return row


## process clean location
def clean_location(value: str):
    value = value.lower()
    if 'hybrid' in value:
        return 'hybrid'
    if 'remote' in value:
        return 'remote'
    value = re.sub(r'[^a-zA-Z,]', ' ',value)
    value = value.replace('locations', '').strip()
    return value

def group_location(value):
    if value == 'remote' or value == 'hybrid' or pd.isna(value):
        return value
    return 'physical location'

def preprocess_data(read_path, write_path):

    ## load dataframe
    coltypes = {'salary': str}
    data: pd.DataFrame = pd.read_csv(read_path, dtype=coltypes, na_values=['Null'], parse_dates=['post_date'], index_col=False)


    ##   DROP Unnamed: 0
    data.drop(columns=['Unnamed: 0'], inplace=True)

    ## drop duplicated rows
    data = data.drop_duplicates(subset=['company_name', 'job_description', 'job_title'])


    data['clean_location'] = data['non_remote_location'].apply(clean_location)

    data['location_group'] = data['clean_location'].apply(group_location)
    ## process date column
    data['post_date'] = pd.to_datetime(data['post_date'].dt.strftime('%Y-%m-%d'))

    data[['lower_salary_range_usd', 'upper_salary_range_usd']] = data['salary'].str.split('-',expand=True)

    

    data['lower_salary_range_usd'] = data['lower_salary_range_usd'].apply(salary_to_yearly)

    data['upper_salary_range_usd'] = data['upper_salary_range_usd'].apply(salary_to_yearly)



    data = data.apply(curr_to_usd, axis=1)

    data = data.apply(calculate_avg_salary, axis=1)

    data.to_csv(write_path, index=False)

