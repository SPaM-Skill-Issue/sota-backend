# SOTA API - Test Documentation

## Overview

This document outlines the testing strategy and plan for the SOTA API. The tests are primarily conducted using Python's `unittest` framework and `Mongomock` to ensure the API's reliability and correctness.

## Test Details

- **Project Name:** SoTA
- **Module Name:** Backend
- **Date Updated:** 11/4/23
- **Testing Tools:** Python unittest, Mongomock

## Test Suites

### Authentication Tests
- **Test Scenario:** Accessing protected API route
  - **Test Case:** With token
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - Token
    - **Expected Result:** Passes the check for auth key.
    - **Status:** To be tested

  - **Test Case:** Without token
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** None
    - **Expected Result:** Fails the check for auth key. Response returns status 401.
    - **Status:** To be tested

- **Test Scenario:** Accessing protected API route that requires permission
  - **Test Case:** With correct permission
    - **Pre-conditions:** 
      1. Has token in header
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - Token with correct permission
    - **Expected Result:** Passes the check for auth key and permission.
    - **Status:** To be tested

  - **Test Case:** Without correct permission
    - **Pre-conditions:** 
      1. Has token in header
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - Token without correct permission
    - **Expected Result:** Passes the check for auth key but fails permission check. Response returns status 401.
    - **Status:** To be tested

### Sports API Tests
- **Test Scenario:** GET /sport/:id
  - **Test Case:** With existing sport ID
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with sport ID that exists in database.
    - **Expected Result:** Response returns detail about sport with the corresponding ID.
    - **Status:** To be tested

  - **Test Case:** With non-existing sport ID
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with sport ID that does not exist in database.
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

### Medal API Tests
- **Test Scenario:** POST /medals/update_medal
  - **Test Case:** With correct body
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with correct fields
    - **Expected Result:** Response returns body with Success. Has correct medal in database.
    - **Status:** To be tested

  - **Test Case:** With missing field
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body that missing some field such as medal count, sport_id
    - **Expected Result:** ""msg"": ""field required"". Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter a country that does not participate in a certain type of sport.
    - **Pre-conditions:** 
      1. Has token in header
      2. Has incorrect token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with a country field containing an invalid country code.
    - **Expected Result:** Raise error. Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter a Sport_id that does not exist.
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with a Sport_id that does not exist.
    - **Expected Result:** Raise error. Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter a Sub_Sport_id that does not exist.
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with a Sub_Sport_id that does not exist.
    - **Expected Result:** Raise error. Response returns status 400.
    - **Status:** To be tested

### Medal Retrieval API Tests
- **Test Scenario:** GET /medal/c/:country_code
  - **Test Case:** Enter a URL path with a country parameter that exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with correct country_code
    - **Expected Result:** Response returns detail about medal count with the corresponding country code.
    - **Status:** To be tested

  - **Test Case:** Enter a URL path with a country parameter that does not exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with incorrect country_code
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

- **Test Scenario:** GET /medal/s/:sport_id
  - **Test Case:** Enter a URL path with a sport id parameter that does exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with correct sport_id
    - **Expected Result:** Response returns detail about medal count with the corresponding sport ID.
    - **Status:** To be tested

  - **Test Case:** Enter a URL path with a sport id parameter that does not exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with incorrect sport_id
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

- **Test Scenario:** GET /medal/s/:sport_id/t/:type_id
  - **Test Case:** Enter a URL path with a sport id and subsport type id that exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with correct sport_id and type_id
    - **Expected Result:** Response returns detail about medal count with the corresponding sport and type ID.
    - **Status:** To be tested

  - **Test Case:** Enter a URL path with a sport id that exist and subsport type id that does not exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with sport_id that exist but type_id doesn't exist
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

  - **Test Case:** Enter a URL path with a sport id that does not exist and subsport type id that exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with sport_id that not exist but type_id does exist
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

  - **Test Case:** Enter a URL path with a sport id and subsport type id that does not exist.
    - **Pre-conditions:** None
    - **Test Steps:** 
      1. Access the API route
    - **Test Data:** - URL path with non-exist sport_id and type_id
    - **Expected Result:** Response returns empty data.
    - **Status:** To be tested

### Audient API Tests
- **Test Scenario:** POST /audient/update_audient_info
  - **Test Case:** With correct body
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with correct fields
    - **Expected Result:** Response returns body with Success. Has correct audience in database.
    - **Status:** To be tested

  - **Test Case:** With missing field
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body that missing some field such as id, country, or gender
    - **Expected Result:** ""msg"": ""field required"". Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter invalid country code
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with a country field containing an invalid country code.
    - **Expected Result:** Raise error. Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter invalid sport_id
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with a Sport_id that does not exist.
    - **Expected Result:** Raise error. Response returns status 400.
    - **Status:** To be tested

  - **Test Case:** Enter gender other than M, F, N
    - **Pre-conditions:** 
      1. Has token in header
      2. Has correct token permission
    - **Test Steps:** 
      1. Construct a JSON body
      2. Request from API using the body
    - **Test Data:** - JSON body with invalid gender value
    - **Expected Result:** ""msg"": ""Invalid value for gender. It must be 'M', 'F', or 'N'."". Response returns status 400.
    - **Status:** To be tested

## Test Files

The tests are organized into several files, each targeting a specific aspect of the API:

- `test_authentication.py`: Tests related to user authentication and token validation, ensuring that endpoints behave correctly under various authentication scenarios.
- `test_get_medal_route.py`: Focuses on testing the retrieval of medal information, verifying correct responses for both existing and non-existing parameters.
- `test_sport_route.py`: Tests the functionality of the SportRouter, covering scenarios for retrieving sport information based on sport ID.
- `test_update_audient_info.py`: Includes tests for updating audient information, covering various scenarios including valid and invalid request bodies.
- `test_update_medal_route.py`: Tests for the `/medals/update_medal` endpoint, ensuring correct handling of medal update requests under different scenarios.

### Base Setup for Tests (`base.py`)

The `base.py` file contains the `setUpTest` class, which sets up the necessary environment for running the tests. This setup includes initializing a mock MongoDB client, loading test data into the database, and setting up the FastAPI test client.

### Running the Tests

To execute the tests, you will need to have Python and the necessary dependencies installed. Make sure to install `mongomock` and `fastapi` if they are not already present in your environment.

#### Command to Run Tests

Use the following command to run all tests:

You need to run the tests with an environment variable (e.g., `TESTING=True`), please use the following format:

```bash
# For Unix-like systems
TESTING=True python -m unittest discover

# For Windows Command Line
set TESTING=True
python -m unittest discover

# For Windows PowerShell
$env:TESTING="True"
python -m unittest discover
```

### Individual Test File Execution

To run tests from an individual file, use the following command format:

```bash
TESTING=True python -m unittest tests/test_filename.py
```

Replace `test_filename.py` with the actual file name, such as `test_authentication.py`.

## Conclusion

This testing documentation provides a comprehensive plan for ensuring the robustness and functionality of the SOTA API. By rigorously testing each aspect of the API, we can guarantee reliable and accurate performance.