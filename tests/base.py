import unittest
from unittest.mock import patch, Mock
from mongomock import MongoClient
from fastapi.testclient import TestClient
from sota.main import app
from sota.database_connection import client
from bson import decode_file_iter


class setUpTest(unittest.TestCase):
    """
    Base test setup class for initializing the test environment.

    This class sets up a mock MongoDB client and preloads it with test data from BSON files.
    It also initializes a FastAPI test client for making requests to the API during tests.
    This setup is executed once before all tests in the suite.

    Attributes:
        mongo_mock_client: An instance of the mock MongoDB client.
        db: A reference to the 'Sota' database within the mock MongoDB client.
        fastapi_client: An instance of the FastAPI test client for API requests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initializes the mock MongoDB client, loads test data, and sets up the FastAPI test client.
        """
        cls.mongo_mock_client = (
            client  # Use the provided MongoDB client (mocked or real)
        )
        cls.db = cls.mongo_mock_client["Sota"]  # Reference to the 'Sota' database

        # Load test data into the database
        cls.load_test_data()

        # Initialize FastAPI test client
        cls.fastapi_client = TestClient(app)

    @classmethod
    def load_test_data(cls):
        """
        Loads test data from BSON files into the mock MongoDB database.

        Supported collections: 'Audient', 'Keys', 'Medal', 'SportDetail', 'SubSportType'.
        Each collection's data is stored in a corresponding BSON file in 'dump_data/Sota'.
        """
        collections = ["Audient", "Keys", "Medal", "SportDetail", "SubSportType"]
        for collection_name in collections:
            with open(f"dump_data/Sota/{collection_name}.bson", "rb") as file:
                collection_data = list(decode_file_iter(file))
                if collection_data:
                    cls.db[collection_name].insert_many(collection_data)

    @classmethod
    def insert_authentication_keys(cls, keys_data):
        """
        Inserts mock authentication keys into the database.

        Args:
            keys_data (list): A list of dictionaries, each containing a key and its scope.
        """
        cls.db["Keys"].insert_many(keys_data)

    def post_request(self, url, token, payload):
        """
        Sends a POST request to a specified URL with a Bearer token and JSON payload.

        Args:
            url (str): The URL to which the request is sent.
            token (str): The Bearer token used for authorization in the request header.
            payload (dict): The JSON payload to be sent with the request.

        Returns:
            Response: The response object from the FastAPI test client.
        """
        return self.fastapi_client.post(
            url, headers={"Authorization": f"Bearer {token}"}, json=payload
        )

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the mock MongoDB database and FastAPI test client after tests are executed.
        """
        cls.mongo_mock_client.drop_database("Sota")
        cls.mongo_mock_client.close()
        cls.fastapi_client.close()
