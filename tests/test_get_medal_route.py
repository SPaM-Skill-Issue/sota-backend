import unittest
from .base import setUpTest
from unittest.mock import patch
from fastapi import status
import itertools

class TestGetMedal(setUpTest):
    """
    Test suite for retrieving medal information in the SOTA API.

    This test class covers the functionality of the Medal Router for various retrieval scenarios,
    including searching by country code, sport ID, and sub-sport ID. It verifies the API's
    response for both existing and non-existing parameters.
    """

    SOME_COUNTRY_CODE = "HU"
    SOME_SPORT_ID = 1
    SOME_SUB_SPORT_ID = 1

    MOCK_MEDAL_BY_COUNTRY_DATA = itertools.tee(
        iter(
            [
                {
                    "country_name": "Hungary",
                    "gold_medals": 0,
                    "silver_medals": 1,
                    "bronze_medals": 0,
                    "individual_sports": [
                        {
                            "sport_id": 1,
                            "sport_name": "Archery",
                            "gold_medals": 0,
                            "silver_medals": 1,
                            "bronze_medals": 0,
                            "sub_sports": [
                                {
                                    "sub_id": 1,
                                    "sub_name": "Individual Men's",
                                    "gold_medals": 0,
                                    "silver_medals": 1,
                                    "bronze_medals": 0,
                                }
                            ],
                        }
                    ],
                    "country_code": "HU",
                }
            ]
        ),
        2,
    )

    MOCK_MEDAL_BY_SPORT_ID_DATA = itertools.tee(
        iter(
            [
                {
                    "sport_name": "Archery",
                    "gold_medals": 1,
                    "silver_medals": 0,
                    "bronze_medals": 0,
                    "individual_countries": [
                        {
                            "country_code": "US",
                            "country_name": "United States",
                            "gold_medals": 1,
                            "silver_medals": 0,
                            "bronze_medals": 0,
                            "sub_sports": [
                                {
                                    "sub_id": 1,
                                    "sub_name": "Individual Men's",
                                    "gold_medals": 1,
                                    "silver_medals": 0,
                                    "bronze_medals": 0,
                                }
                            ],
                        }
                    ],
                    "sport_id": 1,
                }
            ]
        ),
        2,
    )

    MOCK_MEDAL_BY_SUB_SPORT_ID_DATA = itertools.tee(
        iter(
            [
                {
                    "gold_medals": 1,
                    "silver_medals": 0,
                    "bronze_medals": 0,
                    "sport_id": 6,
                    "sport_name": "Basketball",
                    "sub_sport_id": 1,
                    "sub_sport_name": "Tournament Men's",
                    "individual_countries": [
                        {
                            "country_code": "US",
                            "country_name": "United States",
                            "gold_medals": 1,
                            "silver_medals": 0,
                            "bronze_medals": 0,
                        }
                    ],
                }
            ]
        ),
        2,
    )

    MOCK_MEDAL_FOR_NON_EXISTING_PARAMS = iter([])

    @classmethod
    def setUpClass(cls):
        """Set up the necessary resources for running the tests."""
        super().setUpClass()

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_country_with_recorded_country_code(
        self, mock_retrieve_medal_by_country
    ):
        """
        Test the retrieval of medal details for a recorded country code.

        This test verifies the '/medal/c/:country_code' endpoint.
        """
        mock_retrieve_medal_by_country.return_value = self.MOCK_MEDAL_BY_COUNTRY_DATA[0]
        response = self.fastapi_client.get(f"/medal/c/{self.SOME_COUNTRY_CODE}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), list(self.MOCK_MEDAL_BY_COUNTRY_DATA[1])[0])

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_country_with_unrecorded_country_code(
        self, mock_retrieve_medal_by_country
    ):
        """
        Test the retrieval of an empty object for an unrecorded country code.

        This test verifies the '/medal/c/:country_code' endpoint.
        """
        mock_retrieve_medal_by_country.return_value = (
            self.MOCK_MEDAL_FOR_NON_EXISTING_PARAMS
        )
        response = self.fastapi_client.get(f"/medal/c/{self.SOME_COUNTRY_CODE}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_sport_id_recorded_sport_id(
        self, mock_retrieve_medal_by_sport_id
    ):
        """
        Test the retrieval of medal details for a recorded sport ID.

        This test verifies the '/medal/s/:sport_id' endpoint.
        """
        mock_retrieve_medal_by_sport_id.return_value = self.MOCK_MEDAL_BY_SPORT_ID_DATA[
            0
        ]
        response = self.fastapi_client.get(f"/medal/s/{self.SOME_SPORT_ID}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), list(self.MOCK_MEDAL_BY_SPORT_ID_DATA[1])[0])

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_sport_id_with_unrecorded_sport_id(
        self, mock_retrieve_medal_by_sport_id
    ):  
        """
        Test the retrieval of an empty object for an unrecorded sport ID.

        This test verifies the '/medal/s/:sport_id' endpoint.
        """
        mock_retrieve_medal_by_sport_id.return_value = (
            self.MOCK_MEDAL_FOR_NON_EXISTING_PARAMS
        )
        response = self.fastapi_client.get(f"/medal/s/{self.SOME_SPORT_ID}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_subsport_id_with_by_recorded_sport_id_and_sub_sport_id(
        self, mock_retrieve_medal
    ):  
        """
        Test the retrieval of medal details for a recorded sport ID and subsport ID.

        This test verifies the '/medal/s/:sport_id/t/:subsport_id' endpoint.
        """
        mock_retrieve_medal.return_value = self.MOCK_MEDAL_BY_SUB_SPORT_ID_DATA[0]
        response = self.fastapi_client.get(
            f"/medal/s/{self.SOME_SPORT_ID}/t/{self.SOME_SUB_SPORT_ID}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), list(self.MOCK_MEDAL_BY_SUB_SPORT_ID_DATA[1])[0]
        )

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_subsport_id_with_by_unrecorded_sport_id(
        self, mock_retrieve_medal
    ):
        """
        Test the retrieval of an empty object for an unrecorded sport ID and recorded subsport ID.

        This test verifies the '/medal/s/:sport_id/t/:subsport_id' endpoint.
        """
        mock_retrieve_medal.return_value = self.MOCK_MEDAL_FOR_NON_EXISTING_PARAMS
        response = self.fastapi_client.get(
            f"/medal/s/{self.SOME_SPORT_ID}/t/{self.SOME_SUB_SPORT_ID}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_subsport_id_with_by_unrecorded_sub_sport_id(
        self, mock_retrieve_medal
    ):
        """
        Test the retrieval of an empty object for an unrecorded subsport ID and recorded sport ID.

        This test verifies the '/medal/s/:sport_id/t/:subsport_id' endpoint.
        """
        mock_retrieve_medal.return_value = self.MOCK_MEDAL_FOR_NON_EXISTING_PARAMS
        response = self.fastapi_client.get(
            f"/medal/s/{self.SOME_SPORT_ID}/t/{self.SOME_SUB_SPORT_ID}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @patch("sota.routers.medal_router.medal_collection.aggregate")
    def test_get_medal_by_subsport_id_with_by_unrecorded_sport_id_and_sub_sport_id(
        self, mock_retrieve_medal
    ):
        """
        Test the retrieval of an empty object for unrecorded sport ID and subsport ID.

        This test verifies the '/medal/s/:sport_id/t/:subsport_id' endpoint.
        """
        mock_retrieve_medal.return_value = self.MOCK_MEDAL_FOR_NON_EXISTING_PARAMS
        response = self.fastapi_client.get(
            f"/medal/s/{self.SOME_SPORT_ID}/t/{self.SOME_SUB_SPORT_ID}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have been executed."""
        super().tearDownClass()
