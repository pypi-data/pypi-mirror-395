from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import base64
import json
import time
import msal
from os import getenv


def get_client_credential(secret_name: str) -> str:
    """
    Retruns the credential needed to get the token for access to the Dataverse.
    """
    load_dotenv()
    VAULT_URL = getenv("VAULT_URL", "")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=VAULT_URL, credential=credential)
    secret_value = client.get_secret(secret_name).value
    
    if secret_value is None:
        raise RuntimeError("Could not get client credential.")
    
    return secret_value


def get_dataverse_token(dataverse_url: str) -> str:
    """
    Returns the token needed for working with the Dataverse API
    """
    scopes = [f"{dataverse_url}/.default"]
    return get_token_for_scope(scopes)
    

def get_flow_token() -> str:
    """
    Return the token needed for accessing power automate flows.
    """
    scopes = ["https://service.flow.microsoft.com//.default"]
    return get_token_for_scope(scopes)


def get_token_for_scope(scopes: list[str]) -> str:
    load_dotenv()
    TENANT_ID = getenv("TENANT_ID")
    CLIENT_ID = getenv("CLIENT_ID")
    TOKEN_AUTHORITY = getenv("DATAVERSE_TOKEN_AUTHORITY")
    DATAVERSE_SECRET_NAME = getenv("DATAVERSE_SECRET_NAME", "")
    TOKEN_CLIENT_CREDENTIAL = get_client_credential(DATAVERSE_SECRET_NAME)

    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=TOKEN_CLIENT_CREDENTIAL,
        authority=f"{TOKEN_AUTHORITY}{TENANT_ID}",
    )
    token = app.acquire_token_for_client(scopes=scopes)
    
    if not isinstance(token, dict) or "access_token" not in token:
        raise RuntimeError(f"Could not get access token for: {scopes}")
    
    return token["access_token"]


# TODO - Add parameter to define *which* SharePoint

def get_graph_token():
    CLIENT_ID = getenv("CLIENT_ID", "")
    TENANT_ID = getenv("TENANT_ID", "")
    GRAPH_MSAL_AUTHORITY = getenv("GRAPH_MSAL_AUTHORITY", "")
    GRAPH_MSAL_SCOPE = getenv("GRAPH_MSAL_SCOPE", "")
    GRAPH_SECRET_NAME = getenv("GRAPH_SECRET_NAME", "")
    GRAPH_CLIENT_SECRET = get_client_credential(GRAPH_SECRET_NAME)

    msal_app = msal.ConfidentialClientApplication(
        client_id = CLIENT_ID,
        client_credential = GRAPH_CLIENT_SECRET,
        authority = GRAPH_MSAL_AUTHORITY + TENANT_ID,
    )
    result = msal_app.acquire_token_silent(
        scopes = [GRAPH_MSAL_SCOPE],
        account = None,
    )

    if not result:
        result = msal_app.acquire_token_for_client(scopes=[GRAPH_MSAL_SCOPE])

    if isinstance(result, dict) and "error_description" in result:
        raise Exception(result["error_description"])

    if not isinstance(result, dict) or "access_token" not in result:
        raise Exception("No Graph Access Token found")
    
    return result["access_token"]

    
def create_flow_headers() -> dict[str, str]:
    flow_token = get_flow_token()
    return {
        "Authorization": f"Bearer {flow_token}", 
        "Content-Type": "application/json",
    }


def is_jwt_expired(token: str, skew_seconds: int = 60) -> bool:
    """
    Returns True if the JWT access token is expired (or invalid), allowing a small
    clock skew window. This does not validate the signature; it only inspects
    the 'exp' claim from the payload.
    """
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return True

        payload_b64 = parts[1]
        # Pad base64 string if necessary
        padding_needed = (4 - len(payload_b64) % 4) % 4
        payload_b64 += "=" * padding_needed

        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
        exp_timestamp = int(payload.get("exp", 0))
        now = int(time.time())
        return now >= (exp_timestamp - skew_seconds)
    except Exception:
        return True