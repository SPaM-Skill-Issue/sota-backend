import unittest
from unittest.mock import patch
from .base import setUpTest
from fastapi import status


class TestUpdateAudientInfo(setUpTest):
    """
    Test cases for updating audient information.

    These tests cover various scenarios of updating audient information using the
    FastAPI API endpoint '/audient/update_audient_info'. It includes tests for valid
    and invalid request bodies, missing fields, and invalid data values.
    """

    AUDIENT_TOKEN = "audie" * 4

    AUDIENT_ID = "1"
    UPDATE_AUDIENT_INFO_PAYLOAD = {
        "audience": [
            {
                "id": AUDIENT_ID,
                "country_code": "US",
                "sport_id": [1],
                "gender": "M",
                "age": 20,
            }
        ]
    }

    NON_EXISTING_COUNTRY_CODE = "@@"

    @classmethod
    def setUpClass(cls):
        """Set up the test environment and insert necessary authentication keys."""
        super().setUpClass()
        cls._insert_authentication_keys()

    @classmethod
    def _insert_authentication_keys(cls):
        """Insert mock authentication keys into the database."""
        keys_data = [
            {
                "key": cls.AUDIENT_TOKEN,
                "scope": {"PUBLISH_AUDIENCE": True, "PUBLISH_MEDAL": False},
            },
        ]
        cls.db["Keys"].insert_many(keys_data)

    def test_update_audient_info_with_correct_body(self):
        """
        Test updating audient information with a correct request body.
        It expects a successful response with a status code 200.
        """
        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            self.UPDATE_AUDIENT_INFO_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the insert data was present in the database
        pipeline = [{"$match": {"_id": self.AUDIENT_ID}}, {"$project": {"_id": 0}}]
        self.assertEqual(
            list(self.db["Audient"].aggregate(pipeline))[0],
            self.UPDATE_AUDIENT_INFO_PAYLOAD["audience"][0],
        )

    def test_update_audient_info_with_missing_field(self):
        """
        Test updating audient information with a request body missing a required field.

        It expects a response with a status code 400 indicating a bad request.
        """
        incomplete_payload = self.UPDATE_AUDIENT_INFO_PAYLOAD.copy()
        incomplete_payload["audience"][0].pop("country_code", None)

        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            incomplete_payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_audient_info_with_invalid_country_code(self):
        """
        Test updating audient information with an invalid country code.

        It expects a response with a status code 400 indicating a bad request.
        """
        body_with_invalid_country_code = self.UPDATE_AUDIENT_INFO_PAYLOAD.copy()
        body_with_invalid_country_code["audience"][0][
            "country_code"
        ] = self.NON_EXISTING_COUNTRY_CODE

        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            body_with_invalid_country_code,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_audient_info_with_invalid_sport_id(self):
        """
        Test updating audient information with an invalid sport ID.

        It expects a response with a status code 400 indicating a bad request.
        """
        body_with_invalid_sport_id = self.UPDATE_AUDIENT_INFO_PAYLOAD.copy()
        body_with_invalid_sport_id["audience"][0]["sport_id"][0] = -1

        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            body_with_invalid_sport_id,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body_with_invalid_sport_id = self.UPDATE_AUDIENT_INFO_PAYLOAD.copy()
        body_with_invalid_sport_id["audience"][0]["sport_id"][0] = int(1e9)

        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            body_with_invalid_sport_id,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_audient_info_with_invalid_gender(self):
        """
        Test updating audient information with an invalid gender.

        It expects a response with a status code 400 indicating a bad request.
        """
        body_with_invalid_gender = self.UPDATE_AUDIENT_INFO_PAYLOAD.copy()
        body_with_invalid_gender["audience"][0]["gender"] = "Invalid gender"

        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            body_with_invalid_gender,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
