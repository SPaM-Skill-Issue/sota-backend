import unittest
from base import setUpTest
from fastapi import status


class TestAuthentication(setUpTest):
    """
    Tests the authentication and authorization mechanisms of the API endpoints.

    This class verifies that the API endpoints behave correctly in response to
    various authentication scenarios, including valid and invalid tokens, as well
    as tokens with different scopes and permissions.
    """

    VALID_TOKEN = "token" * 4
    AUDIENT_TOKEN = "audie" * 4

    # Test data payloads
    UPDATE_AUDIENCE_INFO_PAYLOAD = {
        "audience": [
            {"id": "1", "country_code": "US", "sport_id": [1], "gender": "M", "age": 20}
        ]
    }

    UPDATE_MEDAL_PAYLOAD = {
        "sport_id": 1,
        "sport_type_id": 1,
        "participants": [
            {"country": "US", "medal": {"gold": 1, "silver": 0, "bronze": 0}}
        ],
    }

    @classmethod
    def setUpClass(cls):
        """
        Prepare the test environment by setting up a mock database and inserting necessary authentication keys.
        """
        super().setUpClass()
        cls._insert_authentication_keys()

    @classmethod
    def _insert_authentication_keys(cls):
        """
        Inserts mock authentication keys into the database to be used in the tests.

        Includes keys with different scopes to test different permission levels.
        """
        keys_data = [
            {
                "key": cls.VALID_TOKEN,
                "scope": {"PUBLISH_AUDIENCE": True, "PUBLISH_MEDAL": True},
            },
            {
                "key": cls.AUDIENT_TOKEN,
                "scope": {"PUBLISH_AUDIENCE": True, "PUBLISH_MEDAL": False},
            },
        ]
        cls.db["Keys"].insert_many(keys_data)

    def test_access_with_valid_token(self):
        """
        Verifies that the API grants access when provided with a valid token.
        """
        response = self.post_request(
            "/audient/update_audient_info",
            self.VALID_TOKEN,
            self.UPDATE_AUDIENCE_INFO_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_without_token(self):
        """
        Ensures that the API denies access when no token is provided.
        """
        response = self.post_request(
            "/audient/update_audient_info",
            "",
            self.UPDATE_AUDIENCE_INFO_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_correct_permission(self):
        """
        Tests that access is granted when a token with the correct permission is provided.
        """
        response = self.post_request(
            "/audient/update_audient_info",
            self.AUDIENT_TOKEN,
            self.UPDATE_AUDIENCE_INFO_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_with_incorrect_permission(self):
        """
        Checks that access is denied when a token lacks the required permission.
        """
        response = self.post_request(
            "/medals/update_medal",
            self.AUDIENT_TOKEN,
            self.UPDATE_MEDAL_PAYLOAD,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the database after all tests have been executed, ensuring no test data remains.
        """
        super().tearDownClass()
