import unittest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from Analysis.process_funcs import extract_keyword_degree, slice_dataframe

class ProccessTunctionTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.data = pd.DataFrame({
            'job_field': ['marketing specialist', 'data analyst', 'data analyst', 
                          'product manager', 'software engineer', 'product manager', 
                          'ui ux designer', 'marketing specialist', 'data analyst', 
                          'marketing specialist', 'product manager', 'product manager', 
                          'data scientist', 'data scientist', 'marketing specialist'],
            'country': [
                'Canada','AUSTRALIA', 'United Kingdom', 'United Kingdom',
                'United Kingdom', 'United Kingdom', 'United Kingdom', 'Canada',
                'United Kingdom', 'USA', 'United Kingdom', 'USA',
                'USA', 'AUSTRALIA', 'Canada'],

            'job_description': ['data data data data data data on where is data in data science data data',
                            'data analysis position requring experience managing complex data systems...',
                            'data management, python proficiency, accuracy, insighful and impactful analysis',
                            'manage company products and teams, ability to work in large teams is essential',
                            'software engineer with experience providing effective cloud solutions, ',
                            'identifies the customer need and the larger business objectives that a product or feature will fulfill',
                            'innovative designs, digital competence',
                            'develop, execute, and monitor marketing programs across a variety of channels',
                            'data skills, tableau, ability to communicate ideas',
                            'data data data data data data on where is data in data science data data',
                            'cloud cloud cloud cloud cloud cloud cloud computing computing is computing the computing',
                            'product cloud data data data data data important team team team team team ',
                            'exclude exclude in team teams team work data data analysis',
                            'product products data analysis well data analysis products data crazy data data well',
                            'choose data analysis cloud cloud python python python python python python python with'
                            ] 

        })



    def test_slice_dataframe(self):

        expeced_df_one = self.data[(self.data['country'] == 'Canada') & (self.data['job_field'] == 'data scientist')]
        expeced_df_two = self.data[(self.data['country'] == 'Canada') ]
        expeced_df_three = self.data[(self.data['job_field'] == 'data analyst')]

        assert_frame_equal(slice_dataframe(self.data, country='Canada', job_field='data scientist'), expeced_df_one)
        assert_frame_equal(slice_dataframe(self.data, country='Canada'), expeced_df_two)
        assert_frame_equal(slice_dataframe(self.data,  job_field='data analyst'), expeced_df_three)

    def test_extract_keyword_degree(self):
        expected_degree  =    {
                               'data': 278,
                               'cloud': 105,
                               'python': 86,
                               'team': 79,
                               'well': 26,
                               }

        self.assertEqual(extract_keyword_degree(self.data, 5), expected_degree)
                               
      
