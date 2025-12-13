import unittest
from colusa.plugins.etr_pragmatic_engineer import SubstackFetch

BASE_URL = 'https://newsletter.pragmaticengineer.com/api/v1'
EMAIL = 'pc@gotit.vn'
PASSWORD = 'Gotit@2024'

class PETestCase(unittest.TestCase):
    def setUp(self):
        self.api = SubstackFetch({'email': EMAIL, 'password': PASSWORD, 'base_url': BASE_URL})
        super().setUp()

    def tearDown(self):
        self.api.close()

    def test_login(self):
        self.assertIsNotNone(self.api)
        self.api.export_cookies()

if __name__ == '__main__':
    unittest.main()
