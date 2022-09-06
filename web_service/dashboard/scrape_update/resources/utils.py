
UNDEFINED_LIST = ['$', '£', 'shift', 'Monday to Friday']

COUNTRY_CURRENCY_CONVERSION = {'Canada': 0.7827, 'Australia': 0.712665, 'United Kingdom': 1.214175}





PATTERNS = {
        'data analyst': ['data%20analyst', 'data+analyst'],
        'data scientist': ['data%20scientist', 'data+scientist',  'data%20science', 'data+science'],
        'marketing specialist': ['marketing%20specialist', 'marketing+specialist'],
        'product manager': ['product+manager', 'product%20manager'],
        'ui ux designer': ['ui+ux+designer', 'ui%20ux%20designer'],
        'software engineer': ['software%20engineer', 'software+engineer',]
}



JOB_FIELDS = [ 'product%20manager', 'data%20scientist', 'Data+scientist', 'Data%20scientist',
            'marketing%20specialist', 'ui%20ux-designer', 'software%20engineer', 
            'data%20analyst'
            ]


BASE_URLS = {
    'Australia': [f'https://au.indeed.com/jobs?q={field}&l=Australia' for field in JOB_FIELDS],
    'United Kingdom': [f'https://uk.indeed.com/jobs?q={field}&l=United%20Kingdom' for field in JOB_FIELDS],
    'Canada': [f'https://ca.indeed.com/jobs?q={field}&l=Canada' for field in JOB_FIELDS],
    'USA': [f'https://www.indeed.com/jobs?q={field}&l=United%20States' for field in JOB_FIELDS],
     }


