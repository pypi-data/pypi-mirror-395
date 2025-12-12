import subprocess
import logging
import requests
import os
import json
from functools import lru_cache
import sys

# Dummy credentials (update as necessary)
DUMMY_USERNAME = "dummyUser"
DUMMY_TOKEN = "dummyToken"
# Licensing server URL (update to your actual licensing server endpoint)
LICENSING_SERVER_URL = "http://licenseserver.example.com/api/check"

def get_machine_uuid() -> str:
    """
    Retrieve the machine UUID using dmidecode.
    Requires dmidecode to be installed and accessible.
    """
    try:
        result = subprocess.run(
            ["dmidecode", "-s", "system-uuid"],
            capture_output=True,
            text=True,
            check=True,
        )
        uuid = result.stdout.strip()
        return uuid
    except Exception as e:
        logging.error("Failed to get machine UUID: %s", e)
        return "UNKNOWN_UUID"

@lru_cache(maxsize=1)
def _load_license_data() -> dict:
    """
    Load license info from license.json under GRID_DATA_DIR.
    Cached to only read disk once.
    """
    data_dir = os.environ.get("GRID_DATA_DIR")
    if not data_dir:
        raise EnvironmentError("GRID_DATA_DIR environment variable is not set")
    license_path = os.path.join(data_dir, "license.json")
    
    with open(license_path, "r") as f:
        data = json.load(f)
        
    return data
    
def is_license_valid() -> bool:
    """
    Check if the license is valid by calling the licensing server.
    Returns True if the license is valid, False otherwise.
    """
    try:
        _load_license_data()    
        return True
    except Exception as e:
        print(e)
        return False

def call_license_server() -> bool:
    """
    Make an API call to the licensing server with username, token, and machine UUID.
    Returns True if the license check is successful (HTTP 200), False otherwise.
    """
    payload = {
        "username": DUMMY_USERNAME,
        "token": DUMMY_TOKEN,
        "uuid": get_machine_uuid(),
    }
    try:
        response = requests.post(LICENSING_SERVER_URL, json=payload, timeout=5)
        if response.status_code == 200:
            return True
        else:
            logging.error("License server returned error: %d", response.status_code)
            return False
    except Exception as e:
        logging.error("Failed to call license server: %s", e)
        return False
    
def get_client_datastore_name() -> str:
    """
    Retrieve the client datastore name from the licensing server using stored credentials.
    Returns the datastore name string if successful, otherwise None.
    """
    try:
        return _load_license_data().get("client_datastore")
    except Exception as e:
        logging.watning("No specific datastore named. Custom data will not be available")
        return None

def get_sas_token(url: str) -> str:
    """
    Make an API call to the licensing server including the download URL.
    Expects the response to include a SAS token that can be used with azcopy.
    Returns the SAS token if successful, otherwise returns None.
    """
    try:
        account_name = url.split("://", 1)[1].split(".", 1)[0]        
        
        if account_name == "gridenterpriseresources":
            # For the gridenterpriseresources account, use the token from license.json
            return _load_license_data().get("storage_token")
        elif account_name == "sfclientdata":
            # For the sfclientdata account, use the token from license.json
            return _load_license_data().get("client_token")
            
    except Exception as e:
        logging.error("Failed to load SAS token from license file: %s", e)
        return None
    
def get_acr_password() -> str:
    """
    Retrieve the registry (ACR) password from the licensing server using stored credentials.
    Returns the password string if successful, otherwise None.
    """
    try:
        return _load_license_data().get("password")
    except Exception as e:
        logging.error("Failed to load ACR password from license file: %s", e)
        return None
    
def get_username() -> str:
    """
    Retrieve the username from the licensing server using stored credentials.
    Returns the username string if successful, otherwise None.
    """
    try:
        return _load_license_data().get("username")
    except Exception as e:
        logging.error("Failed to load username from license file: %s", e)
        return None