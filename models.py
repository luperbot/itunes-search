import requests
from flywheel import Model, Field, Engine

# Testing configuration values
DB_REGION = 'us-west-1'
DB_HOST = 'localhost'
DB_PORT = 8000
DB_KEY = 'dummy'
DB_SECRET = 'dummy'
DB_SECURE = False


def setup_dynamodb(models, region=DB_REGION, access_key=DB_KEY,
                   secret_key=DB_SECRET, host=DB_HOST, port=DB_PORT,
                   is_secure=DB_SECURE):
    """
    Setups DynamoDB Local and registers models.
    Pass function a list of models to register.
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
    for model in models:
        engine.register(model)

    # Create the dynamo table for our registered models
    engine.create_schema()
    return engine


engine = setup_dynamodb([])
