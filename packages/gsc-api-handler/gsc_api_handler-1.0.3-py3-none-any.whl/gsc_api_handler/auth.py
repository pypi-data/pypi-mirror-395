import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from decouple import config

DEFAULT_CREDS_PATH = config("GSC_CLIENT_SECRET", default="client_secret.json")
DEFAULT_TOKEN_PATH = config("GSC_TOKEN_PATH", default="token.pickle")
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def authorize_creds(creds_path: str = DEFAULT_CREDS_PATH, token_path: str = DEFAULT_TOKEN_PATH):
    """

    Authorizing access to GSC API using .env and return webmaster_service object
    """
    creds = None

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token_file:
            pickle.dump(creds, token_file)

    return build('webmasters', 'v3', credentials=creds)
