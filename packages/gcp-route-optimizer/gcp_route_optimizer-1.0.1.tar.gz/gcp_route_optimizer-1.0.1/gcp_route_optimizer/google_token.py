import google.auth.transport.requests
from google.oauth2 import service_account


def generate_google_token(service_account_json: dict):
    """
    Generates an OAuth token using Google Service Account JSON.
    Flask passes the JSON; no AWS logic here.
    """
    creds = service_account.Credentials.from_service_account_info(
        service_account_json,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    creds.refresh(google.auth.transport.requests.Request())
    return creds.token
