import requests
import unittest

from models import AppDetails, engine, STORE_LOOKUP_URL


TEST_APP_IDS = [726232588, 328412701, 651510680]
TEST_COUNTRIES = ['us', 'mx', 'jp', 'kr', 'ru', 'fr', 'de']


class AppDetailsTestCase(unittest.TestCase):

    def setUp(self):
        self.app_ids = TEST_APP_IDS
        self.countries = TEST_COUNTRIES

    def test_get(self):
        app_id = self.app_ids[-1]
        country = self.countries[-1]
        app_details = engine.get(AppDetails, app_id=app_id, country=country)
        self.assertEqual(app_id, app_details.app_id)
        self.assertEqual(country, app_details.country)

    def test_sync(self):
        app_id = self.app_ids[0]
        country = self.countries[0]
        app_details1 = engine.get(AppDetails, app_id=app_id, country=country)
        app_details2 = engine.get(AppDetails, app_id=app_id, country=country)
        app_details1.artistName = "No One"
        app_details1.sync()
        app_details2.sync()
        self.assertEqual(app_details2.artistName, "No One")

    def test_save(self):
        app_id = 100
        country = 'in'
        app_details = AppDetails(app_id, country)
        engine.save(app_details, overwrite=True)
        engine.delete_key(AppDetails, app_id=app_id, country=country)
        app_details = engine.get(AppDetails, app_id=app_id, country=country)
        self.assertIsNone(app_details)


def load_app_details(app_ids, countries):
    for app_id in app_ids:
        for country in countries:
            data = get_app_data(app_id, country)
            app_details = AppDetails(app_id, country, data=data)
            engine.save(app_details, overwrite=True)


def get_app_data(app_id, country):
    params = {'id': app_id, 'country': country}
    response = requests.get(STORE_LOOKUP_URL, params=params)
    data = response.json()['results']
    if not data:
        return
    return data[0]


if __name__ == '__main__':
    print("Loading DynamoDB data...")
    load_app_details(TEST_APP_IDS, TEST_COUNTRIES)
    unittest.main()
