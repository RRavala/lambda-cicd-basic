import json


def handler(event, context):
    """Minimal Lambda: proves the CI/CD pipeline deployed working code."""
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from lambda-cicd-basic, deployed by GitHub Actions"}),
    }
