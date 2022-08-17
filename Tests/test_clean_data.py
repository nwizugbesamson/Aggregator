import unittest
from Scraper.resources.cleandata import CleanData


class CleanDataTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.clean_data = CleanData()

    

    def test_extract_job_field(self):
        job_field_samples = [
            'jobs?q=software%20engineer&l=United%20States&start=10&vjk=85c595eae674594b',
            'jobs?q=Data%20analyst&l=United%20States&vjk=a9ee7913c713aa4c',
            'jobs?q=ui%20ux%20designer&l=United%20States&vjk=a9ee7913c713aa4c',
            'jobs?q=data%20science&l=Australia&start=10&vjk=85c595eae674594b'

        ]
        self.assertEqual(self.clean_data.extract_job_field(job_field_samples[0]), 'software engineer')
        self.assertEqual(self.clean_data.extract_job_field(job_field_samples[1]), 'data analyst')
        self.assertEqual(self.clean_data.extract_job_field(job_field_samples[2]), 'ui ux designer')
        self.assertEqual(self.clean_data.extract_job_field(job_field_samples[3]), 'data scientist')

    def test_clean_rating(self):
        self.assertEqual(
            type(self.clean_data.clean_rating('4.5')), float
            )

        self.assertNotEqual(
            type(self.clean_data.clean_rating('4.5')), str
            )

        self.assertEqual(
            self.clean_data.clean_rating('4.5') , 4.5
            )

    def test_clean_salary(self):
        self.assertEqual(
            self.clean_data.clean_salary('Up to $84.2–$101.43 per hour') , '84.2-101.43'
        )

        self.assertEqual(
            self.clean_data.clean_salary('Earn $84.2K–$101.43K Yearly') , '84.2K-101.43K'
        )


        self.assertEqual(
            self.clean_data.clean_salary('Earn £750–£1000 daily') , '750-1000'
        )

        self.assertEqual(
            self.clean_data.clean_salary('Earn £92,560–£108,700 daily') , '92560-108700'
        )

    def test_clean_post_date(self):
        self.assertEqual(
            self.clean_data.clean_post_date('Posted 5 days ago'), '2022-08-12'
        )

        self.assertEqual(
            self.clean_data.clean_post_date('Hiring Today'), '2022-08-17'
        )

        self.assertEqual(
            self.clean_data.clean_post_date('Posted 30+ days ago'), '2022-07-18'
        )

    def test_clean_job_description(self):
        self.assertEqual(
            self.clean_data.clean_job_description('testing function that \n strips a lenghty paragrapy of new line \n here is the artificially added new line \nThanks'), 
            'testing function that  strips a lenghty paragrapy of new line  here is the artificially added new line Thanks'
        )

    def test_clean_job_type(self):
        job_types = [
            'temp to perm',
            'fixed term contract',
            'temporary contract',
            'casual',
            'hour shift',
            'temporary / co-op'
        ]

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[0]), 'internship'
        )

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[1]), 'contract'
        )

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[2]), 'contract'
        )

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[3]), 'contract'
        )

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[4]), 'undefined'
        )

        self.assertEqual(
            self.clean_data.clean_job_type(job_types[5]), 'temporary'
        )
if __name__ == "__main__":
    unittest.main()