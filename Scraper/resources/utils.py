
UNDEFINED_LIST = ['$', '£', 'shift', 'Monday to Friday']

COUNTRY_CURRENCY_CONVERSION = {'Canada': 0.7827, 'AUSTRALIA': 0.712665, 'United Kingdom': 1.214175}





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

ALLOWED_DOMAINS = ['indeed.com', 'ca.indeed.com', 'uk.indeed.com', 'au.indeed.com']

START_URLS = [
        ## data analysis
        # 'https://au.indeed.com/jobs?q=data%20analyst&l=Australia', 
        # 'https://uk.indeed.com/jobs?q=data%20analyst&l=United%20Kingdom',
        # 'https://ca.indeed.com/jobs?q=data%20analyst&l=Canada', 
        # 'https://www.indeed.com/jobs?q=data%20analyst&l=United%20States', 


        # ## data science
        # 'https://au.indeed.com/jobs?q=data%20science&l=Australia',  
        # 'https://uk.indeed.com/jobs?q=data%20scientist&l=United%20Kingdom', 
        # 'https://ca.indeed.com/jobs?q=data%20scientist&l=Canada', 
        # 'https://www.indeed.com/jobs?q=data%20scientist&l=United%20States', 

        # ## marketing specialist
        # 'https://au.indeed.com/jobs?q=marketing%20specialist&l=Australia',  
        # 'https://uk.indeed.com/jobs?q=marketing%20specialist&l=United%20Kingdom',  
        # 'https://ca.indeed.com/jobs?q=marketing%20specialist&l=Canada',   
        # 'https://www.indeed.com/jobs?q=marketing%20specialist&l=United%20States', 
        
        # ## product manager
        # 'https://au.indeed.com/jobs?q=product%20manager&l=Australia',
        # 'https://uk.indeed.com/jobs?q=product%20manager&l=United%20Kingdom',
        # 'https://ca.indeed.com/jobs?q=product%20manager&l=Canada',    
        # 'https://www.indeed.com/jobs?q=product%20manager&l=United%20States',

        # ## ui ux design
        # 'https://au.indeed.com/jobs?q=ui%20ux%20designer&l=Australia',    
        # 'https://uk.indeed.com/jobs?q=ui%20ux%20designer&l=United%20Kingdom',
        # 'https://ca.indeed.com/jobs?q=ui%20ux%20designer&l=Canada', 
        # 'https://www.indeed.com/jobs?q=ui%20ux%20designer&l=United%20States',  
        
        
        
        # ## software engineer
        # 'https://au.indeed.com/jobs?q=software%20engineer&l=Australia',  
        # 'https://uk.indeed.com/jobs?q=software%20engineer&l=United%20Kingdom', 
        # 'https://ca.indeed.com/jobs?q=software%20engineer&l=Canada', 
        # 'https://www.indeed.com/jobs?q=software+engineer&l=United%20States' 
        
          ]




