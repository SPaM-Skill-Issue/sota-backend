import unittest
from unittest.mock import patch, Mock, MagicMock
from .base import setUpTest
from fastapi import status


class TestUpdateMedal(setUpTest):
    """
    Tests for the '/medals/update_medal' endpoint to ensure correct handling of medal update requests.

    This test suite covers different scenarios including updating medals with valid data,
    handling requests with missing fields, and handling updates for unparticipating countries.
    """

    MEDAL_TOKEN = "medal" * 4
    KEYS_DATA = [
        {
            "key": MEDAL_TOKEN,
            "scope": {"PUBLISH_AUDIENCE": False, "PUBLISH_MEDAL": True},
        },
    ]

    UPDATE_MEDAL_PAYLOAD = {
        "sport_id": 1,
        "sport_type_id": 1,
        "participants": [
            {"country": "US", "medal": {"gold": 1, "silver": 0, "bronze": 0}}
        ],
    }

    NON_EXISTING_SPORT_ID = int(1e9)
    NON_EXISTING_SPORT_TYPE_ID = int(1e9)

    @classmethod
    def setUpClass(cls):
        """Prepare the test environment and insert necessary authentication keys."""
        super().setUpClass()
        cls.insert_authentication_keys(cls.KEYS_DATA)

    def test_update_medal_with_correct_body(self):
        """Ensure successful medal update with valid request payload."""
        response = self.post_request(
            "/medals/update_medal",
            self.MEDAL_TOKEN,
            self.UPDATE_MEDAL_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the insert data was present in the database
        pipeline = [
            {
                "$match": {
                    "country_code": self.UPDATE_MEDAL_PAYLOAD["participants"][0][
                        "country"
                    ],
                }
            },
            {"$unwind": {"path": "$sports"}},
            {"$match": {"sports.sport_id": 1, "sports.type_id": 1}},
        ]

        medal_counts = list(self.db["Medal"].aggregate(pipeline))[0]["sports"]
        keys_to_extract = ["gold", "silver", "bronze"]

        # Check if the medal count matches the updated data
        self.assertEqual(
            {key: medal_counts[key] for key in keys_to_extract},
            self.UPDATE_MEDAL_PAYLOAD["participants"][0]["medal"],
        )

    def test_update_medal_with_missing_field(self):
        """Verify that missing a required field in the payload results in a bad request."""
        incomplete_payload = self.UPDATE_MEDAL_PAYLOAD.copy()
        incomplete_payload.pop("sport_id", None)

        response = self.post_request(
            "/medals/update_medal", self.MEDAL_TOKEN, incomplete_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_medal_with_unparticipate_country(self):
        """Test that updating medals for a country not participating in a sport results in a bad request."""
        body_with_unparticipate_country = self.UPDATE_MEDAL_PAYLOAD.copy()
        body_with_unparticipate_country["participants"][0]["country"] = "TH"

        response = self.post_request(
            "/medals/update_medal",
            self.MEDAL_TOKEN,
            body_with_unparticipate_country,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_medal_with_unexist_sport_id(self):
        """Test that updating medals for a non-existing sport's id results in a bad request."""
        body_with_non_exist_sport_id = self.UPDATE_MEDAL_PAYLOAD.copy()
        body_with_non_exist_sport_id["sport_id"] = self.NON_EXISTING_SPORT_ID

        response = self.post_request(
            "/medals/update_medal",
            self.MEDAL_TOKEN,
            body_with_non_exist_sport_id,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_medal_with_unexist_sport_type_id(self):
        """Test that updating medals for a non-existing sport type's id results in a bad request."""
        body_with_non_exist_sport_type_id = self.UPDATE_MEDAL_PAYLOAD.copy()
        body_with_non_exist_sport_type_id[
            "sport_type_id"
        ] = self.NON_EXISTING_SPORT_TYPE_ID

        response = self.post_request(
            "/medals/update_medal",
            self.MEDAL_TOKEN,
            body_with_non_exist_sport_type_id,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have been executed."""
        super().tearDownClass()
