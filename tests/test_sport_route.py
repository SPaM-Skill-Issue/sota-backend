import unittest
from unittest.mock import patch
from .base import setUpTest
from fastapi import status

class TestSportRouter(setUpTest):
    """
    Test suite for the SportRouter's functionality in handling sport detail requests.

    This test class covers scenarios for retrieving sport information based on sport ID,
    including handling both existing and non-existing sport IDs.
    """

    EXISTING_SPORT_ID = 1
    NON_EXISTING_SPORT_ID = int(1e9)

    MOCK_SPORT_DATA = [
        {
            "sport_id": EXISTING_SPORT_ID,
            "sport_name": "Archery",
            "sport_summary": "Archery is good",
            "participating_countries": ["AU", "US"],
            "sport_types": [
                {
                    "type_id": 1,
                    "type_name": "Individual Men's",
                    "participating_countries": ["AU", "US"],
                }
            ],
        }
    ]

    @classmethod
    def setUpClass(cls):
        """Set up the necessary resources before running the tests."""
        super().setUpClass()

    @patch("sota.routers.sport_router.retrieve_sport_info")
    def test_get_sport_id_with_existing_sport_id(self, mock_retrieve_sport_info):
        """
        Verify that the endpoint '/sport/{sport_id}' correctly returns sport details
        for an existing sport ID.
        """
        mock_retrieve_sport_info.return_value = self.MOCK_SPORT_DATA
        response = self.fastapi_client.get(f"/sport/{self.EXISTING_SPORT_ID}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.MOCK_SPORT_DATA[0])
        mock_retrieve_sport_info.assert_called_once_with(self.EXISTING_SPORT_ID)

    @patch("sota.routers.sport_router.retrieve_sport_info")
    def test_get_sport_id_with_non_existing_sport_id(self, mock_retrieve_sport_info):
        """
        Ensure that the endpoint '/sport/{sport_id}' returns an empty dictionary
        when queried with a non-existing sport ID.
        """
        mock_retrieve_sport_info.return_value = {}
        response = self.fastapi_client.get(f"/sport/{self.NON_EXISTING_SPORT_ID}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have been executed."""
        super().tearDownClass()
