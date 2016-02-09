from datetime import datetime
from time import strptime, mktime

from flywheel import Model, Field, Engine
from flywheel.fields import types

# Testing configuration values
DB_REGION = 'us-west-1'
DB_HOST = 'localhost'
DB_PORT = 8000
DB_KEY = 'dummy'
DB_SECRET = 'dummy'
DB_SECURE = False

STORE_LOOKUP_URL = 'https://itunes.apple.com/lookup'


class AppDetails(Model):
    app_id = Field(data_type=types.IntType, hash_key=True, coerce=True)
    country = Field(data_type=types.StringType)
    advisories = Field(data_type=types.ListType)
    artistId = Field(data_type=types.IntType, coerce=True)
    artistName = Field(data_type=types.StringType)
    artistViewUrl = Field(data_type=types.StringType)
    artworkUrl100 = Field(data_type=types.StringType)
    artworkUrl512 = Field(data_type=types.StringType)
    artworkUrl60 = Field(data_type=types.StringType)
    averageUserRating = Field(data_type=types.FloatType, coerce=True)
    averageUserRatingForCurrentVersion = Field(
            data_type=types.FloatType,
            coerce=True
    )
    bundleId = Field(data_type=types.StringType)
    contentAdvisoryRating = Field(data_type=types.StringType)
    currency = Field(data_type=types.StringType)
    currentVersionReleaseDate = Field(data_type=types.DateTimeType)
    description = Field(data_type=types.StringType)
    features = Field(data_type=types.ListType)
    fileSizeBytes = Field(data_type=types.IntType, coerce=True)
    formattedPrice = Field(data_type=types.StringType)
    genreIds = Field(data_type=types.ListType)
    genres = Field(data_type=types.ListType)
    ipadScreenshotUrls = Field(data_type=types.ListType)
    isGameCenterEnabled = Field(data_type=types.BoolType)
    isVppDeviceBasedLicensingEnabled = Field(data_type=types.BoolType)
    kind = Field(data_type=types.StringType)
    languageCodesISO2A = Field(data_type=types.ListType)
    minimumOsVersion = Field(data_type=types.StringType)
    price = Field(data_type=types.FloatType, coerce=True)
    primaryGenreId = Field(data_type=types.IntType, coerce=True)
    primaryGenreName = Field(data_type=types.StringType)
    releaseDate = Field(data_type=types.DateTimeType, coerce=True)
    releaseNotes = Field(data_type=types.StringType)
    screenshotUrls = Field(data_type=types.ListType)
    sellerName = Field(data_type=types.StringType)
    sellerUrl = Field(data_type=types.StringType)
    supportedDevices = Field(data_type=types.ListType)
    trackCensoredName = Field(data_type=types.StringType)
    trackContentRating = Field(data_type=types.StringType)
    trackId = Field(data_type=types.IntType, coerce=True)
    trackName = Field(data_type=types.StringType)
    trackViewUrl = Field(data_type=types.StringType)
    userRatingCount = Field(data_type=types.IntType, coerce=True)
    userRatingCountForCurrentVersion = Field(
            data_type=types.IntType,
            coerce=True
    )
    version = Field(data_type=types.StringType)
    wrapperType = Field(data_type=types.StringType)

    def __init__(self, app_id, country, data=None):
        if data is None:
            data = {}

        self.app_id = app_id
        self.country = country
        for field, value in data.items():
            if 'Date' in field:
                value = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                value = datetime.fromtimestamp(mktime(value))
            setattr(self, field, value)


def setup_dynamodb(models, region=DB_REGION, access_key=DB_KEY,
                   secret_key=DB_SECRET, host=DB_HOST, port=DB_PORT,
                   is_secure=DB_SECURE):
    """
    Setups DynamoDB Local and registers flywheel models.

    Parameters:
        models : list
            List of flywheel models to register
        region : str, optional
        access_key : str, optional
        secret_key : str, optional
        host : str, optional
        port : int, optional
        is_secure : bool, optional
    """
    # Create an engine and connect to DynamoDB Local
    engine = Engine()
    engine.connect(
        region,
        access_key=access_key,
        secret_key=secret_key,
        host=host,
        port=port,
        is_secure=is_secure
    )

    # Register models with the engine so it can create Dynamo tables
    engine.register(*models)

    # Drop any existing schema in the database, so we can sync it up with
    # current schema. This is only for development.
    engine.delete_schema()

    # Create the dynamo table for our registered models
    engine.create_schema()
    return engine


engine = setup_dynamodb([AppDetails])
