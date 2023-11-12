# Testing Documentation for SOTA API

## Overview

This document provides instructions and information about the test suites for the SOTA API. The tests are written using Python's `unittest` framework and are designed to ensure the correct functioning of various API endpoints and functionalities.

## Test Suites

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

## Important Notes
- The test data for MongoDB is loaded from BSON files located in the `dump_data/Sota` directory. Each collection has a corresponding BSON file.
- The FastAPI test client is used for sending requests to API endpoints within the test cases.