
# Testing Documentation for SOTA API

## Overview

This document provides instructions and information about the test suites for the SOTA API. The tests are written using Python's `unittest` framework and are designed to ensure the correct functioning of various API endpoints and functionalities.

## Test Suites

The tests are organized into several files, each targeting a specific aspect of the API:

- `test_authentication.py`: Tests related to user authentication and token validation.
- `test_sport_router.py`: Focuses on testing the sports-related routes and their interactions with the database.
- `test_update_medal_router.py`: Tests the functionality for updating medal information, ensuring data integrity and proper request handling.

### Base Setup for Tests (`base.py`)

The `base.py` file contains the `setUpTest` class, which sets up the necessary environment for running the tests. This setup includes initializing a mock MongoDB client, loading test data into the database, and setting up the FastAPI test client.

### Running the Tests

To execute the tests, you will need to have Python and the necessary dependencies installed. Make sure to install `mongomock` and `fastapi` if they are not already present in your environment.

#### Command to Run Tests

Use the following command to run all tests:

You need to run the tests with an environment variable (e.g., `TEST=True`), please use the following format:

```bash
# For Unix-like systems
TEST=True python -m unittest discover tests

# For Windows Command Line
set TEST=True
python -m unittest discover tests

# For Windows PowerShell
$env:TEST="True"
python -m unittest discover tests
```

### Individual Test File Execution

To run tests from an individual file, use the following command format:

```bash
python -m unittest tests/test_filename.py
```

Replace `test_filename.py` with the actual file name, such as `test_authentication.py`.

## Important Notes

- Ensure that the MongoDB service is running if you are not using `mongomock`.
- The test data for MongoDB is loaded from BSON files located in the `dump_data/Sota` directory. Each collection has a corresponding BSON file.
- The FastAPI test client is used for sending requests to API endpoints within the test cases.
- After the tests are run, the `tearDownClass` method in `base.py` ensures clean-up of the database and test client.

