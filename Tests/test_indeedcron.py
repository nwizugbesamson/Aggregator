import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal, assert_series_equal
from Scraper.indeedupdates.indeedcron import salary_to_yearly, curr_to_usd, calculate_avg_salary, clean_location, group_location


class IndeedCronTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data = pd.DataFrame(
            {
                'lower_salary_range_usd': [90000, 85000, 100000, 105650, np.nan, 32000, 45000, 89760, 89400, 205670, 86000],
                'upper_salary_range_usd': [np.nan, np.nan, 123540, 150700, np.nan, 92000, 97000, 76000, np.nan, np.nan, 200500],
                'country': ['Australia', 'Canada', 'Australia', 'United Kingdom', 'USA', 'Canada', 'USA', 'Canada', 'United Kingdom', 'Australia', 'Canada']
            }
        )

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_salary_to_yearly(self):
        salary_series = pd.Series(['87.25k', '15.46', '0', np.nan, '2000', '170', '3500', '140k', '115000'])
        expected_result = pd.Series([87250.0, 32156.8, 0.0, np.nan, 520000.0, 353600.0, 42000.0, 140000.0, 115000.0])

        assert_series_equal(salary_series.apply(salary_to_yearly), expected_result)


    def test_currency_to_usd(self):
        expected_data = pd.DataFrame({
            'lower_salary_range_usd':[64139.85, 66529.5, 71266.5, 128277.58875, np.nan, 25046.4, 45000, 70255.152, 108547.245, 146573.81055, 67312.2],
            'upper_salary_range_usd':[np.nan, np.nan, 88042.6341, 182976.1725, np.nan, 72008.4, 97000, 59485.2, np.nan, np.nan, 156931.35],
            'country': ['Australia', 'Canada', 'Australia', 'United Kingdom', 'USA', 'Canada', 'USA', 'Canada', 'United Kingdom', 'Australia', 'Canada'],
            })

        assert_frame_equal(self.data.apply(curr_to_usd, axis=1), expected_data)


    def test_calculate_average_salary_usd(self):
        expected_data = pd.DataFrame({
            'lower_salary_range_usd': [90000, 85000, 100000, 105650, np.nan, 32000, 45000, 89760, 89400, 205670, 86000],
            'upper_salary_range_usd': [np.nan, np.nan, 123540, 150700, np.nan, 92000, 97000, 76000, np.nan, np.nan, 200500],
            'country': ['Australia', 'Canada', 'Australia', 'United Kingdom', 'USA', 'Canada', 'USA', 'Canada', 'United Kingdom', 'Australia', 'Canada'],
            'average_salary_usd': [90000, 85000, 111770.0, 128175.0, np.nan, 62000.0, 71000.0, 82880.0, 89400, 205670, 143250]
        })

        assert_frame_equal(self.data.apply(calculate_avg_salary, axis=1), expected_data)

    def test_clean_location(self):
        test_data = pd.Series(['Hybrid in Bourghmouth', 'Remote', 'remoteIn New Castle', 'New york, ny', 
                                'Mourville ,Mc +24 locations ','melbourne vic', 'brisbane qld 4000', 
                                'san diego, ca 92110', 'oakland, ca 94607  downtown area ',
                                'gastonia, nc 28056'])
                        
        expected_data = pd.Series(['hybrid', 'remote', 'remote', 'new york, ny', 'mourville, mc', 'melbourne vic', 'brisbane qld',
                                 'san diego, ca', 'oakland, ca', 'gastonia, nc'])

        assert_series_equal(test_data.apply(clean_location), expected_data)

    def test_group_location(self):
        test_data = pd.Series(['hybrid', 'remote', np.nan, 'Ohio', 'New Castle', 'remote'])
        expected_result = pd.Series(['hybrid', 'remote', np.nan, 'physical location', 'physical location', 'remote'])

        assert_series_equal(test_data.apply(group_location), expected_result)