# Basic User Authentication

This AWS serverless microservice implements RESTful user credentials management.

## REST API

### Register new user
- Path: `/register`
- Method: `POST`
- Parameters
    - email: User's email
    - password: User's password

### Login
- Path: `/login`
- Method: `POST`
- Parameters
    - email: User's email
    - password: User's password
- Return data:
    - email: User's email
    - access_token: User's access token to other web services

### Change password
- Path: `/password`
- Method: `PUT`
- Headers: `Authorization: Bearer <access_token>`
- Parameters:
    - password: User's current password
    - new_password: User's new password
    
## System Architecture:

API Gateway <--------> Lambda <---------> DynamoDB

## Project Structure:

- infrastucture: Infrastructure as code using CDK.
- runtime: lambda handler using AWS Chalice framework. Per Chalice convention, actual implementation is stored in `chalicelib` directory whereas REST routing is in `app.py`. Implementation is organized into two files:
    - `chalicelib/resources.py`: Implement access to resources.
    - `chalicelib/handlers.py`: Implement function to handle REST requests.

## Requirements:
- AWS CDK need to be installed
- Python 3.11 or later

Other project requirements are specified in requirements.txt. It is best to create a virtual environment for the project:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Deployment:
On environment where all requirements are installed, project can be deploy to AWS with following commands:
```
    cd infrastructure
    cdk bootstrap
    cdk deploy
```

## Running Locally
It is possible to run the instance locally without AWS resource:

1. Start docker instance that host DynamoDB locally:

    ```
    cd runtime/tests/dynamodb 
    docker-compose up --detach
    ```
2. Bootstrap DynamoDB table
    ```
    runtime/tests
		python -m libtest.common
    ```

3. Run chalice local
    ```
    cd runtime
    export ENDPOINT="http://localhost:4566"
		chalice local
    ```

## Unit Testing
The project use native unittest framework. The test requires starting DynamoDB instance, which is defined in `runtime/tests/dynamodb`. All tests are organized in runtime/tests, which needs to be the current directory for proper path context.

- `python -m unittest libtest`: Unit tests for handlers and resources
- `python -m unittest apptest`: Unit tests for the HTTP app using Chalice Client simulate HTTP invocations.

## Makefile
For convenient, a Makefile is created for this project.

- `make venv`: creates virtual environment in .venv directory
- `make test`: run all unit test
- `make deploy`: Deploy to AWS (need proper AWS credentials setup, similar to AWS CLI)
- `make run_local`: Run the local deployment
