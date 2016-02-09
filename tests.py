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


class SearchTestCase(unittest.TestCase):
    """
    Example queries to test filtering/search of items in AppDetails table.

    Do not use table scans. They do not use indexes, instead they search by
    reading every item in the table. Extremely slow.
    """

    def setUp(self):
        engine.save(AppDetails(100000000, 'us', {'price': 1.50}), overwrite=True)
        engine.save(AppDetails(100000000, 'ca', {'price': 5.00}), overwrite=True)
        engine.save(AppDetails(100000000, 'in', {'price': 3.50}), overwrite=True)
        engine.save(AppDetails(100000000, 'mx', {'price': 1.25}), overwrite=True)
        engine.save(AppDetails(100000000, 'sa', {'price': 0}), overwrite=True)

    def print_prices(self, found_apps):
        for results in found_apps:
            for app_details in results:
                print "\tApp ID: %s, Country: %s, Price: %s" % (
                    app_details.app_id, app_details.country, app_details.price
                )

    def test_free_or_cheap(self):
        print("\nFind all apps that are free or a price from $1.50 to $3.50.")
        free_apps = engine(AppDetails).filter(priceFree=1).index('price-index').all()
        cheap_apps = engine(AppDetails).filter(priceFree=0) \
            .filter(AppDetails.price.between_(1.50, 3.50)) \
            .index('price-index').all()
        self.print_prices([free_apps, cheap_apps])

    def test_ipad2(self):
        print("\nFind all apps that work on any model of iPad2.")


def load_app_details(app_ids, countries):
    """
    Queries external app store API for avaliable data for each
    app_id/countries combination.
    If data found, saves details in the AppDetails table.
    """
    for app_id in app_ids:
        for country in countries:
            data = get_app_data(app_id, country)
            if not data:
                continue
            app_details = AppDetails(app_id, country, data=data)
            engine.save(app_details)


def get_app_data(app_id, country):
    """
    Makes a request to the app store API for given app_id (int)
    and country code (str).
    Returns a dictionary of any found data.
    """
    params = {'id': app_id, 'country': country}
    response = requests.get(STORE_LOOKUP_URL, params=params)
    data = response.json()['results']
    if not data:
        return {}
    return data[0]


if __name__ == '__main__':
    print("Loading DynamoDB data...")
    load_app_details(TEST_APP_IDS, TEST_COUNTRIES)
    unittest.main()
